import React, { useState } from "react";
import { createIngredient, updateIngredient, deleteIngredient } from "./api";

export default function IngredientList({ ingredients, onAdded, onDeleted }) {
  const [name, setName] = useState("");
  const [unit, setUnit] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editUnit, setEditUnit] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedName = name.trim();
    if (!trimmedName) return;
    setError(null);
    setSubmitting(true);
    try {
      await createIngredient({ name: trimmedName, unit: unit.trim() });
      setName("");
      setUnit("");
      onAdded();
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  const startEdit = (ing) => {
    setEditingId(ing.id);
    setEditName(ing.name);
    setEditUnit(ing.unit || "");
    setError(null);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditName("");
    setEditUnit("");
  };

  const saveEdit = async () => {
    const trimmedName = editName.trim();
    if (!trimmedName) return;
    setError(null);
    try {
      await updateIngredient(editingId, { name: trimmedName, unit: editUnit.trim() });
      onAdded();
      cancelEdit();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleDelete = async (ing) => {
    if (!confirm(`Delete ingredient "${ing.name}"?`)) return;
    setError(null);
    try {
      await deleteIngredient(ing.id);
      onDeleted?.();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="card">
      <h2>Ingredients</h2>
      <p className="muted">Add ingredients here; then use them when creating recipes. You cannot delete an ingredient that is used in a recipe.</p>
      <form className="ingredient-form" onSubmit={handleSubmit}>
        {error && <div className="error">{error}</div>}
        <div className="ingredient-form-row">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Ingredient name"
            required
            maxLength={120}
          />
          <input
            type="text"
            value={unit}
            onChange={(e) => setUnit(e.target.value)}
            placeholder="Unit (e.g. g, ml)"
            maxLength={32}
          />
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? "Adding…" : "Add"}
          </button>
        </div>
      </form>
      {ingredients.length === 0 ? (
        <p className="muted">No ingredients yet.</p>
      ) : (
        <ul className="ingredient-list-simple">
          {ingredients.map((ing) => (
            <li key={ing.id} className="ingredient-list-item">
              {editingId === ing.id ? (
                <div className="ingredient-edit-row">
                  <input
                    type="text"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    placeholder="Name"
                    maxLength={120}
                    className="ingredient-edit-input"
                  />
                  <input
                    type="text"
                    value={editUnit}
                    onChange={(e) => setEditUnit(e.target.value)}
                    placeholder="Unit"
                    maxLength={32}
                    className="ingredient-edit-input"
                  />
                  <button type="button" className="btn btn-primary btn-sm" onClick={saveEdit}>
                    Save
                  </button>
                  <button type="button" className="btn btn-secondary btn-sm" onClick={cancelEdit}>
                    Cancel
                  </button>
                </div>
              ) : (
                <>
                  <span className="ing-name">{ing.name}</span>
                  {ing.unit && <span className="ing-unit">{ing.unit}</span>}
                  <div className="ingredient-item-actions">
                    <button type="button" className="btn btn-link btn-sm" onClick={() => startEdit(ing)}>
                      Edit
                    </button>
                    <button type="button" className="btn btn-danger btn-sm" onClick={() => handleDelete(ing)}>
                      Delete
                    </button>
                  </div>
                </>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
