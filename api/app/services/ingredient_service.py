"""Business logic for ingredients."""
from app import db
from app.models import Ingredient


def list_ingredients():
    return Ingredient.query.order_by(Ingredient.name).all()


def get_ingredient_by_id(ingredient_id):
    return db.session.get(Ingredient, ingredient_id)


def create_ingredient(name, unit=""):
    name = (name or "").strip()
    if not name:
        raise ValueError("Ingredient name is required")
    existing = Ingredient.query.filter_by(name=name).first()
    if existing:
        raise ValueError(f"Ingredient '{name}' already exists")
    ing = Ingredient(name=name, unit=(unit or "").strip()[:32])
    db.session.add(ing)
    db.session.commit()
    return ing


def update_ingredient(ingredient_id, name=None, unit=None):
    ingredient = get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return None
    if name is not None:
        name = (name or "").strip()
        if not name:
            raise ValueError("Ingredient name cannot be empty")
        existing = Ingredient.query.filter_by(name=name).first()
        if existing and existing.id != ingredient_id:
            raise ValueError(f"Ingredient '{name}' already exists")
        ingredient.name = name
    if unit is not None:
        ingredient.unit = (unit or "").strip()[:32]
    db.session.commit()
    return ingredient


def delete_ingredient(ingredient_id):
    from app.models import RecipeIngredient
    ingredient = get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return False
    if RecipeIngredient.query.filter_by(ingredient_id=ingredient_id).first():
        raise ValueError("Cannot delete ingredient that is used in recipes")
    db.session.delete(ingredient)
    db.session.commit()
    return True
