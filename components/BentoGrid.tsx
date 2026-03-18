'use client'

import React, { useEffect, useState } from 'react'
import { cn } from '@/lib/utils'
import { GlassCard } from './GlassCard'

interface BentoGridItemProps {
  title: string
  description?: string
  icon?: string
  className?: string
  children?: React.ReactNode
  span?: 'default' | 'double' | 'tall'
  onClick?: () => void
  index?: number
}

export function BentoGridItem({
  title,
  description,
  icon,
  className,
  children,
  span = 'default',
  onClick,
  index = 0,
}: BentoGridItemProps) {
  const [isVisible, setIsVisible] = React.useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true)
    }, index * 100)
    return () => clearTimeout(timer)
  }, [index])

  const spanClasses = {
    default: 'md:col-span-1 md:row-span-1',
    double: 'md:col-span-2 md:row-span-1',
    tall: 'md:col-span-1 md:row-span-2',
  }

  return (
    <div
      className={cn(
        'col-span-1 row-span-1 transition-all duration-500',
        spanClasses[span],
        isVisible ? 'animate-slide-up' : 'opacity-0 translate-y-8'
      )}
    >
      <GlassCard
        className={cn('h-full', className)}
        hover={true}
        glow={true}
        onClick={onClick}
      >
        <div className="flex flex-col h-full">
          {icon && (
            <div className="text-4xl mb-4 opacity-70">{icon}</div>
          )}
          <h3 className="text-lg font-bold font-outfit mb-2 text-foreground">
            {title}
          </h3>
          {description && (
            <p className="text-sm text-muted-foreground mb-4 flex-1">
              {description}
            </p>
          )}
          {children}
        </div>
      </GlassCard>
    </div>
  )
}

interface BentoGridProps {
  children: React.ReactNode
  className?: string
}

export function BentoGrid({ children, className }: BentoGridProps) {
  return (
    <div
      className={cn(
        'grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[300px]',
        className
      )}
    >
      {children}
    </div>
  )
}
