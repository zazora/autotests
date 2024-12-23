#импортируем библиотеки
from playwright.sync_api import Page, sync_playwright, expect, Route 
from playwright.async_api import async_playwright 
import time,pytest,asyncio

@pytest.mark.asyncio
@pytest.mark.parametrize("browser_checkout", ["chromium","firefox"])
async def test_steps_valid(browser_checkout):
    async with async_playwright() as playwright:
        browser = await playwright[browser_checkout].launch()
        #browser=getattr(playwright,browser_checkout).launch(headless=False)
        page=await browser.new_page()
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

#Добавить несколько товаров в корзину 
        goods=await page.locator(".inventory_item button").all()
        goods=goods[:3]
        for good in goods:        
                await good.click()
        await asyncio.sleep(1)
   
#Перейти к оформлению заказа, заполнить необходимые данные и подтвердить заказ.
        await page.locator(".shopping_cart_link").click()
        await page.locator(".checkout_button").click()
        await page.locator("#first-name").fill("Vasil")
        await page.locator("#last-name").fill("Zazo")
        await page.locator("#postal-code").fill("123456")
        await page.locator("#continue").click()
        await page.locator("#finish").click()
#Проверить, что после подтверждения заказа отображается соответствующее сообщение 
#об успешном оформлении.    
        confirmation = await page.locator(".complete-header").text_content()
        assert "Thank you" in confirmation

        await browser.close()





    



