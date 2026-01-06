from bs4 import BeautifulSoup
from .config import DEFAULT_DOMAIN
from urllib.parse import urljoin
from batoto_parser.models import Manga, MangaTag, MangaChapter, MangaPage
from batoto_parser.utils import decrypt_batoto, generate_uid
from typing import List, Optional,Set
import json
import re


class BatoToParser:
    """
    Python implementation of the Batoto parser behavior:
    - get_list(page, order, filter_query)
    - get_details(manga_url)
    - get_pages(chapter_url)
    """

    def __init__(self, ctx, domain=DEFAULT_DOMAIN):
        self.ctx = ctx  # MangaLoaderContext instance
        self.domain = domain

    def abs(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return urljoin(f"https://{self.domain}", path)

    def get_list(self, page: int = 1, order: str = "update.za", query: Optional[str] = None) -> List[Manga]:
        if query:
            url = f"https://{self.domain}/search?word={query.replace(' ', '+')}&page={page}"
        else:
            url = f"https://{self.domain}/browse?sort={order}&page={page}"

        resp = self.ctx.http_get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        if soup.select_one(".browse-no-matches"):
            return []
        root = soup.select_one("#series-list")
        if not root:
            return []
        result = []
        for div in root.find_all(recursive=False):
            # --- Core fields ---
            title_el = div.select_one(".item-title")
            title = title_el.get_text(strip=True) if title_el else ""
            rel_href = title_el.get("href") if title_el else ""
            public_url = urljoin(f"https://{self.domain}", rel_href)

            cover_el = div.select_one(".item-cover img")
            cover_url = urljoin(f"https://{self.domain}", cover_el["src"]) if cover_el else None

            # --- Alt titles ---
            alt_titles = set()
            alias_el = div.select_one(".item-alias span.text-muted")
            if alias_el:
                for alt in alias_el.get_text(separator="/").split("/"):
                    alt = alt.strip()
                    if alt:
                        alt_titles.add(alt)

            # --- Genres / Tags ---
            tags = []
            for span in div.select(".item-genre span"):
                text = span.get_text(strip=True)
                if text:
                    key = text.lower().replace(" ", "_")
                    tags.append(MangaTag(title=text.title(), key=key))

            # --- Latest Chapter ---
            chap_el = div.select_one(".item-volch a.visited")
            chapter_title = chap_el.get_text(strip=True) if chap_el else None
            chapter_url = chap_el.get("href") if chap_el else None

            uploader_el = div.select_one('.item-volch a[href*="/user/"]')
            scanlator = uploader_el["href"].split("/")[-1] if uploader_el else None


            # --- Chapter object ---
            chapters = None
            if chapter_url:
                chapters = [
                    MangaChapter(
                        id=generate_uid(chapter_url),
                        title=chapter_title,
                        number=float(re.search(r"\d+", chapter_title).group()) if re.search(r"\d+", chapter_title) else 0.0,
                        url=chapter_url,
                        scanlator=scanlator,
                        upload_date_ms=None,
                        preview=urljoin(f"https://{self.domain}", chapter_url),
                    )
                ]

            # --- Final Manga object ---
            m = Manga(
                id=generate_uid(rel_href),
                title=title,
                alt_titles=alt_titles,
                url=rel_href,
                public_url=public_url,
                cover_url=cover_url,
                large_cover_url=None,
                description_html=None,
                tags=tags,
                state=None,
                authors=set(),
                originalLanguage=None,
                translatedLanguage=None,
                originalWorkStatus=None,
                uploadStatus=None,
                yearOfRelease=None,
                chapterCount=0,
                chapters=chapters
            )

            result.append(m)

        return result


    def get_details(self, manga: Manga) -> Manga:
        full = self.abs(manga.url)
        resp = self.ctx.http_get(full)
        soup = BeautifulSoup(resp.text, "lxml")
        mainer = soup.select_one("#mainer")
        if not mainer:
            return manga
        # --- Extract alternate titles ---
        alt_titles_set = set(manga.alt_titles)  # keep existing ones if any
        alias_el = soup.select_one(".alias-set")
        if alias_el:
            raw_aliases = alias_el.get_text(separator=" ").strip()
            # Split by "/" and clean extra spaces
            aliases = [a.strip() for a in raw_aliases.split("/") if a.strip()]
            alt_titles_set.update(aliases)

        details = mainer.select_one(".detail-set")
        attrs = {}
        if details:
            attr_main = details.select_one(".attr-main")
            if attr_main:
                for item in attr_main.select(".attr-item"):
                    key_el = item.find(recursive=False)
                    if not key_el:
                        continue
                    key = key_el.get_text(strip=True)
                    # second child element
                    children = item.find_all(recursive=False)
                    if len(children) >= 2:
                        attrs[key] = children[1]
        author = None
        if "Authors:" in attrs:
            author = attrs["Authors:"].get_text(strip=True)
        title = soup.select_one("h3.item-title").get_text(strip=True) if soup.select_one("h3.item-title") else manga.title
        large_cover = details.select_one("img[src]")["src"] if details and details.select_one("img[src]") else None
        desc = details.select_one("#limit-height-body-summary .limit-html").decode_contents() if details and details.select_one("#limit-height-body-summary .limit-html") else None
        genres = []
        if "Genres:" in attrs:
            for span in attrs["Genres:"].find_all("span"):
                text = span.get_text(strip=True)
                genres.append(MangaTag(title=text.title(), key=text.lower().replace(" ", "_")))
        #language,status,yearOfRelease
        originalLanguage = attrs["Original language:"].get_text(strip=True) if "Original language:" in attrs else None
        translatedLanguage = attrs["Translated language:"].get_text(strip=True) if "Translated language:" in attrs else None
        originalWorkStatus = attrs["Original work:"].get_text(strip=True) if "Original work:" in attrs else None
        uploadStatus = attrs["Upload status:"].get_text(strip=True) if "Upload status:" in attrs else None
        yearOfRelease = attrs["Year of Release:"].get_text(strip=True) if "Year of Release:" in attrs else None
        # chapters:
        chapters = []
        ep_list = soup.select_one(".episode-list .main")
        if ep_list:
            children = ep_list.find_all(recursive=False)
            # the Kotlin reversed = true; mapChapters reversed -> keep order reversed
            for idx, div in enumerate(reversed(children)):
                ch = self._parse_chapter(div, idx)
                if ch:
                    chapters.append(ch)
        return Manga(
            id=manga.id,
            title=title,
            alt_titles=alt_titles_set,
            url=manga.url,
            public_url=manga.public_url,
            cover_url=manga.cover_url,
            large_cover_url=urljoin(f"https://{self.domain}", large_cover) if large_cover else None,
            description_html=desc,
            tags=list(set(manga.tags + genres)),
            state=None,
            authors={author} if author else manga.authors,
            originalLanguage=originalLanguage,
            translatedLanguage=translatedLanguage,
            originalWorkStatus=originalWorkStatus,
            uploadStatus=uploadStatus,
            yearOfRelease=yearOfRelease,
            chapterCount=len(chapters),
            chapters=chapters,
        )

    def _parse_chapter(self, div, index):
        a = div.select_one("a.chapt")
        if not a:
            return None
        href = a.get("href")
        extra = div.select_one(".extra")
        scanlator = None
        if extra:
            g = extra.find(href=re.compile("/group/"))
            if g:
                scanlator = g.get_text(strip=True)
        # parse date like "3 days ago" -> epoch ms (approx)
        upload_ms = 0
        if extra:
            i_tags = extra.find_all("i")
            if i_tags:
                last = i_tags[-1].get_text(strip=True)
                # simple parser
                upload_ms = self._parse_relative_date(last)
        return MangaChapter(
            id=generate_uid(href),
            title=a.get_text(strip=True),
            number=float(index + 1),
            url=href,
            scanlator=scanlator,
            upload_date_ms=upload_ms,
            preview=urljoin(f"https://{self.domain}", href)
        )

    def _parse_relative_date(self, text: str) -> int:
        # returns epoch ms for approximate date
        import time
        from datetime import datetime, timedelta
        if not text:
            return 0
        m = re.match(r"(\d+)\s+(\w+)", text)
        if not m:
            return 0
        val = int(m.group(1))
        unit = m.group(2)
        now = datetime.utcnow()
        if "sec" in unit:
            dt = now - timedelta(seconds=val)
        elif "min" in unit:
            dt = now - timedelta(minutes=val)
        elif "hour" in unit:
            dt = now - timedelta(hours=val)
        elif "day" in unit:
            dt = now - timedelta(days=val)
        elif "week" in unit:
            dt = now - timedelta(weeks=val)
        elif "month" in unit:
            dt = now - timedelta(days=30*val)
        elif "year" in unit:
            dt = now - timedelta(days=365*val)
        else:
            return 0
        return int(dt.timestamp() * 1000)

    def get_pages(self, chapter_url: str) -> List[MangaPage]:
        full = self.abs(chapter_url)
        resp = self.ctx.http_get(full)
        soup = BeautifulSoup(resp.text, "lxml")
        scripts = soup.find_all("script")
        for script in scripts:
            script_text = script.string or ""
            if "const imgHttps =" in script_text:
                # find images array
                m = re.search(r"const\s+imgHttps\s*=\s*(\[[^\]]*\])", script_text, re.S)
                if not m:
                    continue
                images_json = m.group(1)
                images = json.loads(images_json)
                bato_pass_match = re.search(r"batoPass\s*=\s*([^;]+);", script_text)
                bato_word_match = re.search(r"batoWord\s*=\s*([^;]+);", script_text)
                if not bato_pass_match or not bato_word_match:
                    continue
                bato_pass_expr = bato_pass_match.group(1).strip()
                bato_word_expr = bato_word_match.group(1).strip().strip('\'"')
                # evaluate batoPass js snippet via context (may need to remove trailing semicolons)
                password = self.ctx.evaluate_js(bato_pass_expr)
                if password is None:
                    raise RuntimeError("Cannot evaluate batoPass")
                # decrypt batoWord
                decrypted = decrypt_batoto(bato_word_expr, password, self.ctx.decode_base64)
                args = json.loads(decrypted)
                pages = []
                for i, img in enumerate(images):
                    url = img if not args else img + "?" + args[i]
                    pages.append(MangaPage(id=generate_uid(url), url=url, preview=None))
                return pages
        raise RuntimeError("Cannot find images list in chapter page")
