'use client'

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

interface OrderItem {
  flavor: { name: string, price: string };
  quantity: number;
}

interface OrderData {
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

export default function OrderDetails() {
  const { code } = useParams();
  const [order, setOrder] = useState<OrderData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!code) return;

    async function fetchOrder() {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}order-details/${code}/`);
        if (!res.ok) throw new Error("Order not found");
        const data = await res.json();
        setOrder(data);
      } catch (err: any) {
        setError(err.message);
      }
    }

    fetchOrder();
  }, [code]);

  if (error) return <p className="text-red-600 text-center mt-10">{error}</p>;
  if (!order) return <p className="text-center mt-10">Loading...</p>;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-100 to-yellow-100 p-6">
      <div className="bg-white rounded-xl shadow-lg p-8 max-w-xl w-full text-center">
        <h1 className="text-2xl font-bold mb-4 text-gray-800">
          Order Details
        </h1>
        <p className="text-gray-600 mb-6">
          Order Code: <span className="font-mono">{order.order_code}</span>
        </p>

        <div className="grid grid-cols-2 gap-6 justify-items-center">
          {order.scoops.map(({ flavor, quantity }) => (
            <div key={flavor.name} className="text-center">
              <img
                src={flavorImages[flavor.name] || "/images/default.png"}
                alt={flavor.name}
                className="w-24 h-24 object-cover rounded-full mx-auto mb-2 border-2 border-pink-300"
              />
              <p className="font-semibold text-gray-800">{flavor.name}</p>
              <p className="text-sm text-gray-600">
                {quantity} scoop{quantity > 1 ? "s" : ""}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-8 text-lg font-semibold text-gray-900">
          Total Price: <span className="text-pink-600">€{order.total_price.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}
