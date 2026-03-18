'use client'

import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { BentoGrid, BentoGridItem } from '@/components/BentoGrid'
import { GlassCard } from '@/components/GlassCard'
import { NeonBadge } from '@/components/NeonBadge'
import { ChartPlaceholder } from '@/components/ChartPlaceholder'

export default function DashboardsPage() {
  const dashboards = [
    {
      id: 1,
      name: 'Sales Overview',
      description: '4 charts • Updated 2min ago',
      icon: '📊',
      charts: 4,
      lastUpdate: '2 min',
    },
    {
      id: 2,
      name: 'Customer Analytics',
      description: '6 charts • Updated 15min ago',
      icon: '👥',
      charts: 6,
      lastUpdate: '15 min',
    },
    {
      id: 3,
      name: 'Performance Metrics',
      description: '3 charts • Updated just now',
      icon: '⚡',
      charts: 3,
      lastUpdate: 'now',
    },
    {
      id: 4,
      name: 'Geographic Distribution',
      description: '5 charts • Updated 8min ago',
      icon: '🗺️',
      charts: 5,
      lastUpdate: '8 min',
    },
  ]

  return (
    <div className="min-h-screen bg-background text-foreground">
      <StarField />
      <GlowingOrbs />
      <Sidebar />
      <Topbar />

      <main className="ml-64 mt-16 p-8 relative z-2">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
              <NeonBadge variant="indigo">SMART DASHBOARDS</NeonBadge>
            </div>
            <h1 className="text-4xl font-bold font-outfit">Dashboards</h1>
            <p className="text-muted-foreground">Create and manage custom intelligence boards</p>
          </div>

          <div className="flex gap-3">
            <button className="px-6 py-3 rounded-lg bg-indigo-600/80 hover:bg-indigo-600 text-white font-medium transition-all duration-300 shadow-glow">
              Create Dashboard
            </button>
            <button className="px-6 py-3 rounded-lg glass hover:glass-hover border border-border/50 font-medium transition-all duration-300">
              Import Template
            </button>
          </div>

          {/* Dashboard Grid */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold font-outfit">Your Dashboards</h2>
            <BentoGrid>
              {dashboards.map((dashboard, i) => (
                <BentoGridItem
                  key={dashboard.id}
                  index={i}
                  title={dashboard.name}
                  description={dashboard.description}
                  icon={dashboard.icon}
                  onClick={() => console.log(`Opening ${dashboard.name}`)}
                >
                  <div className="mt-4 text-xs text-muted-foreground space-y-2">
                    <div>
                      <p className="text-muted-foreground">Charts: <span className="text-cyan-400">{dashboard.charts}</span></p>
                    </div>
                    <div className="flex justify-between items-center pt-2 border-t border-border/30">
                      <span>Last Updated</span>
                      <span className="text-indigo-400">{dashboard.lastUpdate}</span>
                    </div>
                  </div>
                </BentoGridItem>
              ))}
            </BentoGrid>
          </div>

          {/* Featured Dashboard */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold font-outfit">Sales Overview Dashboard</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 auto-rows-[300px]">
              <div className="animate-slide-up">
                <ChartPlaceholder title="Monthly Sales" type="line" />
              </div>
              <div className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
                <ChartPlaceholder title="Sales by Category" type="bar" />
              </div>
              <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
                <ChartPlaceholder title="Top Performers" type="bar" />
              </div>
              <div className="animate-slide-up" style={{ animationDelay: '0.3s' }}>
                <ChartPlaceholder title="Revenue Trend" type="line" />
              </div>
            </div>
          </div>

          {/* Dashboard Settings */}
          <GlassCard glow={true}>
            <h3 className="text-lg font-bold font-outfit mb-4">Dashboard Settings</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-4 border-b border-border/30">
                <div>
                  <p className="font-medium">Auto-refresh</p>
                  <p className="text-xs text-muted-foreground">Update every 5 minutes</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" value="" className="sr-only peer" defaultChecked />
                  <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-500/30 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600" />
                </label>
              </div>

              <div className="flex items-center justify-between pb-4 border-b border-border/30">
                <div>
                  <p className="font-medium">Share Dashboard</p>
                  <p className="text-xs text-muted-foreground">Allow others to view</p>
                </div>
                <button className="px-4 py-2 rounded-lg glass hover:glass-hover border border-border/50 text-sm">
                  Configure
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Export Data</p>
                  <p className="text-xs text-muted-foreground">Download as CSV or PDF</p>
                </div>
                <button className="px-4 py-2 rounded-lg glass hover:glass-hover border border-border/50 text-sm">
                  Export
                </button>
              </div>
            </div>
          </GlassCard>
        </div>
      </main>
    </div>
  )
}
