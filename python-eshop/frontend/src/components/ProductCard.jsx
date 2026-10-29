import { useState } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function ProductCard({ item, onAdded }) {
  const { refreshBasket } = useAuth();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [isFav, setIsFav] = useState(item.is_favourite || false);
  const [favLoading, setFavLoading] = useState(false);

  async function handleAdd() {
    setLoading(true);
    setMessage('');
    try {
      await api.addToBasket(item.id);
      await refreshBasket();
      setMessage('Added!');
      onAdded?.();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleToggleFav() {
    if (!api.isAuthenticated()) {
      window.location.href = '/login';
      return;
    }
    setFavLoading(true);
    try {
      if (isFav) {
        await api.removeFavourite(item.id);
      } else {
        await api.addFavourite(item.id);
      }
      setIsFav(!isFav);
    } catch {
      // Silently fail — the catalog will refresh and correct itself
    } finally {
      setFavLoading(false);
    }
  }

  return (
    <article className="card flex flex-col overflow-hidden p-0 transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="relative aspect-square overflow-hidden bg-slate-100">
        <img
          src={item.picture_uri}
          alt={item.name}
          className="h-full w-full object-cover"
        />
        <button
          type="button"
          onClick={handleToggleFav}
          disabled={favLoading}
          className="absolute right-2 top-2 rounded-full bg-white/80 p-2 shadow-sm transition hover:bg-white"
          aria-label={isFav ? 'Remove from favourites' : 'Add to favourites'}
        >
          <svg
            className={`h-5 w-5 ${isFav ? 'text-red-500' : 'text-slate-400'}`}
            fill={isFav ? 'currentColor' : 'none'}
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
          >
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
          </svg>
        </button>
      </div>
      <div className="flex flex-1 flex-col gap-3 p-4">
        <div className="flex-1">
          <p className="text-xs font-medium uppercase tracking-wide text-indigo-600">
            {item.brand_name} · {item.type_name}
          </p>
          <h3 className="mt-1 text-lg font-semibold text-slate-900">{item.name}</h3>
          <p className="mt-2 text-sm text-slate-500 line-clamp-2">{item.description}</p>
        </div>
        <div className="flex items-center justify-between gap-3">
          <p className="text-xl font-bold text-slate-900">${item.price.toFixed(2)}</p>
          <button
            type="button"
            onClick={handleAdd}
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Adding...' : 'Add to basket'}
          </button>
        </div>
        {message && <p className="text-xs font-medium text-emerald-600">{message}</p>}
      </div>
    </article>
  );
}