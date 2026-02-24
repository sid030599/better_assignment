import React, { useState, useEffect } from "react";
import { getRecipe, deleteRecipe } from "./api";
import RecipeForm from "./RecipeForm";

export default function RecipeDetail({ recipeId, ingredients, onBack, onDeleted, onUpdated }) {
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getRecipe(recipeId)
      .then((data) => { if (!cancelled) setRecipe(data); })
      .catch((e) => { if (!cancelled) setError(e.message); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [recipeId]);

  const handleDelete = async () => {
    if (!confirm("Delete this recipe?")) return;
    setError(null);
    try {
      await deleteRecipe(recipeId);
      onDeleted();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleEditSuccess = (updatedRecipe) => {
    if (updatedRecipe) setRecipe(updatedRecipe);
    setEditing(false);
    onUpdated();
  };

  if (loading) return <p className="muted">Loading…</p>;
  if (error && !recipe) {
    return (
      <>
        <div className="error">{error}</div>
        <button type="button" className="btn btn-secondary" onClick={onBack}>
          Back to list
        </button>
      </>
    );
  }

  if (editing && recipe) {
    return (
      <RecipeForm
        ingredients={ingredients}
        recipeId={recipeId}
        initialData={recipe}
        onSubmit={handleEditSuccess}
        onCancel={() => setEditing(false)}
      />
    );
  }

  return (
    <div className="card recipe-detail">
      <div className="recipe-detail-header">
        <h2>{recipe?.name}</h2>
        <div className="recipe-detail-actions">
          <button type="button" className="btn btn-secondary" onClick={onBack}>
            Back
          </button>
          <button type="button" className="btn btn-primary" onClick={() => setEditing(true)}>
            Edit
          </button>
          <button type="button" className="btn btn-danger" onClick={handleDelete}>
            Delete
          </button>
        </div>
      </div>
      {error && <div className="error">{error}</div>}
      {recipe?.instructions && (
        <section className="recipe-section">
          <h3>Instructions</h3>
          <pre className="recipe-instructions">{recipe.instructions}</pre>
        </section>
      )}
      <section className="recipe-section">
        <h3>Ingredients</h3>
        {recipe?.ingredients?.length === 0 ? (
          <p className="muted">No ingredients.</p>
        ) : (
          <ul className="ingredient-list">
            {recipe?.ingredients?.map((item, idx) => (
              <li key={idx}>
                <span className="ing-qty">{item.quantity}</span>
                <span className="ing-unit">{item.unit || "—"}</span>
                <span className="ing-name">{item.ingredient_name}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
