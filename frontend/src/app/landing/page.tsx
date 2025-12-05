'use client';

import Link from 'next/link';
import { 
  AlertTriangle, 
  BarChart3, 
  Shield, 
  Zap, 
  TrendingUp, 
  Bell,
  Users,
  CheckCircle2,
  ArrowRight,
  Menu,
  LogOut,
  UserCircle2,
  Loader2
} from 'lucide-react';
import { useAuth } from '../auth-context';
import { useState } from 'react';

export default function LandingPage() {
  const { user, logout, loading, tokenAgeSeconds } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const age = tokenAgeSeconds?.();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-primary-900 to-slate-900">
      {/* Navigation */}
      <nav className="bg-black/20 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Shield className="h-8 w-8 text-primary-400" />
              <span className="text-2xl font-bold text-white">PAMS</span>
            </div>
            <div className="flex items-center space-x-4 relative">
              {!loading && !user && (
                <>
                  <Link 
                    href="/auth/login" 
                    className="text-gray-300 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-white/10"
                  >
                    Login
                  </Link>
                  <Link 
                    href="/auth/register" 
                    className="bg-accent-600 hover:bg-accent-700 text-white px-5 py-2 rounded-lg font-semibold transition-all"
                  >
                    Sign Up
                  </Link>
                </>
              )}
              {loading && (
                <div className="flex items-center text-primary-200 text-sm">
                  <Loader2 className="h-4 w-4 mr-2 animate-spin"/>Loading...
                </div>
              )}
              {user && (
                <>
                  <Link 
                    href="/dashboard" 
                    className="text-gray-300 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-white/10"
                  >Dashboard</Link>
                  <Link 
                    href="/admin" 
                    className="text-gray-300 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-white/10"
                  >Admin</Link>
                  <button
                    onClick={() => setMenuOpen(o => !o)}
                    className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 px-3 py-2 rounded-lg border border-white/10 text-sm text-white"
                  >
                    <UserCircle2 className="h-5 w-5" />
                    <span className="hidden sm:inline">{user.username}</span>
                    {age !== undefined && (
                      <span className="text-[10px] ml-2 px-2 py-0.5 rounded bg-accent-600/60">
                        {age < 60 ? `${age}s` : `${Math.floor(age/60)}m`}
                      </span>
                    )}
                  </button>
                  {menuOpen && (
                    <div className="absolute right-0 top-14 w-56 bg-slate-900/95 border border-white/10 rounded-lg shadow-xl p-2 backdrop-blur-md">
                      <div className="px-3 py-2 text-xs uppercase tracking-wide text-primary-300/70">Session</div>
                      <div className="px-3 py-2 text-sm text-primary-100 flex items-center justify-between">
                        <span>Token Age</span>
                        <span className="font-mono text-primary-300">{age ? `${age}s` : '—'}</span>
                      </div>
                      <button
                        onClick={logout}
                        className="w-full flex items-center gap-2 text-left px-3 py-2 text-sm text-red-300 hover:bg-red-500/10 rounded-md"
                      >
                        <LogOut className="h-4 w-4" /> Logout
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 leading-tight">
              AI-Powered Product
              <br />
              <span className="bg-gradient-to-r from-primary-400 to-accent-600 bg-clip-text text-transparent">
                Alert Management
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-3xl mx-auto">
              Transform reactive alerts into predictive intelligence. Stop problems before they start 
              with advanced ML-powered monitoring and analytics.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link 
                href="/dashboard" 
                className="bg-accent-600 hover:bg-accent-700 text-white px-8 py-4 rounded-lg font-bold text-lg transition-all transform hover:scale-105 flex items-center gap-2 shadow-lg shadow-accent-500/50"
              >
                Get Started
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link 
                href="/admin" 
                className="bg-white/10 hover:bg-white/20 text-white px-8 py-4 rounded-lg font-bold text-lg transition-all backdrop-blur-sm border border-white/20"
              >
                Admin Console
              </Link>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-20 grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              { label: 'Alerts Processed', value: '10K+', icon: Bell },
              { label: 'Prediction Accuracy', value: '94%', icon: TrendingUp },
              { label: 'Response Time', value: '< 2min', icon: Zap },
              { label: 'Active Users', value: '500+', icon: Users }
            ].map((stat, idx) => (
              <div key={idx} className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-all">
                <stat.icon className="h-8 w-8 text-primary-400 mb-3" />
                <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-gray-300 text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-black/30 backdrop-blur-sm py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Powerful Features</h2>
            <p className="text-xl text-gray-300">Everything you need to manage alerts intelligently</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: BarChart3,
                title: 'Predictive Analytics',
                description: 'ML-powered forecasting predicts stockouts and demand surges before they happen',
                color: 'from-primary-500 to-primary-600'
              },
              {
                icon: AlertTriangle,
                title: 'Smart Alerts',
                description: 'Intelligent alert scoring and deduplication reduces noise by 80%',
                color: 'from-accent-500 to-accent-600'
              },
              {
                icon: TrendingUp,
                title: 'Real-time Monitoring',
                description: 'Live dashboards with instant insights into product health and performance',
                color: 'from-warning-500 to-warning-600'
              },
              {
                icon: Shield,
                title: 'Quality Assurance',
                description: 'Anomaly detection identifies defects and quality issues automatically',
                color: 'from-success-500 to-success-600'
              },
              {
                icon: Zap,
                title: 'Instant Response',
                description: 'Automated workflows trigger actions based on alert severity and patterns',
                color: 'from-accent-400 to-accent-600'
              },
              {
                icon: CheckCircle2,
                title: 'Easy to Use',
                description: 'Intuitive interface designed for non-technical users - no coding required',
                color: 'from-primary-500 to-accent-500'
              }
            ].map((feature, idx) => (
              <div key={idx} className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:bg-white/10 transition-all group">
                <div className={`bg-gradient-to-r ${feature.color} w-16 h-16 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                  <feature.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-gray-300 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">How It Works</h2>
            <p className="text-xl text-gray-300">Simple, powerful, and intelligent</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { step: '1', title: 'Connect Data', description: 'Integrate with your existing systems and data sources' },
              { step: '2', title: 'AI Learns', description: 'Machine learning analyzes patterns and builds predictions' },
              { step: '3', title: 'Get Alerts', description: 'Receive intelligent, prioritized alerts in real-time' },
              { step: '4', title: 'Take Action', description: 'Respond quickly with automated workflows and insights' }
            ].map((item, idx) => (
              <div key={idx} className="relative">
                <div className="bg-gradient-to-br from-accent-600 to-accent-700 w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold text-white mb-4 mx-auto shadow-lg shadow-accent-500/50">
                  {item.step}
                </div>
                <h3 className="text-xl font-bold text-white mb-2 text-center">{item.title}</h3>
                <p className="text-gray-300 text-center">{item.description}</p>
                {idx < 3 && (
                  <div className="hidden md:block absolute top-8 left-1/2 w-full h-0.5 bg-gradient-to-r from-primary-500 to-transparent"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-accent-600 to-accent-700 py-20">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Your Alert Management?
          </h2>
          <p className="text-xl text-accent-100 mb-10">
            Join hundreds of teams using PAMS to predict problems before they happen
          </p>
          <Link 
            href="/dashboard" 
            className="bg-white text-accent-600 hover:bg-gray-100 px-10 py-4 rounded-lg font-bold text-lg transition-all transform hover:scale-105 inline-flex items-center gap-2 shadow-xl"
          >
            Start Your Dashboard
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-black/40 backdrop-blur-sm border-t border-white/10 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Shield className="h-6 w-6 text-primary-400" />
              <span className="text-xl font-bold text-white">PAMS</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2025 Product Alert Management System. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
