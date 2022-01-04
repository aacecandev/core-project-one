from typing import Any, Dict, List

from pydantic import BaseSettings


class DocsSettings(BaseSettings):
    license_name: str = "MIT"
    license_url: str = (
        "https://github.com/aacecandev/core-project-one/blob/main/LICENSE"
    )
    logo_url: str = "https://raw.githubusercontent.com/aacecandev/core-project-one/main/docs/images/logo.png"
    title: str = "Open Data BCN Accidents API"
    version: str = "0.1.0"
    email: str = "dev@aacecan.com"
    repo_url: str = "https://github.com/aacecandev/core-project-one/blob/main/README.md"
    description: str = """
A simple API to retrieve accidents data from Open Data BCN. 🚀

[Open Data BCN](https://opendata.bcn.cat/) is a free and open data portal for Barcelona.

This API does queries regarding accidents occurred in BCN in several years.

## Accidents

You can make the following operations on the accident documents in the database:

- Read all or a subset of accidents
- Create one accident
- Update one accident
- Delete one accident

All the requests will throw:

- Request duration
- Response duration
- Response headers
"""
    terms_of_service: str = "Terms of service"
    tags_metadata: Any = [
        {
            "name": "info",
            "description": "Basic endpoint to test and print debug information about the API.",
            "externalDocs": {
                "description": "Code implementation",
                "url": "https://github.com/aacecandev/core-project-one/app/api/routers/api_info.py",
            },
        },
        {
            "name": "accidents",
            "description": "Endpoint to perform operations on accidents collection",
            "externalDocs": {
                "description": "Code implementation",
                "url": "https://github.com/aacecandev/core-project-one/app/api/routers/accidents.py",
            },
        },
    ]
