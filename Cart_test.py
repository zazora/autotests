#импортируем библиотеки
from playwright.sync_api import Page, sync_playwright, expect, Route
from playwright.async_api import async_playwright  
import time,pytest,asyncio

@pytest.mark.asyncio
@pytest.mark.parametrize("browser_cart", ["chromium","firefox"])
async def test_steps_valid(browser_cart):
     async with async_playwright() as playwright:
        browser = await playwright[browser_cart].launch()
        #browser=getattr(playwright,browser_cart).launch(headless=False)
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

    #Добавить несколько товаров в корзину и убедиться, 
    #что количество товаров и общая сумма отображаются корректно.
        goods = (await page.locator(".inventory_item button").all())
        goods=goods[:3]
        for good in goods:
            await good.click()
         
        await asyncio.sleep(1)
        cart_badge = await page.locator(".shopping_cart_badge").text_content()
        assert int(cart_badge) == len(goods)

        await browser.close()




     







    



