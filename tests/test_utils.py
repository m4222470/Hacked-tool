"""
Utilities tests
"""

import unittest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.url_utils import URLUtils
from utils.validators import URLValidator, ParameterValidator

class TestURLUtils(unittest.TestCase):
    """Test URL utilities"""
    
    def test_extract_domain(self):
        """Test domain extraction"""
        domain = URLUtils.extract_domain('https://example.com/path')
        self.assertEqual(domain, 'example.com')
    
    def test_extract_path(self):
        """Test path extraction"""
        path = URLUtils.extract_path('https://example.com/admin/panel')
        self.assertEqual(path, '/admin/panel')
    
    def test_normalize_urls(self):
        """Test URL normalization"""
        urls = URLUtils.normalize_urls([
            'https://example.com/',
            'https://example.com/',
            'https://example.com'
        ])
        self.assertEqual(len(urls), 1)

class TestURLValidator(unittest.TestCase):
    """Test URL validation"""
    
    def test_valid_domain(self):
        """Test valid domain validation"""
        self.assertTrue(URLValidator.is_valid_domain('example.com'))
        self.assertTrue(URLValidator.is_valid_domain('sub.example.co.uk'))
    
    def test_invalid_domain(self):
        """Test invalid domain validation"""
        self.assertFalse(URLValidator.is_valid_domain('invalid domain'))
        self.assertFalse(URLValidator.is_valid_domain(''))
    
    def test_valid_url(self):
        """Test valid URL validation"""
        self.assertTrue(URLValidator.is_valid_url('https://example.com'))
        self.assertTrue(URLValidator.is_valid_url('http://sub.example.com/path'))
    
    def test_normalize_domain(self):
        """Test domain normalization"""
        normalized = URLValidator.normalize_domain('WWW.EXAMPLE.COM')
        self.assertEqual(normalized, 'example.com')
    
    def test_normalize_url(self):
        """Test URL normalization"""
        normalized = URLValidator.normalize_url('example.com/')
        self.assertTrue(normalized.startswith('https://'))

class TestParameterValidator(unittest.TestCase):
    """Test parameter validation"""
    
    def test_suspicious_parameter(self):
        """Test suspicious parameter detection"""
        self.assertTrue(ParameterValidator.is_suspicious_parameter('admin'))
        self.assertTrue(ParameterValidator.is_suspicious_parameter('debug_mode'))
        self.assertFalse(ParameterValidator.is_suspicious_parameter('username'))
    
    def test_valid_parameter_name(self):
        """Test parameter name validation"""
        self.assertTrue(ParameterValidator.validate_parameter_name('valid_name'))
        self.assertTrue(ParameterValidator.validate_parameter_name('_private'))
        self.assertFalse(ParameterValidator.validate_parameter_name('123invalid'))

if __name__ == '__main__':
    unittest.main()
