'use client'

import { useEffect, useState } from 'react'

interface AlertSummary {
  total_alerts: number
  open_alerts: number
  critical_alerts: number
  recent_24h: number
  by_category: Record<string, number>
}

interface Alert {
  id: number
  product_id: number
  severity: string
  category: string
  description: string
  status: string
  score: number
  confidence: number
  created_at: string
}

export default function Dashboard() {
  const [summary, setSummary] = useState<AlertSummary | null>(null)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      
      // Fetch summary
      const summaryRes = await fetch(`${apiUrl}/api/alerts/dashboard/summary`)
      const summaryData = await summaryRes.json()
      setSummary(summaryData)

      // Fetch recent alerts
      const alertsRes = await fetch(`${apiUrl}/api/alerts/?limit=10&sort_by=score`)
      const alertsData = await alertsRes.json()
      setAlerts(alertsData)

      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      setLoading(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    const colors: Record<string, string> = {
      critical: 'bg-danger-100 text-danger-800 border-danger-300',
      high: 'bg-warning-100 text-warning-800 border-warning-300',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      low: 'bg-primary-100 text-primary-800 border-primary-300',
    }
    return colors[severity] || 'bg-gray-100 text-gray-800 border-gray-300'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl text-gray-600">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-3xl font-bold text-gray-900">
            PAMS Dashboard
          </h1>
          <p className="text-gray-600 mt-1">
            Product Alert Management System - AI-Driven Insights
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-600 mb-2">
              Total Alerts
            </div>
            <div className="text-3xl font-bold text-gray-900">
              {summary?.total_alerts || 0}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-600 mb-2">
              Open Alerts
            </div>
            <div className="text-3xl font-bold text-primary-600">
              {summary?.open_alerts || 0}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-600 mb-2">
              Critical Alerts
            </div>
            <div className="text-3xl font-bold text-danger-600">
              {summary?.critical_alerts || 0}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-600 mb-2">
              Last 24 Hours
            </div>
            <div className="text-3xl font-bold text-accent-600">
              {summary?.recent_24h || 0}
            </div>
          </div>
        </div>

        {/* Alerts by Category */}
        {summary?.by_category && Object.keys(summary.by_category).length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Alerts by Category
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {Object.entries(summary.by_category).map(([category, count]) => (
                <div key={category} className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-gray-900">{count}</div>
                  <div className="text-sm text-gray-600 capitalize">{category}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recent Alerts Table */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">
              Recent High-Priority Alerts
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Severity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {alerts.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                      No alerts found
                    </td>
                  </tr>
                ) : (
                  alerts.map((alert) => (
                    <tr key={alert.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{alert.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${getSeverityColor(alert.severity)}`}>
                          {alert.severity.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">
                        {alert.category}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 max-w-md truncate">
                        {alert.description}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {(alert.score * 100).toFixed(0)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-3 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                          {alert.status}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <button className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg shadow transition">
            Create Alert
          </button>
          <button className="bg-success-600 hover:bg-success-700 text-white font-semibold py-3 px-6 rounded-lg shadow transition">
            Run Prediction
          </button>
          <button className="bg-accent-600 hover:bg-accent-700 text-white font-semibold py-3 px-6 rounded-lg shadow transition">
            View Analytics
          </button>
        </div>
      </main>
    </div>
  )
}
