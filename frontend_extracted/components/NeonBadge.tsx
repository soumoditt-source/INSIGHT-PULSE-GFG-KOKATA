'use client'

import React from 'react'
import { cn } from '@/lib/utils'

type BadgeVariant = 'indigo' | 'purple' | 'magenta' | 'cyan' | 'teal'

interface NeonBadgeProps {
  children: React.ReactNode
  variant?: BadgeVariant
  className?: string
  glow?: boolean
}

const variantStyles = {
  indigo: 'bg-indigo-500/20 border-indigo-500/50 text-indigo-200 shadow-indigo-500/20',
  purple: 'bg-purple-500/20 border-purple-500/50 text-purple-200 shadow-purple-500/20',
  magenta: 'bg-pink-500/20 border-pink-500/50 text-pink-200 shadow-pink-500/20',
  cyan: 'bg-cyan-500/20 border-cyan-500/50 text-cyan-200 shadow-cyan-500/20',
  teal: 'bg-teal-500/20 border-teal-500/50 text-teal-200 shadow-teal-500/20',
}

export function NeonBadge({
  children,
  variant = 'indigo',
  className,
  glow = true,
}: NeonBadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium border',
        'backdrop-blur-sm transition-all duration-300',
        glow && 'shadow-glow',
        variantStyles[variant],
        className
      )}
    >
      {children}
    </span>
  )
}
