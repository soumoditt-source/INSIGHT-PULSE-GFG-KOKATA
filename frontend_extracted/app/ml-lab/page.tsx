'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { BentoGrid, BentoGridItem } from '@/components/BentoGrid'
import { MetricCard } from '@/components/MetricCard'
import { NeonBadge } from '@/components/NeonBadge'
import { GlassCard } from '@/components/GlassCard'
import { apiClient } from '@/lib/api'
import dynamic from 'next/dynamic'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

export default function MLLabPage() {
  const [loading, setLoading] = useState(false)
  const [mlData, setMlData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [datasetLoaded, setDatasetLoaded] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    // Check if dataset is already loaded
    apiClient.getSystemStatus().then((h: any) => {
      setDatasetLoaded(h?.dataset_loaded ?? false)
    }).catch(() => {})
  }, [])

  const runAnalysis = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await apiClient.runMLAnalysis("auto")
      setMlData(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    try {
      await apiClient.uploadDataset(file)
      setDatasetLoaded(true)
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
      setDatasetLoaded(true)
    } finally {
      setUploading(false)
    }
  }

  // Helper metric extractors
  const getTaskColor = (task: string) => {
    if (task?.includes('classification')) return 'emerald'
    if (task?.includes('regression')) return 'indigo'
    return 'purple'
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
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-purple-500 animate-pulse" />
                <NeonBadge variant="purple">MACHINE LEARNING</NeonBadge>
              </div>
              <h1 className="text-4xl font-bold font-outfit">ML Laboratory</h1>
              <p className="text-muted-foreground">Auto-detect Deep Analytics: Classification, Regression & Clustering.</p>
            </div>
            <div className="flex gap-3 flex-wrap">
              <button onClick={() => loadPreset('Amazon Sales.csv')} disabled={uploading} className="px-4 py-2 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20 text-indigo-300 text-sm transition-all disabled:opacity-50">
                {uploading ? '⏳ Loading...' : '📦 Amazon Data'}
              </button>
              <button onClick={() => loadPreset('Insurance Claims.csv')} disabled={uploading} className="px-4 py-2 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-300 text-sm transition-all disabled:opacity-50">
                🛡️ Insurance
              </button>
              <button onClick={() => fileInputRef.current?.click()} disabled={uploading} className="px-4 py-2 rounded-lg bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-purple-300 text-sm transition-all disabled:opacity-50">
                ⏏️ Upload CSV
              </button>
              <input ref={fileInputRef} type="file" accept=".csv,.xlsx,.xls" title="Upload Dataset" placeholder="Upload Dataset" className="hidden" onChange={handleUpload} />
              <button 
                onClick={runAnalysis}
                disabled={loading || uploading}
                className="px-6 py-3 rounded-md bg-indigo-600 hover:bg-indigo-500 text-white shadow-glow transition-all flex items-center justify-center disabled:opacity-50"
              >
                {loading ? (
                  <span className="animate-pulse">Running Neural Engine...</span>
                ) : (
                  <>Run AutoML Analysis 🚀</>
                )}
              </button>
            </div>
          </div>

          {error && (
            <div className="p-4 rounded-md glass border border-red-500/50 text-red-200 text-sm">
              🚨 {error} — Please ensure a dataset is uploaded first!
            </div>
          )}

          {mlData && !loading && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <MetricCard 
                  label="Detected Task" 
                  value={mlData.auto_detected_task || mlData.task || 'N/A'} 
                  icon="🤖" 
                />
                <MetricCard 
                  label={mlData.roc_auc ? 'ROC AUC Score' : (mlData.r2_score ? 'R² Score' : 'Silhouette Score')} 
                  value={
                    mlData.roc_auc ? (mlData.roc_auc * 100).toFixed(1) : 
                    mlData.r2_score ? (mlData.r2_score * 100).toFixed(1) : 
                    mlData.silhouette_score ? mlData.silhouette_score.toFixed(3) : 'N/A'
                  } 
                  unit={mlData.roc_auc || mlData.r2_score ? '%' : ''} 
                  icon="🎯" 
                />
                <MetricCard 
                  label={mlData.f1_score ? 'F1 Score' : (mlData.rmse ? 'RMSE' : 'Clusters Found')} 
                  value={
                    mlData.f1_score ? (mlData.f1_score * 100).toFixed(1) : 
                    mlData.rmse ? mlData.rmse.toFixed(2) : 
                    mlData.n_clusters ?? 'N/A'
                  } 
                  unit={mlData.f1_score ? '%' : ''}
                  icon="⚡" 
                />
                <MetricCard 
                  label="Target Column" 
                  value={mlData.auto_detected_target || 'Unsupervised'} 
                  icon="🎯" 
                />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <GlassCard glow={true}>
                  <h3 className="text-lg font-bold font-outfit mb-4 text-indigo-200">Execution Log Details</h3>
                  <pre className="text-xs text-muted-foreground p-4 bg-black/40 rounded-lg overflow-x-auto border border-white/5 whitespace-pre-wrap">
                    {JSON.stringify(mlData, null, 2)}
                  </pre>
                </GlassCard>

                <GlassCard glow={true}>
                  <h3 className="text-lg font-bold font-outfit mb-4 text-purple-200">AutoML Pipeline</h3>
                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold border border-emerald-500/50">1</div>
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-white">Data Preprocessing & Scaling</p>
                        <p className="text-xs text-muted-foreground">OHE for categoricals, StandardScalar for numerics.</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold border border-indigo-500/50">2</div>
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-white">Target Detection & Task Selection</p>
                        <p className="text-xs text-muted-foreground">Pipeline intelligently identified {mlData.auto_detected_task || mlData.task}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="w-8 h-8 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold border border-purple-500/50">3</div>
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-white">Model Evaluation (ROC AUC / R²)</p>
                        <p className="text-xs text-muted-foreground">Scikit-learn random forest validation completed.</p>
                      </div>
                    </div>
                  </div>
                </GlassCard>
              </div>
            </div>
          )}

          {!mlData && !loading && !error && (
            <div className="text-center p-12 glass rounded-lg border border-border/10 mt-12 relative overflow-hidden">
                  <div className="absolute inset-0 bg-linear-to-br from-primary/20 via-transparent to-indigo-500/20 pointer-events-none" />
               <div className="text-6xl mb-4">🔬</div>
               <h3 className="text-xl font-bold text-white mb-2">Awaiting Computation</h3>
               <p className="text-muted-foreground max-w-md mx-auto">Upload a dataset from the sidebar and click "Run AutoML Analysis" to generate real-time predictive models, ROC AUC scores, and clustering metrics natively.</p>
            </div>
          )}

        </div>
      </main>
    </div>
  )
}
