# keiserlab.org

### development
- we use a container with the repo mounted to `/app/`
- start: `$ docker compose up` or use vscode devcontainer
  - get interactive terminal: `$ docker compose exec -it keiserlab bash`
- dev website serves at http://localhost:4000

#### uv python environment
- `uv` manages the container's python environment
- run python scripts like `uv run myscript.py`
- check for dependency updates: `$ uv lock --upgrade`
  - if updated, include `uv.lock` in the git commit

### rebuilds
- force container rebuild with `$ docker-compose build --no-cache`

#### jekyll theme
- we're using the [Minimal Mistakes](http://mmistakes.github.io/minimal-mistakes) jekyll theme
- theme setup and use: [setup guide](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/)