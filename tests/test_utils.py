"""Unit tests for batoto_parser.utils module."""

import base64
import pytest
from batoto_parser.utils import (
    validate_url,
    validate_domain,
    evp_bytes_to_key,
    decrypt_batoto,
    generate_uid,
)


class TestValidateUrl:
    """Tests for validate_url function."""
    
    def test_valid_urls(self):
        """Test valid URLs return True."""
        assert validate_url("https://bato.si/series/123") is True
        assert validate_url("https://bato.to/title/456") is True
        assert validate_url("http://bato.si/chapter/789") is True
    
    def test_invalid_domain(self):
        """Test URLs from invalid domains return False."""
        assert validate_url("https://example.com/series/123") is False
        assert validate_url("https://google.com") is False
    
    def test_invalid_scheme(self):
        """Test URLs with invalid schemes return False."""
        assert validate_url("ftp://bato.si/series/123") is False
        assert validate_url("file:///path/to/file") is False
    
    def test_malformed_urls(self):
        """Test malformed URLs return False."""
        assert validate_url("not-a-url") is False
        assert validate_url("://missing-scheme") is False
        assert validate_url("") is False
        assert validate_url(None) is False
    
    def test_www_prefix(self):
        """Test www. prefix is handled correctly."""
        assert validate_url("https://www.bato.si/series/123") is True


class TestValidateDomain:
    """Tests for validate_domain function."""
    
    def test_valid_domains(self):
        """Test valid domains return True."""
        assert validate_domain("bato.si") is True
        assert validate_domain("bato.to") is True
        assert validate_domain("example.com") is True
    
    def test_invalid_domains(self):
        """Test invalid domains return False."""
        assert validate_domain("") is False
        assert validate_domain(None) is False
        assert validate_domain("invalid domain!") is False
        assert validate_domain("domain with spaces") is False
    
    def test_domain_with_subdomain(self):
        """Test domains with subdomains."""
        assert validate_domain("www.bato.si") is True
        assert validate_domain("api.example.com") is True


class TestEvpBytesToKey:
    """Tests for evp_bytes_to_key function."""
    
    def test_valid_key_derivation(self):
        """Test key derivation with valid inputs."""
        password = b"test_password"
        salt = b"12345678"
        key, iv = evp_bytes_to_key(password, salt, 32, 16)
        
        assert len(key) == 32
        assert len(iv) == 16
        assert isinstance(key, bytes)
        assert isinstance(iv, bytes)
    
    def test_deterministic_output(self):
        """Test same inputs produce same outputs."""
        password = b"test_password"
        salt = b"12345678"
        
        key1, iv1 = evp_bytes_to_key(password, salt, 32, 16)
        key2, iv2 = evp_bytes_to_key(password, salt, 32, 16)
        
        assert key1 == key2
        assert iv1 == iv2
    
    def test_different_passwords(self):
        """Test different passwords produce different keys."""
        salt = b"12345678"
        
        key1, _ = evp_bytes_to_key(b"password1", salt, 32, 16)
        key2, _ = evp_bytes_to_key(b"password2", salt, 32, 16)
        
        assert key1 != key2
    
    def test_empty_password(self):
        """Test empty password raises ValueError."""
        with pytest.raises(ValueError, match="password cannot be empty"):
            evp_bytes_to_key(b"", b"12345678", 32, 16)
    
    def test_empty_salt(self):
        """Test empty salt raises ValueError."""
        with pytest.raises(ValueError, match="salt cannot be empty"):
            evp_bytes_to_key(b"password", b"", 32, 16)
    
    def test_invalid_salt_length(self):
        """Test invalid salt length raises ValueError."""
        with pytest.raises(ValueError, match="salt should be 8 bytes"):
            evp_bytes_to_key(b"password", b"short", 32, 16)
    
    def test_invalid_key_length(self):
        """Test invalid key length raises ValueError."""
        with pytest.raises(ValueError, match="key_len must be positive"):
            evp_bytes_to_key(b"password", b"12345678", 0, 16)
        
        with pytest.raises(ValueError, match="key_len must be positive"):
            evp_bytes_to_key(b"password", b"12345678", -1, 16)
    
    def test_invalid_iv_length(self):
        """Test invalid IV length raises ValueError."""
        with pytest.raises(ValueError, match="iv_len must be positive"):
            evp_bytes_to_key(b"password", b"12345678", 32, 0)
    
    def test_wrong_type_password(self):
        """Test non-bytes password raises TypeError."""
        with pytest.raises(TypeError, match="password must be bytes"):
            evp_bytes_to_key("password", b"12345678", 32, 16)
    
    def test_wrong_type_salt(self):
        """Test non-bytes salt raises TypeError."""
        with pytest.raises(TypeError, match="salt must be bytes"):
            evp_bytes_to_key(b"password", "12345678", 32, 16)


