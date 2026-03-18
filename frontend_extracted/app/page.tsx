'use client'

import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import { StarField } from '@/components/StarField'
import { GlowingOrbs } from '@/components/GlowingOrbs'
import { BentoGridItem, BentoGrid } from '@/components/BentoGrid'
import { MetricCard } from '@/components/MetricCard'
import { HeroSection } from '@/components/HeroSection'
import Link from 'next/link'
import { useEffect } from 'react'

export default function Home() {
  useEffect(() => {
    const speakWelcome = (msg: SpeechSynthesisUtterance) => {
      let voices = globalThis.speechSynthesis.getVoices();
      let fVoice = voices.find(v => v.name.includes('Female') || v.name.includes('Samantha') || v.name.includes('Zira') || v.name.includes('Google US English'));
      if (fVoice) msg.voice = fVoice;
      globalThis.speechSynthesis.speak(msg);
    };

    const greet = () => {
      if ('speechSynthesis' in globalThis) {
        setTimeout(() => {
          const msg = new SpeechSynthesisUtterance(
            "Welcome to Insight Pulse AI. The ultimate neural data intelligence platform. I am ready to perform a detail analysis on your data with supreme accuracy."
          );
          msg.lang = 'en-US';
          msg.pitch = 1.2;
          msg.rate = 1;
          speakWelcome(msg);
        }, 500);
      }
    };
    
    // Autoplay policy bypass: trigger on first user interaction
    const handleInteraction = () => {
      greet();
      globalThis.removeEventListener('click', handleInteraction);
      globalThis.removeEventListener('scroll', handleInteraction);
    };
    globalThis.addEventListener('click', handleInteraction);
    globalThis.addEventListener('scroll', handleInteraction);
    
    // Try to load voices early
    if ('speechSynthesis' in globalThis) {
      globalThis.speechSynthesis.getVoices();
    }
    
    return () => {
      globalThis.removeEventListener('click', handleInteraction);
      globalThis.removeEventListener('scroll', handleInteraction);
    };
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <StarField />
      <GlowingOrbs />
      
      <Sidebar />
      <Topbar />

      <main className="ml-64 mt-16 p-8 relative z-2">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* AI 3D Hero Section */}
          <HeroSection />

          {/* Live Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 animate-slide-up [animation-delay:200ms]">
            <MetricCard
              label="Data Points Processed"
              value="2.4B"
              unit="monthly"
              trend={{ value: 28, direction: 'up' }}
              icon="📊"
            />
            <MetricCard
              label="Prediction Accuracy"
              value="98.7"
              unit="%"
              trend={{ value: 12, direction: 'up' }}
              icon="🎯"
            />
            <MetricCard
              label="Active Queries"
              value="1,247"
              unit="live"
              trend={{ value: 45, direction: 'up' }}
              icon="⚡"
            />
            <MetricCard
              label="System Uptime"
              value="99.99"
              unit="%"
              trend={{ value: 0, direction: 'up' }}
              icon="✨"
            />
          </div>

          {/* Main Bento Grid */}
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold font-outfit mb-2">Powerful Features</h2>
              <p className="text-muted-foreground">Unlock advanced data analysis with cutting-edge AI capabilities</p>
            </div>

            <BentoGrid>
              <BentoGridItem
                index={0}
                title="Data Chat"
                description="Conversational AI for data exploration and insights"
                icon="💬"
                span="double"
              >
                <div className="text-xs text-muted-foreground mt-4">
                  Natural language queries • Real-time analysis • Smart suggestions
                </div>
              </BentoGridItem>

              <BentoGridItem
                index={1}
                title="ML Laboratory"
                description="Build and train models"
                icon="⚗️"
              >
                <div className="text-xs text-muted-foreground">
                  Classification • Regression • Clustering
                </div>
              </BentoGridItem>

              <BentoGridItem
                index={2}
                title="Data Profiling"
                description="Comprehensive data analysis"
                icon="📈"
                span="tall"
              >
                <div className="flex flex-col gap-2 mt-4">
                  <div className="flex items-center justify-between text-xs">
                    <span>Data Quality</span>
                    <span className="text-emerald-400 font-semibold">95%</span>
                  </div>
                  <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full w-[95%] bg-linear-to-r from-emerald-500 to-teal-500" />
                  </div>
                </div>
              </BentoGridItem>

              <BentoGridItem
                index={3}
                title="Geographic View"
                description="Map-based insights"
                icon="🗺️"
              >
                <div className="text-xs text-muted-foreground">
                  Global data distribution • Regional analytics
                </div>
              </BentoGridItem>

              <BentoGridItem
                index={4}
                title="Query History"
                description="Track and manage queries"
                icon="⏱️"
              >
                <div className="text-xs text-muted-foreground">
                  Audit trail • Performance metrics
                </div>
              </BentoGridItem>

              <BentoGridItem
                index={5}
                title="Smart Dashboards"
                description="Customizable intelligence boards"
                icon="📊"
              >
                <div className="text-xs text-muted-foreground">
                  Real-time updates • Saved views
                </div>
              </BentoGridItem>
            </BentoGrid>
          </div>

          {/* CTA Section */}
          <div className="glass rounded-lg p-12 border border-indigo-500/30 text-center space-y-6 mt-16 animate-slide-up [animation-delay:400ms]">
            <h2 className="text-3xl font-bold font-outfit">Ready to Transform Your Data?</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">
              Join thousands of organizations using InsightPulse AI to unlock actionable insights from their data.
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Link
                href="/chat"
                className="px-8 py-3 rounded-lg bg-indigo-600/80 hover:bg-indigo-600 text-white font-medium transition-all duration-300 shadow-glow hover:shadow-glow-lg"
              >
                Start Free Trial
              </Link>
              <button className="px-8 py-3 rounded-lg glass border border-border/50 font-medium hover:glass-hover transition-all duration-300">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
