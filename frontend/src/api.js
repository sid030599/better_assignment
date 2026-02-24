const API_BASE = "/api";

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) throw new Error(data?.error || res.statusText);
  return data;
}

export async function getRecipes() {
  return request("/recipes");
}

export async function getRecipe(id) {
  return request(`/recipes/${id}`);
}

export async function createRecipe(body) {
  return request("/recipes", { method: "POST", body: JSON.stringify(body) });
}

export async function updateRecipe(id, body) {
  return request(`/recipes/${id}`, { method: "PATCH", body: JSON.stringify(body) });
}

export async function deleteRecipe(id) {
  return request(`/recipes/${id}`, { method: "DELETE" });
}

export async function getIngredients() {
  return request("/ingredients");
}

export async function createIngredient(body) {
  return request("/ingredients", { method: "POST", body: JSON.stringify(body) });
}

export async function updateIngredient(id, body) {
  return request(`/ingredients/${id}`, { method: "PATCH", body: JSON.stringify(body) });
}

export async function deleteIngredient(id) {
  return request(`/ingredients/${id}`, { method: "DELETE" });
}
