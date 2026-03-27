# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude SEO is a Tier 4 Claude Code skill for SEO analysis. It follows the 3-layer architecture (directive in SKILL.md, orchestration via subagents, execution via Python scripts) with 17 skills, 11 subagents, and 7 Python scripts.

## Commands

```bash
# Install (copies skills/agents/scripts to ~/.claude/)
bash install.sh

# Verify Python scripts parse correctly
python3 -m py_compile scripts/fetch_page.py
python3 -m py_compile scripts/cache_manager.py
python3 -m py_compile scripts/render_page.py
python3 -m py_compile scripts/psi_api.py

# Install extensions (require API keys)
./extensions/dataforseo/install.sh
./extensions/banana/install.sh

# Uninstall
bash uninstall.sh
```

The CI pipeline (`.github/workflows/ci.yml`) only runs `py_compile` syntax checks. There is no test suite.

## Architecture

### 3-Layer Flow

1. **Directive layer** (`skills/seo/SKILL.md`): Main entry point and routing table. Parses `/seo <command> <url>` and routes to the correct sub-skill.
2. **Orchestration layer** (`skills/seo-*/SKILL.md`): Each sub-skill defines analysis steps. `/seo audit` spawns up to 11 subagents in parallel via the Agent tool.
3. **Execution layer** (`scripts/*.py`): Python scripts for web fetching, rendering, screenshots, HTML parsing, CWV measurement. All output JSON to stdout, errors to stderr.

### Key Directories

- `skills/seo/references/` — On-demand knowledge files loaded only when needed (schema types, ranking factors, industry templates). Keep these under 200 lines.
- `skills/seo-*/references/` — Per-skill reference files (AI crawlers, CWV details, brand mentions, etc.)
- `agents/seo-*.md` — Subagent definitions. Each uses `model: sonnet` with 15-25 turn limits. Agents are invoked via the Agent tool, never via Bash.
- `schema/templates.json` — JSON-LD templates for 25+ schema types.
- `.claude-plugin/plugin.json` — Plugin manifest for skill discovery.

### Installation Paths

The installer copies files to these locations (NOT the repo itself):
- Skills: `~/.claude/skills/seo/` and `~/.claude/skills/seo-*/`
- Agents: `~/.claude/agents/seo-*.md`
- Scripts: `~/.claude/skills/seo/scripts/`
- Python venv: `~/.claude/skills/seo/.venv/`
- HTML cache: `~/.claude/skills/seo/.cache/`

### Python Scripts

All scripts follow the same pattern: shebang, docstring, argparse CLI, JSON output to stdout, errors to stderr.

| Script | Purpose | Dependencies |
|--------|---------|-------------|
| `fetch_page.py` | Fetch HTML with SSRF protection | requests |
| `cache_manager.py` | Shared HTML cache for parallel agents | requests |
| `render_page.py` | SPA/JS rendering, framework detection | playwright |
| `psi_api.py` | PageSpeed Insights CWV measurement | stdlib only |
| `capture_screenshot.py` | Desktop/mobile screenshots | playwright |
| `analyze_visual.py` | Above-fold analysis, mobile checks | playwright |
| `parse_html.py` | HTML parsing and metadata extraction | beautifulsoup4, lxml |

### Security Patterns (MUST follow in all scripts)

Every script that takes a URL must include SSRF protection:
```python
ip = ipaddress.ip_address(resolved_ip)
if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
    # Block the request
```
DNS resolution failures must fail closed (block the request), not pass through.

File output paths must be validated with `os.path.realpath()` boundary checks (see `capture_screenshot.py` for the pattern).

Extension installers pass credentials via environment variables to Python subprocesses, never via shell interpolation into source code. Settings files are written with `0o600` permissions.

## Development Rules

- SKILL.md files: under 500 lines / 5000 tokens
- Reference files: focused, under 200 lines
- Scripts: docstrings, argparse CLI, JSON output, SSRF protection for any URL input
- Naming: kebab-case for skill directories, snake_case for Python files
- Dependencies: install into `~/.claude/skills/seo/.venv/`, pin versions in `requirements.txt` with CVE-conscious minimums
- Shell scripts: `set -euo pipefail`, quote all variables, never interpolate user input into code strings
- NPM packages in extension installers: pin to exact versions (no `@latest`)

## Extension System

Extensions add MCP server integrations. Each has its own `install.sh` that merges config into `~/.claude/settings.json`:

- **DataForSEO** (`extensions/dataforseo/`): Live SERP data, keyword research, backlinks. Requires DataForSEO API credentials.
- **Banana** (`extensions/banana/`): AI image generation via Gemini/nanobanana-mcp. Requires Google AI API key.

## Ecosystem

- [Claude Banana](https://github.com/AgriciDaniel/banana-claude) — standalone image gen (bundled as extension)
- [Claude Blog](https://github.com/AgriciDaniel/claude-blog) — companion blog engine, consumes SEO findings
