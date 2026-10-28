import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function FavouritesPage() {
  const { isAuthenticated } = useAuth();
  const [favourites, setFavourites] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [removingId, setRemovingId] = useState(null);

  useEffect(() => {
    loadFavourites();
  }, []);

  async function loadFavourites() {
    setLoading(true);
    setError('');
    try {
      const data = await api.getFavourites();
      setFavourites(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleRemove(catalogItemId) {
    setRemovingId(catalogItemId);
    try {
      await api.removeFavourite(catalogItemId);
      await loadFavourites();
    } catch (err) {
      setError(err.message);
    } finally {
      setRemovingId(null);
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="space-y-8">
        <section className="rounded-2xl bg-gradient-to-r from-pink-600 to-rose-600 px-8 py-10 text-white shadow-lg">
          <p className="text-sm font-semibold uppercase tracking-wider text-pink-100">
            Saved for later
          </p>
          <h1 className="mt-2 text-4xl font-bold">Sign in to see your favourites</h1>
          <p className="mt-3 max-w-2xl text-pink-100">
            Sign in to save products and see them here.
          </p>
        </section>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="space-y-8">
        <section className="rounded-2xl bg-gradient-to-r from-pink-600 to-rose-600 px-8 py-10 text-white shadow-lg">
          <p className="text-sm font-semibold uppercase tracking-wider text-pink-100">
            Saved for later
          </p>
          <h1 className="mt-2 text-4xl font-bold">My Favourites</h1>
        </section>
        <p className="text-center text-slate-500">Loading favourites...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-8">
        <section className="rounded-2xl bg-gradient-to-r from-pink-600 to-rose-600 px-8 py-10 text-white shadow-lg">
          <p className="text-sm font-semibold uppercase tracking-wider text-pink-100">
            Saved for later
          </p>
          <h1 className="mt-2 text-4xl font-bold">My Favourites</h1>
        </section>
        <div className="card mx-auto max-w-lg text-center">
          <p className="text-red-700">{error}</p>
          <button type="button" onClick={loadFavourites} className="btn-primary mt-6 inline-flex">
            Try again
          </button>
        </div>
      </div>
    );
  }

  if (!favourites || favourites.length === 0) {
    return (
      <div className="space-y-8">
        <section className="rounded-2xl bg-gradient-to-r from-pink-600 to-rose-600 px-8 py-10 text-white shadow-lg">
          <p className="text-sm font-semibold uppercase tracking-wider text-pink-100">
            Saved for later
          </p>
          <h1 className="mt-2 text-4xl font-bold">My Favourites</h1>
        </section>
        <div className="card mx-auto max-w-lg text-center">
          <h2 className="text-2xl font-bold text-slate-900">You haven't saved any products yet</h2>
          <p className="mt-2 text-slate-500">Browse the catalog and tap the heart icon on products you love.</p>
          <Link to="/" className="btn-primary mt-6 inline-flex">
            Browse the catalog
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <section className="rounded-2xl bg-gradient-to-r from-pink-600 to-rose-600 px-8 py-10 text-white shadow-lg">
        <p className="text-sm font-semibold uppercase tracking-wider text-pink-100">
          Saved for later
        </p>
        <h1 className="mt-2 text-4xl font-bold">My Favourites</h1>
        <p className="mt-3 max-w-2xl text-pink-100">
          {favourites.length} product{favourites.length !== 1 ? 's' : ''} saved
        </p>
      </section>

      {error && <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {favourites.map((fav) => (
          <article
            key={fav.id}
            className="card flex flex-col overflow-hidden p-0 transition hover:-translate-y-0.5 hover:shadow-md"
          >
            <div className="aspect-square overflow-hidden bg-slate-100">
              <img
                src={fav.picture_uri}
                alt={fav.name}
                className="h-full w-full object-cover"
              />
            </div>
            <div className="flex flex-1 flex-col gap-3 p-4">
              <div className="flex-1">
                <p className="text-xs font-medium uppercase tracking-wide text-pink-600">
                  {fav.name}
                </p>
                <p className="mt-2 text-xl font-bold text-slate-900">
                  ${fav.price.toFixed(2)}
                </p>
              </div>
              <div className="flex gap-2">
                <Link
                  to={`/?brand=${fav.catalog_brand_id || ''}&type=${fav.catalog_type_id || ''}`}
                  className="btn-secondary flex-1 text-center"
                >
                  View
                </Link>
                <button
                  type="button"
                  onClick={() => handleRemove(fav.catalog_item_id)}
                  disabled={removingId === fav.catalog_item_id}
                  className="btn-secondary flex items-center gap-1 px-3"
                  aria-label="Remove from favourites"
                >
                  <svg
                    className="h-4 w-4 text-red-500"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                  </svg>
                  {removingId === fav.catalog_item_id ? 'Removing...' : 'Remove'}
                </button>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
