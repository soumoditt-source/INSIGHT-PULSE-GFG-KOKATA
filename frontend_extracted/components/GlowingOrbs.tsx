'use client'

import React from 'react'

interface OrbPosition {
  top: string
  left: string
  size: string
  delay: number
  duration: number
  color: 'purple' | 'indigo' | 'cyan'
}

const orbConfigs: OrbPosition[] = [
  {
    top: '10%',
    left: '5%',
    size: '300px',
    delay: 0,
    duration: 20,
    color: 'purple',
  },
  {
    top: '50%',
    left: '80%',
    size: '250px',
    delay: 2,
    duration: 25,
    color: 'indigo',
  },
  {
    top: '70%',
    left: '10%',
    size: '200px',
    delay: 4,
    duration: 30,
    color: 'cyan',
  },
  {
    top: '20%',
    left: '60%',
    size: '280px',
    delay: 1,
    duration: 22,
    color: 'purple',
  },
]

const colorMap = {
  purple: 'from-purple-600/30 to-purple-400/0',
  indigo: 'from-indigo-600/30 to-indigo-400/0',
  cyan: 'from-cyan-600/30 to-cyan-400/0',
}

export function GlowingOrbs() {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 1 }}>
      {orbConfigs.map((orb, index) => (
        <div
          key={index}
          className={`absolute rounded-full blur-3xl bg-gradient-to-r ${colorMap[orb.color]} opacity-40`}
          style={{
            top: orb.top,
            left: orb.left,
            width: orb.size,
            height: orb.size,
            transform: 'translate(-50%, -50%)',
            animation: `float ${orb.duration}s ease-in-out infinite`,
            animationDelay: `${orb.delay}s`,
          }}
        />
      ))}
    </div>
  )
}
