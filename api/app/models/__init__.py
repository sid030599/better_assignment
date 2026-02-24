"""SQLAlchemy models: Recipe, Ingredient, and their association."""
from datetime import datetime, timezone
from app import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    unit = db.Column(db.String(32), nullable=False, default="")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "unit": self.unit}


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Association: recipe_ingredients links Recipe to Ingredient with quantity
    recipe_ingredients = db.relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "instructions": self.instructions or "",
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "ingredients": [
                {
                    "ingredient_id": ri.ingredient_id,
                    "ingredient_name": ri.ingredient.name,
                    "quantity": ri.quantity,
                    "unit": ri.unit_override or ri.ingredient.unit,
                }
                for ri in self.recipe_ingredients
            ],
        }


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable=False)
    quantity = db.Column(db.String(64), nullable=False)  # e.g. "200", "1/2", "2 cups"
    unit_override = db.Column(db.String(32), default=None)  # override ingredient's default unit

    recipe = db.relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = db.relationship("Ingredient", backref="recipe_ingredients")

    __table_args__ = (db.UniqueConstraint("recipe_id", "ingredient_id", name="uq_recipe_ingredient"),)
