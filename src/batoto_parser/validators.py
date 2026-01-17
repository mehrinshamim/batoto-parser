"""
Input validation functions for batoto-parser.

This module provides validation functions for user inputs including
page numbers, sort orders, search queries, domains, and URLs.
"""

from typing import Optional, Tuple
from urllib.parse import urlparse


# Valid sort orders for Batoto
VALID_SORT_ORDERS = {
    "update.za",  # Recently updated (default)
    "update.az",  # Oldest updated
    "create.za",  # Recently added
    "create.az",  # Oldest added
    "name.az",    # A-Z
    "name.za",    # Z-A
    "views.za",   # Most views
    "views.az",   # Least views
}

# Allowed Batoto domains
ALLOWED_DOMAINS = ("bato.si", "bato.to")

# Validation constraints
MAX_QUERY_LENGTH = 200
MIN_PAGE_NUMBER = 1
MAX_PAGE_NUMBER = 10000  # Reasonable upper limit


class ValidationError(ValueError):
    """Raised when input validation fails."""
    pass


def validate_page_number(page: int) -> int:
    """
    Validate page number is a positive integer within reasonable bounds.
    
    Args:
        page: Page number to validate
        
    Returns:
        Validated page number
        
    Raises:
        ValidationError: If page number is invalid
        
    Examples:
        >>> validate_page_number(1)
        1
        >>> validate_page_number(100)
        100
        >>> validate_page_number(0)
        Traceback (most recent call last):
        ...
        ValidationError: Page number must be at least 1, got 0
    """
    if not isinstance(page, int):
        raise ValidationError(
            f"Page number must be an integer, got {type(page).__name__}"
        )
    
    if page < MIN_PAGE_NUMBER:
        raise ValidationError(
            f"Page number must be at least {MIN_PAGE_NUMBER}, got {page}"
        )
    
    if page > MAX_PAGE_NUMBER:
        raise ValidationError(
            f"Page number cannot exceed {MAX_PAGE_NUMBER}, got {page}"
        )
    
    return page


def validate_sort_order(order: str) -> str:
    """
    Validate sort order is a recognized Batoto sort option.
    
    Args:
        order: Sort order string to validate
        
    Returns:
        Validated sort order
        
    Raises:
        ValidationError: If sort order is invalid
        
    Examples:
        >>> validate_sort_order("update.za")
        'update.za'
        >>> validate_sort_order("invalid")
        Traceback (most recent call last):
        ...
        ValidationError: Invalid sort order 'invalid'. Valid options: ...
    """
    if not isinstance(order, str):
        raise ValidationError(
            f"Sort order must be a string, got {type(order).__name__}"
        )
    
    if not order:
        raise ValidationError("Sort order cannot be empty")
    
    if order not in VALID_SORT_ORDERS:
        valid_orders = ", ".join(sorted(VALID_SORT_ORDERS))
        raise ValidationError(
            f"Invalid sort order '{order}'. "
            f"Valid options: {valid_orders}"
        )
    
    return order


def validate_search_query(query: Optional[str]) -> Optional[str]:
    """
    Validate search query is non-empty and within length limits.
    
    Args:
        query: Search query string to validate (can be None)
        
    Returns:
        Validated query or None
        
    Raises:
        ValidationError: If query is invalid
        
    Examples:
        >>> validate_search_query("naruto")
        'naruto'
        >>> validate_search_query(None)
        >>> validate_search_query("")
        Traceback (most recent call last):
        ...
        ValidationError: Search query cannot be empty
    """
    if query is None:
        return None
    
    if not isinstance(query, str):
        raise ValidationError(
            f"Search query must be a string, got {type(query).__name__}"
        )
    
    # Strip whitespace
    query = query.strip()
    
    if not query:
        raise ValidationError("Search query cannot be empty")
    
    if len(query) > MAX_QUERY_LENGTH:
        raise ValidationError(
            f"Search query too long: {len(query)} characters. "
            f"Maximum allowed: {MAX_QUERY_LENGTH}"
        )
    
    return query


