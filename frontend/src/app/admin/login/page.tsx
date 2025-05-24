'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function AdminLoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}api/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) throw new Error('Invalid credentials');

      const data = await res.json();
      localStorage.setItem('token', data.access);
      router.push('/admin/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed');
    }
  };

  return (
    <div className="max-w-sm mx-auto mt-20 bg-white p-6 shadow rounded text-gray-700 bg-gradient-to-br from-pink-100 to-yellow-700">
      <h1 className="text-2xl font-bold mb-4 text-center">🔐 Admin Login</h1>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <input
        type="text"
        placeholder="Username"
        className="border p-2 w-full mb-2"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        className="border p-2 w-full mb-4"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button
        onClick={handleLogin}
        className="bg-blue-600 text-white px-4 py-2 w-full rounded hover:bg-blue-700"
      >
        Login
      </button>
    </div>
  );
}
