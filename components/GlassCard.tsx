'use client'

import React from 'react'
import { cn } from '@/lib/utils'

interface GlassCardProps {
  children: React.ReactNode
  className?: string
  hover?: boolean
  glow?: boolean
  onClick?: () => void
}

export function GlassCard({
  children,
  className,
  hover = true,
  glow = false,
  onClick,
}: GlassCardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        'glass rounded-lg p-6 transition-all duration-300 cursor-default',
        hover && 'glass-hover',
        glow && 'shadow-glow animate-pulse-glow',
        onClick && 'cursor-pointer',
        className
      )}
    >
      {children}
    </div>
  )
}
