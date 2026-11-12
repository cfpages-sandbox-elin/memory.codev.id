# memory.codev.id — herdr-mem Cloud Console

Production Cloudflare Pages memory viewer for Herdr sessions across the Codev ecosystem.

## Features

- **Google SSO via Supabase Auth**: Single sign-on authentication through project `https://gfnjestxjgkfujzubiqr.supabase.co`.
- **Fail-Closed Security Gate**: Strictly allows `admin@alampintar.org`, `admin@codev.id`, `evelinaquinta@gmail.com`, and `@codev.id` emails. Unauthorized accounts are blocked at the door with an Access Denied barrier.
- **Cross-Project Memory Explorer**: Filter by project (`herdr-mem`, `codex-syamsul-alam`, `domain.codev.id`, `open-seo`, `cmdc-transcripts`, `opencode-transcripts`, `ALL`).
- **Interactive Inspector**: Inspect full observation bodies, sessions, token/char footprints, and one-click copy of CLI drilldown commands.
- **Zero-Dependency Static SPA**: No build step required; instant edge hydration.

## Deployment & Sync

To refresh memory data and deploy live:

```powershell
# 1. Export latest observations from local SQLite DB
python scripts/export-data.py

# 2. Deploy to Cloudflare Pages
npx wrangler pages deploy . --project-name memory-codev-id
```
