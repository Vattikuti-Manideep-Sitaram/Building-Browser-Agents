import asyncio
import json
import os
import logging
import nest_asyncio
import pprint
import base64
from io import BytesIO
import pandas as pd
from playwright.async_api import async_playwright
from openai import OpenAI
from PIL import Image
from tabulate import tabulate
from IPython.display import display, HTML, Markdown
from pydantic import BaseModel
from helpers import get_openai_api_key, visualizeCourses

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=get_openai_api_key())

class WebScraperAgent:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        logger.info("WebScraperAgent initialized")
    
    async def init_browser(self):
        logger.info("Starting Playwright")
        self.playwright = await async_playwright().start()
        logger.info("Launching browser")
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-accelerated-2d-canvas",
                "--disable-gpu",
                "--no-zygote",
                "--disable-audio-output",
                "--disable-software-rasterizer",
                "--disable-webgl",
                "--disable-web-security",
                "--disable-features=LazyFrameLoading",
                "--disable-features=IsolateOrigins",
                "--disable-background-networking"
            ]
        )
        self.page = await self.browser.new_page()
        logger.info("Browser launched and new page created: %s", self.browser)
    
    async def scrape_content(self, url):
        logger.info("Scraping content from URL: %s", url)
        if not self.page or self.page.is_closed():
            logger.info("Page not available or closed, initializing browser")
            await self.init_browser()
        await self.page.goto(url, wait_until="load")
        logger.info("Page loaded, waiting for network to settle")
        await self.page.wait_for_timeout(2000)
        content = await self.page.content()
        logger.info("Content fetched (length: %d chars)", len(content))
        return content
    
    async def take_screenshot(self, path="screenshot.png"):
        logger.info("Taking full-page screenshot: %s", path)
        await self.page.screenshot(path=path, full_page=True)
        logger.info("Screenshot saved to %s", path)
        return path
    
    async def screenshot_buffer(self):
        logger.info("Taking screenshot to buffer")
        screenshot_bytes = await self.page.screenshot(type="png", full_page=False)
        await self.take_screenshot()
        logger.info("Buffer screenshot ready (size: %d bytes)", len(screenshot_bytes))
        return screenshot_bytes
    
    async def close(self):
        logger.info("Closing browser and Playwright")
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")
        if self.playwright:
            await self.playwright.stop()
            logger.info("Playwright stopped")
        self.playwright = None
        self.browser = None
        self.page = None
        logger.info("WebScraperAgent cleaned up")

class DeepLearningCourse(BaseModel):
    title: str
    description: str
    presenter: list[str]
    imageUrl: str
    courseUrl: str

class DeepLearningCourseList(BaseModel):
    courses: list[DeepLearningCourse]

async def process_with_llm(html, instructions):
    logger.info("Invoking OpenAI LLM with instructions: %s", instructions)
    completion = client.beta.chat.completions.parse(
         model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": f"You are an expert web scraping agent. Extract JSON per instructions: {instructions}"},
            {"role": "user", "content": html[:150000]}
        ],
        temperature=0.1,
        response_format=DeepLearningCourseList,
    )
    result = completion.choices[0].message.parsed
    logger.info("LLM returned %d courses", len(result.courses))
    return result

async def webscraper(target_url, instruction):
    logger.info("Starting webscraper for URL: %s", target_url)
    response = None
    screenshot = None
    try:
        html_content = await scraper.scrape_content(target_url)
        screenshot = await scraper.screenshot_buffer()
        response = await process_with_llm(html_content, instruction)
    except Exception as e:
        logger.exception("Error during scraping or processing: %s", e)
    finally:
        await scraper.close()
    return response, screenshot
        
scraper = WebScraperAgent()

target_url = "https://www.deeplearning.ai/courses"
base_url = "https://www.deeplearning.ai"
subject = "Retrieval Augmented Generation (RAG) "

instructions = f"""
Read the description of the courses and only 
provide the three courses that are about {subject}. 
Make sure that we don't have any other
cources in the output
"""

async def main():
    logger.info("Main routine started")
    result, screenshot = await webscraper(target_url, instructions)
    if result:
        logger.info("Scraping completed successfully")
        pprint.pprint(result.dict())
    else:
        logger.warning("No result returned")
    logger.info("Routine finished")
    # await visualizeCourses(result=result, 
    #                    screenshot=screenshot, 
    #                    target_url=target_url, 
    #                    instructions=instructions, 
    #                    base_url=base_url)

if __name__ == "__main__":
    asyncio.run(main())
