from typing import Generator

import pytest
from playwright.sync_api import Page, sync_playwright

from helpers.page_objects import MainPage, LoginPage


@pytest.fixture(name="page")
def get_new_page() -> Generator[Page, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


@pytest.fixture
def login(page) -> None:
    MainPage(page).navigate()
    login_page = LoginPage(page)
    login_page.continue_with_username()
    login_page.login("admin", "admin")
