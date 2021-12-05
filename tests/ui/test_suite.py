from typing import Generator

import pytest
from playwright.sync_api import sync_playwright, Page

from helpers.page_objects import MainPage, LoginPage, FavoriteProjectsPage, AdminPage
from tests.api.test_suite import get_client as client

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
    """ TC001 - Authorization with username and password / positive scenario
     User is able to authorize with username and password credentials to TeamCity.

     Expected Result: User is redirected to https://awesomepipeline.teamcity.com/favorite/projects.
     User is able to see 'Welcome to TeamCity' section. 'Create project...' is also available.
    """

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
    assert favorite_projects_page.get_create_project_button().inner_text() == 'Create project...'


def test_add_project(page, login):
    """ TC003 - Create a project from a repository URL / positive scenario
     Expected result: 'Gradle Site Plugin' is present in the list of projects
    """
    favorite_projects_page = FavoriteProjectsPage(page)
    favorite_projects_page.open_create_project()
    admin_page = AdminPage(page)
    connections_list = admin_page.get_connections_list()
    assert connections_list.inner_text() == ('From a repository URL\n From GitHub.com\n From Bitbucket Cloud\n'
                                             ' From GitLab.com\n Manually')
    admin_page.add_project_from_url("https://github.com/gradle/gradle-site-plugin.git")
    connection_status = admin_page.get_connection_status()
    assert connection_status.text_content() == '\n    ✓\n    The connection to the VCS repository has been verified\n  '

# TODO: check this asserts. Needs modifications
    check_data = admin_page.check_data_before_proceed()
    assert check_data.text_content() == "Gradle Site Plugin"
    assert check_data.text_content("#buildTypeName") == "Build"
    assert check_data.text_content("#branch") == "refs/heads/master"

    admin_page.proceed()

    notification = admin_page.get_project_create_notification()
    assert notification.text_content() == ('New project "Gradle Site Plugin", build configuration "Build" and VCS root'
                                           ' "https://github.com/gradle/gradle-site-plugin.git#refs/heads/master"'
                                           ' have been successfully created.')
    main_page = MainPage(page)
    main_page.open_projects()
    page.wait_for_selector('[id="https://awesomepipeline.teamcity.com_all_project_GradleSitePlugin"]')


def test_run_first_build(page, login):
    """ TC004 - Run the first custom build / positive scenario
    Expected result:  build number should be #1.
    Result of the build - 'Success'
    """
    # Delete project
    # TODO: Add delete and create project in nicer way
    client.delete("/app/rest/projects/gradle_site_plugin")
    # TODO: Add project adding via API here
    page.click('[title="Gradle Site Plugin"]')
    page.click('[data-test="run-build"]')
    assert page.wait_for_selector('[title="Build number: 1"]') and page.wait_for_selector('[aria-label="Success"]')
