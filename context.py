import subprocess
import requests
from typing import Optional

class MangaLoaderContext:
    """
    Minimal context object. Holds a requests.Session (with cookie jar),
    and an evaluate_js function that can run a small JS snippet via node.
    """

    def __init__(self, user_agent: str = "Mozilla/5.0"):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    # convenience HTTP GET returning Response
    def http_get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, **kwargs)

    # evaluate a small JS expression (string) and return its result as string.
    # This runs node if available. For production, embed a JS engine for speed.
    def evaluate_js(self, js_expr: str) -> Optional[str]:
        # wrap expression into something that prints JSON string safely
        # js_expr is expected to produce a value (string/number)
        script = f'console.log(JSON.stringify({js_expr}))'
        try:
            proc = subprocess.run(
                ["node", "-e", script],
                capture_output=True,
                check=True,
                text=True,
                timeout=5,
            )
            out = proc.stdout.strip()
            if not out:
                return None
            import json
            try:
                val = json.loads(out)
                return val if isinstance(val, str) else str(val)
            except Exception:
                return out
        except Exception:
            return None

    def decode_base64(self, s: str) -> bytes:
        import base64
        return base64.b64decode(s)
