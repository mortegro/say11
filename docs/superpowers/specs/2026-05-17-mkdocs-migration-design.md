# Design: Migrate docs from Jekyll + Just the Docs to MkDocs + Material

**Date:** 2026-05-17  
**Status:** Approved

---

## Goal

Replace the Jekyll + Just the Docs setup with MkDocs + Material for MkDocs. The
docs are five pages served on GitHub Pages. The migration is mechanical: swap
the build tool, clean up Jekyll-specific syntax, and keep the content unchanged.

---

## Dependencies

Add to `pyproject.toml` under `[dependency-groups]` (dev):

```
mkdocs-material>=9.6
```

`mkdocs` is pulled in transitively. Delete `docs/_config.yml` (and any
`Gemfile`/`Gemfile.lock` if present).

---

## `mkdocs.yml` (repo root)

```yaml
site_name: say-e11
site_description: TTS CLI replicating macOS say — powered by ElevenLabs or Deepgram
docs_dir: docs
theme:
  name: material
  palette:
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.top
    - search.highlight

nav:
  - Home: index.md
  - Getting Started:
    - Installation: installation.md
  - Reference:
    - Usage: usage.md
    - Configuration: configuration.md
    - Voice Presets: voice-presets.md

exclude_docs: |
  superpowers/
```

---

## Markdown content changes

### All pages (installation, usage, configuration, voice-presets)

- Remove `{: .no_toc }` line after the `# Heading`
- Remove the `<details open markdown="block">…{:toc}</details>` TOC block
  (Material renders a TOC automatically in the right sidebar)
- Remove `nav_order:` from frontmatter (MkDocs ignores it; nav order is
  controlled by `mkdocs.yml`)
- Remove `---` horizontal-rule separators between sections

### `index.md`

- Drop `layout: home` from frontmatter (keep or drop `title:` — not required by
  MkDocs)
- Replace Jekyll button syntax `[Label](url){: .btn .btn-primary ...}` with
  Material button syntax `[Label](url){ .md-button .md-button--primary }`
- Remove `{: .fs-6 .fw-300 }` font-size directives (no equivalent needed)

### `usage.md`

Replace the `{: .note }` paragraph with a Material admonition:

```markdown
!!! note
    Deepgram does not support rate control. If you use `-r` with Deepgram, a
    warning is printed and the audio plays at normal speed.
```

### `configuration.md`, `voice-presets.md`

No special syntax beyond the TOC/separator removals listed above.

---

## Deployment

```bash
# Preview locally
uv run mkdocs serve

# Deploy to GitHub Pages (creates/updates gh-pages branch)
uv run mkdocs gh-deploy
```

No CI workflow. On first deploy, GitHub Pages must be configured in the repo
settings to serve from the `gh-pages` branch.

---

## Out of scope

- GitHub Actions CI for automated deploys
- Versioned docs (mike plugin)
- Any content additions or restructuring beyond the five existing pages
