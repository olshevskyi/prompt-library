# Prompt Library API

REST API for storing, tagging and filtering AI prompts.
Built with **FastAPI**, **SQLAlchemy 2.0**, **SQLite** and **Pydantic v2**.

## Run

```bash
uv sync
uv run fastapi dev app/main.py
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

The SQLite file `prompts.db` is created on first start.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/prompts` | Create a prompt, returns `201` |
| `GET` | `/prompts` | List prompts |
| `GET` | `/prompts/{id}` | Get one prompt, `404` if missing |
| `PATCH` | `/prompts/{id}` | Partial update, only sent fields change |
| `DELETE` | `/prompts/{id}` | Delete, returns `204` |

Query parameters for `GET /prompts` (they can be combined):

| Param | Example | Meaning |
|-------|---------|---------|
| `category` | `?category=dev` | exact category match |
| `favorite` | `?favorite=true` | only favorites / only non-favorites |
| `tag` | `?tag=python` | prompts that have this tag |

## Example

```bash
curl -X POST http://127.0.0.1:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{"title": "Bug report triage",
       "body": "Classify this bug report by severity and component.",
       "category": "dev",
       "tags": ["triage", "python"]}'
```

```json
{
  "title": "Bug report triage",
  "body": "Classify this bug report by severity and component.",
  "category": "dev",
  "tags": [
    { "id": 2, "name": "python" },
    { "id": 9, "name": "triage" }
  ],
  "is_favorite": false,
  "id": 7,
  "created_at": "2026-11-22T17:55:33",
  "updated_at": "2026-11-22T17:55:33"
}
```

## Project structure

```
app/
├── main.py           creates the FastAPI app, registers routers, creates tables
├── database.py       engine, SessionLocal, Base, get_db() dependency
├── models.py         SQLAlchemy tables: prompts, tags, prompt_tags
├── schemas.py        Pydantic models: PromptCreate, PromptUpdate, PromptRead, TagRead
├── crud.py           all database queries, no HTTP here
└── routers/
    └── prompts.py    HTTP layer: status codes, 404s, query params
tests/
├── conftest.py       in-memory SQLite + dependency override
├── test_prompts.py   CRUD, validation, PATCH semantics, filters
└── test_tags.py      tag create / replace / filter
```

Each layer has one job: the router speaks HTTP, `crud.py` speaks SQL,
schemas define the public contract and models define the storage.

## Tests

```bash
uv run pytest -v
```

12 tests. Every test gets fresh tables in an in-memory SQLite database,
and `get_db` is replaced via `app.dependency_overrides`, so tests never touch `prompts.db`.

## Design decisions

- **Tags in their own table.** A comma-separated `tags` column can't be indexed,
  filtered reliably or renamed in one place. An association table `prompt_tags`
  gives a proper many-to-many relation, and filtering is a single `EXISTS` query
  (`Prompt.tags.any(Tag.name == tag)`).
- **PATCH changes only what was sent.** `model_dump(exclude_unset=True)` separates
  "field not sent" from "field sent". Explicit `null`s are ignored, so a client
  can't wipe a `NOT NULL` column. Tags are replaced only if the `tags` key is present.
- **Separate input and output schemas.** `PromptCreate` has no `id` or timestamps,
  `PromptRead` returns them. `PromptUpdate` makes every field optional.
- **Session per request.** `get_db()` is a generator dependency: it yields a session
  and closes it in `finally`, even if the endpoint raises.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Next up: `{{variable}}` templates with a render endpoint, and full-text search.
