---
workspace-code:  wenen-siteseeing
workspace: Wenen Siteseeing
value_stream: knv { must be lowercase }
value_stream-phases: ["knv.01"] { must be lowercase }
canon_url: https://gitlab-maxia.basetide.com/entoli/entoli-canon.git
agents_url: https://gitlab-maxia.basetide.com/entoli/entoli-agents.git
---

# Policy for the Wenen Siteseeing workspace

This workspace belongs to the value stream **Korte Niet-Werkreis** **KNV**.

## Trip details

- **Bestemming**: Wenen
- **Reizigers**: Hans en Leanne
- **Periode**: 29 mei – 2 juni (4 nachten / 4 daagse trip)
- **Value stream phase**: KNV.01

## Mandatory reading order of foundations

Every automated role, agent or runner applies the following mandatory reading order at the start of its operation:

**In the central canon repository** (see `canon_url` in the frontmatter):
1. `foundations/.injection-sources/`
2. filtering on the general ontology and the ontology specific to the assigned value stream
3. application of generic rules and the rules applicable to the relevant value stream phase

**In this workspace**:
4. workspace-specific policy (this file)

Skipping, reordering, or implicitly applying this reading order is not permitted.

**Without demonstrable application of the constitution, any action is invalid.**

## This policy is workspace-specific

This policy describes only the workspace-specific scope. For all rules, exceptions, details and constitutional provisions we fully follow the guidelines in the central canon repository.

The constitution, general rules, and governance applicable to all workspaces are maintained in the central canon repository, referenced by `canon_url` in the frontmatter.
The agents are defined in the agents repository, referenced by `agents_url` in the frontmatter.

## Canon Repository Synchronisation

In all automated and manual processes the central canon repository is consulted. This always starts with a `git pull` to ensure the most recent foundations are used.

**Error**: When the canon repository is not reachable or cannot be found, an error is raised and the process stops.

## Scope

### What we record in this workspace

- Planning en voorbereiding van de Wenen-trip (29 mei – 2 juni)
- Bezienswaardighedenselectie, bezoekschema's en routeplannen
- Reserveringen, tickets en logistieke informatie
- Reisdagboek en aantekeningen tijdens de trip

### What does not belong in this workspace

Other domains fall outside this workspace and belong in other repositories. Examples include:
- Andere reizen of bestemmingen
- Werkgerelateerde zaken
- Financiële administratie buiten de reiskosten om

## Convention over Configuration

This workspace follows the principle **Convention over Configuration** (*charter-driven self-discovery*):

- **Minimal input**: Agents and runners expect only the strictly necessary parameters from the user.
- **Automatic discovery**: All other artefacts are automatically derived from the folder structure and naming conventions.
- **Charter as policy source**: An agent's charter determines which artefacts are relevant for that agent.
- **No redundant input**: Parameters that can be derived from convention or charter are not requested from the user.

## Language

The language used in this workspace is **Dutch** (Nederlands). All documentation, notes, artefacts, and agent communication are in Dutch.

## Workspace-specific additions

- **Taal**: Nederlands voor alle documentatie en communicatie
- **Periode**: Trip loopt van 29 mei t/m 2 juni 2026
- **Reizigers**: Hans en Leanne

---

*Last updated: 2026-05-25 by Hans*
