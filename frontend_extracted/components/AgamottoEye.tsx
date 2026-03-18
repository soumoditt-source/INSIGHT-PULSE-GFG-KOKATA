"use client"

import React, { useRef } from 'react'
// @ts-ignore
import { Canvas, useFrame } from '@react-three/fiber'
// @ts-ignore
import { Sphere, MeshDistortMaterial, Sparkles, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

// The inner glowing core
function Core() {
  const particlesRef = useRef<THREE.Mesh>(null)

  useFrame((state: any) => {
    if (!particlesRef.current) return
    const time = state.clock.getElapsedTime()
    particlesRef.current.rotation.y = time * 0.15
    particlesRef.current.rotation.z = time * 0.1
    
    // Neural pulse effect
    const s = 1 + Math.sin(time * 1.5) * 0.05
    particlesRef.current.scale.set(s, s, s)
  })

  return (
    <Sphere ref={particlesRef} args={[1.5, 64, 64]}>
      <MeshDistortMaterial
        color="#00ffff"
        emissive="#0088ff"
        emissiveIntensity={2}
        distort={0.4}
        speed={1.5}
        roughness={0.2}
        metalness={0.8}
        wireframe={true}
      />
    </Sphere>
  )
}

// The outer shell/rings of the "eye"
function AgamottoShell() {
  const groupRef = useRef<THREE.Group>(null)

  useFrame((state: any) => {
    if (!groupRef.current) return
    groupRef.current.rotation.y = state.clock.getElapsedTime() * -0.1
    groupRef.current.rotation.z = Math.sin(state.clock.getElapsedTime() * 0.5) * 0.2
  })

  return (
    <group ref={groupRef}>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[2.5, 0.05, 32, 100]} />
        <meshStandardMaterial color="#00ffcc" emissive="#00aaaa" emissiveIntensity={1} metalness={1} roughness={0} />
      </mesh>
      <mesh rotation={[0, Math.PI / 2, 0]}>
        <torusGeometry args={[2.8, 0.02, 32, 100]} />
        <meshStandardMaterial color="#66ccff" emissive="#33aaff" emissiveIntensity={0.8} metalness={1} roughness={0} />
      </mesh>
    </group>
  )
}

export function AgamottoEye() {
  return (
    <div className="absolute inset-0 w-full h-full z-0 pointer-events-none opacity-80 mix-blend-screen">
      <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={2} color="#00ffff" />
        <pointLight position={[-10, -10, -10]} intensity={1} color="#6666ff" />
        
        <Core />
        <AgamottoShell />
        
        <Sparkles 
          count={200} 
          scale={8} 
          size={2} 
          speed={0.4} 
          opacity={0.6}
          color="#aaffff"
        />
        
        {/* We disable zoom/pan so it just acts as a background hero piece */}
        <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} />
      </Canvas>
    </div>
  )
}
