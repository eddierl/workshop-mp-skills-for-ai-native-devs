import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Header() {
  const { email, isAuthenticated, basketCount, logout } = useAuth();

  return (
    <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link to="/" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-lg font-bold text-white">
            e
          </div>
          <div>
            <p className="text-lg font-bold text-slate-900">eShopOnWeb</p>
            <p className="text-xs text-slate-500">Python tutorial edition</p>
          </div>
        </Link>

        <nav className="flex items-center gap-4">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `text-sm font-medium ${isActive ? 'text-indigo-600' : 'text-slate-600 hover:text-slate-900'}`
            }
          >
            Catalog
          </NavLink>

          {isAuthenticated && (
            <NavLink
              to="/favourites"
              className={({ isActive }) =>
                `text-sm font-medium ${isActive ? 'text-pink-600' : 'text-slate-600 hover:text-slate-900'}`
              }
            >
              <span className="flex items-center gap-1">
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
                Favourites
              </span>
            </NavLink>
          )}

          <Link
            to="/basket"
            className="relative rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          >
            Basket
            {basketCount > 0 && (
              <span className="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-indigo-600 px-1 text-xs font-bold text-white">
                {basketCount}
              </span>
            )}
          </Link>

          {isAuthenticated ? (
            <>
              <NavLink
                to="/orders"
                className={({ isActive }) =>
                  `text-sm font-medium ${isActive ? 'text-indigo-600' : 'text-slate-600 hover:text-slate-900'}`
                }
              >
                My Orders
              </NavLink>
              <span className="hidden text-sm text-slate-500 sm:inline">{email}</span>
              <button type="button" onClick={logout} className="btn-secondary">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-secondary">
                Login
              </Link>
              <Link to="/register" className="btn-primary">
                Register
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}