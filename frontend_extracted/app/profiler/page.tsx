'use client'

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

export default function ProfilerPage() {
  const [loading, setLoading] = useState(true)
  const [profile, setProfile] = useState<any>(null)
  const [health, setHealth] = useState<any>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profData, healthData] = await Promise.all([
          apiClient.getProfile(),
          apiClient.getSystemStatus()
        ])
        setProfile(profData)
        setHealth(healthData)
      } catch (e) {
        console.error("Failed to fetch profile data")
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

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
              <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse" />
              <NeonBadge variant="cyan">DATA PROFILING</NeonBadge>
            </div>
            <h1 className="text-4xl font-bold font-outfit">Data Profiler</h1>
            <p className="text-muted-foreground">Comprehensive analysis of your active dataset.</p>
          </div>

          {loading ? (
            <div className="text-center p-12 glass animate-pulse">Running Deep Profiling...</div>
          ) : !profile ? (
            <div className="text-center p-12 glass text-red-400 border border-red-500/20">🚨 No dataset loaded. Please upload a dataset from the sidebar.</div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 animate-in slide-in-from-bottom-4 fade-in duration-700">
                <MetricCard label="Total Records" value={health?.rows?.toLocaleString() || '0'} icon="📊" />
                <MetricCard label="Data Quality" value={profile?.data_quality_score?.score || 0} unit="/ 100" icon="✓" />
                <MetricCard label="Missing Values" value={Object.keys(profile?.missing_values || {}).length} icon="⚠️" />
                <MetricCard label="Total Columns" value={health?.columns || '0'} icon="📋" />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in slide-in-from-bottom-8 fade-in duration-700">
                {/* Quality Score */}
                <GlassCard glow={true} className="lg:col-span-1 border border-cyan-500/30">
                  <h3 className="text-lg font-bold font-outfit mb-6 text-cyan-100">Quality Index</h3>
                  <div className="text-center">
                    <div className="relative w-32 h-32 mx-auto mb-6">
                      <div className="absolute inset-0 rounded-full border-8 border-cyan-500/20" />
                      <div
                        className="absolute inset-0 rounded-full border-8 border-transparent border-t-cyan-500 border-r-indigo-500 animate-[spin_4s_linear_infinite]"
                      />
                      <div className="absolute inset-2 rounded-full bg-background flex items-center justify-center shadow-[inset_0_0_20px_rgba(6,182,212,0.2)]">
                        <span className="text-4xl font-bold font-outfit text-cyan-400">
                          {profile?.data_quality_score?.grade || 'N/A'}
                        </span>
                      </div>
                    </div>
                    <p className="text-cyan-300 font-medium">{profile?.data_quality_score?.score}% Integrity</p>
                  </div>
                </GlassCard>

                {/* Missing Values */}
                <GlassCard glow={true} className="lg:col-span-2">
                  <h3 className="text-lg font-bold font-outfit mb-4 text-indigo-200">Missing Data Matrix</h3>
                  <div className="space-y-2 max-h-64 overflow-y-auto pr-2 custom-scrollbar">
                    {profile?.missing_values && Object.entries(profile.missing_values).length > 0 ? (
                      Object.entries(profile.missing_values).map(([col, count]: [string, any], i) => (
                        <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-black/40 border border-white/5">
                          <p className="font-mono text-sm text-indigo-300">{col}</p>
                          <p className="text-sm font-semibold text-rose-400">{count} missing</p>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 text-center text-emerald-400 font-medium">✨ Pristine Dataset - No missing values detected.</div>
                    )}
                  </div>
                </GlassCard>
              </div>

              {/* Raw Profiling Log */}
              <GlassCard glow={true} className="border border-purple-500/20">
                <h3 className="text-lg font-bold font-outfit mb-4 text-purple-200">Raw Integrity JSON Stream</h3>
                <pre className="text-xs text-muted-foreground p-4 bg-black/50 rounded-lg overflow-auto max-h-96 border border-white/5 whitespace-pre-wrap font-mono">
                  {JSON.stringify(profile, null, 2)}
                </pre>
              </GlassCard>
            </>
          )}

        </div>
      </main>
    </div>
  )
}
