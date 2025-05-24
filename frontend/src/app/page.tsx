'use client';

import { useEffect, useState } from 'react';

type FlavorOption = {
  id: number;
  name: string;
};

type ScoopSelection = {
  flavorId: number;
  quantity: number;
};
type ErrorResponse = {
  error: string
}

const flavorImages: Record<string, string> = {
  ChocolateOrange: "/images/chocolate-orange.jpg",
  Cherry: "/images/cherry.jpg",
  Pistachio: "/images/pistachio.jpg",
  Vanilla: "/images/vanilla.jpg",
  Raspberry: "/images/raspberry.jpg",
};

export default function OrderPage() {
  const [flavors, setFlavors] = useState<FlavorOption[]>([]);
  const [selections, setSelections] = useState<ScoopSelection[]>([]);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<{ order_code: string; total_price: number } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const apiBase = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    fetch(`${apiBase}flavors/`)
      .then(res => res.json())
      .then(setFlavors)
      .catch(console.error);
  }, []);

  const handleQuantityChange = (flavorId: number, quantity: number) => {
    setSelections(prev =>
      prev.map(sel => sel.flavorId === flavorId ? { ...sel, quantity } : sel)
        .concat(prev.some(sel => sel.flavorId === flavorId) ? [] : [{ flavorId, quantity }])
    );
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const orderData = {
        scoops: selections
          .filter(sel => sel.quantity > 0)
          .map(sel => ({
            flavor: sel.flavorId,
            quantity: sel.quantity,
          })),
      };

      const res = await fetch(`${apiBase}create-order/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData),
      });
      if (res.status >= 400) {
        
        const errorData: ErrorResponse = await res.json();
        setError(errorData.error);
      }
      const data = await res.json();
      setResponse(data);
    } catch (err) {
     console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-yellow-50 to-pink-100 p-6">
      <div className="bg-white rounded-xl shadow-xl p-8 max-w-2xl w-full text-center">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">🍦 Créez votre commande de glace ici </h1>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-6 mb-6">
          {flavors.map(flavor => (
            <div key={flavor.id} className="bg-white p-4 rounded shadow text-center">
              <img
                src={flavorImages[flavor.name] || "/images/default.png"}
                alt={flavor.name}
                className="w-24 h-24 mx-auto mb-2 rounded-full border-2 border-pink-300 object-cover"
              />
              <p className="font-semibold text-gray-800">{flavor.name}</p>
              <input
                type="number"
                min={0}
                onChange={e =>
                  handleQuantityChange(flavor.id, parseInt(e.target.value, 10) || 0)
                }
                className="mt-2 border rounded p-1 w-20 mx-auto text-center text-black"
              />
            </div>
          ))}
        </div>
        {error && (
  <div className="mt-4 p-3 bg-red-100 text-red-800 border border-red-400 rounded">
    ❌ Error occurred: {error}
  </div>
)}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition"
        >
          {loading ? 'Submitting...' : 'Submit Order'}
        </button>

        {response && (
          <div className="mt-8 p-6 bg-green-50 border border-green-400 rounded-lg shadow-md">
            <h2 className="text-xl font-bold text-green-700 mb-2">✅ Order placed successfully!</h2>
            <p className="text-lg text-gray-800">
              <strong className="text-green-800">Order Code:</strong>{' '}
              <span className="font-mono text-green-900 bg-green-100 px-2 py-1 rounded">{response.order_code}</span>
            </p>
            <p className="text-lg text-gray-800 mt-1">
              <strong className="text-green-800">Total Price:</strong>{' '}
              <span className="font-semibold text-green-900">€{response.total_price}</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
