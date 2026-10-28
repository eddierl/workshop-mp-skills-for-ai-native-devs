export default function CatalogFilters({ brands, types, brandId, typeId, onChange }) {
  return (
    <div className="card flex flex-col gap-4 sm:flex-row sm:items-end">
      <div className="flex-1">
        <label htmlFor="brand" className="mb-1 block text-sm font-medium text-slate-700">
          Brand
        </label>
        <select
          id="brand"
          value={brandId}
          onChange={(event) => onChange({ brandId: event.target.value, typeId })}
          className="input-field"
        >
          <option value="">All brands</option>
          {brands.map((brand) => (
            <option key={brand.id} value={brand.id}>
              {brand.brand}
            </option>
          ))}
        </select>
      </div>

      <div className="flex-1">
        <label htmlFor="type" className="mb-1 block text-sm font-medium text-slate-700">
          Type
        </label>
        <select
          id="type"
          value={typeId}
          onChange={(event) => onChange({ brandId, typeId: event.target.value })}
          className="input-field"
        >
          <option value="">All types</option>
          {types.map((type) => (
            <option key={type.id} value={type.id}>
              {type.type}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
