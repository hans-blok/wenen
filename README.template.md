# {{project-name}}

{{Describe the scope of this workspace in 1 or 2 sentences.}}

## Repository

| | |
|---|---|
| **GitLab** | `https://gitlab.com/{{organisation}}/{{project-name}}` |
| **GitLab Pages** | `https://{{organisation}}.gitlab.io/{{project-name}}` |

## Installation

Install the required packages with pip:

```bash
pip install -r requirements-docs.txt
```

Required packages:

- **mkdocs** — static documentation generator
- **mkdocs-material** — Material theme for MkDocs

## Using MkDocs

Start the local documentation server (choose a free port, e.g. 8005):

```bash
mkdocs serve -a 127.0.0.1:8005
```

View the documentation at: [http://127.0.0.1:8005](http://127.0.0.1:8005)

### Stopping MkDocs (PowerShell)

```powershell
Get-Process | Where-Object { $_.Name -like "*python*" } | Select-Object Id, ProcessName
Stop-Process -Id <id> -Force
```
