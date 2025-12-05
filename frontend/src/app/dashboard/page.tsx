'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  BarChart3,
  TrendingUp,
  AlertTriangle,
  Package,
  ArrowLeft,
  Bell,
  CheckCircle2,
  XCircle,
  Clock,
  Filter,
  Download,
  Plus,
  LogOut,
  UserCircle2
} from 'lucide-react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { useAuth } from '../auth-context';
import { useRouter } from 'next/navigation';

interface DashboardData {
  summary: {
    total_alerts: number;
    open_alerts: number;
    critical_alerts: number;
    recent_24h: number;
    by_category: Record<string, number>;
  };
  alerts: Array<{
    id: number;
    product_id: number;
    severity: string;
    category: string;
    description: string;
    status: string;
    score: number;
    confidence: number;
    created_at: string;
  }>;
  products: Array<{
    id: number;
    sku: string;
    name: string;
    category: string;
    current_stock: number;
    reorder_point: number;
    status: string;
  }>;
}

const SEVERITY_COLORS: Record<string, string> = {
  critical: '#ef4444',
  high: '#f97316',
  medium: '#f59e0b',
  low: '#3b82f6'
};

export default function UserDashboard() {
  const { user, loading, token, logout, tokenAgeSeconds } = useAuth();
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [timeRange, setTimeRange] = useState('7d');
  const [menuOpen, setMenuOpen] = useState(false);
  const [showAlertModal, setShowAlertModal] = useState(false);
  const age = tokenAgeSeconds?.();

  useEffect(() => {
    if (!loading && !user) {
      router.replace('/auth/login?next=/dashboard');
    }
  }, [loading, user, router]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      const [summaryRes, alertsRes, productsRes] = await Promise.all([
        fetch(`${apiUrl}/api/alerts/dashboard/summary`),
        fetch(`${apiUrl}/api/alerts/?limit=20&sort_by=score`),
        fetch(`${apiUrl}/api/products/`)
      ]);

      const summary = await summaryRes.json();
      const alerts = await alertsRes.json();
      const products = await productsRes.json();

      setData({ summary, alerts, products });
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }
  };

  const getSeverityBadge = (severity: string) => {
    const styles: Record<string, string> = {
      critical: 'bg-danger-100 text-danger-800 border-danger-300',
      high: 'bg-warning-100 text-warning-800 border-warning-300',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      low: 'bg-primary-100 text-primary-800 border-primary-300'
    };
    return styles[severity] || styles.low;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open':
        return <Clock className="h-4 w-4 text-warning-500" />;
      case 'resolved':
        return <CheckCircle2 className="h-4 w-4 text-success-500" />;
      case 'closed':
        return <XCircle className="h-4 w-4 text-gray-500" />;
      default:
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
    }
  };

  // Prepare chart data
  const categoryData = data?.summary.by_category 
    ? Object.entries(data.summary.by_category).map(([name, value]) => ({ name, value }))
    : [];

  const severityData = data?.alerts
    ? Object.entries(
        data.alerts.reduce((acc, alert) => {
          acc[alert.severity] = (acc[alert.severity] || 0) + 1;
          return acc;
        }, {} as Record<string, number>)
      ).map(([name, value]) => ({ name, value }))
    : [];

  if (loading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-purple-200">
        <div className="text-center">
          <div className="animate-pulse text-lg">Checking authentication...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <Link href="/landing" className="flex items-center space-x-2 text-gray-600 hover:text-gray-900">
                <ArrowLeft className="h-5 w-5" />
                <span>Back</span>
              </Link>
              <h1 className="text-2xl font-bold text-gray-900">User Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4 relative">
              <button onClick={()=>setShowAlertModal(true)} className="flex items-center space-x-2 px-4 py-2 bg-accent-600 text-white rounded-lg hover:bg-accent-700 transition-colors">
                <Plus className="h-5 w-5" />
                <span>New Alert</span>
              </button>
              <Link
                href="/admin"
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >Admin Panel</Link>
              <div className="relative">
                <button onClick={()=>setMenuOpen(o=>!o)} className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  <UserCircle2 className="h-5 w-5" />
                  <span className="hidden md:inline">{user.username}</span>
                  {age !== undefined && <span className="text-[10px] ml-2 px-2 py-0.5 rounded bg-accent-600/10 text-accent-700 font-mono">{age<60? `${age}s`:`${Math.floor(age/60)}m`}</span>}
                </button>
                {menuOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-xl p-2 z-50">
                    <div className="px-3 py-1 text-xs uppercase tracking-wide text-gray-500">Session</div>
                    <div className="px-3 py-2 text-sm flex items-center justify-between">
                      <span>Token Age</span>
                      <span className="font-mono text-xs text-gray-600">{age? `${age}s`:'—'}</span>
                    </div>
                    <button onClick={logout} className="w-full flex items-center gap-2 text-left px-3 py-2 text-sm text-danger-600 hover:bg-danger-50 rounded-md">
                      <LogOut className="h-4 w-4" /> Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-accent-100 rounded-lg">
                <Bell className="h-6 w-6 text-accent-600" />
              </div>
              <span className="text-sm text-gray-500">Total</span>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              {data?.summary.total_alerts || 0}
            </div>
            <div className="text-sm text-gray-600">Total Alerts</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-primary-100 rounded-lg">
                <Clock className="h-6 w-6 text-primary-600" />
              </div>
              <span className="text-sm text-gray-500">Open</span>
            </div>
            <div className="text-3xl font-bold text-primary-600 mb-1">
              {data?.summary.open_alerts || 0}
            </div>
            <div className="text-sm text-gray-600">Open Alerts</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-danger-100 rounded-lg">
                <AlertTriangle className="h-6 w-6 text-danger-600" />
              </div>
              <span className="text-sm text-gray-500">Critical</span>
            </div>
            <div className="text-3xl font-bold text-danger-600 mb-1">
              {data?.summary.critical_alerts || 0}
            </div>
            <div className="text-sm text-gray-600">Critical Issues</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-success-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-success-600" />
              </div>
              <span className="text-sm text-gray-500">24h</span>
            </div>
            <div className="text-3xl font-bold text-success-600 mb-1">
              {data?.summary.recent_24h || 0}
            </div>
            <div className="text-sm text-gray-600">Last 24 Hours</div>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Alert Categories */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">Alerts by Category</h2>
              <BarChart3 className="h-5 w-5 text-gray-400" />
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categoryData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Severity Distribution */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">Alert Severity</h2>
              <AlertTriangle className="h-5 w-5 text-gray-400" />
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={severityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={SEVERITY_COLORS[entry.name] || '#6366f1'} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
          <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-900">Recent Alerts</h2>
            <div className="flex items-center space-x-3">
              <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                <Filter className="h-4 w-4" />
                <span>Filter</span>
              </button>
              <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                <Download className="h-4 w-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Alert</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data?.alerts.slice(0, 10).map((alert) => (
                  <tr key={alert.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="text-sm font-medium text-gray-900">#{alert.id}</div>
                      </div>
                      <div className="text-sm text-gray-500 max-w-xs truncate">{alert.description}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${getSeverityBadge(alert.severity)}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">
                      {alert.category}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-purple-600 h-2 rounded-full" 
                            style={{ width: `${alert.score * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-700">
                          {(alert.score * 100).toFixed(0)}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(alert.status)}
                        <span className="text-sm text-gray-900 capitalize">{alert.status}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button className="text-purple-600 hover:text-purple-900 font-medium">
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Products Overview */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-bold text-gray-900">Product Inventory</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
            {data?.products.map((product) => (
              <Link 
                key={product.id} 
                href={`/products/${product.id}`}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-primary-300 transition-all cursor-pointer"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <Package className="h-5 w-5 text-gray-400" />
                    <span className="text-xs font-mono text-gray-500">{product.sku}</span>
                  </div>
                  <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">
                    {product.status || 'Active'}
                  </span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{product.name}</h3>
                <div className="text-sm text-gray-600 mb-3 capitalize">{product.category}</div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Stock:</span>
                  <span className={`font-semibold ${product.current_stock <= product.reorder_point ? 'text-red-600' : 'text-green-600'}`}>
                    {product.current_stock} units
                  </span>
                </div>
                {product.current_stock <= product.reorder_point && (
                  <div className="mt-2 text-xs text-red-600 flex items-center space-x-1">
                    <AlertTriangle className="h-3 w-3" />
                    <span>Below reorder point</span>
                  </div>
                )}
              </Link>
            ))}
          </div>
        </div>
      </main>
      {showAlertModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Create Alert</h3>
              <button onClick={()=>setShowAlertModal(false)} className="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <AlertForm token={token} onSuccess={()=>{setShowAlertModal(false); fetchDashboardData();}} />
          </div>
        </div>
      )}
    </div>
  );
}

// Inline alert creation form component
function AlertForm({ token, onSuccess }:{ token:string|null; onSuccess:()=>void }) {
  const [form, setForm] = useState({ product_id:'', severity:'medium', category:'quality', description:'' });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string|null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const submit = async (e:React.FormEvent) => {
    e.preventDefault();
    if(!token){ setError('Not authenticated'); return; }
    setSubmitting(true); setError(null);
    try {
      const res = await fetch(`${apiUrl}/api/alerts/`, {
        method:'POST',
        headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}` },
        body: JSON.stringify({
          product_id: Number(form.product_id),
          severity: form.severity,
          category: form.category,
          description: form.description || 'Manual alert'
        })
      });
      if(!res.ok){ setError(`Failed (${res.status})`); }
      else { onSuccess(); }
    } catch(err){ setError('Network error'); }
    finally { setSubmitting(false); }
  };

  return (
    <form onSubmit={submit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-xs font-medium text-gray-600">Product ID</label>
          <input className="mt-1 w-full rounded-md border-gray-300 focus:ring-purple-500 focus:border-purple-500" value={form.product_id} onChange={e=>setForm({...form, product_id:e.target.value})} required />
        </div>
        <div>
          <label className="text-xs font-medium text-gray-600">Severity</label>
          <select className="mt-1 w-full rounded-md border-gray-300 focus:ring-purple-500 focus:border-purple-500" value={form.severity} onChange={e=>setForm({...form, severity:e.target.value})}>
            {['critical','high','medium','low'].map(s=> <option key={s}>{s}</option>)}
          </select>
        </div>
        <div>
          <label className="text-xs font-medium text-gray-600">Category</label>
          <select className="mt-1 w-full rounded-md border-gray-300 focus:ring-purple-500 focus:border-purple-500" value={form.category} onChange={e=>setForm({...form, category:e.target.value})}>
            {['quality','supply','demand','expiration','defect','supplier'].map(s=> <option key={s}>{s}</option>)}
          </select>
        </div>
        <div className="col-span-2">
          <label className="text-xs font-medium text-gray-600">Description</label>
          <textarea className="mt-1 w-full rounded-md border-gray-300 focus:ring-purple-500 focus:border-purple-500" rows={3} value={form.description} onChange={e=>setForm({...form, description:e.target.value})} />
        </div>
      </div>
      {error && <div className="text-sm text-red-600">{error}</div>}
      <div className="flex items-center justify-end gap-3 pt-2">
        <button type="button" onClick={onSuccess} className="text-sm px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-50">Close</button>
        <button disabled={submitting} className="text-sm px-4 py-2 rounded-md bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2">
          {submitting && <span className="h-4 w-4 animate-spin border-2 border-white/30 border-t-white rounded-full" />}
          Create
        </button>
      </div>
    </form>
  );
}
