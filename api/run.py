"""Run the Flask app. Use for local development only."""
import os
from app import create_app

app = create_app()

with app.app_context():
    from app import db
    from app.models import Recipe, Ingredient, RecipeIngredient  # noqa: F401
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_RUN_PORT", os.environ.get("PORT", 5001)))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "1") == "1")
