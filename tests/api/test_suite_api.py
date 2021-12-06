import pytest

from helpers.api_client import APIClient


def test_add_project(client, delete_project):
    """ TC003 - Create a project from a repository URL / positive scenario
     Expected result: 'Gradle Site Plugin' is present in the list of projects
    """
    response = client.create_project(name="Gradle Site Plugin", id="GradleSitePlugin")
    assert response.status_code == 200
    response = client.add_git_root(
        id="my_custom_root", name="MyCustomRoot", url="https://github.com/gradle/gradle-site-plugin.git"
    )
    assert response.status_code == 200


def test_run_build(client, project):
    """ TC004 - Run the first custom build / positive scenario
    Expected result: Result of the build - 'queued'
    """
    response = client.run_build(vcs_root_id="my_custom_root")
    assert response.status_code == 200
    build_queue_dict = response.json()
    build_id = (build_queue_dict['id'])
    response = client.get_build_status(build_id=build_id)
    assert response.status_code == 200
    state = response.json()["build"][0]["state"]
    # Build could be already started or just queued when assert is executed, but in scope of this test both are valid.
    assert state in ("queued", "running")


@pytest.mark.parametrize("credentials", [("admin", "admin")])
def test_login(credentials):
    """ TC001 - Authorization token
     User is able to authorize with token to TeamCity.

     Why is this test in the end of suite? Well, I've got "403 status code due to failed CSRF check". I carefully read
     the documentation and found that it is possible to temporary disable CSRF. But in order to use internal settings
     in 'Diagnostics' I should have not the trial version of TeamCity to be able to run server not locally.
    """
    client = APIClient(credentials=credentials)
    response = client.session.get("/app/rest/server")
    assert response.status_code == 200
