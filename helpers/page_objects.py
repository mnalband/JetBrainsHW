from typing import Union, Optional

from playwright.sync_api import Page as SyncPage, Response as SyncResponse, Locator as SyncLocator
from playwright.async_api import Page as AsyncPage, Response as AsyncResponse, Locator as AsyncLocator


PageType = Union[SyncPage, AsyncPage]
ResponseType = Union[SyncResponse, AsyncResponse]
LocatorType = Union[SyncLocator, AsyncLocator]


class PageObject:
    def __init__(self, browser_page: PageType):
        self.URL = 'https://awesomepipeline.teamcity.com'
        self.page = browser_page

    def navigate(self) -> Optional[ResponseType]:
        return self.page.goto(self.URL)

    def get_locator(self, selector: str) -> LocatorType:
        locator = self.page.locator(selector)
        locator.wait_for()
        return locator


class MainPage(PageObject):
    pass


class LoginPage(PageObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.URL = f"{self.URL}/login.html"

    def continue_with_username(self) -> None:
        return self.page.click('[id="loginPasswordSwitch"]')

    def login(self, username: str, password: str) -> None:
        self.page.fill('input[name="username"]', username)
        self.page.fill('input[name="password"]', password)
        self.page.click('[class="btn loginButton"]')

    def get_header(self) -> LocatorType:
        return self.get_locator('#header')

    def get_login_form(self) -> LocatorType:
        return self.get_locator("#loginForm")


class FavoriteProjectsPage(PageObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.URL = f"{self.URL}/favorite/projects"

    def get_create_project(self) -> LocatorType:
        return self.get_locator('.FavoriteProjectsPage__links-container--xd .ring-button-primary')

    def create_project(self) -> None:
        self.get_create_project().click()
