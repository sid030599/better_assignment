import React, { useState, useEffect, useCallback } from "react";
import { getRecipes, getIngredients } from "./api";
import RecipeList from "./RecipeList";
import RecipeDetail from "./RecipeDetail";
import RecipeForm from "./RecipeForm";
import IngredientList from "./IngredientList";

export default function App() {
  const [recipes, setRecipes] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [view, setView] = useState("list"); // list | detail | add | ingredients
  const [selectedRecipeId, setSelectedRecipeId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadRecipes = useCallback(async () => {
    setError(null);
    try {
      const data = await getRecipes();
      setRecipes(data);
    } catch (e) {
      setError(e.message);
      setRecipes([]);
    }
  }, []);

  const loadIngredients = useCallback(async () => {
    try {
      const data = await getIngredients();
      setIngredients(data);
    } catch {
      setIngredients([]);
    }
  }, []);

  useEffect(() => {
    setLoading(true);
    Promise.all([loadRecipes(), loadIngredients()]).finally(() => setLoading(false));
  }, [loadRecipes, loadIngredients]);

  const openRecipe = (id) => {
    setSelectedRecipeId(id);
    setView("detail");
  };

  const handleRecipeCreated = () => {
    loadRecipes();
    setView("list");
  };

  const handleRecipeDeleted = () => {
    setSelectedRecipeId(null);
    loadRecipes();
    setView("list");
  };

  const handleIngredientAdded = () => {
    loadIngredients();
  };

  if (loading) return <p className="muted">Loading…</p>;

  return (
    <>
      <header className="header">
        <h1>Recipe & Ingredient Manager</h1>
        <nav>
          <button type="button" className="btn btn-link" onClick={() => setView("list")}>
            Recipes
          </button>
          <button type="button" className="btn btn-link" onClick={() => setView("add")}>
            Add recipe
          </button>
          <button type="button" className="btn btn-link" onClick={() => setView("ingredients")}>
            Ingredients
          </button>
        </nav>
      </header>
      {error && (
        <div className="error" role="alert">
          {error}
        </div>
      )}
      {view === "list" && (
        <RecipeList recipes={recipes} onSelect={openRecipe} />
      )}
      {view === "detail" && selectedRecipeId && (
        <RecipeDetail
          recipeId={selectedRecipeId}
          ingredients={ingredients}
          onBack={() => setView("list")}
          onDeleted={handleRecipeDeleted}
          onUpdated={loadRecipes}
        />
      )}
      {view === "add" && (
        <RecipeForm
          ingredients={ingredients}
          onSubmit={handleRecipeCreated}
          onCancel={() => setView("list")}
        />
      )}
      {view === "ingredients" && (
        <IngredientList
          ingredients={ingredients}
          onAdded={handleIngredientAdded}
          onDeleted={handleIngredientAdded}
        />
      )}
    </>
  );
}
