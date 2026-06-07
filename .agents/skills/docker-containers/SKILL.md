---
name: docker-containers
description: Build, repair, and harden Docker-based development and deployment setups for applications and services. Use when any agent needs to create or update `Dockerfile`, `.dockerignore`, `compose.yaml` or `docker-compose.yml`, container entrypoints, multi-stage builds, local service orchestration, or container debugging workflows. Trigger for requests such as containerizing a Node/Python/Go app, adding Postgres or Redis with Compose, shrinking images, fixing container startup failures, debugging port or volume issues, improving Docker caching, or making a container setup safer for production.
---

# Docker Containers

## Overview

Use this skill to move from "make this run in Docker" to a working, debuggable setup with sane defaults. Prefer small, reviewable changes and preserve the app's current run behavior unless the user asks to change it.

For concrete starter patterns, read [examples.md](./references/examples.md).

## Workflow Decision Tree

Choose the path that matches the request:

- No container files yet: create `Dockerfile`, `.dockerignore`, and optionally `compose.yaml`.
- Existing Docker setup is broken: inspect the current files first, then fix the smallest root cause.
- Local multi-service dev is needed: add or repair `compose.yaml` with app, database, cache, and named volumes as needed.
- Image is too large or slow: convert to multi-stage builds, tighten copy patterns, and improve cache layering.
- Production safety is requested: run as non-root when practical, set explicit ports and env handling, and avoid baking secrets into images.

## Gather Context First

Read the app before editing container files:

- Detect the runtime and package manager from existing files such as `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Gemfile`, or framework config.
- Find the real start command from scripts, docs, or the current process manager.
- Check whether the app needs build output before runtime, such as TypeScript, Next.js, Vite, or compiled binaries.
- Identify external dependencies such as PostgreSQL, Redis, queues, object storage, or headless browsers.
- Check for local-only assumptions that break in containers, especially hardcoded `localhost`, file paths, and missing bind addresses.

If the stack-specific pattern is not obvious, read [recipes.md](./references/recipes.md).

## Containerize an App

Follow this order:

1. Pick a small, official base image that matches the runtime version already used by the project.
2. Add a `.dockerignore` before broad `COPY` steps to keep build context small.
3. Copy dependency manifests first, install dependencies, then copy the rest of the source to preserve cache hits.
4. Use multi-stage builds when the runtime does not need compilers, package managers, or source files.
5. Expose only the application port actually used by the service.
6. Set the startup command to match the existing app behavior.

Prefer these defaults:

- Use one process per container unless the user explicitly wants a process supervisor.
- Bind servers to `0.0.0.0`, not `127.0.0.1`.
- Use exec-form `CMD` and `ENTRYPOINT`.
- Keep build steps deterministic and avoid shell tricks unless required by the app.

## Add Compose for Local Development

Use Compose when the app needs supporting services or a repeatable local workflow.

Include:

- one service for the app
- one service per dependency such as `db`, `redis`, or `worker`
- named volumes for persistent local state when data durability matters
- env file wiring only if the project already uses it or the user wants it

Compose rules:

- Use service names for container-to-container hostnames, not `localhost`.
- Map only the ports needed on the host machine.
- Add healthchecks when startup ordering matters.
- Prefer `depends_on` plus healthchecks over sleep-based startup hacks.
- Keep dev-oriented bind mounts out of production examples unless the user asks for dev containers specifically.

## Debug Failing Containers

Work from symptoms to root cause:

1. Read the container files and start command.
2. Check whether the service listens on the expected port and address.
3. Confirm required files are copied into the image.
4. Check env vars, working directory, file permissions, and executable paths.
5. Verify inter-service networking and DNS names under Compose.
6. Verify readiness issues separately from simple startup failures.

Common fixes:

- Port works locally but not in Docker: bind to `0.0.0.0`.
- Build is slow: reorder layers so dependency install happens before source copy.
- Runtime cannot find files: fix `WORKDIR`, `COPY`, or build output path.
- App cannot reach database: use the Compose service name instead of `localhost`.
- Container exits immediately: fix the command, foreground process, or missing env vars.

If the failure pattern matches a known Docker issue, read [troubleshooting.md](./references/troubleshooting.md).

## Production-Safe Defaults

Apply these by default unless they conflict with the app:

- Use multi-stage builds for compiled or bundled applications.
- Keep images minimal and omit dev-only tooling from runtime layers.
- Avoid `latest` tags in examples when a major version is known.
- Avoid copying `.env` files or secrets into the image.
- Prefer a non-root user in the runtime stage when file permissions allow it.
- Keep writable paths explicit.
- Document required runtime env vars instead of hardcoding them.

Do not over-engineer:

- Do not add Kubernetes, reverse proxies, or process supervisors unless the task actually needs them.
- Do not invent healthchecks, workers, or sidecars without evidence in the app.
- Do not replace the application's package manager or framework conventions just to make the Dockerfile look cleaner.

## Output Checklist

Before finishing, verify that:

- container files match the actual app runtime
- ports, env vars, and service hostnames are coherent
- build layers are cache-friendly
- the startup command matches the existing app behavior
- the setup distinguishes local dev concerns from production concerns
- the final result includes a short usage example such as `docker build`, `docker run`, or `docker compose up`

## References

- Read [examples.md](./skills/docker-containers/examples.md) for concrete starter Dockerfile and Compose patterns.
- Read [recipes.md](./skills/docker-containers/recipes.md) for starter patterns by stack.
- Read [troubleshooting.md](./skills/docker-containers/troubleshooting.md) for common failure modes and fixes.
