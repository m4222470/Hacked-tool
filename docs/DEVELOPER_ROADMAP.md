# 🛠️ دليل المطور - خريطة الطريق

## المرحلة الأولى: التأسيس ✅ COMPLETED

- [x] تحليل 9 مشاكل معمارية
- [x] إنشاء 10 مجلدات منظمة
- [x] إنشاء نظام Core (7 ملفات)
- [x] تطبيق نظام Plugins
- [x] تطبيق نظام Config (YAML)
- [x] بناء 4 وحدات منطقية
- [x] إنشاء 25+ اختبار شامل
- [x] توثيق شامل

**الحالة**: ✅ اكتمل بنسبة 100%

---

## المرحلة الثانية: التطوير الفعلي (UPCOMING)

### الخطوة 1: تحسين Fingerprinting Module
**الملف**: `src/modules/reconnaissance/fingerprinting.py`

**المهام**:
1. ربط قاعدة البيانات `data/fingerprints/technologies.json`
2. بناء محرك matching متقدم
3. دعم:
   - استخراج Headers
   - تحليل HTML comments
   - اكتشاف CMS من URLs
   - اكتشاف Javascript frameworks

**الكود الهيكلي**:
```python
import json
from pathlib import Path
from typing import Dict, List, Tuple

class FingerprintingModule(BasePlugin):
    name = "Fingerprinting"
    
    def __init__(self):
        super().__init__()
        self.fingerprints = self._load_fingerprints()
    
    def _load_fingerprints(self) -> Dict:
        """Load technologies database"""
        db_path = Path(__file__).parent.parent.parent.parent / 'data' / 'fingerprints' / 'technologies.json'
        with open(db_path) as f:
            return json.load(f)
    
    def execute(self, target: str, options: Dict = None) -> Dict:
        """Fingerprint technologies on target"""
        technologies = self._detect_technologies(target)
        return {
            'target': target,
            'technologies': technologies,
            'count': len(technologies)
        }
    
    def _detect_technologies(self, target: str) -> List[Dict]:
        """Match technologies"""
        # 1. Fetch headers
        # 2. Parse HTML
        # 3. Match patterns
        # 4. Return matches
        pass
```

---

### الخطوة 2: تحسين Port Scanner Module
**الملف**: `src/modules/scanning/port_scanner.py`

**المهام**:
1. Implement فعلي للـ Port Scanning
2. اكتشاف الخدمات (Service Detection)
3. جمع Banner Information
4. Parallel scanning مع threading

**المتطلبات**:
```bash
# أضف لـ requirements.txt
socket  # Built-in
nmap    # Optional
paramiko  # للـ SSH
```

**الكود الهيكلي**:
```python
import socket
import threading
from typing import List, Dict

class PortScannerModule(BasePlugin):
    name = "Port Scanner"
    
    def execute(self, target: str, options: Dict = None) -> Dict:
        """Scan ports on target"""
        ports = options.get('ports', [22, 80, 443, 8080])
        open_ports = self._scan_ports(target, ports)
        return {
            'target': target,
            'open_ports': open_ports,
            'total_scanned': len(ports)
        }
    
    def _scan_ports(self, target: str, ports: List[int]) -> List[Dict]:
        """Scan individual ports"""
        results = []
        for port in ports:
            if self._is_port_open(target, port):
                service = self._detect_service(target, port)
                results.append({
                    'port': port,
                    'status': 'open',
                    'service': service
                })
        return results
    
    def _is_port_open(self, host: str, port: int) -> bool:
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
```

---

### الخطوة 3: تحسين Vulnerability Mapper Module
**الملف**: `src/modules/analysis/vulnerability_mapper.py`

**المهام**:
1. Integrate مع CVE Database (NVD API)
2. Match technologies to CVEs
3. Risk assessment وـ Scoring
4. Generate recommendations

**المتطلبات**:
```bash
# أضف لـ requirements.txt
requests>=2.28.0
```

