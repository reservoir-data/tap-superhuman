# `tap-superhuman`

`tap-superhuman` is a Singer tap for Superhuman Docs (formerly Coda), built with the Meltano SDK for Singer Taps.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

## Capabilities

- `catalog`
- `discover`
- `about`
- `stream-maps`

## Settings

| Setting | Required | Default | Description |
|:-----------|:--------:|:-------:|:------------|
| auth_token | True | None | The token to authenticate against the API service. |

A full list of supported settings and capabilities is available by running: `tap-superhuman --about`

### Source Authentication and Authorization

See the documentation: https://docs.superhuman.com/developers/apis/v1#section/Authentication.

## Usage

You can easily run `tap-superhuman` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-superhuman --version
tap-superhuman --help
tap-superhuman --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_superhuman/tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-superhuman` CLI interface directly using `poetry run`:

```bash
poetry run tap-superhuman --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-superhuman
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-superhuman --version
# OR run a test `elt` pipeline:
meltano elt tap-superhuman target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
