import React from "react";

export default function RecipeList({ recipes, onSelect }) {
  if (recipes.length === 0) {
    return (
      <p className="muted card">
        No recipes yet. Add one via &quot;Add recipe&quot; or create ingredients first under &quot;Ingredients&quot;.
      </p>
    );
  }
  return (
    <ul className="recipe-list">
      {recipes.map((r) => (
        <li key={r.id} className="card recipe-card">
          <button type="button" className="recipe-card-btn" onClick={() => onSelect(r.id)}>
            <span className="recipe-name">{r.name}</span>
            <span className="recipe-meta">
              {r.ingredients?.length ?? 0} ingredient{r.ingredients?.length !== 1 ? "s" : ""}
            </span>
          </button>
        </li>
      ))}
    </ul>
  );
}
