import type { Metadata } from 'next'
import './globals.css'
import { AuthProvider } from './auth-context'

export const metadata: Metadata = {
  title: 'PAMS - Product Alert Management System',
  description: 'AI-driven Product Alert Management with Predictive Analytics',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
