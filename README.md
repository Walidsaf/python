# Encoding Explorer

A Python converter app for decimal, binary, ASCII, and UTF-8. It now runs as a desktop GUI, a terminal app, and a publishable web app.

## Features
* Decimal, binary, ASCII, and UTF-8 conversions
* Shared Python conversion engine in `converter.py`
* Desktop GUI with examples, copy output, menu bar, dark mode, and saved history
* Web app with HTML, CSS, JavaScript, dark mode, local history, and a Python API
* Unit tests for the converter logic

## Install
Create and use the local virtual environment:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

If the desktop GUI is missing Tkinter on Ubuntu/Debian:
```bash
sudo apt install python3-tk
```

## Run The Desktop App
```bash
python3 app.py
```

The old command still works:
```bash
python3 test.py
```

## Run The Terminal App
```bash
python3 app.py --cli
```

## Run The Web App
```bash
.venv/bin/python app.py --web
```

Then open:
```text
http://127.0.0.1:5000
```

You can also run the web server directly:
```bash
.venv/bin/python web_app.py
```

## Project Files
* `app.py` - main launcher for desktop, terminal, and web modes
* `test.py` - compatibility wrapper for the old run command
* `converter.py` - shared conversion logic
* `web_app.py` - Flask backend and API
* `templates/index.html` - web page HTML
* `static/styles.css` - web design
* `static/app.js` - browser behavior connected to Python
* `test_converter.py` - unit tests
* `Procfile`, `render.yaml`, `wsgi.py` - deployment helpers

## Web API
The website connects to Python through:
```text
POST /api/convert
```

Example JSON body:
```json
{
  "choice": "1",
  "value": "42"
}
```

Example response:
```json
{
  "ok": true,
  "result": "101010",
  "conversion": {
    "key": "1",
    "label": "Decimal -> Binary",
    "outputLabel": "Binary"
  }
}
```

## Publish
For Render, this repo includes `render.yaml`. The start command is:
```bash
gunicorn web_app:app
```

For other Python hosts, use:
```bash
pip install -r requirements.txt
gunicorn web_app:app
```

## Keyboard Shortcuts
* `Ctrl+Enter` converts
* `Escape` clears

## Tests
```bash
.venv/bin/python -m unittest
```
