import pyppeteer
from settings import *
from settings import api
import platform
from util import *


async def pre_auth():
    if check_cookie():
        return True
    sys_version = platform.platform()
    if sys_version.startswith("Windows"):
        path = ob_chrome_path()
    else:
        path = macos_chrome_path
    browser = await pyppeteer.launch({
        'headless': False,
        'defaultViewport': None,
        'executablePath': path,
    })
    pages = await browser.pages()
    page = pages[0] or await browser.newPage()
    await page.goto(api['auth'])
    await page.waitForNavigation()
    cookies = await page.cookies()
    await browser.close()
    return save_cookie(cookies)
