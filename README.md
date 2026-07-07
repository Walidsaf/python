# Encoding Explorer

A Python converter app for decimal, binary, ASCII, and UTF-8. It runs as a desktop GUI, a terminal app, and a publicly deployed web app.

**Live:** [citex.name.ng](https://citex.name.ng) (frontend, Netlify) → proxies to [python-v6nq.onrender.com](https://python-v6nq.onrender.com) (backend API, Render)

## Features
* Decimal, binary, ASCII, and UTF-8 conversions
* Shared Python conversion engine in `converter.py`
* Desktop GUI with examples, copy output, menu bar, dark mode, and saved history
* Web app with HTML, CSS, JavaScript, dark mode, local history, and a Python API
* Responsive layout (desktop two-column workspace + history sidebar, single-column on mobile)
* Unit tests for the converter logic
* Indexed on Google, with sitemap and site verification set up

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

## Run The Web App (local)
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

Running locally this way serves both the API and the Jinja-rendered `templates/index.html` from one Flask process, so `window.CONVERSIONS` is templated in automatically. This is different from the production setup below.

## Project Files
* `app.py` - main launcher for desktop, terminal, and web modes
* `test.py` - compatibility wrapper for the old run command
* `converter.py` - shared conversion logic (single source of truth for all `CONVERSIONS`)
* `web_app.py` - Flask backend and API
* `templates/index.html` - Jinja-rendered web page, used only when Flask serves the frontend itself (local dev / same-origin deploys)
* `static/styles.css` - web design
* `static/app.js` - browser behavior connected to Python
* `test_converter.py` - unit tests
* `Procfile`, `render.yaml`, `wsgi.py` - deployment helpers for Render
* `frontend-deploy/` - **not yet committed to this repo** — the static bundle actually deployed to Netlify (see below)

## Production Architecture

The live site splits frontend and backend across two hosts, which needs a bit more than just running `web_app.py`:

* **Backend (Render):** runs `web_app.py` via `gunicorn`, exposes `POST /api/convert`. Free tier spins down after ~15 min idle; first request after that can take 30-50s to wake up.
* **Frontend (Netlify):** a static-only bundle — Netlify never runs Python, so it can't resolve Jinja (`{{ conversions | tojson }}`). Instead, `frontend-deploy/index.html` hardcodes `window.CONVERSIONS` to mirror `converter.py`'s `CONVERSIONS` tuple exactly (`key`, `label`, `hint`, `example`). **If `converter.py` ever changes, this list must be updated by hand to match.**
* **Proxy:** `frontend-deploy/_redirects` forwards `/api/*` from Netlify to the Render backend, so `app.js` can keep calling `/api/convert` as a relative path with no CORS setup needed:
  ```text
  /api/*  https://python-v6nq.onrender.com/api/:splat  200
  ```

### `frontend-deploy/` layout (deployed to Netlify, not yet in git)
```text
frontend-deploy/
├── index.html       (hardcoded CONVERSIONS, no Jinja, relative asset paths)
├── _redirects       (proxies /api/* to Render backend)
├── robots.txt        (points crawlers to sitemap.xml)
├── sitemap.xml       (single URL: https://citex.name.ng/)
└── static/
    ├── styles.css
    └── app.js
```

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

## SEO
* `google-site-verification` meta tag in `frontend-deploy/index.html`, verified in Google Search Console
* `frontend-deploy/sitemap.xml` submitted via Search Console
* `frontend-deploy/robots.txt` allows all crawlers and points to the sitemap
* Open Graph tags and meta description in `index.html`'s `<head>`
* Still open: favicon set (16x16, 32x32, apple-touch-icon) and JSON-LD structured data — planned, not yet added

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

For the frontend, drop the whole `frontend-deploy/` folder onto Netlify (or connect the repo for auto-deploy — not yet set up; currently deployed manually via Netlify Drop).

## Keyboard Shortcuts
* `Ctrl+Enter` converts
* `Escape` clears

## Tests
```bash
.venv/bin/python -m unittest
```

## Roadmap
* Commit `frontend-deploy/` to this repo (currently only deployed to Netlify, not version-controlled)
* Automate Netlify deployment via GitHub instead of manual Drop
* Add a keep-alive ping to avoid Render's cold-start delay
* Add favicon set and JSON-LD structured data
* Add basic analytics