'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  Users,
  AlertTriangle,
  Package,
  BarChart3,
  Settings,
  TrendingUp,
  Activity,
  Database,
  ArrowLeft,
  Plus,
  Edit,
  Trash2,
  Download,
  Upload,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Clock,
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

interface AdminStats {
  total_products: number;
  total_alerts: number;
  total_users: number;
  system_health: number;
  alerts_by_status: Record<string, number>;
  alerts_by_severity: Record<string, number>;
  recent_activity: Array<{
    id: number;
    type: string;
    description: string;
    timestamp: string;
  }>;
}

export default function AdminDashboard() {
  const { user, loading, token, logout } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [products, setProducts] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [dataLoading, setDataLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'products' | 'alerts' | 'users' | 'settings'>('overview');
  const [menuOpen, setMenuOpen] = useState(false);
  const [showProductModal, setShowProductModal] = useState(false);
  const [showAlertModal, setShowAlertModal] = useState(false);

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.replace('/auth/login?next=/admin');
      } else {
        // Basic role gate: treat username 'admin' as admin for now
        if (user.username !== 'admin') {
          router.replace('/dashboard');
        }
      }
    }
  }, [loading, user, router]);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      const [productsRes, alertsRes, summaryRes] = await Promise.all([
        fetch(`${apiUrl}/api/products/`),
        fetch(`${apiUrl}/api/alerts/?limit=50`),
        fetch(`${apiUrl}/api/alerts/dashboard/summary`)
      ]);

      const productsData = await productsRes.json();
      const alertsData = await alertsRes.json();
      const summaryData = await summaryRes.json();

      setProducts(productsData);
      setAlerts(alertsData);

      // Build admin stats
      const alertsByStatus = alertsData.reduce((acc: any, alert: any) => {
        acc[alert.status] = (acc[alert.status] || 0) + 1;
        return acc;
      }, {});

      const alertsBySeverity = alertsData.reduce((acc: any, alert: any) => {
        acc[alert.severity] = (acc[alert.severity] || 0) + 1;
        return acc;
      }, {});

      setStats({
        total_products: productsData.length,
        total_alerts: alertsData.length,
        total_users: 2, // Mock data
        system_health: 95,
        alerts_by_status: alertsByStatus,
        alerts_by_severity: alertsBySeverity,
        recent_activity: [] // Mock data
      });

      setDataLoading(false);
    } catch (error) {
      console.error('Failed to fetch admin data:', error);
      setDataLoading(false);
    }
  };

  const statusData = stats?.alerts_by_status
    ? Object.entries(stats.alerts_by_status).map(([name, value]) => ({ name, value }))
    : [];

  const severityData = stats?.alerts_by_severity
    ? Object.entries(stats.alerts_by_severity).map(([name, value]) => ({ name, value }))
    : [];

  if (loading || dataLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <div className="text-xl text-gray-600">Loading Admin Dashboard...</div>
        </div>
      </div>
    );
  }

  if (!user || user.username !== 'admin') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-purple-200">
        <div className="text-center space-y-2">
          <div className="animate-pulse text-lg">Authorizing...</div>
          <p className="text-xs opacity-60">Verifying admin privileges</p>
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
              <div className="flex items-center space-x-2">
                <Settings className="h-6 w-6 text-purple-600" />
                <h1 className="text-2xl font-bold text-gray-900">Admin Panel</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button 
                onClick={fetchAdminData}
                className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Refresh</span>
              </button>
              <div className="relative">
                <button onClick={()=>setMenuOpen(o=>!o)} className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  <UserCircle2 className="h-5 w-5" />
                  <span className="hidden md:inline">{user?.username}</span>
                </button>
                {menuOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-xl p-2 z-50">
                    <button onClick={logout} className="w-full flex items-center gap-2 text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md">
                      <LogOut className="h-4 w-4" /> Logout
                    </button>
                  </div>
                )}
              </div>
              <Link 
                href="/dashboard" 
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                User View
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
          <div className="flex border-b border-gray-200">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'products', label: 'Products', icon: Package },
              { id: 'alerts', label: 'Alerts', icon: AlertTriangle },
              { id: 'users', label: 'Users', icon: Users },
              { id: 'settings', label: 'Settings', icon: Settings }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-6 py-4 font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'border-b-2 border-purple-600 text-purple-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
                <div className="flex items-center justify-between mb-4">
                  <Package className="h-8 w-8 opacity-80" />
                  <TrendingUp className="h-5 w-5 opacity-80" />
                </div>
                <div className="text-3xl font-bold mb-1">{stats?.total_products || 0}</div>
                <div className="text-purple-100">Total Products</div>
              </div>

              <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl shadow-lg p-6 text-white">
                <div className="flex items-center justify-between mb-4">
                  <AlertTriangle className="h-8 w-8 opacity-80" />
                  <Activity className="h-5 w-5 opacity-80" />
                </div>
                <div className="text-3xl font-bold mb-1">{stats?.total_alerts || 0}</div>
                <div className="text-primary-100">Active Alerts</div>
              </div>

              <div className="bg-gradient-to-br from-success-500 to-success-600 rounded-xl shadow-lg p-6 text-white">
                <div className="flex items-center justify-between mb-4">
                  <Users className="h-8 w-8 opacity-80" />
                  <CheckCircle2 className="h-5 w-5 opacity-80" />
                </div>
                <div className="text-3xl font-bold mb-1">{stats?.total_users || 0}</div>
                <div className="text-success-100">Active Users</div>
              </div>

              <div className="bg-gradient-to-br from-warning-500 to-warning-600 rounded-xl shadow-lg p-6 text-white">
                <div className="flex items-center justify-between mb-4">
                  <Database className="h-8 w-8 opacity-80" />
                  <Activity className="h-5 w-5 opacity-80" />
                </div>
                <div className="text-3xl font-bold mb-1">{stats?.system_health || 0}%</div>
                <div className="text-warning-100">System Health</div>
              </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-6">Alerts by Status</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={statusData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {statusData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={['#22c55e', '#f59e0b', '#c026d3', '#ef4444'][index % 4]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-6">Alerts by Severity</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={severityData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* System Status */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-6">System Status</h3>
              <div className="space-y-4">
                {[ 
                  { name: 'API Server', status: 'Operational', uptime: '99.9%' },
                  { name: 'Database', status: 'Operational', uptime: '99.8%' },
                  { name: 'ML Models', status: 'Operational', uptime: '98.5%' },
                  { name: 'Background Jobs', status: 'Operational', uptime: '99.2%' }
                ].map((service, idx) => (
                  <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      <span className="font-medium text-gray-900">{service.name}</span>
                    </div>
                    <div className="flex items-center space-x-4">
                      <span className="text-sm text-gray-600">Uptime: {service.uptime}</span>
                      <span className="text-sm font-medium text-green-600">{service.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">Product Management</h2>
              <div className="flex items-center space-x-3">
                <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  <Upload className="h-4 w-4" />
                  <span>Import</span>
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  <Download className="h-4 w-4" />
                  <span>Export</span>
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors" onClick={()=>setShowProductModal(true)}>
                  <Plus className="h-4 w-4" />
                  <span>Add Product</span>
                </button>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SKU</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reorder Point</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {products.map((product) => (
                    <tr key={product.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">{product.sku}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        <Link href={`/products/${product.id}`} className="text-primary-600 hover:text-primary-800 hover:underline">
                          {product.name}
                        </Link>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 capitalize">{product.category}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={`font-semibold ${product.current_stock <= product.reorder_point ? 'text-red-600' : 'text-green-600'}`}>
                          {product.current_stock}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{product.reorder_point}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                          Active
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <div className="flex items-center space-x-3">
                          <Link href={`/products/${product.id}`} className="text-primary-600 hover:text-primary-900">
                            <Edit className="h-4 w-4" />
                          </Link>
                          <button className="text-red-600 hover:text-red-900">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Alerts Tab */}
        {activeTab === 'alerts' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">Alert Management</h2>
              <div className="flex items-center space-x-3">
                <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  <Download className="h-4 w-4" />
                  <span>Export All</span>
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors" onClick={()=>setShowAlertModal(true)}>
                  <Plus className="h-4 w-4" />
                  <span>Create Alert</span>
                </button>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {alerts.slice(0, 20).map((alert) => (
                    <tr key={alert.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{alert.id}</td>
                      <td className="px-6 py-4 text-sm text-gray-900 max-w-md truncate">{alert.description}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                          alert.severity === 'critical' ? 'bg-danger-100 text-danger-800' :
                          alert.severity === 'high' ? 'bg-warning-100 text-warning-800' :
                          alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-primary-100 text-primary-800'
                        }`}>
                          {alert.severity.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 capitalize">{alert.category}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {(alert.score * 100).toFixed(0)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm capitalize">{alert.status}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(alert.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <div className="flex items-center space-x-3">
                          <button className="text-primary-600 hover:text-primary-900">
                            <Edit className="h-4 w-4" />
                          </button>
                          <button className="text-danger-600 hover:text-danger-900">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <Users className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">User Management</h3>
            <p className="text-gray-600 mb-6">Manage user accounts, roles, and permissions</p>
            <button className="px-6 py-3 bg-accent-600 text-white rounded-lg hover:bg-accent-700 transition-colors">
              Coming Soon
            </button>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <Settings className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">System Settings</h3>
            <p className="text-gray-600 mb-6">Configure system preferences, integrations, and notifications</p>
            <button className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
              Coming Soon
            </button>
          </div>
        )}
      </div>

      {showProductModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Add Product</h3>
              <button onClick={()=>setShowProductModal(false)} className="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <ProductForm token={token} onSuccess={()=>{setShowProductModal(false); fetchAdminData();}} />
          </div>
        </div>
      )}
      {showAlertModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Create Alert</h3>
              <button onClick={()=>setShowAlertModal(false)} className="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <AdminAlertForm token={token} products={products} onSuccess={()=>{setShowAlertModal(false); fetchAdminData();}} />
          </div>
        </div>
      )}
    </div>
  );
}

function ProductForm({ token, onSuccess }:{ token:string|null; onSuccess:()=>void }) {
  const [form, setForm] = useState({ sku:'', name:'', category:'', current_stock:'0', reorder_point:'0' });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string|null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const submit = async (e:React.FormEvent) => {
    e.preventDefault();
    if(!token){ setError('Not authenticated'); return; }
    setSubmitting(true); setError(null);
    try {
      const res = await fetch(`${apiUrl}/api/products/`, {
        method:'POST',
        headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}` },
        body: JSON.stringify({
          sku: form.sku,
          name: form.name,
          category: form.category,
          current_stock: Number(form.current_stock),
          reorder_point: Number(form.reorder_point)
        })
      });
      if(!res.ok) setError(`Failed (${res.status})`); else onSuccess();
    } catch(err){ setError('Network error'); } finally { setSubmitting(false); }
  };
  return <form onSubmit={submit} className="space-y-4">
    <div className="grid grid-cols-2 gap-4">
      <div><label className="text-xs font-medium text-gray-600">SKU</label><input className="mt-1 w-full rounded-md border-gray-300 focus:ring-purple-500 focus:border-purple-500" value={form.sku} onChange={e=>setForm({...form, sku:e.target.value})} required /></div>
      <div><label className="text-xs font-medium text-gray-600">Name</label><input className="mt-1 w-full rounded-md border-gray-300" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} required /></div>
      <div><label className="text-xs font-medium text-gray-600">Category</label><input className="mt-1 w-full rounded-md border-gray-300" value={form.category} onChange={e=>setForm({...form, category:e.target.value})} required /></div>
      <div><label className="text-xs font-medium text-gray-600">Current Stock</label><input type="number" className="mt-1 w-full rounded-md border-gray-300" value={form.current_stock} onChange={e=>setForm({...form, current_stock:e.target.value})} required /></div>
      <div><label className="text-xs font-medium text-gray-600">Reorder Point</label><input type="number" className="mt-1 w-full rounded-md border-gray-300" value={form.reorder_point} onChange={e=>setForm({...form, reorder_point:e.target.value})} required /></div>
    </div>
    {error && <div className="text-sm text-red-600">{error}</div>}
    <div className="flex justify-end gap-3 pt-2">
      <button type="button" onClick={onSuccess} className="text-sm px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-50">Close</button>
      <button disabled={submitting} className="text-sm px-4 py-2 rounded-md bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2">{submitting && <span className="h-4 w-4 animate-spin border-2 border-white/30 border-t-white rounded-full" />}Create</button>
    </div>
  </form>;
}

function AdminAlertForm({ token, onSuccess, products }:{ token:string|null; onSuccess:()=>void; products:any[] }) {
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
      if(!res.ok) setError(`Failed (${res.status})`); else onSuccess();
    } catch(err){ setError('Network error'); } finally { setSubmitting(false); }
  };
  return <form onSubmit={submit} className="space-y-4">
    <div className="grid grid-cols-2 gap-4">
      <div className="col-span-2"><label className="text-xs font-medium text-gray-600">Product</label><select className="mt-1 w-full rounded-md border-gray-300" value={form.product_id} onChange={e=>setForm({...form, product_id:e.target.value})} required><option value="">Select product</option>{products.map(p=> <option key={p.id} value={p.id}>{p.name}</option>)}</select></div>
      <div><label className="text-xs font-medium text-gray-600">Severity</label><select className="mt-1 w-full rounded-md border-gray-300" value={form.severity} onChange={e=>setForm({...form, severity:e.target.value})}>{['critical','high','medium','low'].map(s=> <option key={s}>{s}</option>)}</select></div>
      <div><label className="text-xs font-medium text-gray-600">Category</label><select className="mt-1 w-full rounded-md border-gray-300" value={form.category} onChange={e=>setForm({...form, category:e.target.value})}>{['quality','supply','demand','expiration','defect','supplier'].map(s=> <option key={s}>{s}</option>)}</select></div>
      <div className="col-span-2"><label className="text-xs font-medium text-gray-600">Description</label><textarea className="mt-1 w-full rounded-md border-gray-300" rows={3} value={form.description} onChange={e=>setForm({...form, description:e.target.value})} /></div>
    </div>
    {error && <div className="text-sm text-red-600">{error}</div>}
    <div className="flex justify-end gap-3 pt-2">
      <button type="button" onClick={onSuccess} className="text-sm px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-50">Close</button>
      <button disabled={submitting} className="text-sm px-4 py-2 rounded-md bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2">{submitting && <span className="h-4 w-4 animate-spin border-2 border-white/30 border-t-white rounded-full" />}Create</button>
    </div>
  </form>;
}
