"use client";
import { useState } from 'react';
import { useAuth } from '../../auth-context';
import Link from 'next/link';
import { UserPlus, Loader2 } from 'lucide-react';

export default function RegisterPage() {
  const { register } = useAuth();
  const [form, setForm] = useState({ username: '', email: '', password: '', full_name: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const ok = await register(form);
    if (!ok) {
      setError('Registration failed (username/email may be taken)');
      setLoading(false);
      return;
    }
    window.location.href = '/dashboard';
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 px-4">
      <div className="w-full max-w-md bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
          <p className="text-purple-200">Join PAMS and unlock intelligent monitoring</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-purple-100 mb-1">Username</label>
            <input
              name="username"
              value={form.username}
              onChange={handleChange}
              className="w-full rounded-lg bg-white/10 border border-white/20 text-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-purple-300"
              placeholder="yourname"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-purple-100 mb-1">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full rounded-lg bg-white/10 border border-white/20 text-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-purple-300"
              placeholder="you@example.com"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-purple-100 mb-1">Full Name (optional)</label>
            <input
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              className="w-full rounded-lg bg-white/10 border border-white/20 text-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-purple-300"
              placeholder="Jane Doe"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-purple-100 mb-1">Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="w-full rounded-lg bg-white/10 border border-white/20 text-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder-purple-300"
              placeholder="••••••••"
              required
            />
          </div>
          {error && <div className="text-red-400 text-sm">{error}</div>}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg shadow-lg shadow-purple-500/30 transition-all"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <UserPlus className="h-5 w-5" />}
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>
        <div className="mt-6 text-center text-purple-200 text-sm">
          Already have an account?{' '}
          <Link href="/auth/login" className="text-purple-400 hover:text-purple-300 font-medium">Sign in</Link>
        </div>
        <div className="mt-6 text-center">
          <Link href="/landing" className="text-purple-300 hover:text-purple-200 text-sm">← Back to landing</Link>
        </div>
      </div>
    </div>
  );
}
