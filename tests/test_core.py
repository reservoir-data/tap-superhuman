"""Tests standard tap features using the built-in SDK tests library."""  # noqa: CPY001

from __future__ import annotations

import datetime

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_superhuman.tap import TapSuperhuman

SAMPLE_CONFIG = {"start_date": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")}

TestTapSuperhuman = get_tap_test_class(
    TapSuperhuman,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(
        ignore_no_records=True,
    ),
    # TODO: Enable this test after the SDK handles AllOf properties.  # noqa: TD002, TD003
    include_stream_attribute_tests=True,
)
