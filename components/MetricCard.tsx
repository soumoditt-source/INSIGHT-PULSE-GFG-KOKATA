'use client'

import React from 'react'
import { GlassCard } from './GlassCard'

interface MetricCardProps {
  label: string
  value: string | number
  unit?: string
  trend?: {
    value: number
    direction: 'up' | 'down'
  }
  icon?: React.ReactNode
  className?: string
}

export function MetricCard({
  label,
  value,
  unit,
  trend,
  icon,
  className,
}: MetricCardProps) {
  return (
    <GlassCard className={className} glow={false} hover={false}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
            {label}
          </p>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-foreground font-outfit">
              {value}
            </span>
            {unit && (
              <span className="text-sm text-muted-foreground">{unit}</span>
            )}
          </div>
          {trend && (
            <div className="mt-3 flex items-center gap-1">
              <span
                className={`text-sm font-medium ${
                  trend.direction === 'up'
                    ? 'text-emerald-400'
                    : 'text-red-400'
                }`}
              >
                {trend.direction === 'up' ? '↑' : '↓'} {trend.value}%
              </span>
            </div>
          )}
        </div>
        {icon && (
          <div className="text-2xl opacity-60 ml-4">
            {icon}
          </div>
        )}
      </div>
    </GlassCard>
  )
}
