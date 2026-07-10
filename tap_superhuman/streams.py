"""Stream type classes for tap-superhuman."""  # noqa: CPY001

from __future__ import annotations

from importlib import resources
from typing import TYPE_CHECKING, Any, override

from singer_sdk import OpenAPISchema, StreamSchema
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.streams import RESTStream

from tap_superhuman import openapi

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


OPENAPI_SCHEMA = OpenAPISchema[str](resources.files(openapi).joinpath("openapi.json"))


class SuperhumanStream(RESTStream[str]):
    """Superhuman Docs stream class."""

    openapi_ref: str

    url_base = "https://coda.io/apis/v1"
    records_jsonpath = "$.items[*]"
    next_page_token_jsonpath = "$.nextPageToken"  # noqa: S105
    primary_keys = ("id",)
    replication_key = None

    @property
    @override
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(token=self.config["auth_token"])

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL parameters for the Superhuman Docs API.

        Returns:
            A dictionary of URL parameters.
        """
        params: dict[str, Any] = {
            "limit": 100,
        }
        if next_page_token:
            params["pageToken"] = next_page_token
        return params


class Docs(SuperhumanStream):
    """Superhuman Docs documents."""

    name = "docs"
    path = "/docs"
    schema = StreamSchema(OPENAPI_SCHEMA, key="Doc")

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the `docs` stream."""
        super().__init__(*args, **kwargs)
        self.schema["properties"]["sourceDoc"] = {
            "x-schema-name": "DocReference",
            "description": "Reference to a Superhuman doc.",
            "type": "object",
            "required": [
                "id",
                "type",
                "browserLink",
                "href",
            ],
            "additionalProperties": False,
            "properties": {
                "id": {
                    "type": "string",
                    "description": "ID of the Superhuman doc.",
                    "example": "AbCDeFGH",
                },
                "type": {
                    "type": "string",
                    "description": "The type of this resource.",
                    "enum": [
                        "doc",
                    ],
                    "x-tsType": "Type.Doc",
                },
                "href": {
                    "type": "string",
                    "format": "url",
                    "description": "API link to the Superhuman doc.",
                    "example": "https://coda.io/apis/v1/docs/AbCDeFGH",
                },
                "browserLink": {
                    "type": "string",
                    "format": "url",
                    "description": "Browser-friendly link to the Superhuman doc.",
                    "example": "https://coda.io/d/_dAbCDeFGH",
                },
            },
        }

    @override
    def get_child_context(
        self,
        record: Record,
        context: Context | None,
    ) -> Context | None:
        """Get context for docs child streams.

        Returns:
            A dictionary of child context.
        """
        return {"docId": record["id"]}


class _DocChild(SuperhumanStream):
    parent_stream_type = Docs

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a stream with `docs` as parent stream.

        Args:
            args: Positional arguments.
            kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.schema["properties"]["docId"] = {
            "type": "string",
            "description": "Parent document ID",
        }


class Pages(_DocChild):
    """Superhuman Docs document pages."""

    name = "pages"
    path = "/docs/{docId}/pages"
    schema = StreamSchema(OPENAPI_SCHEMA, key="Page")


class Controls(_DocChild):
    """Superhuman Docs document controls."""

    name = "controls"
    path = "/docs/{docId}/controls"
    schema = StreamSchema(OPENAPI_SCHEMA, key="ControlReference")


class Formulas(_DocChild):
    """Superhuman Docs document pages."""

    name = "formulas"
    path = "/docs/{docId}/formulas"
    schema = StreamSchema(OPENAPI_SCHEMA, key="Formula")

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize `formulas` stream."""
        super().__init__(*args, **kwargs)
        del self.schema["properties"]["value"]
        self.schema["properties"]["value__string"] = {
            "description": "A Superhuman result or entity expressed as a primitive type.",  # ruff:ignore[line-too-long]
            "type": "string",
            "example": "$12.34",
        }
        self.schema["properties"]["value__number"] = {
            "description": "A Superhuman result or entity expressed as a primitive type.",  # ruff:ignore[line-too-long]
            "type": "number",
            "example": 12.34,
        }
        self.schema["properties"]["value__boolean"] = {
            "description": "A Superhuman result or entity expressed as a primitive type.",  # ruff:ignore[line-too-long]
            "type": "boolean",
            "example": True,
        }

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process formula records.

        Returns:
            A dictionary of post-processed formula records.
        """
        value = row.pop("value", None)
        if isinstance(value, str):
            row["value__string"] = value
        elif isinstance(value, bool):
            row["value__boolean"] = value
        elif isinstance(value, float):
            row["value__number"] = value
        return row


class Permissions(_DocChild):
    """Superhuman Docs document permissions."""

    name = "permissions"
    path = "/docs/{docId}/acl/permissions"
    schema = StreamSchema(OPENAPI_SCHEMA, key="Permission")

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize `permissions` stream."""
        super().__init__(*args, **kwargs)
        self.schema["properties"]["principal"]["type"] = "object"


class Tables(_DocChild):
    """Superhuman Docs document tables."""

    name = "tables"
    path = "/docs/{docId}/tables"
    schema = StreamSchema(OPENAPI_SCHEMA, key="Table")

    @override
    def get_child_context(
        self,
        record: Record,
        context: Context | None,
    ) -> Context | None:
        """Get context for `tables` child streams.

        Returns:
            A dictionary of child context.
        """
        return {
            "docId": context["docId"] if context else None,
            "tableIdOrName": record["id"],
        }


class _TableChild(SuperhumanStream):
    parent_stream_type = Tables

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a stream with `tables` as parent stream."""
        super().__init__(*args, **kwargs)
        self.schema["properties"]["tableIdOrName"] = {
            "type": "string",
            "description": "Parent table ID",
        }


class Columns(_TableChild):
    """Superhuman Docs document table columns."""

    name = "columns"
    path = "/docs/{docId}/tables/{tableIdOrName}/columns"
    schema = StreamSchema(OPENAPI_SCHEMA, key="Column")

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize `columns` stream."""
        super().__init__(*args, **kwargs)
        self.schema["properties"]["format"]["type"] = "object"


class Rows(_TableChild):
    """Superhuman Docs document table rows."""

    name = "rows"
    path = "/docs/{docId}/tables/{tableIdOrName}/rows"
    parent_stream_type = Tables
    schema = StreamSchema(OPENAPI_SCHEMA, key="Row")

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize `rows` stream."""
        super().__init__(*args, **kwargs)
        self.schema["properties"]["values"].pop("additionalProperties")
