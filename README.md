# Recipe & Ingredient Manager

A small full-stack app: **Flask API** + **React** + **SQLite**. Manage ingredients and recipes with quantities.

## Stack

- **Backend:** Python 3.10+, Flask, Flask-SQLAlchemy, Marshmallow, Flask-CORS
- **Frontend:** React 18, Vite
- **Database:** SQLite (file: `api/instance/recipes.db`)

## Quick start

### Backend

```bash
cd api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

API runs at **http://localhost:5001**. Override port with `FLASK_RUN_PORT` or `PORT`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App at **http://localhost:3000**; proxies `/api` to the backend.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/recipes` | List all recipes (with ingredients) |
| POST | `/api/recipes` | Create recipe (body: `name`, `instructions?`, `ingredients?`) |
| GET | `/api/recipes/:id` | Get one recipe with ingredients |
| PATCH | `/api/recipes/:id` | Update recipe |
| DELETE | `/api/recipes/:id` | Delete recipe |
| GET | `/api/ingredients` | List all ingredients |
| POST | `/api/ingredients` | Create ingredient (body: `name`, `unit?`) |
| GET | `/api/ingredients/:id` | Get one ingredient |

Recipe body for create/update: `ingredients` is a list of `{ "ingredient_id", "quantity", "unit_override?" }`.

## Project layout

```
api/
  app/
    models/       # Recipe, Ingredient, RecipeIngredient
    schemas/      # Marshmallow validation
    services/     # Business logic
    routes/       # HTTP layer
  config.py
  run.py
  tests/
frontend/
  src/
    App.jsx, api.js, RecipeList, RecipeDetail, RecipeForm, IngredientList
```

## Technical decisions

1. **Two entities + join:** Recipes and Ingredients are separate; `RecipeIngredient` links them with `quantity` and optional `unit_override`. Clear relational model.
2. **Layered backend:** Routes → schemas (validation) → services → models. Keeps HTTP and persistence out of business logic.
3. **Validation at boundary:** Marshmallow validates all inputs; services enforce rules (e.g. ingredient exists, unique name).
4. **SQLite:** No extra process; switch to PostgreSQL via `DATABASE_URI` for production.

## Tests

```bash
cd api
source .venv/bin/activate
pytest -v
```

## AI guidance

- **AGENTS.md** — Scope, boundaries, correctness, and constraints for AI agents.
- **.cursor/rules/** — Backend and frontend conventions.

## Risks & extensions

- **Risks:** No auth; SQLite for single-user/dev. Add auth and a production DB for multi-user.
- **Extensions:** Edit recipe, search/filter recipes, export, units per ingredient only (no override).
