'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { GlassCard } from '@/components/GlassCard'
import { NeonBadge } from '@/components/NeonBadge'
import { LoadingState } from '@/components/LoadingState'
import { apiClient } from '@/lib/api'
import dynamic from 'next/dynamic'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

export default function DashboardsPage() {
  const [loading, setLoading] = useState(true)
  const [health, setHealth] = useState<any>(null)
  const [profile, setProfile] = useState<any>(null)
  const [distributions, setDistributions] = useState<any>(null)
  const [forecast, setForecast] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)

  const fetchAll = async () => {
    setLoading(true)
    setError(null)
    try {
      let h: any = null
      try { h = await apiClient.getSystemStatus() } catch { h = { dataset_loaded: false } }
      setHealth(h)
      if (h?.dataset_loaded) {
        const [p, d, f] = await Promise.allSettled([
          apiClient.getProfile(),
          apiClient.getDistributions(),
          apiClient.getForecast(),
        ])
        if (p.status === 'fulfilled') setProfile(p.value)
        if (d.status === 'fulfilled') setDistributions(d.value)
        if (f.status === 'fulfilled') setForecast((f.value as any))
      }
    } catch {
      setHealth({ dataset_loaded: false })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchAll() }, [])

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    try {
      await apiClient.uploadDataset(file)
      await fetchAll()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  const loadPreset = async (name: string) => {
    setUploading(true)
    try {
      await fetch('/api/load-preset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
      })
      await fetchAll()
    } finally {
      setUploading(false)
    }
  }

  const commonLayout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'rgba(0,0,0,0.2)',
    font: { color: '#a5b4fc', size: 11 },
    margin: { t: 30, b: 40, l: 50, r: 20 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)', color: '#6366f1' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)', color: '#6366f1' },
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <StarField />
      <GlowingOrbs />
      <Sidebar />
      <Topbar />

      <main className="ml-64 mt-16 p-8 relative z-2">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div className="space-y-2">
              <NeonBadge variant="indigo">SMART DASHBOARDS</NeonBadge>
              <h1 className="text-4xl font-bold font-outfit">Live Dashboards</h1>
              <p className="text-muted-foreground">Real-time intelligence from your active dataset.</p>
            </div>
            <div className="flex gap-3 flex-wrap">
              <button onClick={() => loadPreset('Amazon Sales.csv')} disabled={uploading} className="px-4 py-2 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20 text-indigo-300 text-sm transition-all disabled:opacity-50">
                📦 Amazon Data
              </button>
              <button onClick={() => loadPreset('Insurance Claims.csv')} disabled={uploading} className="px-4 py-2 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-300 text-sm transition-all disabled:opacity-50">
                🛡️ Insurance Data
              </button>
              <button onClick={() => fileInputRef.current?.click()} disabled={uploading} className="px-4 py-2 rounded-lg bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-purple-300 text-sm font-medium transition-all disabled:opacity-50">
                {uploading ? '⏳ Loading...' : '⏏️ Upload Dataset'}
              </button>
              <input ref={fileInputRef} type="file" accept=".csv,.xlsx,.xls,.pdf" title="Upload Dataset" placeholder="Upload Dataset" className="hidden" onChange={handleUpload} />
              <button onClick={fetchAll} disabled={loading} className="px-4 py-2 rounded-lg glass hover:glass-hover border border-border/50 text-sm transition-all disabled:opacity-50">
                🔄 Refresh
              </button>
            </div>
          </div>

          {error && (
            <div className="p-4 rounded-lg glass border border-red-500/30 text-red-300 text-sm">🚨 {error}</div>
          )}

          {loading ? (
            <div className="py-24 flex justify-center"><LoadingState message="Loading live dataset intelligence..." /></div>
          ) : !health?.dataset_loaded ? (
            <GlassCard glow={true} className="border border-indigo-500/30 text-center py-20 space-y-6">
              <div className="text-6xl">📊</div>
              <h2 className="text-2xl font-bold font-outfit">No Dataset Loaded</h2>
              <p className="text-muted-foreground max-w-md mx-auto">Load a preset dataset or upload your own CSV/Excel file to generate live dashboard charts powered by real data.</p>
              <div className="flex gap-4 justify-center flex-wrap">
                <button onClick={() => loadPreset('Amazon Sales.csv')} className="px-6 py-3 rounded-lg bg-indigo-600/80 hover:bg-indigo-600 text-white font-medium transition-all shadow-glow">📦 Load Amazon Dataset</button>
                <button onClick={() => loadPreset('Insurance Claims.csv')} className="px-6 py-3 rounded-lg bg-emerald-600/80 hover:bg-emerald-600 text-white font-medium transition-all">🛡️ Load Insurance Dataset</button>
                <button onClick={() => fileInputRef.current?.click()} className="px-6 py-3 rounded-lg glass hover:glass-hover border border-border/50 font-medium transition-all">⏏️ Upload Custom CSV</button>
              </div>
            </GlassCard>
          ) : (
            <>
              {/* Summary Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Total Records', value: health?.rows?.toLocaleString() ?? '0', icon: '📊' },
                  { label: 'Dataset', value: health?.dataset_name ?? 'Loaded', icon: '📁' },
                  { label: 'Data Quality', value: `${profile?.data_quality_score?.score ?? '—'}/100`, icon: '✓' },
                  { label: 'Geo Points', value: Object.keys(health?.geo_detected ?? {}).length > 0 ? 'Detected' : 'None', icon: '🗺️' },
                ].map(({ label, value, icon }) => (
                  <GlassCard key={label} className="border border-white/5 text-center py-4">
                    <div className="text-2xl mb-1">{icon}</div>
                    <p className="text-xl font-bold font-outfit text-indigo-200">{value}</p>
                    <p className="text-xs text-muted-foreground mt-1">{label}</p>
                  </GlassCard>
                ))}
              </div>

              {/* Distribution Charts */}
              {distributions && Object.keys(distributions).length > 0 && (
                <div className="space-y-4">
                  <h2 className="text-2xl font-bold font-outfit">Distribution Analysis</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {Object.entries(distributions).slice(0, 4).map(([col, distData]: [string, any]) => (
                      <GlassCard key={col} className="border border-indigo-500/20 p-4" glow={true}>
                        <h3 className="text-sm font-semibold text-indigo-300 mb-3">{col}</h3>
                        {distData?.type === 'numeric' ? (
                          <Plot
                            data={[{
                              type: 'bar',
                              x: distData.bins,
                              y: distData.counts,
                              marker: { color: 'rgba(99,102,241,0.7)', line: { color: 'rgba(99,102,241,1)', width: 1 } },
                            }]}
                            layout={{ ...commonLayout, height: 220, title: '' }}
                            config={{ displayModeBar: false, responsive: true }}
                            style={{ width: '100%' }}
                          />
                        ) : (
                          <Plot
                            data={[{
                              type: 'bar',
                              x: distData?.labels ?? [],
                              y: distData?.values ?? [],
                              marker: { color: 'rgba(168,85,247,0.7)', line: { color: 'rgba(168,85,247,1)', width: 1 } },
                            }]}
                            layout={{ ...commonLayout, height: 220, title: '' }}
                            config={{ displayModeBar: false, responsive: true }}
                            style={{ width: '100%' }}
                          />
                        )}
                      </GlassCard>
                    ))}
                  </div>
                </div>
              )}

              {/* Forecast Chart */}
              {forecast?.fig_json && (
                <div className="space-y-4">
                  <h2 className="text-2xl font-bold font-outfit">Forecasting & Trend</h2>
                  <GlassCard glow={true} className="border border-purple-500/20 p-4">
                    <Plot
                      data={JSON.parse(forecast.fig_json).data}
                      layout={{ ...commonLayout, ...JSON.parse(forecast.fig_json).layout, height: 350 }}
                      config={{ displayModeBar: false, responsive: true }}
                      style={{ width: '100%' }}
                    />
                  </GlassCard>
                </div>
              )}

              {/* Missing Values */}
              {profile?.missing_values && (
                <GlassCard glow={true} className="border border-cyan-500/20">
                  <h3 className="text-lg font-bold font-outfit mb-4 text-cyan-100">Data Quality — Missing Values Matrix</h3>
                  <div className="space-y-2 max-h-48 overflow-y-auto">
                    {Object.entries(profile.missing_values).length === 0 ? (
                      <div className="text-center text-emerald-400 font-medium p-4">✨ Pristine Dataset — No missing values!</div>
                    ) : (
                      Object.entries(profile.missing_values).map(([col, count]: [string, any]) => (
                        <div key={col} className="flex justify-between items-center p-3 bg-black/30 rounded-lg border border-white/5">
                          <span className="font-mono text-sm text-indigo-300">{col}</span>
                          <span className="text-sm font-semibold text-rose-400">{count} missing</span>
                        </div>
                      ))
                    )}
                  </div>
                </GlassCard>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  )
}
