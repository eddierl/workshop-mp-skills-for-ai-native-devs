import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../api/client';
import CatalogFilters from '../components/CatalogFilters';
import Pagination from '../components/Pagination';
import ProductCard from '../components/ProductCard';

export default function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [brands, setBrands] = useState([]);
  const [types, setTypes] = useState([]);
  const [catalog, setCatalog] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const brandId = searchParams.get('brand') || '';
  const typeId = searchParams.get('type') || '';
  const page = Number(searchParams.get('page') || 1);

  useEffect(() => {
    Promise.all([api.getBrands(), api.getTypes()])
      .then(([brandData, typeData]) => {
        setBrands(brandData);
        setTypes(typeData);
      })
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    setLoading(true);
    api
      .getCatalogItems({
        brandId: brandId || undefined,
        typeId: typeId || undefined,
        page,
      })
      .then(setCatalog)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [brandId, typeId, page]);

  function handleFilterChange({ brandId: nextBrand, typeId: nextType }) {
    const params = new URLSearchParams();
    if (nextBrand) params.set('brand', nextBrand);
    if (nextType) params.set('type', nextType);
    params.set('page', '1');
    setSearchParams(params);
  }

  function handlePageChange(nextPage) {
    const params = new URLSearchParams(searchParams);
    params.set('page', String(nextPage));
    setSearchParams(params);
  }

  return (
    <div className="space-y-8">
      <section className="rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 px-8 py-10 text-white shadow-lg">
        <p className="text-sm font-semibold uppercase tracking-wider text-indigo-100">
          Welcome to the store
        </p>
        <h1 className="mt-2 text-4xl font-bold">Browse the catalog</h1>
        <p className="mt-3 max-w-2xl text-indigo-100">
          Filter by brand or type, add items to your basket, and checkout when you are ready.
        </p>
      </section>

      <CatalogFilters
        brands={brands}
        types={types}
        brandId={brandId}
        typeId={typeId}
        onChange={handleFilterChange}
      />

      {error && <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}

      {loading ? (
        <p className="text-center text-slate-500">Loading catalog...</p>
      ) : (
        <>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {catalog?.items.map((item) => (
              <ProductCard key={item.id} item={item} />
            ))}
          </div>

          {catalog?.items.length === 0 && (
            <p className="text-center text-slate-500">No products match your filters.</p>
          )}

          <Pagination
            page={catalog?.page || 1}
            totalPages={catalog?.total_pages || 1}
            onPageChange={handlePageChange}
          />
        </>
      )}
    </div>
  );
}
