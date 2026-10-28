import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function CheckoutPage() {
  const navigate = useNavigate();
  const { isAuthenticated, refreshBasket } = useAuth();
  const [basket, setBasket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/checkout' } });
      return;
    }

    api
      .getBasket()
      .then(setBasket)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [isAuthenticated, navigate]);

  async function handlePayNow() {
    if (!basket) return;
    setSubmitting(true);
    setError('');
    try {
      await api.createOrder(basket.id);
      await refreshBasket();
      navigate('/success');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <p className="text-center text-slate-500">Loading checkout...</p>;
  }

  if (!basket || basket.items.length === 0) {
    return (
      <div className="card mx-auto max-w-lg text-center">
        <h1 className="text-2xl font-bold text-slate-900">Nothing to checkout</h1>
        <Link to="/" className="btn-primary mt-6 inline-flex">
          Back to catalog
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Checkout</h1>
        <p className="mt-1 text-slate-500">Review your order before paying.</p>
      </div>

      {error && <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}

      <div className="card space-y-4">
        <h2 className="text-lg font-semibold text-slate-900">Order summary</h2>
        {basket.items.map((item) => (
          <div key={item.id} className="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0">
            <div>
              <p className="font-medium text-slate-900">{item.product_name}</p>
              <p className="text-sm text-slate-500">
                {item.quantity} x ${item.unit_price.toFixed(2)}
              </p>
            </div>
            <p className="font-semibold text-slate-900">${item.line_total.toFixed(2)}</p>
          </div>
        ))}
        <div className="flex items-center justify-between border-t border-slate-200 pt-4">
          <span className="text-lg font-semibold text-slate-900">Total</span>
          <span className="text-2xl font-bold text-slate-900">${basket.total.toFixed(2)}</span>
        </div>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-slate-900">Shipping address</h2>
        <p className="mt-2 text-slate-600">
          123 Main St.<br />
          Kent, OH 44240<br />
          United States
        </p>
        <p className="mt-3 text-sm text-slate-500">
          This tutorial uses a fixed address, just like the original eShopOnWeb sample.
        </p>
      </div>

      <div className="flex gap-3">
        <Link to="/basket" className="btn-secondary">
          Back to basket
        </Link>
        <button type="button" className="btn-primary" onClick={handlePayNow} disabled={submitting}>
          {submitting ? 'Processing...' : 'Pay now'}
        </button>
      </div>
    </div>
  );
}
