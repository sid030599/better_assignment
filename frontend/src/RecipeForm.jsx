import React, { useState, useEffect } from "react";
import { createRecipe, updateRecipe } from "./api";

export default function RecipeForm({ ingredients, onSubmit, onCancel, recipeId, initialData }) {
  const isEdit = Boolean(recipeId);
  const [name, setName] = useState("");
  const [instructions, setInstructions] = useState("");
  const [lines, setLines] = useState([{ ingredient_id: "", quantity: "", unit_override: "" }]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (initialData) {
      setName(initialData.name || "");
      setInstructions(initialData.instructions || "");
      const ings = initialData.ingredients || [];
      if (ings.length > 0) {
        setLines(
          ings.map((item) => ({
            ingredient_id: item.ingredient_id ?? "",
            quantity: item.quantity ?? "",
            unit_override: item.unit_override ?? item.unit ?? "",
          }))
        );
      }
    }
  }, [initialData]);

  const addLine = () => {
    setLines((prev) => [...prev, { ingredient_id: "", quantity: "", unit_override: "" }]);
  };

  const updateLine = (idx, field, value) => {
    setLines((prev) => {
      const next = [...prev];
      next[idx] = { ...next[idx], [field]: value };
      return next;
    });
  };

  const removeLine = (idx) => {
    if (lines.length <= 1) return;
    setLines((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedName = name.trim();
    if (!trimmedName) return;
    setError(null);
    setSubmitting(true);
    const ingredientsPayload = lines
      .filter((l) => l.ingredient_id && l.quantity.trim())
      .map((l) => ({
        ingredient_id: Number(l.ingredient_id),
        quantity: l.quantity.trim(),
        unit_override: l.unit_override.trim() || undefined,
      }));
    try {
      if (isEdit) {
        const updated = await updateRecipe(recipeId, {
          name: trimmedName,
          instructions: instructions.trim(),
          ingredients: ingredientsPayload,
        });
        onSubmit(updated);
      } else {
        await createRecipe({
          name: trimmedName,
          instructions: instructions.trim(),
          ingredients: ingredientsPayload,
        });
        onSubmit();
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h2>{isEdit ? "Edit recipe" : "Add recipe"}</h2>
      {error && <div className="error">{error}</div>}
      <label>
        Recipe name
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Pasta al pomodoro"
          required
          maxLength={200}
        />
      </label>
      <label>
        Instructions
        <textarea
          value={instructions}
          onChange={(e) => setInstructions(e.target.value)}
          placeholder="Steps to make the recipe…"
          rows={4}
          maxLength={5000}
        />
      </label>
      <div className="form-section">
        <div className="form-section-head">
          <h3>Ingredients</h3>
          <button type="button" className="btn btn-link btn-sm" onClick={addLine}>
            + Add ingredient
          </button>
        </div>
        {lines.map((line, idx) => (
          <div key={idx} className="ingredient-row">
            <select
              value={line.ingredient_id}
              onChange={(e) => updateLine(idx, "ingredient_id", e.target.value)}
            >
              <option value="">Select…</option>
              {ingredients.map((ing) => (
                <option key={ing.id} value={ing.id}>
                  {ing.name} ({ing.unit || "—"})
                </option>
              ))}
            </select>
            <input
              type="text"
              value={line.quantity}
              onChange={(e) => updateLine(idx, "quantity", e.target.value)}
              placeholder="e.g. 200 or 1/2 cup"
            />
            <input
              type="text"
              value={line.unit_override}
              onChange={(e) => updateLine(idx, "unit_override", e.target.value)}
              placeholder="Unit override (optional)"
            />
            <button type="button" className="btn btn-danger btn-sm" onClick={() => removeLine(idx)}>
              Remove
            </button>
          </div>
        ))}
      </div>
      <div className="form-actions">
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? "Saving…" : isEdit ? "Update recipe" : "Save recipe"}
        </button>
      </div>
    </form>
  );
}
