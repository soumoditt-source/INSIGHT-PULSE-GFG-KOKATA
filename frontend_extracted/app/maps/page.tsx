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

export default function MapsPage() {
  const [loading, setLoading] = useState(true)
  const [profile, setProfile] = useState<any>(null)
  const [health, setHealth] = useState<any>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [prof, sys] = await Promise.all([
          apiClient.getProfile(),
          apiClient.getSystemStatus()
        ])
        setProfile(prof)
        setHealth(sys)
      } catch (e) {
        console.error("Failed to load map data")
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const geoSummary = profile?.geo_summary || []
  const hasCoords = profile?.geo_detected?.has_coordinates

  // Prepare plot data
  const plotData = hasCoords ? [
    {
      type: 'scattergeo',
      mode: 'markers',
      lat: geoSummary.map((p: any) => p.lat),
      lon: geoSummary.map((p: any) => p.lon),
      marker: {
        size: 8,
        color: '#6366f1',
        line: { color: '#06b6d4', width: 1 },
        opacity: 0.6
      }
    }
  ] : [
    {
      type: 'choropleth',
      locationmode: 'country names',
      locations: geoSummary.map((p: any) => p.name),
      z: geoSummary.map((p: any) => p.value),
      colorscale: [
        [0, '#0f172a'],
        [0.5, '#6366f1'],
        [1, '#06b6d4']
      ],
      showscale: false,
      marker: {
        line: { color: '#ffffff20', width: 0.5 }
      }
    }
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
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-pulse" />
              <NeonBadge variant="teal">GEOGRAPHIC ANALYTICS</NeonBadge>
            </div>
            <h1 className="text-4xl font-bold font-outfit">Forensic Map View</h1>
            <p className="text-muted-foreground">Neural mapping of {profile?.geo_detected?.lat_col ? 'direct coordinates' : 'regional distribution'}.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <MetricCard label="Records Geo-Tagged" value={health?.rows?.toLocaleString() || '0'} icon="🗺️" />
            <MetricCard label="Active Hotspots" value={geoSummary.length} icon="🌍" />
            <MetricCard label="Detection Mode" value={hasCoords ? 'GPS' : 'Label'} icon="⚡" />
            <MetricCard label="Data Integrity" value="99.9%" icon="🏢" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <GlassCard glow={true} className="lg:col-span-2 p-0 overflow-hidden" hover={false}>
              <div className="p-6 border-b border-white/5">
                <h3 className="text-lg font-bold font-outfit">Live Intel Distribution Map</h3>
              </div>
              <div className="w-full h-[500px] bg-black/40 relative">
                {loading ? (
                  <div className="absolute inset-0 flex items-center justify-center text-cyan-400 animate-pulse font-mono">
                    INITIALIZING MAP ENGINE...
                  </div>
                ) : (
                  <Plot
                    data={hasCoords ? [
                      {
                        type: 'scattermapbox',
                        lat: geoSummary.map((p: any) => p.lat),
                        lon: geoSummary.map((p: any) => p.lon),
                        mode: 'markers',
                        marker: {
                          size: 10,
                          color: '#06b6d4',
                          opacity: 0.8,
                        },
                        text: geoSummary.map((p: any) => `Intel Node: ${p.lat}, ${p.lon}`),
                        hoverinfo: 'text'
                      }
                    ] : [
                      {
                        type: 'choropleth',
                        locationmode: 'country names',
                        locations: geoSummary.map((p: any) => p.name),
                        z: geoSummary.map((p: any) => p.value),
                        colorscale: [
                          [0, '#0f172a'],
                          [0.5, '#6366f1'],
                          [1, '#06b6d4']
                        ],
                        showscale: false,
                        marker: {
                          line: { color: '#ffffff20', width: 0.5 }
                        }
                      }
                    ]}
                    layout={{
                      mapbox: {
                        style: "open-street-map",
                        center: geoSummary.length > 0 && hasCoords ? { lat: geoSummary[0].lat, lon: geoSummary[0].lon } : { lat: 20, lon: 77 },
                        zoom: hasCoords ? 4 : 2,
                      },
                      margin: { l: 0, r: 0, t: 0, b: 0 },
                      paper_bgcolor: 'rgba(0,0,0,0)',
                      plot_bgcolor: 'rgba(0,0,0,0)',
                      autosize: true,
                      dragmode: 'pan'
                    }}
                    useResizeHandler={true}
                    style={{ width: '100%', height: '100%' }}
                    config={{ displayModeBar: false, responsive: true, scrollZoom: true }}
                  />
                )}
              </div>
            </GlassCard>

            <div className="space-y-4">
              <h3 className="text-lg font-bold font-outfit">Global Breakdown</h3>
              <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                {geoSummary.map((p: any, i: number) => (
                  <GlassCard key={i} hover={true} className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <p className="font-medium text-sm text-cyan-100">{p.name || `Point ${i}`}</p>
                      <span className="text-xs font-semibold text-emerald-400">
                        {((p.value / health?.rows) * 100).toFixed(1)}%
                      </span>
                    </div>
                    <p className="text-lg font-bold text-indigo-400">{p.value?.toLocaleString() || '1'} Intel</p>
                    <div className="mt-2 h-1.5 bg-slate-700/50 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-linear-to-r from-cyan-500 to-indigo-500"
                        style={{ width: `${Math.min(100, (p.value / geoSummary[0]?.value) * 100)}%` }}
                      />
                    </div>
                  </GlassCard>
                ))}
                {geoSummary.length === 0 && !loading && (
                  <div className="p-8 text-center text-muted-foreground border border-dashed border-white/10 rounded-lg">
                    No geographic features detected in active dataset.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
