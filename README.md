# Wenen 2026 – Leanne & Hans in Oostenrijk

Reisplanning voor een 4-daagse trip naar Wenen van **Hans en Leanne**, van 29 mei t/m 2 juni 2026.

## Repository

| | |
|---|---|
| **GitHub** | `https://github.com/hans/wenen-siteseeing` |
| **GitHub Pages** | `https://hans.github.io/wenen-siteseeing` |

## Programma

| Dag | Thema |
|-----|-------|
| Vrijdag 29 mei | Treinreis Wijk bij Duurstede → Frankfurt → Wenen (aankomst 23:45) |
| Zaterdag 30 mei | Belvedere (Klimt's *De Kus*), Hofburg, Burggarten, binnenstad |
| Zondag 31 mei | Dagtrip Graz – Schwarzenegger Museum & bezoek Renske |
| Maandag 1 juni | Schönbrunn, Prater, Reuzenrad, Naschmarkt, Donaukanal |
| Dinsdag 2 juni | Terugreis Wenen → München → Utrecht (vertrek 08:30) |

## Verblijf

**Easy Flat Stadt Park**, Wenen

## Artefacten

De dagplanningen staan in de map `artefacten/`:

- `00-sightseeing-overzicht.md` – overzicht van alle bezoeken met prijzen en boekinfo
- `01-vrijdag.md` – treinreis en aankomst
- `02-zaterdag.md` – Belvedere en binnenstad
- `03-zondag.md` – dagtrip Graz
- `04-maandag-01-juni.md` – Schönbrunn en Prater
- `05-dinsdag-02-juni.md` – terugreis

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
