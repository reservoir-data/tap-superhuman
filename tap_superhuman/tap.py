"""Superhuman Docs tap class."""  # noqa: CPY001

from __future__ import annotations

from typing import TYPE_CHECKING, override

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_superhuman import streams

if TYPE_CHECKING:
    from collections.abc import Sequence


class TapSuperhuman(Tap):
    """Singer tap for Superhuman Docs, built with the Meltano SDK for Singer Taps."""

    name = "tap-superhuman"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the API service.",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> Sequence[streams.SuperhumanStream]:
        return [
            streams.Docs(tap=self),
            streams.Pages(tap=self),
            streams.Formulas(tap=self),
            streams.Controls(tap=self),
            streams.Permissions(tap=self),
            streams.Tables(tap=self),
            streams.Columns(tap=self),
            streams.Rows(tap=self),
        ]
