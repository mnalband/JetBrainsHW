from typing import Tuple

import httpx


class APIClient:

    def __init__(self, base_url: str = "https://awesomepipeline.teamcity.com", token: str = None, credentials: Tuple[str, str] = None):
        parameters = {
            "headers": {
                "Accept": "application/json",
            }
        }
        if credentials is not None:
            base_url += "/httpAuth"
            parameters["auth"] = credentials
        parameters["base_url"] = base_url
        if token is None:
            parameters["headers"]["authorization"] = ("Bearer eyJ0eXAiOiAiVENWMiJ9.bGg3UC1iVlNocENJZTdHTXpLdmIyak5fNnVR"
                                                      ".NTkzYTVjNmEtYTRmMy00NmU3LWIxMGEtNDM0ZmExNTRjNmNl")
        self.session = httpx.Client(**parameters)

    def create_project(self, parent_locator: str = "id:_Root", *, name: str, id: str):
        payload = {
            "parentProject": {
                "locator": parent_locator
            },
            "name": name,
            "id": id,
            "copyAllAssociatedSettings": True,
        }
        return self.session.post("/app/rest/projects", json=payload)

    def delete_project(self, id: str):
        return self.session.delete(f"/app/rest/projects/{id}")

    def add_git_root(self, *, id: str, name: str, url: str):
        """Add VSC (git) root to the default project.

        For the limited scope of this task a lot of fields are left in default state and can't be changed,
        i.e. project id.
        """

        payload = {
            "id": id,
            "name": name,
            "vcsName": "jetbrains.git",
            "project": {
                "id": "GradleSitePlugin"
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
                        "value": url
                    }
                ]
            }
        }
        return self.session.post("/app/rest/vcs-roots", json=payload)

    def add_build(self, *, name: str, vcs_id: str, project_id: str):
        payload = {
            "id": vcs_id,
            "name": name,
            "project": {
                "id": project_id,
            },
            "templates": {
                "buildType": [
                    {
                        "id": "Build",
                    }
                ]
            }
        }
        return self.session.post("/app/rest/buildTypes", json=payload)

    def run_build(self, *, vcs_root_id: str):
        payload = {
            "buildType": {
                "id": vcs_root_id
            }
        }
        return self.session.post('/app/rest/buildQueue', json=payload)

    def get_build_status(self, *, build_id: str):
        params = {"locator": f"id:{build_id}"}
        return self.session.get("/app/rest/builds", params=params)
