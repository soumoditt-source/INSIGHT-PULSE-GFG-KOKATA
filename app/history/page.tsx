'use client'

import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { GlassCard } from '@/components/GlassCard'
import { NeonBadge } from '@/components/NeonBadge'
import { MetricCard } from '@/components/MetricCard'

export default function HistoryPage() {
  const queries = [
    {
      id: 1,
      query: 'Select top 10 products by sales',
      type: 'Query',
      status: 'Success',
      time: '1.2s',
      timestamp: '2024-03-18 14:32:45',
      rows: '10',
    },
    {
      id: 2,
      query: 'Analyze regional distribution trends',
      type: 'Analysis',
      status: 'Success',
      time: '3.4s',
      timestamp: '2024-03-18 14:28:12',
      rows: '1,247',
    },
    {
      id: 3,
      query: 'Generate sales forecast for Q2',
      type: 'Forecast',
      status: 'Success',
      time: '8.7s',
      timestamp: '2024-03-18 14:15:33',
      rows: '92',
    },
    {
      id: 4,
      query: 'Detect anomalies in transaction data',
      type: 'Anomaly Detection',
      status: 'Success',
      time: '5.2s',
      timestamp: '2024-03-18 13:42:00',
      rows: '47',
    },
    {
      id: 5,
      query: 'Compare customer segments',
      type: 'Analysis',
      status: 'Failed',
      time: '2.1s',
      timestamp: '2024-03-18 13:28:19',
      rows: '0',
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
              <div className="w-2 h-2 rounded-full bg-magenta-500 animate-pulse" />
              <NeonBadge variant="magenta">QUERY AUDIT</NeonBadge>
            </div>
            <h1 className="text-4xl font-bold font-outfit">Query History</h1>
            <p className="text-muted-foreground">Track and manage all queries and analyses</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <MetricCard label="Total Queries" value="1,247" trend={{ value: 128, direction: 'up' }} icon="📝" />
            <MetricCard label="Success Rate" value="99.2" unit="%" trend={{ value: 0.8, direction: 'up' }} icon="✓" />
            <MetricCard label="Avg Duration" value="2.8" unit="s" trend={{ value: 5, direction: 'down' }} icon="⏱️" />
            <MetricCard label="Peak Queries" value="485" unit="/min" trend={{ value: 15, direction: 'up' }} icon="📊" />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-3">
            {['All', 'Query', 'Analysis', 'Forecast', 'Success', 'Failed'].map((filter) => (
              <button
                key={filter}
                className="px-4 py-2 rounded-full glass hover:glass-hover border border-border/50 text-sm transition-all duration-200"
              >
                {filter}
              </button>
            ))}
          </div>

          {/* Query Table */}
          <GlassCard glow={true}>
            <h3 className="text-lg font-bold font-outfit mb-4">Recent Queries</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border/30">
                    <th className="text-left py-3 px-4 text-muted-foreground font-medium">Query</th>
                    <th className="text-left py-3 px-4 text-muted-foreground font-medium">Type</th>
                    <th className="text-left py-3 px-4 text-muted-foreground font-medium">Time</th>
                    <th className="text-left py-3 px-4 text-muted-foreground font-medium">Rows</th>
                    <th className="text-left py-3 px-4 text-muted-foreground font-medium">Status</th>
                    <th className="text-left py-3 px-4 text-muted-foreground font-medium">Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  {queries.map((q) => (
                    <tr
                      key={q.id}
                      className="border-b border-border/20 hover:bg-slate-800/20 transition-colors cursor-pointer"
                    >
                      <td className="py-3 px-4 max-w-xs truncate">{q.query}</td>
                      <td className="py-3 px-4">
                        <NeonBadge variant="indigo" className="text-xs">
                          {q.type}
                        </NeonBadge>
                      </td>
                      <td className="py-3 px-4 text-purple-400 font-semibold">{q.time}</td>
                      <td className="py-3 px-4 text-cyan-400">{q.rows}</td>
                      <td className="py-3 px-4">
                        <span
                          className={`text-xs px-2 py-1 rounded-full ${
                            q.status === 'Success'
                              ? 'bg-emerald-500/20 text-emerald-200'
                              : 'bg-red-500/20 text-red-200'
                          }`}
                        >
                          {q.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-muted-foreground text-xs">{q.timestamp}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>

          {/* Pagination */}
          <div className="flex justify-between items-center">
            <p className="text-sm text-muted-foreground">Showing 1-5 of 1,247 queries</p>
            <div className="flex gap-2">
              <button className="px-4 py-2 rounded-lg glass hover:glass-hover border border-border/50 transition-all">
                Previous
              </button>
              <button className="px-4 py-2 rounded-lg glass-hover border border-indigo-500/50">1</button>
              <button className="px-4 py-2 rounded-lg glass hover:glass-hover border border-border/50">2</button>
              <button className="px-4 py-2 rounded-lg glass hover:glass-hover border border-border/50">3</button>
              <button className="px-4 py-2 rounded-lg glass hover:glass-hover border border-border/50 transition-all">
                Next
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
