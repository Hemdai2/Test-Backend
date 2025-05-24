'use client';

import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white px-6 py-4 shadow-md">
      <div className="flex justify-between items-center max-w-6xl mx-auto">
        <div className="text-xl font-bold">🍦 Nalo glacier automate</div>
        <div className="space-x-4">
          <Link href="/" className="hover:underline">Home</Link>
          <Link href="/order/" className="hover:underline">View Order</Link>
          <Link href="/admin/dashboard" className="hover:underline">Admin</Link>
          <Link href="/admin/login" className="hover:underline">Login</Link>
        </div>
      </div>
    </nav>
  );
}