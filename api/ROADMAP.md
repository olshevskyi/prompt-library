# Roadmap: Prompt Library API

Each step = a bit of Python theory (just what the step needs) + a piece of the project.
Mark `[x]` when done and reviewed.

## Working API with a database
- [x] 0 Setup: uv, venv, first endpoint
- [x] 1 Python basics (playground/basics.py) — fix line 9, move on
- [x] 2 Classes + Pydantic → `app/schemas.py`
- [x] 3 SQL basics + SQLAlchemy → `app/database.py`, `app/models.py`, Prompt only
- [x] 4 `with` / `yield` / `Depends` → `app/crud.py` + `app/routers/prompts.py`: POST, GET list, GET by id
- [x] 5 PATCH, DELETE, filters `?category=&favorite=`

## Tests, tags, stretch
- [x] 6 pytest → `tests/test_prompts.py`
- [x] 7 Tag model + many-to-many
- [ ] 8 Templates `{{var}}` + render endpoint, search
- [ ] 9 If time left: usage counter, import/export JSON

- [x] Angular UI → ../ui
