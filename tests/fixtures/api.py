import pytest

from helpers.api_client import APIClient


@pytest.fixture(scope="session", name="client")
def get_client():
    return APIClient()


@pytest.fixture
def delete_project(request, client):
    """Delete default project.

    This fixture is defined as finalizer and not called after yield in `create_project` because
    it allows simultaneously to chain fixtures and use it as independent fixture for tests
    where project is created manually.
    """
    def finalizer():
        response = client.delete_project("GradleSitePlugin")
        print(response.text)
        assert response.status_code == 204
    request.addfinalizer(finalizer)


@pytest.fixture(name="project")
def create_project(client, delete_project):
    """Create default project."""
    response = client.create_project(name="Gradle Site Plugin", id="GradleSitePlugin")
    assert response.status_code == 200
    response = client.add_git_root(
        id="my_custom_root", name="MyCustomRoot", url="https://github.com/gradle/gradle-site-plugin.git"
    )
    print(response.text)
    assert response.status_code == 200
    client.add_build(name="Build", vcs_id="my_custom_root", project_id="GradleSitePlugin")
