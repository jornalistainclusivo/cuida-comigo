---
name: "recipes"
description: "Curated Dockerfiles and Compose configs for common dev environments."
---

# Docker Recipes

Use these as starting patterns. Match the repo's current runtime and commands instead of forcing these examples verbatim.

## Node.js service

- Base image: `node:<major>-alpine` when native modules are not a problem; otherwise prefer Debian slim.
- Copy `package.json` and lockfile first.
- Run `npm ci` for reproducible installs when a lockfile exists.
- Build in one stage and run compiled output in a smaller runtime stage for TypeScript or bundlers.
- Set `CMD` to the existing start script or built server entrypoint.

## Python service

- Base image: `python:<major.minor>-slim`.
- Copy `requirements.txt` or `pyproject.toml` before source code.
- Disable bytecode generation and enable unbuffered logs only when useful for the app.
- Install build tooling only in the build stage when native dependencies are needed.
- Run the existing server command, for example `gunicorn`, `uvicorn`, or the project CLI.

## Go service

- Build with `golang:<version>` and copy the binary into a minimal runtime image.
- Cache module downloads by copying `go.mod` and `go.sum` first.
- Prefer a static binary when the app and dependencies support it.
- Keep runtime images minimal and copy only the final binary plus required assets.

## Static frontend

- Build in a Node stage.
- Serve with the framework's own runtime when SSR is required.
- Serve static output with a lightweight web server only when the app is fully static.
- Keep API base URLs runtime-configurable when the app needs different environments.

## Compose patterns

- `app + db`: add a named volume for database state and use service-name DNS.
- `app + redis`: expose only the app port to the host unless debugging Redis directly.
- `app + worker`: share the same image with a different command when the codebase supports it.
- Add healthchecks when app startup depends on database readiness.

## `.dockerignore` baseline

Start by excluding:

- `.git`
- `node_modules`
- Python virtualenv directories
- local build artifacts such as `dist`, `build`, `.next`, or coverage output
- editor files and OS junk
- `.env*` unless the user explicitly wants them copied for a controlled local workflow
