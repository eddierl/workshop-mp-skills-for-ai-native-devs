import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function BasketPage() {
  const navigate = useNavigate();
  const { refreshBasket, isAuthenticated } = useAuth();
  const [basket, setBasket] = useState(null);
  const [quantities, setQuantities] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadBasket();
  }, []);

  async function loadBasket() {
    setLoading(true);
    try {
      const data = await api.getBasket();
      setBasket(data);
      setQuantities(
        Object.fromEntries(data.items.map((item) => [String(item.id), item.quantity])),
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpdate() {
    setSaving(true);
    setError('');
    try {
      const updated = await api.updateBasket(quantities);
      setBasket(updated);
      await refreshBasket();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  function handleCheckout() {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/basket' } });
      return;
    }
    navigate('/checkout');
  }

  if (loading) {
    return <p className="text-center text-slate-500">Loading basket...</p>;
  }

  if (!basket || basket.items.length === 0) {
    return (
      <div className="card mx-auto max-w-lg text-center">
        <h1 className="text-2xl font-bold text-slate-900">Your basket is empty</h1>
        <p className="mt-2 text-slate-500">Browse the catalog and add something you like.</p>
        <Link to="/" className="btn-primary mt-6 inline-flex">
          Continue shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Your basket</h1>
        <p className="mt-1 text-slate-500">Update quantities before checkout.</p>
      </div>

      {error && <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}

      <div className="space-y-4">
        {basket.items.map((item) => (
          <div key={item.id} className="card flex flex-col gap-4 sm:flex-row sm:items-center">
            <img
              src={item.picture_uri}
              alt={item.product_name}
              className="h-24 w-24 rounded-lg object-cover"
            />
            <div className="flex-1">
              <h2 className="text-lg font-semibold text-slate-900">{item.product_name}</h2>
              <p className="text-sm text-slate-500">${item.unit_price.toFixed(2)} each</p>
            </div>
            <div className="flex items-center gap-3">
              <label className="text-sm text-slate-600" htmlFor={`qty-${item.id}`}>
                Qty
              </label>
              <input
                id={`qty-${item.id}`}
                type="number"
                min="0"
                value={quantities[String(item.id)] ?? item.quantity}
                onChange={(event) =>
                  setQuantities((current) => ({
                    ...current,
                    [String(item.id)]: Number(event.target.value),
                  }))
                }
                className="input-field w-24"
              />
              <p className="w-24 text-right font-semibold text-slate-900">
                ${(item.unit_price * (quantities[String(item.id)] ?? item.quantity)).toFixed(2)}
              </p>
            </div>
          </div>
        ))}
      </div>

      <div className="card flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm text-slate-500">Total</p>
          <p className="text-3xl font-bold text-slate-900">${basket.total.toFixed(2)}</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Link to="/" className="btn-secondary">
            Continue shopping
          </Link>
          <button type="button" className="btn-secondary" onClick={handleUpdate} disabled={saving}>
            {saving ? 'Updating...' : 'Update basket'}
          </button>
          <button type="button" className="btn-primary" onClick={handleCheckout}>
            Checkout
          </button>
        </div>
      </div>
    </div>
  );
}