**الكود الهيكلي**:
```python
import requests
from typing import List, Dict

class VulnerabilityMapperModule(BasePlugin):
    name = "Vulnerability Mapper"
    NVD_API = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    
    def execute(self, target: str, options: Dict = None) -> Dict:
        """Map vulnerabilities"""
        technologies = options.get('technologies', [])
        vulnerabilities = self._fetch_vulnerabilities(technologies)
        return {
            'target': target,
            'vulnerabilities': vulnerabilities,
            'risk_score': self._calculate_risk_score(vulnerabilities)
        }
    
    def _fetch_vulnerabilities(self, technologies: List[str]) -> List[Dict]:
        """Fetch CVEs for technologies"""
        all_vulns = []
        for tech in technologies:
            # Query NVD API
            vulns = self._query_nvd(tech)
            all_vulns.extend(vulns)
        return all_vulns
    
    def _calculate_risk_score(self, vulns: List[Dict]) -> float:
        """Calculate overall risk"""
        if not vulns:
            return 0.0
        scores = [v.get('cvss_v3_base_score', 0) for v in vulns]
        return sum(scores) / len(scores)
```

---

### الخطوة 4: تحسين External Connector Module
**الملف**: `src/modules/integrations/external_connector.py`

**المهام**:
1. Integration مع Shodan API
2. Integration مع Censys API
3. Integration مع URLhaus
4. API Key Management

**الكود الهيكلي**:
```python
import os
from typing import Dict, List

class ExternalConnectorModule(BasePlugin):
    name = "External Connector"
    
    def __init__(self):
        super().__init__()
        self.shodan_key = os.getenv('SHODAN_API_KEY')
        self.censys_key = os.getenv('CENSYS_API_KEY')
    
    def execute(self, target: str, options: Dict = None) -> Dict:
        """Query external data sources"""
        results = {
            'target': target,
            'shodan': self._query_shodan(target),
            'censys': self._query_censys(target),
            'urlhaus': self._query_urlhaus(target)
        }
        return results
    
    def _query_shodan(self, target: str) -> Dict:
        """Query Shodan for host"""
        if not self.shodan_key:
            return {'error': 'API key not configured'}
        # Implementation
        return {}
```

---

## المرحلة الثالثة: الواجهات والـ APIs

### الخطوة 5: بناء REST API
**ملف جديد**: `src/api/routes.py`

```python
from flask import Flask, request, jsonify
from src.core.engine import engine
from src.core.session_manager import session_manager

app = Flask(__name__)

@app.route('/api/scan', methods=['POST'])
def start_scan():
    """Start new scan"""
    data = request.json
    target = data.get('target')
    
    session = session_manager.create_session(target, data)
    session_manager.start_session(session.session_id)
    
    # Trigger scan (async)
    # engine.run_scan(target, data, session.session_id)
    
    return jsonify({
        'session_id': session.session_id,
        'status': 'started'
    })

@app.route('/api/session/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get session status"""
    session = session_manager.get_session(session_id)
    return jsonify(session.to_dict())

@app.route('/api/results/<session_id>', methods=['GET'])
def get_results(session_id):
    """Get scan results"""
    session = session_manager.get_session(session_id)
    return jsonify({'results': session.results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

### الخطوة 6: بناء Web Dashboard
**مجلد جديد**: `web/`

```
web/
├── index.html          # الصفحة الرئيسية
├── dashboard.html      # لوحة التحكم
├── css/
│   └── style.css      # الأنماط
└── js/
    └── app.js         # المنطق
```

**مثال HTML**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Security Scanner Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <h1>Security Scanner</h1>
        <form id="scanForm">
            <input type="text" id="target" placeholder="Enter target domain">
            <button type="submit">Start Scan</button>
        </form>
        <div id="results"></div>
    </div>
    <script src="js/app.js"></script>
</body>
</html>
```

---

## المرحلة الرابعة: قاعدة البيانات

### الخطوة 7: تكامل قاعدة البيانات
**ملف جديد**: `src/core/database.py`

```python
import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / 'data' / 'scanner.db'
        self._initialize()
    
    def _initialize(self):
        """Create tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    target TEXT NOT NULL,
                    status TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    result_id INTEGER PRIMARY KEY,
                    session_id TEXT,
                    module TEXT,
                    data TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            conn.commit()
    
    def save_session(self, session):
        """Save session to DB"""
        pass
    
    def save_result(self, session_id, module, data):
        """Save result to DB"""
        pass
```

