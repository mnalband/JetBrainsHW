from typing import Union, Optional, Dict

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
    def open_projects(self):
        self.page.click('[title="Projects"]')


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

    def get_create_project_button(self) -> LocatorType:
        return self.get_locator('.FavoriteProjectsPage__links-container--xd .ring-button-primary')

    def open_create_project(self) -> None:
        self.get_create_project_button().click()


class AdminPage(PageObject):

    def proceed(self):
        self.page.click('[value="Proceed"]')

    def get_connections_list(self) -> LocatorType:
        return self.get_locator('.menuList.menuList_create')

    def add_project_from_url(self, url: str):
        self.page.fill('[id="url"]', url)
        self.proceed()

    def get_connection_status(self) -> LocatorType:
        return self.get_locator('.connectionSuccessful')

    def get_project_create_notification(self) -> LocatorType:
        return self.get_locator('[id="unprocessed_objectsCreated"]')

    def get_project_data(self) -> Dict[str, LocatorType]:
        return {
            "name": self.get_locator("#projectName"),
            "build_type": self.get_locator("#buildTypeName"),
            "branch_spec": self.get_locator(r"#teamcity\:branchSpec"),
        }
