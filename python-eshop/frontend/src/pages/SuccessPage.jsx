import { Link } from 'react-router-dom';

export default function SuccessPage() {
  return (
    <div className="card mx-auto max-w-lg text-center">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100 text-3xl">
        ✓
      </div>
      <h1 className="mt-6 text-3xl font-bold text-slate-900">Thank you for your order!</h1>
      <p className="mt-2 text-slate-500">
        Your order has been placed successfully. You can view it in My Orders.
      </p>
      <div className="mt-8 flex flex-wrap justify-center gap-3">
        <Link to="/" className="btn-primary">
          Continue shopping
        </Link>
        <Link to="/orders" className="btn-secondary">
          View my orders
        </Link>
      </div>
    </div>
  );
}
