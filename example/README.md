# Example

This folder is a minimal working example that you can copy to get started.

## Environment

Use a virtual environment as follows.

Before development, run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --requirement requirements.txt
```

After development, run

```bash
deactivate
```

## Development

See what's available with

```bash
journal --help
```

To test, run

```bash
journal test
```

To test in an isolated Docker environment, there is also `journal test_in_isolation`, which may be useful for continuous integration.

Render a notebook as in

```bash
journal generate --open src/notebooks/uncertainty.py
```

Edit a notebook interactively with

```bash
journal interact
```
