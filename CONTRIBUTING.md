# Contributing

## Setup

```bash
git clone https://github.com/aayushmaanhooda/fastapi-seed
cd fastapi-seed
uv sync
```

## Making changes

- Templates live in `src/fastapi_seed/templates/`
- Prompt flow is in `src/fastapi_seed/prompts.py`
- File generation logic is in `src/fastapi_seed/generator.py`

## Testing

```bash
uv run pytest          # run tests
uv run ruff check .    # lint
uv run ruff format .   # format
```

## Testing the CLI locally

```bash
uv run fastapi-seed init my-test-app
```

## Submitting a PR

1. Fork the repo
2. Create a branch (`git checkout -b my-feature`)
3. Make your changes + add tests if needed
4. Ensure `pytest` and `ruff check .` pass
5. Open a pull request
