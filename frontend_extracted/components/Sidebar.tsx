'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { DatasetUploader } from './DatasetUploader'

export function Sidebar() {
  const pathname = usePathname()
  const [isOpen, setIsOpen] = useState(true)

  const navItems = [
    { href: '/', label: 'Home', icon: '🏠' },
    { href: '/chat', label: 'Data Chat', icon: '💬' },
    { label: 'Forecast', icon: '🔮', href: '/forecast' },
    { label: 'Presentation', icon: '🎭', href: '/presentation' },
    { label: 'Settings', icon: '⚙️', href: '/settings' },
    { href: '/ml-lab', label: 'ML Lab', icon: '⚗️' },
    { href: '/profiler', label: 'Data Profiler', icon: '📊' },
    { href: '/maps', label: 'Map View', icon: '🗺️' },
    { href: '/history', label: 'Query History', icon: '⏱️' },
    { href: '/dashboards', label: 'Dashboards', icon: '📈' },
  ]

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-40 md:hidden glass p-2 rounded-lg hover:glass-hover"
      >
        ☰
      </button>

      <aside
        className={cn(
          'fixed left-0 top-0 h-screen w-64 glass border-r border-border/50 p-6 flex flex-col gap-8',
          'transition-all duration-300 z-30',
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        )}
      >
        <div className="flex items-center justify-center gap-2 font-outfit font-bold text-xl">
          <span className="text-2xl">◆</span>
          <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            InsightPulse
          </span>
        </div>

        <nav className="flex-1 space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200',
                  isActive
                    ? 'glass-hover border-indigo-500/50 text-indigo-200'
                    : 'text-muted-foreground hover:text-foreground'
                )}
                onClick={() => setIsOpen(false)}
              >
                <span className="text-lg">{item.icon}</span>
                <span className="text-sm font-medium">{item.label}</span>
              </Link>
            )
          })}
        </nav>

        <DatasetUploader />

        <div className="glass rounded-lg p-4 text-xs text-muted-foreground border border-border/30">
          <p className="font-semibold mb-2">v5.0.0 Ultimate</p>
          <p>Next-gen intelligence platform powered by AI</p>
        </div>
      </aside>

      {isOpen && (
        <div
          className="fixed inset-0 md:hidden z-20 bg-black/50"
          onClick={() => setIsOpen(false)}
        />
      )}

      <div className="hidden md:block fixed left-0 top-0 h-screen w-64" />
    </>
  )
}
