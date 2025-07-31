from typing import Optional, Tuple, Type
from langchain_core.pydantic_v1 import root_validator
from langchain_core.tools import BaseTool
from langchain_core.utils import guard_import

from playwright.sync_api import Browser as SyncBrowser
from playwright.async_api import Browser as AsyncBrowser

def lazy_import_playwright_browsers() -> Tuple[Type[AsyncBrowser], Type[SyncBrowser]]:
    return (
        guard_import(module_name="playwright.async_api").Browser,
        guard_import(module_name="playwright.sync_api").Browser,
    )

class BaseBrowserTool(BaseTool):
    sync_browser: Optional["SyncBrowser"] = None
    async_browser: Optional["AsyncBrowser"] = None

    @root_validator
    def validate_browser_provided(cls, values: dict) -> dict:
        lazy_import_playwright_browsers()
        if values.get("async_browser") is None and values.get("sync_browser") is None:
            raise ValueError("Either async_browser or sync_browser must be specified.")
        return values

    @classmethod
    def from_browser(cls, sync_browser: Optional[SyncBrowser] = None, async_browser: Optional[AsyncBrowser] = None) -> "BaseBrowserTool":
        lazy_import_playwright_browsers()
        return cls(sync_browser=sync_browser, async_browser=async_browser)