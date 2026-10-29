# Publish Tech-Me to GitHub

This package is not automatically published. Create a public repository under the account that will maintain it, and review the contents before pushing.

## Prerequisites

- Git
- A GitHub account with permission to create repositories
- GitHub CLI (`gh`) installed and signed in **or** a manually created empty GitHub repo

## Publish using GitHub CLI

From inside the extracted `tech-me` directory (PowerShell, Command Prompt or a POSIX shell with `git` and `gh` available):

```bash
git init
git add .
git commit -m "Initial Tech-Me agent skill"
git branch -M main
gh repo create L4ncelotz/tech-me --public --source . --remote origin --push
```

The command assumes `L4ncelotz/tech-me` is available and the current GitHub account has write access. If the repository already exists, **do not** overwrite it; inspect the existing repository and use normal Git workflows.

## Publish without GitHub CLI

1. Create a **public empty repository** named `tech-me` on GitHub. Do **not** auto-initialize with a README or license (both exist in this package).
2. From inside the extracted directory:

```bash
git init
git add .
git commit -m "Initial Tech-Me agent skill"
git branch -M main
git remote add origin https://github.com/L4ncelotz/tech-me.git
git push -u origin main
```

Authenticate with your own account as required by GitHub. Never place a token or secret in a command or repository file.

## After publishing

Run the repository's GitHub Actions workflow and, where available, upstream `skills-ref` validation. Then test a clean install:

```bash
npx skills add L4ncelotz/tech-me --skill tech-me
```

Confirm your agent reads the skill on an architecture request, and that it does not activate for a routine bug fix. A public repository does not guarantee immediate listing or any particular ranking on skills.sh; check the live directory separately.

For a first release, record actual baseline-vs-skill evaluation results using `evals/RUNBOOK.md` before claiming validated model improvements or cross-agent support.
