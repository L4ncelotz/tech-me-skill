# Tech-Me

**Evidence-based technical architecture decisions, without the stack bias.**

Tech-Me is a portable Agent Skill that interviews you **only as much as needed**, evaluates requirements and hard constraints before choosing technologies, challenges architectural assumptions, and explains the trade-offs behind its recommendation.

> Discover requirements. Challenge assumptions. Design with evidence.

[Agent Skills format](https://agentskills.io/specification) · [Skills CLI](https://skills.sh/docs/cli)

## What it does

- **Adaptive discovery:** asks one high-impact question at a time and stops when information is sufficient. “Recommend now” is always valid.
- **Bias-controlled evaluation:** separates requirements and hard constraints from a user's past stacks and preferences.
- **Constraint-first design:** filters non-viable choices before comparing credible alternatives.
- **Reasonable defaults:** handles unknown answers without endless questioning; labels assumptions instead of inventing facts.
- **Evidence proportional to risk:** checks fast-changing claims with available tools, or flags uncertainty.
- **Existing-project awareness:** inspects relevant, accessible non-secret codebase materials when available, read-only by default.
- **Architecture quality gate:** challenges overengineering, migration cost, operational risk and unjustified dependencies.
- **Clear decision report:** leads with the recommendation, then alternatives, trade-offs, risks, and revisit triggers.
- **Portable core:** a single `SKILL.md` works without MCP servers or external dependencies. Optional capabilities degrade gracefully.

## Install

After this repository is published as `L4ncelotz/tech-me` on GitHub:

```bash
npx skills add L4ncelotz/tech-me --skill tech-me
```

For local development (from the repository root):

```bash
npx skills add ./skills/tech-me
```

The skills CLI may prompt for an agent and install location. Automatic activation and command naming vary by agent; the portable contract is the skill metadata and instructions, **not** a guaranteed `/tech-me` slash command on every platform.

## Use

Ask your agent, for example:

```text
Use Tech-Me. I want to build a small internal inventory application.
Help me choose a maintainable architecture. Ask only necessary questions.
```

```text
Use Tech-Me to review our current backend architecture.
Do not edit code. Identify evidence for or against moving to microservices.
```

```text
Use Tech-Me. Compare SQLite and PostgreSQL for my offline-first app.
Recommend now using reasonable assumptions instead of a long interview.
```

### Example conversation (illustrative, not a benchmark)

**User:** I want to make an inventory web app for my company.

**Tech-Me:** Will this be used only by employees, or also by customers? That affects access control and hosting.

**User:** Employees only. Maybe 20 people.

**Tech-Me:** Is there an existing database or server that you must use?

**User:** We have a Windows Server and Oracle.

**Tech-Me:** Those are important constraints. I'll use them to assess the simplest viable architecture, rather than proposing a new hosting platform by default.

## Files

```text
tech-me/
├── skills/tech-me/
│   ├── SKILL.md                 # Portable instructions
│   ├── references/
│   │   ├── discovery.md         # Adaptive questions and stop conditions
│   │   ├── evaluation.md        # Constraints, evidence and bias control
│   │   └── output.md            # Decision reporting patterns
│   └── assets/adr-template.md   # Optional ADR template
├── evals/
│   ├── scenarios.json           # Scenario-based evaluation fixtures
│   ├── RUBRIC.md                # Human scoring criteria
│   └── RUNBOOK.md               # Baseline vs skill-enabled procedure
├── scripts/validate_repo.py    # Stdlib-only structural checks
├── tests/test_validator.py     # Automated validator regression checks
├── .github/workflows/validate.yml
├── CONTRIBUTING.md
├── PUBLISHING.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Validate and evaluate

Requires Python 3.10+ **for repository validation only**, not for running the skill itself.

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

Optional upstream specification validation if `skills-ref` is installed:

```bash
skills-ref validate ./skills/tech-me
```

The local validator checks a subset of spec and evaluation-fixture structure; it is **not** a substitute for the upstream `skills-ref` validation. The evaluation scenarios and rubric enable repeatable **human review** of model behavior; no model-based evaluation results or cross-agent compatibility claims are implied. See [Evaluation Runbook](evals/RUNBOOK.md).

## Design boundaries

- No required web search, MCP server, subscription, or runtime dependency.
- No automatic file changes, package installs, or deployments.
- No requirement to use a particular framework, vendor, cloud, or language.
- No claim to guarantee the objectively optimal architecture. Recommendations depend on evidence and requirements.

## Publishing

See [PUBLISHING.md](PUBLISHING.md) for GitHub setup, publishing and clean-install verification. The ZIP is **not** a published GitHub repository.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions that improve neutrality, clarity and evaluation coverage are welcome.

## License

MIT — see [LICENSE](LICENSE).
