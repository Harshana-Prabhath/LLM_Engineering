from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from typing import Optional,List

def create_sync_playwright_browser(headless: bool = True):
    with sync_playwright() as p:
        return p.chromium.launch(headless=headless)
    

async def create_async_playwright_browser(headless: bool = True, args: Optional[List[str]] = None):
    playwright = await async_playwright().start()
    return await playwright.chromium.launch(headless=headless, args=args)