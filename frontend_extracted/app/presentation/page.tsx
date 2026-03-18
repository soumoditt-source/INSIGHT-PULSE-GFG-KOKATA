'use client'

import React, { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { GlassCard } from '@/components/GlassCard'
import { NeonBadge } from '@/components/NeonBadge'
import { LoadingState } from '@/components/LoadingState'
import axios from 'axios'
import dynamic from 'next/dynamic'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

export default function PresentationPage() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [slides, setSlides] = useState<any[]>([])

  const handleGenerate = async () => {
    if (!query.trim()) return
    setLoading(true)
    try {
      const res = await axios.post('/api/presentation', {
        query: query,
        chat_history: []
      })
      if (res.data?.slides) {
        setSlides(res.data.slides)
      } else {
        console.error("No slides returned", res.data)
      }
    } catch (e) {
      console.error("Presentation generation failed", e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <StarField />
      <GlowingOrbs />
      <Sidebar />
      <Topbar />

      <main className="ml-64 mt-16 p-8 relative z-2">
        <div className="max-w-6xl mx-auto space-y-8">
          <div className="space-y-4">
            <NeonBadge variant="purple">POWER BI AUTOMATION</NeonBadge>
            <h1 className="text-4xl font-bold font-outfit">Presentation Engine</h1>
            <p className="text-muted-foreground">Generate comprehensive strategic decks from data queries.</p>
          </div>

          <div className="flex gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., 'Summarize growth trends and regional performance'"
              className="flex-1 px-4 py-3 rounded-lg glass border border-indigo-500/20 focus:border-indigo-500/50 outline-none transition-all"
            />
            <button
              onClick={handleGenerate}
              className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-bold shadow-glow transition-all"
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Generate Deck'}
            </button>
          </div>

          {loading && (
            <div className="py-20 flex justify-center">
              <LoadingState message="J.A.R.V.I.S. is compiling your presentation..." />
            </div>
          )}

          <div className="grid grid-cols-1 gap-12 mt-12">
            {slides.map((slide, i) => (
              <GlassCard key={slide.title || `slide-${i}`} className="min-h-[400px] flex flex-col p-12 border-indigo-500/30">
                <div className="flex justify-between items-start mb-8">
                  <h2 className="text-3xl font-bold font-outfit text-indigo-100">{slide.title}</h2>
                  <span className="text-xs font-mono text-indigo-400 opacity-50">SLIDE {i + 1}</span>
                </div>

                <div className="flex-1">
                  {slide.type === 'title' && (
                    <div className="h-full flex flex-col items-center justify-center text-center">
                      <p className="text-xl text-indigo-300 italic">{slide.subtitle}</p>
                    </div>
                  )}

                  {slide.type === 'bullets' && (
                    <ul className="space-y-4">
                      {slide.content.map((bullet: string, j: number) => (
                        <li key={`bullet-${i}-${j}`} className="flex gap-3 text-lg text-indigo-50/90">
                          <span className="text-indigo-500 mt-1.5">•</span>
                          {bullet}
                        </li>
                      ))}
                    </ul>
                  )}

                  {slide.type === 'chart' && slide.fig_json && (
                    <div className="w-full h-[350px] bg-black/20 rounded-xl overflow-hidden p-4 border border-white/5">
                      <Plot
                        data={JSON.parse(slide.fig_json).data}
                        layout={{
                          ...JSON.parse(slide.fig_json).layout,
                          paper_bgcolor: 'rgba(0,0,0,0)',
                          plot_bgcolor: 'rgba(0,0,0,0)',
                          font: { color: '#e0e0ff' },
                          autosize: true
                        }}
                        style={{ width: '100%', height: '100%' }}
                        useResizeHandler={true}
                      />
                    </div>
                  )}
                </div>
              </GlassCard>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
