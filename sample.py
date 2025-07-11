import asyncio
from playwright.async_api import async_playwright

async def main():
    # Manually start Playwright
    playwright = await async_playwright().start()

    # Launch browser
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://bing.com")
    print(await page.title())

    # Clean up: close browser and stop Playwright
    await browser.close()
    await playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())
