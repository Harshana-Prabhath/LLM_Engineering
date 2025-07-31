import asyncio
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
import nest_asyncio

nest_asyncio.apply()

async def test():
    
    browser =  create_async_playwright_browser(headless=False)

    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)

    tools = toolkit.get_tools()

    tools_by_name = {tool.name: tool for tool in tools}
    print( tools_by_name)
    navigate_tool = tools_by_name["navigate_browser"]
    text_extract_tool = tools_by_name["extract_text"]

    await navigate_tool.arun(
        {"url":"https://www.dailymirror.lk/breaking-news/Sri-Lanka-to-tour-England-for-white-ball-series-in-September/108-315075"}
    )

    print("Navigation Completed!")

    text =  await text_extract_tool.arun(
            {}
            )

    print(text)
   




asyncio.run(test())

