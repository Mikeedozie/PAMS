'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { 
  Package, 
  TrendingUp, 
  TrendingDown,
  AlertTriangle, 
  CheckCircle2,
  BarChart3,
  Calendar,
  DollarSign,
  Truck,
  Archive,
  ArrowLeft,
  Edit,
  Trash2,
  Bell,
  Activity,
  ShoppingCart,
  Box,
  Clock
} from 'lucide-react';
import { useAuth } from '../../auth-context';

interface Product {
  id: number;
  sku: string;
  name: string;
  category: string;
  description?: string;
  price?: number;
  stock_level?: number;
  current_stock?: number;
  reorder_point?: number;
  supplier?: string;
  created_at?: string;
  status?: string;
}

interface Alert {
  id: number;
  product_id: number;
  severity: string;
  category: string;
  description: string;
  status: string;
  created_at: string;
}

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { token } = useAuth();
  const [product, setProduct] = useState<Product | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const productId = params.id as string;

  useEffect(() => {
    fetchProductDetails();
  }, [productId]);

  const fetchProductDetails = async () => {
    try {
      setLoading(true);
      
      // Fetch product details
      const productRes = await fetch(`${apiUrl}/api/products/${productId}`);
      if (!productRes.ok) {
        throw new Error('Product not found');
      }
      const productData = await productRes.json();
      
      // Fetch all alerts and filter by product_id
      const alertsRes = await fetch(`${apiUrl}/api/alerts/`);
      const allAlerts = await alertsRes.json();
      const productAlerts = allAlerts.filter((alert: Alert) => 
        alert.product_id === parseInt(productId)
      );
      
      setProduct(productData);
      setAlerts(productAlerts);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load product details');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      const res = await fetch(`${apiUrl}/api/products/${productId}`, {
        method: 'DELETE',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      
      if (res.ok) {
        router.push('/dashboard');
      } else {
        setError('Failed to delete product');
      }
    } catch (err) {
      setError('Error deleting product');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading product details...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-16 w-16 text-danger-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Product Not Found</h1>
          <p className="text-gray-600 mb-6">{error || 'The product you\'re looking for doesn\'t exist.'}</p>
          <Link 
            href="/dashboard"
            className="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-semibold transition-all"
          >
            <ArrowLeft className="h-5 w-5" />
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const stockLevel = product.stock_level || product.current_stock || 0;
  const reorderPoint = product.reorder_point || 10;
  const isLowStock = stockLevel <= reorderPoint;
  const stockPercentage = Math.min((stockLevel / (reorderPoint * 2)) * 100, 100);
  
  const criticalAlerts = alerts.filter(a => a.severity === 'critical' && a.status === 'open').length;
  const openAlerts = alerts.filter(a => a.status === 'open').length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link 
                href="/dashboard"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowLeft className="h-6 w-6" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{product.name}</h1>
                <p className="text-sm text-gray-500 font-mono">{product.sku}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button 
                onClick={() => router.push(`/products/${productId}/edit`)}
                className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-all"
              >
                <Edit className="h-4 w-4" />
                Edit
              </button>
              <button 
                onClick={() => setShowDeleteModal(true)}
                className="flex items-center gap-2 px-4 py-2 bg-danger-600 hover:bg-danger-700 text-white rounded-lg transition-all"
              >
                <Trash2 className="h-4 w-4" />
                Delete
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alert Banner */}
        {isLowStock && (
          <div className="mb-6 bg-danger-50 border-l-4 border-danger-500 p-4 rounded-r-lg">
            <div className="flex items-center">
              <AlertTriangle className="h-5 w-5 text-danger-600 mr-3" />
              <div>
                <p className="font-semibold text-danger-900">Low Stock Alert</p>
                <p className="text-sm text-danger-700">
                  Current stock ({stockLevel} units) is at or below the reorder point ({reorderPoint} units)
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Stock Status */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-primary-100 rounded-lg">
                <Archive className="h-6 w-6 text-primary-600" />
              </div>
              {isLowStock ? (
                <TrendingDown className="h-5 w-5 text-danger-500" />
              ) : (
                <TrendingUp className="h-5 w-5 text-success-500" />
              )}
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stockLevel}</div>
            <div className="text-sm text-gray-600">Units in Stock</div>
            <div className="mt-4 bg-gray-200 rounded-full h-2 overflow-hidden">
              <div 
                className={`h-full transition-all ${isLowStock ? 'bg-danger-500' : 'bg-success-500'}`}
                style={{ width: `${stockPercentage}%` }}
              />
            </div>
          </div>

          {/* Price */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-success-100 rounded-lg">
                <DollarSign className="h-6 w-6 text-success-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              ${product.price?.toFixed(2) || '0.00'}
            </div>
            <div className="text-sm text-gray-600">Unit Price</div>
          </div>

          {/* Active Alerts */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg ${criticalAlerts > 0 ? 'bg-danger-100' : 'bg-warning-100'}`}>
                <Bell className={`h-6 w-6 ${criticalAlerts > 0 ? 'text-danger-600' : 'text-warning-600'}`} />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{openAlerts}</div>
            <div className="text-sm text-gray-600">Open Alerts</div>
            {criticalAlerts > 0 && (
              <div className="mt-2 text-xs text-danger-600 font-semibold">
                {criticalAlerts} Critical
              </div>
            )}
          </div>

          {/* Reorder Point */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-accent-100 rounded-lg">
                <Activity className="h-6 w-6 text-accent-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{reorderPoint}</div>
            <div className="text-sm text-gray-600">Reorder Point</div>
          </div>
        </div>

        {/* Main Details Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Product Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Package className="h-5 w-5 text-primary-600" />
                Product Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Product Name</label>
                  <p className="text-lg text-gray-900 mt-1">{product.name}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">SKU</label>
                  <p className="text-lg text-gray-900 mt-1 font-mono">{product.sku}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Category</label>
                  <p className="text-lg text-gray-900 mt-1 capitalize">{product.category}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Status</label>
                  <div className="mt-1">
                    {isLowStock ? (
                      <span className="inline-flex items-center gap-1 px-3 py-1 bg-danger-100 text-danger-700 rounded-full text-sm font-semibold">
                        <AlertTriangle className="h-4 w-4" />
                        Low Stock
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-3 py-1 bg-success-100 text-success-700 rounded-full text-sm font-semibold">
                        <CheckCircle2 className="h-4 w-4" />
                        In Stock
                      </span>
                    )}
                  </div>
                </div>
                {product.supplier && (
                  <div>
                    <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Supplier</label>
                    <p className="text-lg text-gray-900 mt-1 flex items-center gap-2">
                      <Truck className="h-5 w-5 text-gray-400" />
                      {product.supplier}
                    </p>
                  </div>
                )}
                {product.created_at && (
                  <div>
                    <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Created</label>
                    <p className="text-lg text-gray-900 mt-1 flex items-center gap-2">
                      <Calendar className="h-5 w-5 text-gray-400" />
                      {new Date(product.created_at).toLocaleDateString()}
                    </p>
                  </div>
                )}
              </div>
              {product.description && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Description</label>
                  <p className="text-gray-700 mt-2 leading-relaxed">{product.description}</p>
                </div>
              )}
            </div>

            {/* Inventory Metrics */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-primary-600" />
                Inventory Metrics
              </h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Box className="h-5 w-5 text-primary-600" />
                    <span className="font-medium text-gray-900">Current Stock</span>
                  </div>
                  <span className="text-2xl font-bold text-gray-900">{stockLevel}</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Activity className="h-5 w-5 text-accent-600" />
                    <span className="font-medium text-gray-900">Reorder Point</span>
                  </div>
                  <span className="text-2xl font-bold text-gray-900">{reorderPoint}</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <ShoppingCart className="h-5 w-5 text-success-600" />
                    <span className="font-medium text-gray-900">Available to Order</span>
                  </div>
                  <span className="text-2xl font-bold text-success-600">{Math.max(stockLevel - reorderPoint, 0)}</span>
                </div>
                {product.price && (
                  <div className="flex items-center justify-between p-4 bg-primary-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <DollarSign className="h-5 w-5 text-primary-600" />
                      <span className="font-medium text-gray-900">Total Inventory Value</span>
                    </div>
                    <span className="text-2xl font-bold text-primary-600">
                      ${(product.price * stockLevel).toFixed(2)}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Recent Alerts */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Bell className="h-5 w-5 text-primary-600" />
                Related Alerts
                {alerts.length > 0 && (
                  <span className="ml-2 px-2 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">
                    {alerts.length}
                  </span>
                )}
              </h2>
              {alerts.length === 0 ? (
                <div className="text-center py-8">
                  <CheckCircle2 className="h-12 w-12 text-success-500 mx-auto mb-3" />
                  <p className="text-gray-600">No alerts for this product</p>
                  <p className="text-sm text-gray-500 mt-1">Everything is running smoothly!</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {alerts.slice(0, 5).map((alert) => (
                    <div 
                      key={alert.id}
                      className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-1 text-xs font-semibold rounded ${
                            alert.severity === 'critical' ? 'bg-danger-100 text-danger-700' :
                            alert.severity === 'high' ? 'bg-warning-100 text-warning-700' :
                            alert.severity === 'medium' ? 'bg-primary-100 text-primary-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {alert.severity.toUpperCase()}
                          </span>
                          <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded capitalize">
                            {alert.category}
                          </span>
                        </div>
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          alert.status === 'open' ? 'bg-danger-50 text-danger-700' :
                          alert.status === 'in_progress' ? 'bg-warning-50 text-warning-700' :
                          'bg-success-50 text-success-700'
                        }`}>
                          {alert.status.replace('_', ' ').toUpperCase()}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-2">{alert.description}</p>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <Clock className="h-3 w-3" />
                        {new Date(alert.created_at).toLocaleString()}
                      </div>
                    </div>
                  ))}
                  {alerts.length > 5 && (
                    <button className="w-full py-2 text-primary-600 hover:text-primary-700 font-medium text-sm">
                      View all {alerts.length} alerts →
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar - Quick Actions */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-accent-600 hover:bg-accent-700 text-white rounded-lg transition-all font-semibold">
                  <Bell className="h-5 w-5" />
                  Create Alert
                </button>
                <button className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-all font-semibold">
                  <ShoppingCart className="h-5 w-5" />
                  Reorder Stock
                </button>
                <button className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-all font-semibold">
                  <BarChart3 className="h-5 w-5" />
                  View Analytics
                </button>
              </div>
            </div>

            {/* Stock Status Card */}
            <div className={`rounded-xl shadow-sm border-2 p-6 ${
              isLowStock ? 'bg-danger-50 border-danger-200' : 'bg-success-50 border-success-200'
            }`}>
              <div className="flex items-center justify-center mb-4">
                {isLowStock ? (
                  <AlertTriangle className="h-12 w-12 text-danger-600" />
                ) : (
                  <CheckCircle2 className="h-12 w-12 text-success-600" />
                )}
              </div>
              <h3 className={`text-lg font-bold text-center mb-2 ${
                isLowStock ? 'text-danger-900' : 'text-success-900'
              }`}>
                {isLowStock ? 'Action Required' : 'Stock Healthy'}
              </h3>
              <p className={`text-sm text-center ${
                isLowStock ? 'text-danger-700' : 'text-success-700'
              }`}>
                {isLowStock 
                  ? `Stock level is ${stockLevel - reorderPoint} units below the reorder point. Consider restocking soon.`
                  : `Stock level is healthy with ${stockLevel - reorderPoint} units above the reorder point.`
                }
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
            <div className="text-center mb-6">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-danger-100 mb-4">
                <AlertTriangle className="h-6 w-6 text-danger-600" />
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Delete Product</h3>
              <p className="text-gray-600">
                Are you sure you want to delete <strong>{product.name}</strong>? This action cannot be undone.
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-semibold transition-all"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 px-4 py-2 bg-danger-600 hover:bg-danger-700 text-white rounded-lg font-semibold transition-all"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
