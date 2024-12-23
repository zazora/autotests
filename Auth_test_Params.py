import pytest, time, asyncio
from playwright.sync_api import Page, sync_playwright, expect
from playwright.async_api import async_playwright

@pytest.mark.asyncio
@pytest.mark.parametrize("username","password",[
    ("standard_user", "secret_sauce"),  # Валидные данные
    ("locked_out_user", "secret_sauce"),  # Невалидный пользователь
    ("", "secret_sauce"),  # Пустое имя пользователя
    ("standard_user", ""),  # Пустой пароль
    ])
# Параметризация браузеров
@pytest.mark.parametrize("browser_params", ["chromium", "firefox"])  
async def test_steps_valid(browser_params, username, password):
    async with async_playwright() as playwright:
    # Запускаем браузер в зависимости от переданного имени
        browser = await playwright[browser_params].launch()
        #browser = getattr(playwright, browser_params).launch(headless=False)
        page = await browser.new_page()

    # Заходим на страницу
        await page.goto("https://www.saucedemo.com/")
    # Заполняем имя пользователя и пароль
        await page.locator("#user-name").fill(username)
        await page.locator("#password").fill(password)
        await page.get_by_role("button", name="Login").click()
        await asyncio.sleep(1)
    # Проверяем результат ветвлением
        if username == "standard_user" and password == "secret_sauce":
        # Успешный вход
            await expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        else:
        # Ошибка 
            error_message = await page.locator(".error-message-container").text_content()
            assert "Epic sadface" in error_message

        await browser.close()

    



