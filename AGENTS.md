# Submitly — AI Development Guidelines

## Project Context

Submitly is an Assignment Submission & Evaluation Platform for colleges.

Before working on any task, read `PRD.md` to understand the product requirements and scope.

## Technology Stack

- Backend: Python + Django
- Frontend: Django Templates + HTML + CSS + JavaScript
- Database: SQLite for local development
- Architecture should remain compatible with PostgreSQL
- Deployment target: Vercel

Do not introduce React, Next.js, Express, Vite, or another frontend/backend framework unless explicitly requested.

## Development Principles

- Keep the architecture simple and understandable.
- Prefer Django's built-in functionality where appropriate.
- Avoid unnecessary dependencies.
- Do not implement features outside the current issue.
- Do not modify unrelated files.
- Follow existing project conventions.
- Preserve security and authorization checks.
- Do not make assumptions about product requirements when they are unclear.

## Before Implementation

For every issue:

1. Read `PRD.md`.
2. Inspect the existing project structure.
3. Understand the current Git state.
4. Identify the files that need to change.
5. Create an implementation plan.
6. Wait for approval before making significant changes.

## After Implementation

1. Run appropriate tests and verification commands.
2. Check for Django configuration errors.
3. Review changed files.
4. Explain what was changed.
5. Report any remaining issues or assumptions.

## Git

Use clear conventional commit messages.

Examples:

- `docs: add product requirements`
- `feat: implement student authentication`
- `fix: prevent unauthorized submission access`
- `test: add submission validation tests`

Do not create commits unless explicitly requested.