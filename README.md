# Wenen 2026 – Leanne & Hans in Oostenrijk

Reisplanning voor een 4-daagse trip naar Wenen van **Hans en Leanne**, van 29 mei t/m 2 juni 2026.

## Repository

| | |
|---|---|
| **GitHub** | `https://github.com/hans-blok/wenen` |
| **GitHub Pages** | `https://hans-blok.github.io/wenen` |


## GitHub Pages instellen

### 1. Repository aanmaken op GitHub

Maak een **public** repository aan met de naam `wenen-siteseeing`.

### 2. GitHub Actions workflow

Het bestand `.github/workflows/deploy.yml` bevat de automatische deployment:

```yaml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements-docs.txt
      - run: mkdocs gh-deploy --force
```

### 3. GitHub Pages activeren

> **Let op**: de branch `gh-pages` bestaat nog niet — die wordt automatisch aangemaakt door de workflow bij de eerste push naar `main`.

Stappen:
1. Push naar `main` en wacht tot de GitHub Action succesvol is afgerond
2. Ga naar de repository op GitHub
3. **Settings** → **Pages**
4. Onder *Branch*: kies `gh-pages` / `/ (root)`
5. Klik **Save**

De site is na de eerste succesvolle build beschikbaar op:
`https://hans-blok.github.io/wenen`

### 4. site_url instellen in mkdocs.yml

```yaml
site_url: "https://hans-blok.github.io/wenen"
```

## Installatie

Installeer de benodigde packages met pip:

```bash
pip install -r requirements-docs.txt
```

Benodigde packages:

- **mkdocs** — static documentatiegenerator
- **mkdocs-material** — Material theme voor MkDocs

## MkDocs gebruiken

Start de lokale documentatieserver (kies een vrije poort, bijv. 8005):

```bash
mkdocs serve -a 127.0.0.1:8005
```

Bekijk de documentatie op: [http://127.0.0.1:8005](http://127.0.0.1:8005)

### MkDocs stoppen (PowerShell)

```powershell
Get-Process | Where-Object { $_.Name -like "*python*" } | Select-Object Id, ProcessName
Stop-Process -Id <id> -Force
```
