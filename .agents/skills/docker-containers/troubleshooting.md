---
name: "troubleshooting"
description: "Common fixes for container networking, volumes, and build errors."
---

# Docker Troubleshooting

Use this checklist when a container build or startup is failing.

## Build failures

- Dependency install fails: confirm lockfiles, package manager version, and required OS libraries.
- Source copy invalidates cache: move dependency install earlier and add `.dockerignore`.
- Build output missing: confirm the build step writes to the path copied into the runtime stage.

## Startup failures

- Process exits instantly: confirm `CMD` points to a long-running foreground process.
- Port is unreachable from host: confirm the app listens on `0.0.0.0` and the port is published.
- Executable not found: confirm `WORKDIR`, file paths, and executable permissions.

## Compose networking

- App cannot reach database: replace `localhost` with the Compose service name.
- Service starts before dependency is ready: add a healthcheck and gate startup on readiness.
- Host port collisions: remap host ports without changing internal container ports unless necessary.

## File and permission issues

- Bind mount hides built files: check whether a host mount replaces files created during image build.
- Non-root runtime cannot write: fix ownership or redirect writes to an allowed path.
- Line ending problems in scripts: ensure shell entrypoints use Unix line endings.

## Diagnostic commands

Use the smallest command that proves the failure:

- `docker build .`
- `docker run --rm -p HOST:CONTAINER IMAGE`
- `docker compose up --build`
- `docker compose logs SERVICE`
- `docker exec -it CONTAINER sh`