---

## قائمة المهام التفصيلية

### PRIORITY: HIGH 🔴

- [ ] **FP-1**: تحسين Fingerprinting Module
  - [ ] ربط قاعدة technologies.json
  - [ ] بناء Header Parser
  - [ ] بناء HTML Parser
  - [ ] كتابة 5+ اختبارات
  - **المدة المتوقعة**: 4 ساعات

- [ ] **PS-1**: تحسين Port Scanner Module
  - [ ] Implement Socket API بشكل كامل
  - [ ] إضافة Threading
  - [ ] Service Detection
  - [ ] كتابة 5+ اختبارات
  - **المدة المتوقعة**: 5 ساعات

### PRIORITY: MEDIUM 🟡

- [ ] **VM-1**: تحسين Vulnerability Mapper
  - [ ] Integration مع CVE Database
  - [ ] Risk Scoring Algorithm
  - [ ] كتابة 3+ اختبارات
  - **المدة المتوقعة**: 6 ساعات

- [ ] **API-1**: بناء REST API
  - [ ] Setup Flask
  - [ ] Implement endpoint /scan
  - [ ] Implement endpoint /session/<id>
  - [ ] كتابة اختبارات API
  - **المدة المتوقعة**: 3 ساعات

### PRIORITY: LOW 🟢

- [ ] **DASH-1**: بناء Web Dashboard
  - [ ] تصميم واجهة المستخدم
  - [ ] ربط مع API
  - [ ] إضافة الرسوم البيانية
  - **المدة المتوقعة**: 8 ساعات

- [ ] **DB-1**: تكامل قاعدة البيانات
  - [ ] Setup SQLite
  - [ ] تصميم Schema
  - [ ] Implement ORM (optional)
  - **المدة المتوقعة**: 4 ساعات

---

## معايير الجودة

### Code Quality
- ✅ Type hints على جميع الدوال
- ✅ Docstrings عربي/إنجليزي
- ✅ Error handling شامل
- ✅ Logging على جميع العمليات
- ✅ Passing all tests

### Testing
```python
# كل module يجب أن يحتوي على:
# - Unit Tests (70% minimum)
# - Integration Tests
# - Error Cases
# - Edge Cases

# مثال:
class TestFingerprintingModule(unittest.TestCase):
    def test_valid_target(self):
        result = module.execute('example.com')
        self.assertIn('technologies', result)
    
    def test_empty_target(self):
        with self.assertRaises(ValueError):
            module.execute('')
    
    def test_invalid_domain(self):
        with self.assertRaises(ValueError):
            module.execute('invalid..')
```

### Documentation
- ✅ README لكل module
- ✅ Docstrings شاملة
- ✅ Examples في README
- ✅ API Documentation

---

## الموارد والمراجع

### مكتبات مقترحة
```bash
# Core
requests>=2.28.0
pyyaml>=6.0
python-dotenv>=0.20.0

# Scanning
nmap-python  # إذا توفر
scapy>=2.5.0

# Web
Flask>=2.3.0
flask-cors>=4.0.0

# Database
sqlalchemy>=2.0.0

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
```

### مراجع خارجية
- [NVD API Documentation](https://nvd.nist.gov/developers/vulnerabilities)
- [Shodan API](https://developer.shodan.io/)
- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE/CVSS Scoring](https://www.first.org/cvss/)

---

## Metrics للتتبع

```
المرحلة الحالية: 1/4 ✅ 25%
المرحلة القادمة: 2/4 (تطوير الوحدات) 25%
المرحلة الثالثة: 3/4 (APIs) 25%
المرحلة الرابعة: 4/4 (قاعدة البيانات) 25%

إجمالي Progress: 25%
```

---

**نقطة الانطلاق**: ابدأ بـ FP-1 (Fingerprinting Module)
**الوقت المتوقع للإكمال**: 3-4 أسابيع
**الفريق المطلوب**: 1-2 مطور Python متقدم

