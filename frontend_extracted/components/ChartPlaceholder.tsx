'use client'

import React from 'react'
import { GlassCard } from './GlassCard'

interface ChartPlaceholderProps {
  title?: string
  type?: 'line' | 'bar' | 'pie' | 'scatter'
  data?: any
}

export function ChartPlaceholder({
  title = 'Analytics Chart',
  type = 'line',
}: ChartPlaceholderProps) {
  // Simulated chart visualization
  const generateChartBars = () => {
    return Array.from({ length: 12 }, (_, i) => {
      const height = Math.floor(Math.random() * 80) + 20
      return (
        <div
          key={i}
          className="flex flex-col items-center gap-2 flex-1"
        >
          <div className="relative w-full h-48 flex items-end justify-center gap-1">
            {Array.from({ length: 3 }, (_, j) => (
              <div
                key={j}
                className={`flex-1 rounded-t transition-all duration-500 ${
                  j === 0
                    ? 'bg-indigo-500 opacity-60'
                    : j === 1
                      ? 'bg-purple-500 opacity-50'
                      : 'bg-pink-500 opacity-40'
                }`}
                style={{ height: `${height + j * 15}%` }}
              />
            ))}
          </div>
        </div>
      )
    })
  }

  return (
    <GlassCard glow={true} hover={false}>
      <div className="h-full flex flex-col">
        <h3 className="text-sm font-semibold text-foreground mb-4 font-outfit">
          {title}
        </h3>

        <div className="flex-1 flex flex-col justify-end">
          <div className="flex items-end gap-1 h-40">
            {Array.from({ length: 20 }, (_, i) => {
              const height = Math.abs(
                Math.sin(i * 0.5) * 100 +
                Math.cos(i * 0.3) * 30 +
                50
              )
              return (
                <div
                  key={i}
                  className="flex-1 bg-gradient-to-t from-indigo-500 to-purple-500 rounded-t opacity-60 hover:opacity-100 transition-opacity cursor-pointer group relative"
                  style={{
                    height: `${height}%`,
                  }}
                >
                  <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-black/80 px-2 py-1 rounded text-xs text-white opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none">
                    {Math.round(height)}
                  </div>
                </div>
              )
            })}
          </div>

          <div className="flex justify-between text-xs text-muted-foreground mt-4 px-1">
            <span>Start</span>
            <span>Mid</span>
            <span>End</span>
          </div>
        </div>

        <div className="mt-6 flex gap-4 pt-4 border-t border-border/30">
          <div className="text-xs">
            <p className="text-muted-foreground">Avg Value</p>
            <p className="text-lg font-bold text-indigo-400">$2,847</p>
          </div>
          <div className="text-xs">
            <p className="text-muted-foreground">Peak Value</p>
            <p className="text-lg font-bold text-purple-400">$4,120</p>
          </div>
          <div className="text-xs">
            <p className="text-muted-foreground">Trend</p>
            <p className="text-lg font-bold text-emerald-400">+12.5%</p>
          </div>
        </div>
      </div>
    </GlassCard>
  )
}
