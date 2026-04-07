# keiserlab.org

### development
- we use a container with the repo mounted to `/app/`
- start: `$ docker compose up` or use vscode devcontainer
  - get interactive terminal: `$ docker compose exec -it keiserlab bash`
- dev website serves at http://localhost:4000

#### ruby environment via bundler
- `bundle` manages the container's ruby environment
- check for dependency updates:
  1. bundler: `$ bundle update --bundler`
  2. all other gems: `$ bundle update`

#### python environment via uv
- `uv` manages the container's python environment
- run python scripts like `uv run myscript.py`
- check for dependency updates: `$ uv lock --upgrade`
  - if updated, include `uv.lock` in the git commit

#### github cli
- set `GH_TOKEN` on the host so it's available inside the container:
  ```bash
  export GH_TOKEN=$(gh auth token)
  ```
- add this to `~/.zshenv` (not `~/.zshrc`) so it's available during vscode devcontainer auto-rebuilds

#### claude code
- the vscode devcontainer auto-installs the Claude Code extension
- or install the CLI directly: `curl -fsSL https://claude.ai/install.sh | bash`
- set `ANTHROPIC_API_KEY` in your environment to authenticate

### rebuilds
- force container rebuild with `$ docker-compose build --no-cache`

#### jekyll theme
- we're using the [Minimal Mistakes](http://mmistakes.github.io/minimal-mistakes) jekyll theme
- theme setup and use: [setup guide](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/)