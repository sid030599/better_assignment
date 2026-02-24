"""API routes: recipes and ingredients."""
from flask import Blueprint, request, jsonify

from app.schemas import (
    RecipeCreateSchema,
    RecipeUpdateSchema,
    IngredientSchema,
)
from app.services import recipe_service, ingredient_service

recipes_bp = Blueprint("recipes", __name__)
ingredients_bp = Blueprint("ingredients", __name__)

_recipe_create = RecipeCreateSchema()
_recipe_update = RecipeUpdateSchema()
_ingredient_schema = IngredientSchema()


# ---- Recipes ----
@recipes_bp.route("/recipes", methods=["GET"])
def list_recipes():
    recipes = recipe_service.list_recipes()
    return jsonify([r.to_dict() for r in recipes])


@recipes_bp.route("/recipes", methods=["POST"])
def create_recipe():
    try:
        data = _recipe_create.load(request.get_json() or {})
    except Exception as e:
        return jsonify({"error": _err(e)}), 400
    try:
        recipe = recipe_service.create_recipe(
            name=data["name"],
            instructions=data.get("instructions", ""),
            ingredients_data=data.get("ingredients", []),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(recipe.to_dict()), 201


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = recipe_service.get_recipe_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "Not found"}), 404
    return jsonify(recipe.to_dict())


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["PATCH"])
def update_recipe(recipe_id):
    try:
        data = _recipe_update.load(request.get_json() or {})
    except Exception as e:
        return jsonify({"error": _err(e)}), 400
    try:
        recipe = recipe_service.update_recipe(
            recipe_id,
            name=data.get("name"),
            instructions=data.get("instructions"),
            ingredients_data=data.get("ingredients"),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if not recipe:
        return jsonify({"error": "Not found"}), 404
    return jsonify(recipe.to_dict())


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    if not recipe_service.delete_recipe(recipe_id):
        return jsonify({"error": "Not found"}), 404
    return "", 204


# ---- Ingredients ----
@ingredients_bp.route("/ingredients", methods=["GET"])
def list_ingredients():
    ingredients = ingredient_service.list_ingredients()
    return jsonify([i.to_dict() for i in ingredients])


@ingredients_bp.route("/ingredients", methods=["POST"])
def create_ingredient():
    try:
        data = _ingredient_schema.load(request.get_json() or {})
    except Exception as e:
        return jsonify({"error": _err(e)}), 400
    try:
        ing = ingredient_service.create_ingredient(
            name=data["name"],
            unit=data.get("unit", ""),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(ing.to_dict()), 201


@ingredients_bp.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id):
    ing = ingredient_service.get_ingredient_by_id(ingredient_id)
    if not ing:
        return jsonify({"error": "Not found"}), 404
    return jsonify(ing.to_dict())


@ingredients_bp.route("/ingredients/<int:ingredient_id>", methods=["PATCH"])
def update_ingredient(ingredient_id):
    try:
        data = _ingredient_schema.load(request.get_json() or {}, partial=True)
    except Exception as e:
        return jsonify({"error": _err(e)}), 400
    try:
        ing = ingredient_service.update_ingredient(
            ingredient_id,
            name=data.get("name"),
            unit=data.get("unit"),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if not ing:
        return jsonify({"error": "Not found"}), 404
    return jsonify(ing.to_dict())


@ingredients_bp.route("/ingredients/<int:ingredient_id>", methods=["DELETE"])
def delete_ingredient_route(ingredient_id):
    try:
        if not ingredient_service.delete_ingredient(ingredient_id):
            return jsonify({"error": "Not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return "", 204


def _err(e):
    return str(e.messages) if hasattr(e, "messages") else str(e)
