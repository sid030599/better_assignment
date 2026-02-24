# AI agent guidance — Recipe & Ingredient Manager

Use this to keep the system understandable and correct when making changes.

## Scope

- **Backend:** Python 3.10+, Flask, SQLAlchemy, Marshmallow.
- **Frontend:** React 18, functional components, local state.
- **Database:** Relational (SQLite dev; configurable for production).

## Boundaries

1. **Routes** — HTTP only: parse request, validate with schemas, call services, return JSON. No business logic.
2. **Services** — Business logic only. Use `db` and models; accept/return plain data. No request/response objects.
3. **Models** — Persistence and relationships (Recipe, Ingredient, RecipeIngredient). No validation logic.
4. **Schemas** — Request/response validation (Marshmallow). Enforce lengths and required fields.

When adding features, put logic in the correct layer. Do not leak HTTP or DB details into services.

## Correctness and safety

- Validate all API inputs with Marshmallow. Return 400 with a clear `error` message for invalid data.
- Enforce rules in services (e.g. ingredient exists, recipe name non-empty, unique ingredient name).
- Recipe-ingredient links: validate `ingredient_id` exists and quantity is non-empty.

## Change resilience

- New endpoints or fields: extend schemas and services, then add/update one route. Avoid editing many files.
- Adding a new field to Recipe or Ingredient: update model, schema, service, and API contract together.

## Verification

- Prefer automated tests for API and service behaviour. Run with `pytest` from `api/`.
- After changes to validation or business rules, add or update tests.

## Observability

- Return consistent JSON error shape: `{"error": "..."}` with appropriate status codes.
- Do not expose stack traces or internal details to the client in production.

## Do not

- Add confidential or employer-owned code or prompts.
- Put business logic in routes or validation logic in models.
- Skip validation for new request body or query parameters.
- Introduce dependencies without updating requirements.txt / package.json and README.
