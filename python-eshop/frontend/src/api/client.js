const BASKET_ID_KEY = 'eshop_basket_id';
const TOKEN_KEY = 'eshop_token';
const EMAIL_KEY = 'eshop_email';

function getBasketId() {
  let id = localStorage.getItem(BASKET_ID_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(BASKET_ID_KEY, id);
  }
  return id;
}

function getAuthHeaders() {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  } else {
    headers['X-Basket-Id'] = getBasketId();
  }
  return headers;
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    const detail = Array.isArray(error.detail)
      ? error.detail.map((item) => item.msg).join(', ')
      : error.detail;
    throw new Error(detail || 'Request failed');
  }

  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  getBasketId,
  getToken: () => localStorage.getItem(TOKEN_KEY),
  getEmail: () => localStorage.getItem(EMAIL_KEY),
  setAuth(token, email) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(EMAIL_KEY, email);
  },
  clearAuth() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(EMAIL_KEY);
  },
  isAuthenticated() {
    return Boolean(localStorage.getItem(TOKEN_KEY));
  },

  getBrands: () => request('/api/catalog/brands'),
  getTypes: () => request('/api/catalog/types'),
  getCatalogItems: ({ brandId, typeId, page }) => {
    const params = new URLSearchParams({ page: String(page || 1) });
    if (brandId) params.set('brand_id', brandId);
    if (typeId) params.set('type_id', typeId);
    return request(`/api/catalog/items?${params}`);
  },

  getBasket: () => request('/api/basket'),
  addToBasket: (catalogItemId, quantity = 1) =>
    request('/api/basket/items', {
      method: 'POST',
      body: JSON.stringify({ catalog_item_id: catalogItemId, quantity }),
    }),
  updateBasket: (quantities) =>
    request('/api/basket/items', {
      method: 'PUT',
      body: JSON.stringify({ quantities }),
    }),

  register: (email, password) =>
    request('/api/auth/register', {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
        'X-Basket-Id': getBasketId(),
      },
      body: JSON.stringify({ email, password }),
    }),
  login: (email, password) =>
    request('/api/auth/login', {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
        'X-Basket-Id': getBasketId(),
      },
      body: JSON.stringify({ email, password }),
    }),

  createOrder: (basketId) =>
    request('/api/orders', {
      method: 'POST',
      body: JSON.stringify({ basket_id: basketId }),
    }),
  getOrders: () => request('/api/orders'),
  getOrder: (orderId) => request(`/api/orders/${orderId}`),
};
