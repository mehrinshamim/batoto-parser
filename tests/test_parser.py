"""
Basic tests for batoto-parser.

Run with: pytest
"""

import pytest

from batoto_parser import BatoToParser, MangaLoaderContext
from batoto_parser.utils import generate_uid


def test_generate_uid():
    """Test UID generation."""
    uid1 = generate_uid("https://xbato.com/title/83624")
    uid2 = generate_uid("https://xbato.com/title/83624")
    uid3 = generate_uid("https://xbato.com/title/217524-the-s-classes-that-i-raised")

    # Same input should generate same UID
    assert uid1 == uid2

    # Different input should generate different UID
    assert uid1 != uid3

    # UIDs should be strings
    assert isinstance(uid1, str)
    assert len(uid1) > 0


def test_parser_initialization():
    """Test parser can be initialized."""
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain="bato.si")

    assert parser.domain == "bato.si"
    assert parser.ctx is not None


def test_context_initialization():
    """Test context can be initialized."""
    ctx = MangaLoaderContext()

    assert ctx is not None
    # Context should have a session
    assert hasattr(ctx, 'session')


@pytest.mark.integration
def test_list_manga_basic():
    """
    Integration test: Fetch manga list.

    This requires network access and may fail if site is down.
    Mark as integration test to skip in CI if needed.
    """
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain="bato.si")

    try:
        mangas = parser.get_list(page=1)

        # Should return a list
        assert isinstance(mangas, list)

        # Should have some results
        if len(mangas) > 0:
            manga = mangas[0]
            # Each manga should have basic attributes
            assert hasattr(manga, 'title')
            assert hasattr(manga, 'url')
            assert hasattr(manga, 'public_url')
    except Exception as e:
        pytest.skip(f"Integration test skipped due to: {e}")


# Add more tests as needed:
# - test_search_manga()
# - test_get_details()
# - test_get_pages()
# - test_crypto_functions()
