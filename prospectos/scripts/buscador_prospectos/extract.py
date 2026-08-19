from __future__ import annotations

from dataclasses import dataclass

import trafilatura


@dataclass
class Extracted:
    title: str | None
    text: str | None
    language: str | None


def extract(html: str, url: str) -> Extracted:
    if not html:
        return Extracted(title=None, text=None, language=None)
    meta = trafilatura.extract_metadata(html, default_url=url)
    text = trafilatura.extract(html, include_comments=False, include_tables=False,
                               favor_recall=True, url=url)
    return Extracted(
        title=(meta.title if meta else None),
        text=text,
        language=(meta.language if meta else None),
    )
