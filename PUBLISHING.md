# Publishing and Release Guide

This document covers the release, packaging, and distribution workflow for Tech-Me.

## Canonical Repository Status

The canonical upstream repository is live at:
**`https://github.com/L4ncelotz/tech-me-skills`**

Do not run initial `git init` or destructive force-pushes against this repository. Use standard Git feature-branch and tagging workflows.

---

## Release & Tagging Workflow (Maintainers)

Follow these steps when cutting a new version release:

### 1. Pre-release Verification
Run all local validation and evaluation checks:
```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/run_evals.py --dry-run
```
Ensure `CHANGELOG.md` reflects all changes and version bumps.

### 2. Commit and Tag
Ensure the working tree is completely clean, then create and push an annotated Git tag with semantic versioning:
```bash
# Example for v0.1.0
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin main
git push origin v0.1.0
```

### 3. Build Clean Distribution Package
Before creating the GitHub release, package the release archive. Release packaging requires a clean, committed Git working tree and extracts exclusively from the committed Git tree (`git archive`):
```bash
# Automated packaging with integrity assertions
python scripts/pack_release.py --version 0.1.0
```
This creates `dist/tech-me-0.1.0.zip` containing only committed files and asserts zero leakage of `.git/`, `__pycache__`, `.pytest_cache`, `.venv`, `.env*`, or temporary files.

Alternatively, if packaging directly via Git:
```bash
git archive --format=zip --prefix=tech-me-0.1.0/ -o dist/tech-me-0.1.0.zip HEAD
```

### 4. Create GitHub Release
Attach the generated distribution archive to the GitHub Release:
```bash
gh release create v0.1.0 dist/tech-me-0.1.0.zip \
  --title "v0.1.0 - Initial Evaluated Release" \
  --notes-file CHANGELOG.md
```

---
## Downstream Forking & Mirroring

If you are maintaining a private fork or mirror under another GitHub account:
1. Fork `L4ncelotz/tech-me-skills` via the GitHub UI or `gh repo fork L4ncelotz/tech-me-skills`.
2. Configure your downstream remote:
   ```bash
   git remote add downstream https://github.com/<your-user>/tech-me-skills.git
   git push -u downstream main
   ```
3. Never overwrite or force-push to upstream `origin`.

---

## Clean Installation Verification

After publishing a tag or release, verify that agent runtimes can install and consume the skill cleanly:

```bash
npx skills add L4ncelotz/tech-me-skills --skill tech-me
```

Confirm your agent runtime reads the skill when presented with an architecture decision request, and that it does not falsely activate for routine bug fixes or syntax questions.
