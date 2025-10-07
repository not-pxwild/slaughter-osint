# -----------------------------------------------------------------------------
# Copyright (c) 2025 pxwild. All Rights Reserved.
# pxwild PROPRIETARY AND CONFIDENTIAL — NOT FOR MODIFICATION OR REDISTRIBUTION.
#
# This software and its source code are proprietary to pxwild. Unauthorized
# copying, modification, distribution, decompilation, reverse engineering, or
# creation of derivative works is strictly prohibited without prior written
# permission from pxwild. Any attempt to modify or remove this notice is a
# material breach of the license and will be acted upon to the fullest extent
# permitted by law.
# -----------------------------------------------------------------------------

import aiohttp
import asyncio
from typing import Dict, Any, Optional

class AsyncHTTP:
    def __init__(self, user_agent: str = "slaughter-osint/0.1", timeout: int = 15):
        self.user_agent = user_agent
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def fetch(self, url: str, method: str = "GET", headers: Optional[Dict] = None, params: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        hdrs = {"User-Agent": self.user_agent}
        if headers:
            hdrs.update(headers)
        try:
            async with aiohttp.ClientSession(timeout=self.timeout, headers=hdrs) as s:
                async with s.request(method, url, params=params, json=json) as resp:
                    text = await resp.text()
                    return {"status": resp.status, "text": text, "url": str(resp.url)}
        except Exception as e:
            return {"status": None, "error": str(e), "url": url}

    async def get_json(self, url: str, **kwargs):
        res = await self.fetch(url, **kwargs)
        if res.get("status") and res["status"] < 400:
            try:
                import json
                return {"ok": True, "data": json.loads(res["text"]), "meta": res}
            except Exception:
                return {"ok": False, "error": "invalid-json", "meta": res}
        return {"ok": False, "meta": res}
