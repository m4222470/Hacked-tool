# README

Welcome to Hacked-tool v2.0 - Professional Reconnaissance Scanner

See [docs/INDEX.md](docs/INDEX.md) for full documentation.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run a scan
python main.py -d example.com

# Run tests
python -m pytest tests/
```

## Features

- 🚀 **Fast Async Scanning** - 40x faster than sequential
- 🔍 **Technology Detection** - Detects 11+ frameworks
- 🛡️ **Security Focused** - Comprehensive vulnerability detection
- 🔌 **Plugin System** - Easily extensible architecture
- 📊 **Modular Design** - Clean separation of concerns
- 🧪 **Well Tested** - Comprehensive test suite

## Directory Structure

```
src/              # Source code
├── core/         # Core engine components
├── modules/      # Scanning modules
├── plugins/      # Plugin system
└── utils/        # Utilities

config/           # YAML configurations
data/             # Data files
tests/            # Test suite
docs/             # Documentation
output/           # Output directory
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design
- [User Guide](docs/USER_GUIDE.md) - How to use
- [API Reference](docs/API_REFERENCE.md) - API docs
- [Plugin Development](docs/PLUGIN_SYSTEM.md) - Create plugins

## License

MIT License
