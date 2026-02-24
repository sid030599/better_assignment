"""API tests. Run from api dir: pytest -v"""
import pytest
from app import create_app
from app import db
from app.models import Recipe, Ingredient, RecipeIngredient


@pytest.fixture
def client():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.close()
        db.drop_all()


def test_list_recipes_empty(client):
    r = client.get("/api/recipes")
    assert r.status_code == 200
    assert r.get_json() == []


def test_create_ingredient(client):
    r = client.post("/api/ingredients", json={"name": "Flour", "unit": "g"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "Flour"
    assert data["unit"] == "g"
    assert "id" in data


def test_create_ingredient_duplicate_fails(client):
    client.post("/api/ingredients", json={"name": "Salt", "unit": "g"})
    r = client.post("/api/ingredients", json={"name": "Salt", "unit": "pinch"})
    assert r.status_code == 400


def test_list_ingredients(client):
    client.post("/api/ingredients", json={"name": "Water", "unit": "ml"})
    r = client.get("/api/ingredients")
    assert r.status_code == 200
    data = r.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Water"


def test_create_recipe_with_ingredients(client):
    ing = client.post("/api/ingredients", json={"name": "Flour", "unit": "g"}).get_json()
    r = client.post(
        "/api/recipes",
        json={
            "name": "Simple Dough",
            "instructions": "Mix and bake.",
            "ingredients": [
                {"ingredient_id": ing["id"], "quantity": "200", "unit_override": "g"},
            ],
        },
    )
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "Simple Dough"
    assert len(data["ingredients"]) == 1
    assert data["ingredients"][0]["ingredient_name"] == "Flour"
    assert data["ingredients"][0]["quantity"] == "200"


def test_create_recipe_invalid_ingredient_id(client):
    r = client.post(
        "/api/recipes",
        json={
            "name": "Bad Recipe",
            "ingredients": [{"ingredient_id": 99999, "quantity": "1"}],
        },
    )
    assert r.status_code == 400


def test_get_recipe(client):
    ing = client.post("/api/ingredients", json={"name": "Sugar", "unit": "g"}).get_json()
    create = client.post(
        "/api/recipes",
        json={
            "name": "Sweet",
            "ingredients": [{"ingredient_id": ing["id"], "quantity": "50"}],
        },
    )
    rid = create.get_json()["id"]
    r = client.get(f"/api/recipes/{rid}")
    assert r.status_code == 200
    data = r.get_json()
    assert data["name"] == "Sweet"
    assert len(data["ingredients"]) == 1


def test_delete_recipe(client):
    create = client.post("/api/recipes", json={"name": "To Delete", "ingredients": []})
    rid = create.get_json()["id"]
    r = client.delete(f"/api/recipes/{rid}")
    assert r.status_code == 204
    get_r = client.get(f"/api/recipes/{rid}")
    assert get_r.status_code == 404


def test_update_ingredient(client):
    create = client.post("/api/ingredients", json={"name": "Flour", "unit": "g"})
    iid = create.get_json()["id"]
    r = client.patch(f"/api/ingredients/{iid}", json={"name": "White Flour", "unit": "grams"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["name"] == "White Flour"
    assert data["unit"] == "grams"


def test_delete_ingredient_unused(client):
    create = client.post("/api/ingredients", json={"name": "Orphan", "unit": ""})
    iid = create.get_json()["id"]
    r = client.delete(f"/api/ingredients/{iid}")
    assert r.status_code == 204
    get_r = client.get(f"/api/ingredients/{iid}")
    assert get_r.status_code == 404


def test_delete_ingredient_in_use_fails(client):
    ing = client.post("/api/ingredients", json={"name": "Salt", "unit": "g"}).get_json()
    client.post(
        "/api/recipes",
        json={"name": "Dish", "ingredients": [{"ingredient_id": ing["id"], "quantity": "1"}]},
    )
    r = client.delete(f"/api/ingredients/{ing['id']}")
    assert r.status_code == 400
    assert "used in recipes" in r.get_json().get("error", "")
