"""Request/response validation."""
from marshmallow import Schema, fields, validate


class IngredientSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    unit = fields.Str(load_default="", validate=validate.Length(max=32))


class RecipeIngredientInputSchema(Schema):
    ingredient_id = fields.Int(required=True)
    quantity = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    unit_override = fields.Str(load_default=None, validate=validate.Length(max=32))


class RecipeCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    instructions = fields.Str(load_default="", validate=validate.Length(max=5000))
    ingredients = fields.List(
        fields.Nested(RecipeIngredientInputSchema()),
        load_default=[],
        validate=validate.Length(max=100),
    )


class RecipeUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=200))
    instructions = fields.Str(validate=validate.Length(max=5000))
    ingredients = fields.List(
        fields.Nested(RecipeIngredientInputSchema()),
        validate=validate.Length(max=100),
    )
