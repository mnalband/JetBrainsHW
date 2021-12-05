import httpx
import pytest


@pytest.fixture(scope="session", name="client")
def get_client():
    client = httpx.Client(
        base_url="https://awesomepipeline.teamcity.com",
        headers={
            "Authorization": "Bearer eyJ0eXAiOiAiVENWMiJ9.bGg3UC1iVlNocENJZTdHTXpLdmIyak5fNnVR.NTkzYTVjNmEtYTRmMy00NmU3LWIxMGEtNDM0ZmExNTRjNmNl",
            "Accept": "application/json",
        }
    )
    return client


@pytest.mark.parametrize("credentials", [("admin", "admin")])
def test_login(client, credentials):
    client.auth = credentials
    response = client.get("/httpAuth/app/rest/server")
    assert response.status_code == 200


def delete_project(client):
    return client.delete("/app/rest/projects/gradle_site_plugin")


def test_add_project(client):
    client.delete("/app/rest/projects/gradle_site_plugin")
    payload = {
        "parentProject": {
            "locator": "id:_Root"
        },
        "name": "Gradle Site Plugin",
        "id": "gradle_site_plugin",
        "copyAllAssociatedSettings": True
    }
    r = client.post("/app/rest/projects", json=payload)
    assert r.status_code == 200

    payload = {
        "id": "my_custom_root",
        "name": "MyCustomRoot",
        "vcsName": "jetbrains.git",
        "project": {
            "id": "gradle_site_plugin"
        },
        "properties": {
            "property": [
                {
                    "name": "authMethod",
                    "value": "ANONYMOUS"
                },
                {
                    "name": "branch",
                    "value": "refs/heads/master"
                },
                {
                    "name": "url",
                    "value": "https://github.com/gradle/gradle-site-plugin.git"
                }
            ]
        }
    }
    r = client.post("/app/rest/vcs-roots", json=payload)
    assert r.status_code == 200

    payload = {
        "id": "my_custom_root",
        "name": "Build",
        "project": {
            "id": "gradle_site_plugin",
        },
        "templates": {
            "buildType": [
                {
                    "id": "Build",
                }
            ]
        }
    }
    r = client.post("/app/rest/buildTypes", json=payload)


def test_run_build(client):
    client.delete("/app/rest/projects/gradle_site_plugin")
    payload = {
        "parentProject": {
            "locator": "id:_Root"
        },
        "name": "Gradle Site Plugin",
        "id": "gradle_site_plugin",
        "copyAllAssociatedSettings": True
    }
    r = client.post("/app/rest/projects", json=payload)
    assert r.status_code == 200

    payload = {
        "id": "my_custom_root",
        "name": "MyCustomRoot",
        "vcsName": "jetbrains.git",
        "project": {
            "id": "gradle_site_plugin"
        },
        "properties": {
            "property": [
                {
                    "name": "authMethod",
                    "value": "ANONYMOUS"
                },
                {
                    "name": "branch",
                    "value": "refs/heads/master"
                },
                {
                    "name": "url",
                    "value": "https://github.com/gradle/gradle-site-plugin.git"
                }
            ]
        }
    }
    r = client.post("/app/rest/vcs-roots", json=payload)
    assert r.status_code == 200

    payload = {
        "id": "my_custom_root",
        "name": "Build",
        "project": {
            "id": "gradle_site_plugin",
        },
        "templates": {
            "buildType": [
                {
                    "id": "Build",
                }
            ]
        }
    }
    r = client.post("/app/rest/buildTypes", json=payload)
    payload = {
            "buildType": {
                "id": "my_custom_root"
            }
        }
    r = client.post('/app/rest/buildQueue', json=payload)
    build_queue_dict = r.json()
    id_build = (build_queue_dict['id'])

    params = {
        "locator": f"id:{id_build}",
    }

    r = client.get("/app/rest/builds", params=params)
    build_dict = r.json()
    print(build_dict)
    # status = (build_dict['state'])
    # print(status)


