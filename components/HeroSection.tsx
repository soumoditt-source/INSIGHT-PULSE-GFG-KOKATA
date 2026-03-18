"use client"

import Link from 'next/link'
import { AgamottoEye } from '@/components/AgamottoEye'
import { NeonBadge } from '@/components/NeonBadge'

export function HeroSection() {
  return (
    <div className="relative w-full h-[80vh] flex flex-col items-center justify-center overflow-hidden mix-blend-screen bg-transparent z-10">
      
      {/* 3D Background Eye */}
      <div className="absolute inset-0 z-0">
        <AgamottoEye />
      </div>

      {/* Foreground Content */}
      <div className="relative z-10 flex flex-col items-center justify-center text-center space-y-6 px-4 animate-slide-up mt-12 bg-black/20 backdrop-blur-sm p-12 rounded-3xl border border-indigo-500/20 shadow-glow-lg">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <NeonBadge variant="indigo">J.A.R.V.I.S. INTELLIGENCE CORE v5.0</NeonBadge>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold font-outfit text-balance tracking-tighter drop-shadow-2xl">
          <span className="text-white drop-shadow-lg">Talk to your</span><br />
          <span className="bg-gradient-to-r from-cyan-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent animate-text-glow">
            Data.
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-indigo-100/80 max-w-2xl leading-relaxed font-light drop-shadow-md">
          Upload any dataset. Ask questions in plain English. Get instant multi-chart dashboards, zero-hallucination insights, and ML-powered analysis.
        </p>

        <div className="flex flex-wrap gap-6 pt-8">
          <Link
            href="/chat"
            className="group relative px-8 py-4 bg-indigo-600/20 border border-cyan-400/50 rounded-xl overflow-hidden hover:scale-105 transition-all duration-300"
          >
            <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 opacity-0 group-hover:opacity-100 transition-opacity" />
            <span className="relative z-10 text-cyan-50 font-semibold tracking-wider flex items-center gap-2">
              INITIALIZE CHAT <span className="text-cyan-400 group-hover:translate-x-1 transition-transform">→</span>
            </span>
          </Link>
          <Link 
            href="/dashboards"
            className="px-8 py-4 rounded-xl glass border border-border/50 text-indigo-100 font-medium hover:glass-hover transition-all duration-300 hover:text-white"
          >
            Open CRM
          </Link>
        </div>
      </div>
    </div>
  )
}
