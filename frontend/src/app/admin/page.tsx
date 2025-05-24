'use client';

import { useEffect, useState } from 'react';

interface Flavor {
    name: string, price: string, id: number
}

interface Tub {
  id: number;
  flavor: Flavor;
  scoops_left: number;
}

interface OrderItem {
  flavor: Flavor;
  quantity: number;
}

interface Order {
  order_code: string;
  total_price: number;
  scoops: OrderItem[];
}

const flavorImages: Record<string, string> = {
  ChocolateOrange: "/images/chocolate-orange.jpg",
  Cherry: "/images/cherry.jpg",
  Pistachio: "/images/pistachio.jpg",
  Vanilla: "/images/vanilla.jpg",
  Raspberry: "/images/raspberry.jpg",
};

export default function AdminPage() {
  const [tubs, setTubs] = useState<Tub[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const apiBase = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    fetch(`${apiBase}tubs/`)
      .then(res => res.json())
      .then(setTubs)
      .catch(console.error);

    fetch(`${apiBase}orders/`)
      .then(res => res.json())
      .then(setOrders)
      .catch(console.error);
  }, []);

  const handleRefill = async (tubId: number) => {
    const res = await fetch(`${apiBase}tub/refill-tub/${tubId}/`, { method: 'POST' });
    if (res.ok) {
      const updated = await res.json();
      setTubs(prev => prev.map(t => (t.id === tubId ? updated : t)));
    } else {
      console.error(res.json());
      alert("Failed to refill");
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto text-gray-700 bg-gradient-to-br from-pink-100 to-yellow-700">
      <h1 className="text-3xl font-bold mb-6 text-center">🧑‍🍳 Admin Dashboard</h1>

      {/* Tub Stock Section */}
      <section className="mb-10">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">📦 Tub Stock</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {tubs.map(tub => (
            <div
              key={tub.id}
              className="flex items-center gap-4 bg-white p-4 rounded-xl shadow border"
            >
              <img
                src={flavorImages[tub.flavor.name] || '/images/default.png'}
                alt={tub.flavor.name}
                className="w-20 h-20 rounded object-cover"
              />
              <div className="flex-1">
                <p className="text-lg font-semibold">{tub.flavor.name}</p>
                <p className="text-sm text-gray-600">Remaining scoops: {tub.scoops_left}</p>
                {tub.scoops_left != 40 && (
                  <button
                    onClick={() => handleRefill(tub.id)}
                    className="mt-2 bg-green-600 text-black text-sm px-3 py-1 rounded hover:bg-red-700"
                  >
                  ♻️ Refill
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Orders Section */}
      <section>
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">🧾 Recent Orders</h2>
        <div className="space-y-4">
          {orders.map(order => (
            <div
              key={order.order_code}
              className="bg-white p-4 rounded-xl shadow border"
            >
              <p className="font-bold text-indigo-600 mb-1">Order Code: {order.order_code}</p>
              <p className="mb-2 text-gray-700">Total Price: <strong>€{order.total_price}</strong></p>
              <div className="flex flex-wrap gap-4">
                {order.scoops.map((item, idx) => (
                  <div key={idx} className="flex flex-col items-center w-24">
                    <img
                      src={flavorImages[item.flavor.name] || '/images/default.png'}
                      alt={item.flavor.name}
                      className="w-16 h-16 rounded object-cover mb-1"
                    />
                    <p className="text-sm text-center">{item.flavor.name}</p>
                    <p className="text-xs text-gray-500">{item.quantity} scoop{item.quantity > 1 ? 's' : ''}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
