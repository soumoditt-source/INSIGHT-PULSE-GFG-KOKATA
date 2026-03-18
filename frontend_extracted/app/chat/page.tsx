'use client'

import React, { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { ChatUI } from '@/components/ChatUI'
import { GlassCard } from '@/components/GlassCard'
import { NeonBadge } from '@/components/NeonBadge'
import dynamic from 'next/dynamic'

// Same interfaces from ChatUI for strong typing
interface ChartData {
  title: string;
  type: string;
  fig_json: string;
}

interface BackendResponse {
  insights: string[];
  sql: string;
  charts: ChartData[];
  duration_ms: number;
  row_count: number;
  followup_suggestions: string[];
  error?: string;
}

// Dynamically import Plot for the sidebar
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

export default function ChatPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [latestData, setLatestData] = useState<BackendResponse | null>(null)

  const handleSendMessage = async (message: string) => {
    // Fired before the API call finishes (to show loading)
    setIsLoading(true)
  }

  // Callback for when ChatUI receives the final payload from the backend
  const handleBotResponse = (data: BackendResponse) => {
    setLatestData(data)
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <StarField />
      <GlowingOrbs />

      <Sidebar />
      <Topbar />

      <main className="ml-64 mt-16 p-8 relative z-2">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-180px)]">
            {/* Chat Column */}
            <div className="lg:col-span-1 flex flex-col">
              <div className="mb-4 space-y-2">
                <h1 className="text-2xl font-bold font-outfit text-indigo-100 drop-shadow-[0_0_10px_rgba(129,140,248,0.5)]">Data Chat</h1>
                <p className="text-sm text-indigo-200/60 font-mono uppercase tracking-widest">
                  Terminal Access
                </p>
              </div>

              <GlassCard className="flex-1 flex flex-col p-0 overflow-hidden border border-indigo-500/30 shadow-glow-lg" glow={true}>
                <div className="p-6 flex-1 flex flex-col overflow-hidden">
                  <ChatUI
                    onSendMessage={handleSendMessage}
                    onResponseReceived={handleBotResponse}
                    isLoading={isLoading}
                  />
                </div>
              </GlassCard>
            </div>

            {/* Analytics Column */}
            <div className="lg:col-span-2 flex flex-col gap-6 overflow-y-auto pr-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold font-outfit text-indigo-100 drop-shadow-[0_0_8px_rgba(129,140,248,0.5)]">
                    Live Analytics
                  </h2>
                  <NeonBadge variant={isLoading ? "cyan" : "teal"}>
                    {isLoading ? "COMPUTING..." : "REAL-TIME"}
                  </NeonBadge>
                </div>
                <p className="text-sm text-indigo-200/60 font-mono tracking-wider">
                  Dynamic visual intelligence from main core
                </p>
              </div>

              {/* Dynamic Charts Area */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {!latestData && !isLoading && (
                  <div className="col-span-full h-[400px] flex items-center justify-center border border-indigo-500/20 rounded-xl bg-black/20 backdrop-blur-md">
                     <p className="text-indigo-400/50 font-mono animate-pulse">AWAITING QUERY INPUT...</p>
                  </div>
                )}
                
                {isLoading && (
                   <div className="col-span-full h-[400px] flex items-center justify-center border border-cyan-500/30 rounded-xl bg-cyan-900/10 backdrop-blur-md">
                     <div className="flex flex-col items-center gap-4">
                        <div className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-400 rounded-full animate-spin shadow-[0_0_15px_rgba(34,211,238,0.5)]" />
                        <p className="text-cyan-400 font-mono animate-pulse tracking-widest text-sm">PROCESSING NEURAL ANALYSIS</p>
                     </div>
                   </div>
                )}

                {!isLoading && latestData?.charts && latestData.charts.map((chart, idx) => {
                  try {
                    const fig = JSON.parse(chart.fig_json)
                    if(fig.layout) {
                      fig.layout.paper_bgcolor = 'rgba(0,0,0,0)'
                      fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
                      fig.layout.font = { color: '#e0e0ff' }
                    }
                    return (
                      <div key={idx} className={idx === 0 && latestData.charts.length % 2 !== 0 ? "lg:col-span-2 animate-scale-in" : "animate-scale-in"}>
                        <GlassCard className="h-[350px] p-2 flex flex-col" glow={true}>
                          <p className="text-xs text-indigo-300 font-mono uppercase px-4 pt-2 truncate">{chart.title}</p>
                          <div className="flex-1 w-full h-full p-2">
                            <Plot
                              data={fig.data}
                              layout={{ ...fig.layout, autosize: true, margin: { l: 40, r: 20, t: 20, b: 40 } }}
                              useResizeHandler={true}
                              style={{ width: '100%', height: '100%' }}
                              config={{ displayModeBar: false, responsive: true }}
                            />
                          </div>
                        </GlassCard>
                      </div>
                    )
                  } catch(e) { return null }
                })}
              </div>

              {/* Data Summary (SQL + Performance) */}
              <div className="space-y-3 mt-6">
                <h3 className="text-lg font-bold font-outfit text-indigo-100">Execution Telemetry</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <GlassCard glow={false} hover={true}>
                    <p className="text-xs text-indigo-300/70 font-mono mb-1">DATA POINTS</p>
                    <div className="flex items-end gap-2">
                      <span className="text-2xl font-bold text-white font-outfit">
                        {latestData ? latestData.row_count.toLocaleString() : '---'}
                      </span>
                      <span className="text-[10px] text-cyan-400 font-mono">ROWS</span>
                    </div>
                  </GlassCard>
                  
                  <GlassCard glow={false} hover={true}>
                    <p className="text-xs text-indigo-300/70 font-mono mb-1">LATENCY</p>
                    <div className="flex items-end gap-2">
                      <span className="text-2xl font-bold text-white font-outfit">
                        {latestData ? (latestData.duration_ms / 1000).toFixed(2) : '---'}
                      </span>
                      <span className="text-[10px] text-cyan-400 font-mono">SEC</span>
                    </div>
                  </GlassCard>

                  <GlassCard glow={false} hover={true} className="overflow-hidden">
                    <p className="text-xs text-indigo-300/70 font-mono mb-1">LAST SQL GENERATED</p>
                    <div className="text-[10px] font-mono whitespace-nowrap overflow-hidden text-ellipsis text-emerald-400/80 mt-2">
                      {latestData ? latestData.sql : 'No recent query'}
                    </div>
                  </GlassCard>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
