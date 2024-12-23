#импортируем библиотеки
from playwright.sync_api import Page, sync_playwright, expect, Route 
from playwright.async_api import async_playwright 
import time,pytest,asyncio

@pytest.mark.asyncio
@pytest.mark.parametrize("browser_logout", ["chromium","firefox"])
async def test_steps_valid(browser_logout):
    async with async_playwright() as playwright:
        browser = await playwright[browser_logout].launch()
        #browser=getattr(playwright,browser_logout).launch(headless=False)
        page= await browser.new_page()
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
#Проверить корректность процесса выхода из учетной записи  
        await page.locator("#react-burger-menu-btn").click()
        await page.locator("#logout_sidebar_link").click()

        assert page.url == "https://www.saucedemo.com/"
    
        await browser.close()







     







    


