#импортируем библиотеки
from playwright.sync_api import Page, sync_playwright, expect, Route 
from playwright.async_api import async_playwright 
import time, pytest, asyncio

# Параметризация браузеров
@pytest.mark.asyncio
@pytest.mark.parametrize("browser_auth", ["chromium", "firefox"])  
async def test_steps_valid(browser_auth):
    async with async_playwright() as playwright:
# Запускаем браузер по имени
        browser = await playwright[browser_auth].launch()
        #browser = getattr(playwright, browser_auth).launch(headless=False)
        page = await browser.new_page()
#заходим на страницу   
        await page.goto("https://www.saucedemo.com/")

# Получаем текст, кроме тех, что в <h1>
        login_list = (await page.locator(".login_credentials").inner_text()).splitlines()[1:]
        password = (await page.locator(".login_password").inner_text()).splitlines()[1].strip().strip('"')

    #Проверить успешный вход с валидными учетными данными.
        await page.locator("#user-name").fill(login_list[0])
        await page.locator("#password").fill(password)
        await page.get_by_role("button",name="Login").click()
        await asyncio.sleep(1)

        assert page.url == "https://www.saucedemo.com/inventory.html"

        await browser.close()








     







    



