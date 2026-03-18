"use client"
import React, { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { GlassCard } from '@/components/GlassCard'
import { NeonBadge } from '@/components/NeonBadge'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('general')

  return (
    <div className="min-h-screen bg-background text-foreground">
      <StarField />
      <GlowingOrbs />
      <Sidebar />
      <Topbar />

      <main className="ml-64 mt-16 p-8 relative z-2">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-slate-400" />
              <NeonBadge variant="default">SYSTEM ARCHITECTURE</NeonBadge>
            </div>
            <h1 className="text-4xl font-bold font-outfit">Configuration Matrix</h1>
            <p className="text-muted-foreground text-sm">
               Manage your system instance, AI tiering, and forensic security protocols.
            </p>
          </div>

          <div className="flex gap-4 border-b border-white/5 mb-8">
            {['general', 'security', 'ai-engine'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`pb-4 px-4 text-sm font-medium transition-all ${
                  activeTab === tab ? 'text-indigo-400 border-b-2 border-indigo-500' : 'text-muted-foreground'
                }`}
              >
                {tab.toUpperCase()}
              </button>
            ))}
          </div>

          <GlassCard className="p-8 space-y-8">
            {activeTab === 'general' && (
              <div className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-semibold block text-indigo-300">Display Language</label>
                  <select className="w-full bg-black/40 border border-white/10 rounded-lg p-3 text-sm focus:outline-none focus:border-indigo-500">
                    <option>English (Neural Standard)</option>
                    <option>Bengali (Kolkata Regional)</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-semibold block text-indigo-300">Data Sample Rate</label>
                  <input type="range" className="w-full accent-indigo-500" />
                  <div className="flex justify-between text-[10px] text-muted-foreground uppercase font-mono">
                    <span>Performance</span>
                    <span>Accuracy</span>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'ai-engine' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between glass p-4 rounded-lg border-emerald-500/20">
                   <div>
                     <p className="font-bold text-sm">Neural Fallback Strategy</p>
                     <p className="text-xs text-muted-foreground">Automatic 4-Stage Redundancy</p>
                   </div>
                   <div className="bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full text-[10px] font-bold">ACTIVE</div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-semibold block text-indigo-300">Primary Provider</label>
                  <div className="grid grid-cols-2 gap-4">
                     <div className="glass p-3 border-indigo-500/50 rounded-lg text-center cursor-pointer">Google Gemini</div>
                     <div className="glass p-3 border-white/5 rounded-lg text-center cursor-pointer opacity-50">OpenRouter</div>
                  </div>
                </div>
              </div>
            )}

            <div className="pt-6 border-t border-white/5 flex justify-end">
               <button className="px-6 py-2 bg-indigo-600 rounded-lg text-sm font-bold shadow-glow hover:bg-indigo-700 transition-all">
                  SAVE PROTOCOL
               </button>
            </div>
          </GlassCard>

          <footer className="text-center text-[10px] text-muted-foreground font-mono uppercase tracking-widest opacity-30">
             Instance Node: BOM-1 // GFG-KOLKATA-SHWCSE
          </footer>
        </div>
      </main>
    </div>
  )
}
