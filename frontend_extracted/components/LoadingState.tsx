'use client'

import React from 'react'

interface LoadingStateProps {
  message?: string
  size?: 'sm' | 'md' | 'lg'
}

export function LoadingState({
  message = 'Loading...',
  size = 'md',
}: LoadingStateProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-12 h-12',
    lg: 'w-20 h-20',
  }

  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <div className="relative">
        <div
          className={`${sizeClasses[size]} border-2 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin`}
        />
        <div className="absolute inset-0 animate-pulse-glow" />
      </div>
      {message && (
        <p className="text-sm text-muted-foreground animate-pulse">{message}</p>
      )}
    </div>
  )
}
