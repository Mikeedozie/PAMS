"use client";
import { useState } from 'react';
import { useAuth } from '../../auth-context';
import Link from 'next/link';
import { LogIn, Loader2 } from 'lucide-react';

export default function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const ok = await login(username, password);
    if (!ok) {
      setError('Invalid credentials');
      setLoading(false);
      return;
    }
    window.location.href = '/dashboard';
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-primary-900 to-slate-900 px-4">
      <div className="w-full max-w-md bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-primary-200">Sign in to access your dashboard</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-primary-100 mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-lg bg-white/10 border border-white/20 text-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500 placeholder-primary-300"
              placeholder="admin"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-primary-100 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg bg-white/10 border border-white/20 text-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500 placeholder-primary-300"
              placeholder="••••••••"
              required
            />
          </div>
          {error && <div className="text-danger-400 text-sm">{error}</div>}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-accent-600 hover:bg-accent-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg shadow-lg shadow-accent-500/30 transition-all"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <LogIn className="h-5 w-5" />}
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>
        <div className="mt-6 text-center text-primary-200 text-sm">
          Don&apos;t have an account?{' '}
          <Link href="/auth/register" className="text-accent-400 hover:text-accent-300 font-medium">Create one</Link>
        </div>
        <div className="mt-4 text-center text-xs text-primary-300 opacity-70">
          Demo: admin / Admin123!  |  analyst / Analyst123!
        </div>
        <div className="mt-6 text-center">
          <Link href="/landing" className="text-primary-300 hover:text-primary-200 text-sm">← Back to landing</Link>
        </div>
      </div>
    </div>
  );
}
