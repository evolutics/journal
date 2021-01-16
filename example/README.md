# Example

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

Render a notebook as in

```bash
journal generate --open src/notebooks/uncertainty.py
```

Edit a notebook interactively with

```bash
journal interact
```
