"""Unit tests for batoto_parser.validators module."""

import pytest
from batoto_parser.validators import (
    ValidationError,
    validate_page_number,
    validate_sort_order,
    validate_search_query,
    validate_domain,
    validate_url,
    validate_chapter_url,
    validate_manga_url,
)


class TestValidatePageNumber:
    """Tests for validate_page_number function."""
    
    def test_valid_page_numbers(self):
        """Test valid page numbers are accepted."""
        assert validate_page_number(1) == 1
        assert validate_page_number(10) == 10
        assert validate_page_number(100) == 100
        assert validate_page_number(9999) == 9999
    
    def test_invalid_type(self):
        """Test non-integer types are rejected."""
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_page_number("1")
        
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_page_number(1.5)
    
    def test_negative_page(self):
        """Test negative page numbers are rejected."""
        with pytest.raises(ValidationError, match="must be at least 1"):
            validate_page_number(0)
        
        with pytest.raises(ValidationError, match="must be at least 1"):
            validate_page_number(-1)
    
    def test_page_too_large(self):
        """Test excessively large page numbers are rejected."""
        with pytest.raises(ValidationError, match="cannot exceed"):
            validate_page_number(10001)


class TestValidateSortOrder:
    """Tests for validate_sort_order function."""
    
    def test_valid_sort_orders(self):
        """Test all valid sort orders are accepted."""
        valid_orders = [
            "update.za", "update.az",
            "create.za", "create.az",
            "name.az", "name.za",
            "views.za", "views.az",
        ]
        for order in valid_orders:
            assert validate_sort_order(order) == order
    
    def test_invalid_sort_order(self):
        """Test invalid sort orders are rejected."""
        with pytest.raises(ValidationError, match="Invalid sort order"):
            validate_sort_order("invalid")
        
        with pytest.raises(ValidationError, match="Invalid sort order"):
            validate_sort_order("random.order")
    
    def test_empty_sort_order(self):
        """Test empty sort order is rejected."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_sort_order("")
    
    def test_invalid_type(self):
        """Test non-string types are rejected."""
        with pytest.raises(ValidationError, match="must be a string"):
            validate_sort_order(123)


class TestValidateSearchQuery:
    """Tests for validate_search_query function."""
    
    def test_valid_queries(self):
        """Test valid search queries are accepted."""
        assert validate_search_query("naruto") == "naruto"
        assert validate_search_query("one piece") == "one piece"
        assert validate_search_query("  trimmed  ") == "trimmed"
    
    def test_none_query(self):
        """Test None query is accepted."""
        assert validate_search_query(None) is None
    
    def test_empty_query(self):
        """Test empty query is rejected."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_search_query("")
        
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_search_query("   ")
    
    def test_query_too_long(self):
        """Test excessively long queries are rejected."""
        long_query = "a" * 201
        with pytest.raises(ValidationError, match="too long"):
            validate_search_query(long_query)
    
    def test_invalid_type(self):
        """Test non-string types are rejected."""
        with pytest.raises(ValidationError, match="must be a string"):
            validate_search_query(123)


class TestValidateDomain:
    """Tests for validate_domain function."""
    
    def test_valid_domains(self):
        """Test valid domains are accepted."""
        assert validate_domain("bato.si") == "bato.si"
        assert validate_domain("bato.to") == "bato.to"
    
    def test_domain_normalization(self):
        """Test domain normalization (lowercase, www removal)."""
        assert validate_domain("BATO.SI") == "bato.si"
        assert validate_domain("www.bato.si") == "bato.si"
        assert validate_domain("  bato.to  ") == "bato.to"
    
    def test_invalid_domain(self):
        """Test invalid domains are rejected."""
        with pytest.raises(ValidationError, match="not allowed"):
            validate_domain("example.com")
        
        with pytest.raises(ValidationError, match="not allowed"):
            validate_domain("google.com")
    
    def test_empty_domain(self):
        """Test empty domain is rejected."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_domain("")
    
    def test_invalid_type(self):
        """Test non-string types are rejected."""
        with pytest.raises(ValidationError, match="must be a string"):
            validate_domain(123)


class TestValidateUrl:
    """Tests for validate_url function."""
    
    def test_valid_urls(self):
        """Test valid URLs are accepted."""
        urls = [
            "https://bato.si/series/123",
            "https://bato.to/title/456",
            "http://bato.si/chapter/789",
        ]
        for url in urls:
            assert validate_url(url) == url
    
    def test_invalid_scheme(self):
        """Test URLs with invalid schemes are rejected."""
        with pytest.raises(ValidationError, match="Invalid URL scheme"):
            validate_url("ftp://bato.si/series/123")
    
    def test_invalid_domain(self):
        """Test URLs from invalid domains are rejected."""
        with pytest.raises(ValidationError, match="not allowed"):
            validate_url("https://example.com/series/123")
    
    def test_malformed_url(self):
        """Test malformed URLs are rejected."""
        with pytest.raises(ValidationError, match="Invalid URL format"):
            validate_url("not-a-url")
        
        with pytest.raises(ValidationError, match="Invalid URL format"):
            validate_url("://missing-scheme")
    
    def test_empty_url(self):
        """Test empty URL is rejected."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_url("")
    
    def test_invalid_type(self):
        """Test non-string types are rejected."""
        with pytest.raises(ValidationError, match="must be a string"):
            validate_url(123)


class TestValidateChapterUrl:
    """Tests for validate_chapter_url function."""
    
    def test_valid_chapter_urls(self):
        """Test valid chapter URLs are accepted."""
        urls = [
            "https://bato.si/chapter/123",
            "https://bato.to/chapter/456/page-1",
        ]
        for url in urls:
            assert validate_chapter_url(url) == url
    
    def test_non_chapter_url(self):
        """Test non-chapter URLs are rejected."""
        with pytest.raises(ValidationError, match="must contain '/chapter/'"):
            validate_chapter_url("https://bato.si/series/123")


class TestValidateMangaUrl:
    """Tests for validate_manga_url function."""
    
    def test_valid_manga_urls(self):
        """Test valid manga URLs are accepted."""
        urls = [
            "https://bato.si/series/123",
            "https://bato.to/title/456",
        ]
        for url in urls:
            assert validate_manga_url(url) == url
    
    def test_non_manga_url(self):
        """Test non-manga URLs are rejected."""
        with pytest.raises(ValidationError, match="must contain '/series/' or '/title/'"):
            validate_manga_url("https://bato.si/chapter/123")
