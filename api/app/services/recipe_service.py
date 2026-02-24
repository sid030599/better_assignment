"""Business logic for recipes and recipe-ingredient links."""
from app import db
from app.models import Recipe, Ingredient, RecipeIngredient


def list_recipes():
    return Recipe.query.order_by(Recipe.created_at.desc()).all()


def get_recipe_by_id(recipe_id):
    return db.session.get(Recipe, recipe_id)


def create_recipe(name, instructions="", ingredients_data=None):
    name = (name or "").strip()
    if not name:
        raise ValueError("Recipe name is required")
    recipe = Recipe(
        name=name,
        instructions=(instructions or "").strip()[:5000],
    )
    db.session.add(recipe)
    db.session.flush()
    _set_recipe_ingredients(recipe, ingredients_data or [])
    db.session.commit()
    db.session.refresh(recipe)
    return recipe


def update_recipe(recipe_id, name=None, instructions=None, ingredients_data=None):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        return None
    if name is not None:
        name = (name or "").strip()
        if not name:
            raise ValueError("Recipe name cannot be empty")
        recipe.name = name
    if instructions is not None:
        recipe.instructions = (instructions or "").strip()[:5000]
    if ingredients_data is not None:
        _set_recipe_ingredients(recipe, ingredients_data)
    db.session.commit()
    db.session.refresh(recipe)
    return recipe


def delete_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        return False
    db.session.delete(recipe)
    db.session.commit()
    return True


def _set_recipe_ingredients(recipe, ingredients_data):
    """Replace recipe's ingredients with the given list. Validates ingredient_ids exist."""
    for ri in recipe.recipe_ingredients:
        db.session.delete(ri)
    for item in ingredients_data:
        ing = db.session.get(Ingredient, item["ingredient_id"])
        if not ing:
            raise ValueError(f"Ingredient id {item['ingredient_id']} not found")
        quantity = (item.get("quantity") or "").strip()[:64]
        if not quantity:
            raise ValueError("Quantity is required for each ingredient")
        unit_override = (item.get("unit_override") or "").strip() or None
        if unit_override:
            unit_override = unit_override[:32]
        ri = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ing.id,
            quantity=quantity,
            unit_override=unit_override,
        )
        db.session.add(ri)
