# Team

For invited collaborators only.

## Branch structure

```
main   ←  stable releases only, never push here directly
dev    ←  all PRs target this branch
you/your-feature  ←  your work branch, created from dev
```

---

## Shrey joins the team — here's exactly what he does

### 1. Clone the repo (first time only)

```bash
git clone https://github.com/aayushmaanhooda/fastapi-seed
cd fastapi-seed
```

### 2. Get on dev and pull the latest

```bash
git checkout dev
git pull origin dev
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Create his own branch off dev

```bash
git checkout -b shrey/fix-unicode-bug
```

> Branch name = `yourname/what-you-are-doing`
> Shrey names his branches like: `shrey/fix-unicode-bug`, `shrey/improve-prompts`, `shrey/add-sqlite-support`

### 5. Make his changes

Where things live:
- Templates → `src/fastapi_seed/templates/`
- Prompt flow → `src/fastapi_seed/prompts.py`
- File generation → `src/fastapi_seed/generator.py`

### 6. Test before pushing

```bash
uv run pytest                          # all tests must pass
uv run ruff check .                    # no lint errors
uv run ruff format .                   # format code
uv run fastapi-seed init my-test-app   # manually smoke test the CLI
```

### 7. Push his branch

```bash
git push -u origin shrey/fix-unicode-bug
```

### 8. Open a PR → into `dev`, not `main`

Shrey opens a PR from `shrey/fix-unicode-bug` → `dev` on GitHub.

---

## Rules

- Never push directly to `main` or `dev`
- Always branch off the latest `dev`
- One feature per branch — keep PRs focused
- Tests must pass before opening a PR