def validate_domain(domain: str) -> str:
    """
    Validate domain is properly formatted and in allowed list.
    
    Args:
        domain: Domain name to validate
        
    Returns:
        Validated domain
        
    Raises:
        ValidationError: If domain is invalid
        
    Examples:
        >>> validate_domain("bato.si")
        'bato.si'
        >>> validate_domain("bato.to")
        'bato.to'
        >>> validate_domain("invalid.com")
        Traceback (most recent call last):
        ...
        ValidationError: Domain 'invalid.com' not allowed. Valid domains: bato.si, bato.to
    """
    if not isinstance(domain, str):
        raise ValidationError(
            f"Domain must be a string, got {type(domain).__name__}"
        )
    
    if not domain:
        raise ValidationError("Domain cannot be empty")
    
    # Normalize domain (lowercase, remove www.)
    domain = domain.lower().strip()
    domain = domain.replace("www.", "")
    
    if domain not in ALLOWED_DOMAINS:
        valid_domains = ", ".join(ALLOWED_DOMAINS)
        raise ValidationError(
            f"Domain '{domain}' not allowed. "
            f"Valid domains: {valid_domains}"
        )
    
    return domain


def validate_url(
    url: str,
    allowed_domains: Tuple[str, ...] = ALLOWED_DOMAINS
) -> str:
    """
    Validate URL is properly formatted and from an allowed domain.
    
    Args:
        url: URL string to validate
        allowed_domains: Tuple of allowed domain names
        
    Returns:
        Validated URL
        
    Raises:
        ValidationError: If URL is invalid
        
    Examples:
        >>> validate_url("https://bato.si/series/123")
        'https://bato.si/series/123'
        >>> validate_url("invalid-url")
        Traceback (most recent call last):
        ...
        ValidationError: Invalid URL format: invalid-url
    """
    if not isinstance(url, str):
        raise ValidationError(
            f"URL must be a string, got {type(url).__name__}"
        )
    
    if not url:
        raise ValidationError("URL cannot be empty")
    
    url = url.strip()
    
    try:
        parsed = urlparse(url)
        
        # Check if URL has scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError(
                f"Invalid URL format: {url}. "
                "URL must include scheme (http/https) and domain."
            )
        
        # Check if scheme is http or https
        if parsed.scheme not in ("http", "https"):
            raise ValidationError(
                f"Invalid URL scheme: {parsed.scheme}. "
                "Only http and https are supported."
            )
        
        # Check if domain is in allowed list
        domain = parsed.netloc.lower()
        domain = domain.replace("www.", "")
        
        if domain not in allowed_domains:
            valid_domains = ", ".join(allowed_domains)
            raise ValidationError(
                f"Domain '{domain}' not allowed. "
                f"Valid domains: {valid_domains}"
            )
        
        return url
        
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid URL format: {url}. Error: {e}")


def validate_chapter_url(url: str) -> str:
    """
    Validate chapter URL format.
    
    Args:
        url: Chapter URL to validate
        
    Returns:
        Validated chapter URL
        
    Raises:
        ValidationError: If URL is invalid or not a chapter URL
        
    Examples:
        >>> validate_chapter_url("https://bato.si/chapter/123")
        'https://bato.si/chapter/123'
    """
    validated_url = validate_url(url)
    
    # Check if URL contains /chapter/ path
    if "/chapter/" not in validated_url.lower():
        raise ValidationError(
            f"Invalid chapter URL: {url}. "
            "Chapter URLs must contain '/chapter/' in the path."
        )
    
    return validated_url


def validate_manga_url(url: str) -> str:
    """
    Validate manga/series URL format.
    
    Args:
        url: Manga URL to validate
        
    Returns:
        Validated manga URL
        
    Raises:
        ValidationError: If URL is invalid or not a manga URL
        
    Examples:
        >>> validate_manga_url("https://bato.si/series/123")
        'https://bato.si/series/123'
    """
    validated_url = validate_url(url)
    
    # Check if URL contains /series/ or /title/ path
    if "/series/" not in validated_url.lower() and "/title/" not in validated_url.lower():
        raise ValidationError(
            f"Invalid manga URL: {url}. "
            "Manga URLs must contain '/series/' or '/title/' in the path."
        )
    
    return validated_url
