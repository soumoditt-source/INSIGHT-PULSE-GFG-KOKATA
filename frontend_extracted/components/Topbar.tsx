'use client'

import React, { useState, useEffect } from 'react'
import { NeonBadge } from './NeonBadge'

export function Topbar() {
  const [time, setTime] = useState('')
  const [status, setStatus] = useState('ONLINE')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const updateTime = () => {
      setTime(new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      }))
    }

    updateTime()
    const interval = setInterval(updateTime, 1000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="fixed top-0 left-64 right-0 h-16 glass border-b border-border/50 flex items-center justify-between px-8 z-20">
      <div className="flex items-center gap-4">
        <div className="text-sm font-mono text-muted-foreground w-24">
          {mounted ? time : <span className="animate-pulse">_ _ _ _</span>}
        </div>
        <div className="flex items-center gap-3">
          <NeonBadge variant="indigo">GEMINI 1.5 PRO ACTIVE</NeonBadge>
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/20">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-sky-500"></span>
            </span>
            <span className="text-[10px] font-mono text-sky-400 uppercase tracking-widest animate-pulse">
              Super Intelligence Mode
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="text-xs text-muted-foreground">
          Status: <span className="text-emerald-400 font-semibold">{status}</span>
        </div>
        <div className="w-8 h-8 rounded-full bg-indigo-500/30 border border-indigo-500/50 flex items-center justify-center text-xs font-bold cursor-pointer hover:bg-indigo-500/40 transition-all">
          U
        </div>
      </div>
    </div>
  )
}
