import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function OrderDetailPage() {
  const { orderId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: `/orders/${orderId}` } });
      return;
    }

    api
      .getOrder(orderId)
      .then(setOrder)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [isAuthenticated, navigate, orderId]);

  if (loading) {
    return <p className="text-center text-slate-500">Loading order...</p>;
  }

  if (error || !order) {
    return (
      <div className="card mx-auto max-w-lg text-center">
        <p className="text-red-700">{error || 'Order not found'}</p>
        <Link to="/orders" className="btn-secondary mt-4 inline-flex">
          Back to orders
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Order #{order.id}</h1>
          <p className="mt-1 text-slate-500">{new Date(order.order_date).toLocaleString()}</p>
        </div>
        <Link to="/orders" className="btn-secondary">
          Back to orders
        </Link>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-slate-900">Items</h2>
        <div className="mt-4 space-y-4">
          {order.items.map((item) => (
            <div key={item.id} className="flex items-center gap-4 border-b border-slate-100 pb-4 last:border-0">
              <img
                src={item.picture_uri}
                alt={item.product_name}
                className="h-16 w-16 rounded-lg object-cover"
              />
              <div className="flex-1">
                <p className="font-medium text-slate-900">{item.product_name}</p>
                <p className="text-sm text-slate-500">
                  {item.units} x ${item.unit_price.toFixed(2)}
                </p>
              </div>
              <p className="font-semibold text-slate-900">${item.line_total.toFixed(2)}</p>
            </div>
          ))}
        </div>
        <div className="mt-4 flex items-center justify-between border-t border-slate-200 pt-4">
          <span className="text-lg font-semibold text-slate-900">Total</span>
          <span className="text-2xl font-bold text-slate-900">${order.total.toFixed(2)}</span>
        </div>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-slate-900">Shipped to</h2>
        <p className="mt-2 text-slate-600">
          {order.ship_to_street}<br />
          {order.ship_to_city}, {order.ship_to_state} {order.ship_to_zip_code}<br />
          {order.ship_to_country}
        </p>
      </div>
    </div>
  );
}
