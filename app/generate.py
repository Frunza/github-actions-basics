#!/usr/bin/env python3

from typing import Dict, List, Any

def formatLinks(links: List[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for link in links:
        if not isinstance(link, dict):
            continue
        label = str(link.get("label", "")).strip()
        url = str(link.get("url", "")).strip()
        if label and url:
            parts.append(f"[{label}]({url})")
    return " ".join(parts)
