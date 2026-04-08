# keiserlab.org

### development

We use Docker for Jekyll serving only. VS Code, Claude Code, and other dev tools run on the host (not in the devcontainer).

- start Jekyll: `$ docker compose up` (or `docker compose up -d` for background)
  - get interactive terminal: `$ docker compose exec -it keiserlab bash`
- dev website serves at http://localhost:4000
- edit files, run python scripts, and use git on the host

#### ruby environment via bundler
- `bundle` manages the container's ruby environment (for Jekyll)
- check for dependency updates:
  1. bundler: `$ bundle update --bundler`
  2. all other gems: `$ bundle update`

#### python environment via uv
- `uv` manages python on the host (not in the container)
- run python scripts like `uv run myscript.py` or `uvx --with <pkg> python3 -c "..."`
- check for dependency updates: `$ uv lock --upgrade`
  - if updated, include `uv.lock` in the git commit

#### claude code
- run Claude Code CLI on the host: `claude`
- set `ANTHROPIC_API_KEY` in your environment to authenticate

#### alternative: devcontainer workflow
- a vscode devcontainer is available if you prefer running everything inside the container
- the devcontainer auto-installs the Claude Code extension
- or install the CLI directly: `curl -fsSL https://claude.ai/install.sh | bash`
- set `GH_TOKEN` on the host so it's available inside the container:
  ```bash
  export GH_TOKEN=$(gh auth token)
  ```
- add this to `~/.zshenv` (not `~/.zshrc`) so it's available during vscode devcontainer auto-rebuilds

### rebuilds
- force container rebuild with `$ docker-compose build --no-cache`

#### jekyll theme
- we're using the [Minimal Mistakes](http://mmistakes.github.io/minimal-mistakes) jekyll theme
- theme setup and use: [setup guide](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/)