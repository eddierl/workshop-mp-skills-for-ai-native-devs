import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function OrdersPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/orders' } });
      return;
    }

    api
      .getOrders()
      .then(setOrders)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [isAuthenticated, navigate]);

  if (loading) {
    return <p className="text-center text-slate-500">Loading orders...</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">My orders</h1>
        <p className="mt-1 text-slate-500">View your past purchases.</p>
      </div>

      {error && <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}

      {orders.length === 0 ? (
        <div className="card text-center">
          <p className="text-slate-500">You have not placed any orders yet.</p>
          <Link to="/" className="btn-primary mt-4 inline-flex">
            Start shopping
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <Link
              key={order.id}
              to={`/orders/${order.id}`}
              className="card block transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-lg font-semibold text-slate-900">Order #{order.id}</p>
                  <p className="text-sm text-slate-500">
                    {new Date(order.order_date).toLocaleString()}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold text-slate-900">${order.total.toFixed(2)}</p>
                  <p className="text-sm text-slate-500">{order.item_count} items</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
