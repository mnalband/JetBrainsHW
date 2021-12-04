from typing import Generator

import pytest
from playwright.sync_api import sync_playwright, Page

from helpers.page_objects import MainPage, LoginPage, FavoriteProjectsPage


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


@pytest.mark.parametrize("username,password", [("admin", "admin"), ])
def test_login(page, username, password):
    main_page = MainPage(page)
    main_page.navigate()

    login_page = LoginPage(page)
    assert page.url == login_page.URL

    login_page.continue_with_username()
    assert login_page.get_header().text_content() == 'Log in to TeamCity'
    assert login_page.get_login_form().is_visible()
    login_page.login(username, password)

    favorite_projects_page = FavoriteProjectsPage(page)
    page.wait_for_url(favorite_projects_page.URL)
    assert favorite_projects_page.get_create_project().inner_text() == 'Create project...'


def test_add_project(page, login):
    favorite_projects_page = FavoriteProjectsPage(page)
    favorite_projects_page.create_project()
    page.wait_for_selector('.menuList.menuList_create')
    menu_list = page.inner_text('.menuList.menuList_create')
    list1 = 'From a repository URL\n From GitHub.com\n From Bitbucket Cloud\n From GitLab.com\n Manually'
    assert menu_list == list1
    # TODO:  Add assertion to check that Parent Root is <Root project>
    # assert page.inner_text('.runnerFormTable')
    page.fill('[id="url"]', 'https://github.com/gradle/gradle-site-plugin.git')
    page.click('[value="Proceed"]')
    assert page.wait_for_selector('.connectionSuccessful')
    assert page.text_content('.connectionSuccessful') == '\n    ✓\n    The connection to the VCS repository has been ' \
                                                         'verified\n  '
    page.click('[value="Proceed"]')
    assert page.wait_for_selector('[id="unprocessed_objectsCreated"]')
    assert page.text_content('[id="unprocessed_objectsCreated"]') == 'New project "Gradle Site Plugin", build ' \
                                                                     'configuration "Build" and VCS root ' \
                                                                     '"https://github.com/gradle/gradle-site-plugin' \
                                                                     '.git#refs/heads/master" have been successfully ' \
                                                                     'created.'
    page.click('[title="Projects"]')
    assert page.wait_for_selector('[id="https://awesomepipeline.teamcity.com_all_project_GradleSitePlugin"]')


def test_run_first_build(page, login):
    page.click('[title="Gradle Site Plugin"]')
    page.click('[data-test="run-build"]')
    assert page.wait_for_selector('[title="Build number: 1"]') and page.wait_for_selector('[aria-label="Success"]')
