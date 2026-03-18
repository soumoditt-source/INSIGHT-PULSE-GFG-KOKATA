'use client'

import React, { useState, useRef, useEffect } from 'react'

export function DatasetUploader() {
  const [isUploading, setIsUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [activeDataset, setActiveDataset] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/health')
        if (res.ok) {
          const data = await res.json()
          if (data.dataset_loaded) {
            setActiveDataset(data.dataset_name)
          }
        }
      } catch (e) {
        console.error("Health check failed")
      }
    }
    checkHealth()
    const interval = setInterval(checkHealth, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    setMessage('Uploading...')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (res.ok) {
        setMessage(`✅ ${data.rows || 0} rows loaded!`)
        setActiveDataset(file.name)
        setTimeout(() => window.location.reload(), 1500)
      } else {
        setMessage(`❌ ${data.detail || 'Upload failed'}`)
      }
    } catch (err) {
      console.error(err)
      setMessage('❌ Server unreachable')
    } finally {
      setIsUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
      setTimeout(() => setMessage(''), 5000)
    }
  }

  return (
    <div className="glass rounded-lg p-4 border border-border/30 flex flex-col gap-3">
      <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest flex justify-between items-center">
        <span>Active Dataset</span>
        {activeDataset && <span className="text-cyan-400 capitalize bg-cyan-950/30 px-2 py-0.5 rounded border border-cyan-800/30 truncate max-w-[120px]">{activeDataset}</span>}
      </div>
      
      <div className="flex flex-col gap-2">
        <button
          onClick={async () => { 
            setIsUploading(true);
            try {
              const res = await fetch('/api/load-preset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: 'Amazon Sales.csv' })
              });
              if (res.ok) window.location.reload();
            } finally { setIsUploading(false); }
          }}
          disabled={isUploading}
          className="w-full py-1.5 px-3 text-[11px] rounded bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20 text-indigo-300 flex items-center gap-2 transition-all disabled:opacity-50"
        >
          📦 Load Amazon Dataset
        </button>
        <button
          onClick={async () => { 
            setIsUploading(true);
            try {
              const res = await fetch('/api/load-preset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: 'Insurance Claims.csv' })
              });
              if (res.ok) window.location.reload();
            } finally { setIsUploading(false); }
          }}
          disabled={isUploading}
          className="w-full py-1.5 px-3 text-[11px] rounded bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-300 flex items-center gap-2 transition-all disabled:opacity-50"
        >
          🛡️ Load Insurance Dataset
        </button>
      </div>

      <div className="h-px bg-border/20 my-1" />

      <input
        type="file"
        accept=".csv,.xlsx,.xls"
        className="hidden"
        ref={fileInputRef}
        onChange={handleUpload}
      />
      <button
        onClick={() => fileInputRef.current?.click()}
        disabled={isUploading}
        className="w-full py-2 flex items-center justify-center gap-2 rounded-md bg-gradient-to-r from-indigo-500/20 to-purple-500/20 hover:from-indigo-500/40 hover:to-purple-500/40 border border-indigo-500/30 text-indigo-100 transition-all font-medium text-sm shadow-glow hover:shadow-glow-lg disabled:opacity-50"
      >
        {isUploading ? (
          <span className="animate-pulse">Injecting Data...</span>
        ) : (
          <>
            <span className="text-base">⏏️</span> Inject Custom CSV
          </>
        )}
      </button>
      {message && <div className="text-xs text-center text-emerald-400 font-medium animate-in fade-in">{message}</div>}
    </div>
  )
}
