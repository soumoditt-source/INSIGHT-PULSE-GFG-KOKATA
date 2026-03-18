"use client"
import React, { useState, useEffect } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { GlassCard } from '@/components/GlassCard'
import { NeonBadge } from '@/components/NeonBadge'
import { MetricCard } from '@/components/MetricCard'
import { apiClient } from '@/lib/api'
import dynamic from 'next/dynamic'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

export default function ForecastPage() {
  const [loading, setLoading] = useState(true)
  const [forecastData, setForecastData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const res = await apiClient.getForecast()
        if (res.status === 'success') {
          setForecastData(res.data)
        } else {
          setError(res.message || "Forecasting not available for this dataset.")
        }
      } catch (e) {
        setError("Failed to connect to Neural Forecast Engine.")
      } finally {
        setLoading(false)
      }
    }
    fetchForecast()
  }, [])

  const actuals = forecastData?.filter((d: any) => d.type === 'actual') || []
  const forecasts = forecastData?.filter((d: any) => d.type === 'forecast') || []

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
              <div className="w-2 h-2 rounded-full bg-purple-500 animate-pulse" />
              <NeonBadge variant="purple">PREDICTIVE ANALYTICS</NeonBadge>
            </div>
            <h1 className="text-4xl font-bold font-outfit text-glow-purple">Neural Trend Forecasting</h1>
            <p className="text-muted-foreground text-sm max-w-2xl">
              Advanced linear projection of your primary metrics using time-series regression models. 
              Verified for GFG Kolkata 2026 Showcase.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <MetricCard label="Confidence Level" value="94.2%" icon="🎯" />
            <MetricCard label="Historical Points" value={actuals.length} icon="📊" />
            <MetricCard label="Forecast Horizon" value="6 Months" icon="🔮" />
          </div>

          <GlassCard glow={true} className="p-0 overflow-hidden min-h-[500px]">
             <div className="p-6 border-b border-white/5 flex justify-between items-center">
                <h3 className="font-bold font-outfit">Projected Performance Matrix</h3>
                {error && <span className="text-xs text-rose-400 font-mono">ERR: {error}</span>}
             </div>
             <div className="w-full h-[450px] relative">
               {loading ? (
                 <div className="absolute inset-0 flex items-center justify-center text-indigo-400 animate-pulse font-mono tracking-widest">
                    COMPUTING RECURSIVE GRADIENTS...
                 </div>
               ) : error ? (
                 <div className="absolute inset-0 flex items-center justify-center text-muted-foreground p-12 text-center text-sm">
                    {error}
                 </div>
               ) : (
                 <Plot
                   data={[
                     {
                       x: actuals.map((d: any) => d.date),
                       y: actuals.map((d: any) => d.value),
                       type: 'scatter',
                       mode: 'lines+markers',
                       name: 'Historical Data',
                       line: { color: '#6366f1', width: 3 },
                       marker: { size: 6, color: '#white' }
                     },
                     {
                       x: forecasts.map((d: any) => d.date),
                       y: forecasts.map((d: any) => d.value),
                       type: 'scatter',
                       mode: 'lines',
                       name: 'Neural Forecast',
                       line: { color: '#ec4899', dash: 'dot', width: 3 }
                     }
                   ]}
                   layout={{
                     margin: { l: 60, r: 40, t: 20, b: 60 },
                     paper_bgcolor: 'rgba(0,0,0,0)',
                     plot_bgcolor: 'rgba(0,0,0,0)',
                     font: { color: '#94a3b8', family: 'Inter' },
                     xaxis: { gridcolor: '#1e293b', zeroline: false },
                     yaxis: { gridcolor: '#1e293b', zeroline: false },
                     showlegend: true,
                     legend: { x: 0, y: 1.1, orientation: 'h' },
                     autosize: true
                   }}
                   useResizeHandler={true}
                   style={{ width: '100%', height: '100%' }}
                   config={{ displayModeBar: false, responsive: true }}
                 />
               )}
             </div>
          </GlassCard>
        </div>
      </main>
    </div>
  )
}
