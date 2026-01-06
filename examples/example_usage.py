"""
Example usage of batoto-parser as a library.

This demonstrates how to use batoto-parser programmatically
in your own Python projects.
"""

from batoto_parser import BatoToParser, MangaLoaderContext, Manga
from batoto_parser.utils import generate_uid


def example_list_manga():
    """Example: List/browse manga from the site."""
    print("=" * 60)
    print("Example 1: Listing manga")
    print("=" * 60)
    
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain="bato.si")
    
    # Get first page
    mangas = parser.get_list(page=1)
    
    print(f"Found {len(mangas)} manga on page 1:")
    for manga in mangas[:5]:  # Show first 5
        print(f"  - {manga.title}")
        print(f"    URL: {manga.public_url}")
    print()


def example_search_manga():
    """Example: Search for specific manga."""
    print("=" * 60)
    print("Example 2: Searching manga")
    print("=" * 60)
    
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain="bato.si")
    
    # Search
    query = "one piece"
    results = parser.get_list(page=1, query=query)
    
    print(f"Search results for '{query}':")
    for manga in results[:3]:  # Show first 3
        print(f"  - {manga.title}")
        print(f"    URL: {manga.public_url}")
    print()


def example_get_details():
    """Example: Get detailed manga information."""
    print("=" * 60)
    print("Example 3: Getting manga details")
    print("=" * 60)
    
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain="bato.si")
    
    # Create minimal manga object (you'd get this from list/search)
    manga = Manga(
        id=generate_uid("/series/Example-Manga"),
        title="Example Manga",
        alt_titles=set(),
        url="/series/Example-Manga",
        public_url="https://bato.si/series/Example-Manga",
        cover_url=None,
        large_cover_url=None,
        description_html=None,
        tags=[],
        state=None,
        authors=set(),
        originalLanguage=None,
        translatedLanguage=None,
        originalWorkStatus=None,
        uploadStatus=None,
        yearOfRelease=None,
        chapterCount=0,
        chapters=[],
    )
    
    # Get full details
    detailed_manga = parser.get_details(manga)
    
    print(f"Title: {detailed_manga.title}")
    print(f"Authors: {', '.join(detailed_manga.authors)}")
    print(f"Status: {detailed_manga.state}")
    print(f"Chapters: {detailed_manga.chapterCount}")
    print(f"First 3 chapters:")
    for chapter in detailed_manga.chapters[:3]:
        print(f"  - Chapter {chapter.chapterNumber}: {chapter.title}")
        print(f"    URL: {chapter.public_url}")
    print()


def example_get_pages():
    """Example: Get chapter pages/images."""
    print("=" * 60)
    print("Example 4: Getting chapter pages")
    print("=" * 60)
    
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain="bato.si")
    
    # Get pages for a chapter (requires Node.js)
    chapter_url = "/reader/12345"  # Replace with real chapter URL
    
    try:
        pages = parser.get_pages(chapter_url)
        
        print(f"Found {len(pages)} pages in chapter:")
        for page in pages[:5]:  # Show first 5
            print(f"  - Page {page.pageNumber}: {page.imageUrl}")
    except Exception as e:
        print(f"Error getting pages (ensure Node.js is installed): {e}")
    print()


def example_custom_domain():
    """Example: Use with a different domain."""
    print("=" * 60)
    print("Example 5: Using custom domain")
    print("=" * 60)
    
    # You can parse other Batoto-style sites
    ctx = MangaLoaderContext()
    parser = BatoToParser(ctx, domain="example-manga-site.com")
    
    print("Parser configured for: example-manga-site.com")
    print("(This would work if the site uses Batoto's layout)")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Batoto Parser - Library Usage Examples" + " " * 9 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    try:
        example_list_manga()
    except Exception as e:
        print(f"Example 1 failed: {e}\n")
    
    try:
        example_search_manga()
    except Exception as e:
        print(f"Example 2 failed: {e}\n")
    
    try:
        # example_get_details()  # Commented out - needs real manga URL
        print("Example 3: Skipped (needs real manga URL)")
        print()
    except Exception as e:
        print(f"Example 3 failed: {e}\n")
    
    try:
        # example_get_pages()  # Commented out - needs real chapter URL
        print("Example 4: Skipped (needs real chapter URL)")
        print()
    except Exception as e:
        print(f"Example 4 failed: {e}\n")
    
    example_custom_domain()
    
    print("=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()