class TestDecryptBatoto:
    """Tests for decrypt_batoto function."""
    
    def test_invalid_base64(self):
        """Test invalid base64 data raises ValueError."""
        with pytest.raises(ValueError, match="Failed to decode base64"):
            decrypt_batoto("not-valid-base64!!!", "password", base64.b64decode)
    
    def test_missing_salted_header(self):
        """Test data without Salted__ header raises ValueError."""
        # Create valid base64 but without Salted__ header
        data = base64.b64encode(b"no header here")
        with pytest.raises(ValueError, match="missing 'Salted__' header"):
            decrypt_batoto(data.decode(), "password", base64.b64decode)
    
    def test_data_too_short(self):
        """Test data that's too short raises ValueError."""
        # Create data with header but too short
        data = base64.b64encode(b"Salted__short")
        with pytest.raises(ValueError, match="too short"):
            decrypt_batoto(data.decode(), "password", base64.b64decode)
    
    def test_empty_encrypted_data(self):
        """Test empty encrypted data raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            decrypt_batoto("", "password", base64.b64decode)
    
    def test_empty_password(self):
        """Test empty password raises ValueError."""
        data = base64.b64encode(b"Salted__12345678" + b"x" * 16)
        with pytest.raises(ValueError, match="password cannot be empty"):
            decrypt_batoto(data.decode(), "", base64.b64decode)
    
    def test_wrong_type_encrypted_data(self):
        """Test non-string encrypted data raises TypeError."""
        with pytest.raises(TypeError, match="encrypted_b64 must be str"):
            decrypt_batoto(123, "password", base64.b64decode)
    
    def test_wrong_type_password(self):
        """Test non-string password raises TypeError."""
        data = base64.b64encode(b"Salted__12345678" + b"x" * 16)
        with pytest.raises(TypeError, match="password must be str"):
            decrypt_batoto(data.decode(), 123, base64.b64decode)
    
    def test_non_callable_decoder(self):
        """Test non-callable decoder raises TypeError."""
        with pytest.raises(TypeError, match="must be callable"):
            decrypt_batoto("data", "password", "not-a-function")


class TestGenerateUid:
    """Tests for generate_uid function."""
    
    def test_valid_uid_generation(self):
        """Test UID generation with valid inputs."""
        uid = generate_uid("/series/123/manga-title")
        
        assert isinstance(uid, str)
        assert len(uid) == 40  # SHA-1 produces 40 hex characters
    
    def test_deterministic_output(self):
        """Test same input produces same UID."""
        input_str = "/series/123/manga-title"
        
        uid1 = generate_uid(input_str)
        uid2 = generate_uid(input_str)
        
        assert uid1 == uid2
    
    def test_different_inputs(self):
        """Test different inputs produce different UIDs."""
        uid1 = generate_uid("/series/123")
        uid2 = generate_uid("/series/456")
        
        assert uid1 != uid2
    
    def test_empty_string(self):
        """Test empty string raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            generate_uid("")
    
    def test_wrong_type(self):
        """Test non-string input raises TypeError."""
        with pytest.raises(TypeError, match="Input must be str"):
            generate_uid(123)
        
        with pytest.raises(TypeError, match="Input must be str"):
            generate_uid(None)
    
    def test_unicode_handling(self):
        """Test UID generation with Unicode characters."""
        uid = generate_uid("/series/漫画/title")
        
        assert isinstance(uid, str)
        assert len(uid) == 40
