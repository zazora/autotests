#импортируем библиотеки
from playwright.sync_api import Page, sync_playwright, expect, Route 
from playwright.async_api import async_playwright 
import time,pytest,asyncio

@pytest.mark.asyncio
@pytest.mark.parametrize("browser_auth_negative",["chromium","firefox"])
async def test_auth_negative(browser_auth_negative):
    async with async_playwright() as playwright:
        browser = await playwright[browser_auth_negative].launch()
        #browser=getattr(playwright,browser_auth_negative).launch(headless=False)
        page= await browser.new_page()
#заходим на страницу   
        await page.goto("https://www.saucedemo.com/")

# Получаем текст, кроме тех, что в <h1>
        login_list = (await page.locator(".login_credentials").inner_text()).splitlines()[1:]
        password = (await page.locator(".login_password").inner_text()).splitlines()[1].strip().strip('"')

    #Проверить успешный вход с невалидными учетными данными.  
        await page.locator("#user-name").fill(login_list[0]+"you")
        await page.locator("#password").fill(password)
        await page.get_by_role("button",name="Login").click()
    
    #Проверить отображение сообщений об ошибке при вводе неверных данных.
        error_message=await page.locator(".error-message-container").text_content()
    
        assert "Epic sadface" in error_message

        await asyncio.sleep(1)

        await browser.close()


