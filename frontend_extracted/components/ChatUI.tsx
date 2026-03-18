'use client'

import React, { useState, useRef, useEffect } from 'react'
import { GlassCard } from './GlassCard'
import { LoadingState } from './LoadingState'
import { NeonBadge } from './NeonBadge'
import { cn } from '@/lib/utils'

import axios from 'axios'
import dynamic from 'next/dynamic'
import Link from 'next/link'
// @ts-ignore
import puter from '@heyputer/puter.js'

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

interface ChartData {
  title: string;
  type: string;
  fig_json: string;
}

interface BackendResponse {
  insights: string[];
  sql: string;
  charts: ChartData[];
  duration_ms: number;
  row_count: number;
  followup_suggestions: string[];
  pathway?: string[];
  agent_metadata?: any;
  error?: string;
}

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string | BackendResponse
  timestamp: Date
}

interface ChatUIProps {
  onSendMessage?: (message: string) => Promise<void>
  onResponseReceived?: (data: BackendResponse) => void
  isLoading?: boolean
}

export function ChatUI({ onSendMessage, onResponseReceived, isLoading = false }: ChatUIProps) {
  const [messages, setMessages] = useState<Message[]>([])
  
  // Suppress hydration mismatch by setting initial message client-side
  useEffect(() => {
    setMessages([
      {
        id: '1',
        role: 'assistant',
        content: 'System Initialized. I am J.A.R.V.I.S., your neural intelligence core. Ask me to cross-reference databases, predict trends, or generate visualizations.',
        timestamp: new Date(),
      }
    ])
  }, [])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userText = input
    const userMessage = {
      id: Math.random().toString(),
      role: 'user' as const,
      content: userText,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')

    try {
      if (onSendMessage) {
        // Trigger external loading state if needed
        await onSendMessage(userText)
      }

      // 💥 ACTUAL BACKEND CALL 💥
      const response = await axios.post('http://localhost:8000/generate', {
        query: userText,
        session_id: 'jarvis-frontend-session',
        chat_history: messages.map(m => ({
          role: m.role,
          content: typeof m.content === 'string' ? m.content : JSON.stringify(m.content)
        }))
      })

      const data = response.data as BackendResponse

      if (data.error) {
        throw new Error(data.error)
      }

      if (onResponseReceived) {
        onResponseReceived(data)
      }

      const assistantMessage = {
        id: Math.random().toString(),
        role: 'assistant' as const,
        content: data,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error: any) {
      console.warn('Primary AI Engine failed, engaging Puter.js fallback...', error)
      
      try {
        // Fallback to Puter.js AI
        const puterResponse = await puter.ai.chat(userText, { model: 'gpt-4o' })
        
        const extractContent = (res: any): string => {
          if (typeof res === 'string') return res;
          if (res?.message?.content) return res.message.content;
          if (Array.isArray(res?.message?.content)) {
            return res.message.content.map((c: any) => typeof c === 'string' ? c : c.text || '').join('\n');
          }
          return JSON.stringify(res || 'Intelligence reconstructed.');
        }

        const assistantMessage = {
          id: Math.random().toString(),
          role: 'assistant' as const,
          content: {
            insights: [extractContent(puterResponse)],
            sql: '-- Falling back to Neural Proxy (Puter.js)',
            charts: [],
            duration_ms: 0,
            row_count: 0,
            followup_suggestions: ['Explain further', 'Analyze deep'],
            pathway: ['Engaging Neural Proxy (Puter.js)', 'Bypassing primary core', 'Response reconstructed']
          } as BackendResponse,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, assistantMessage])
      } catch (puterError: any) {
        setMessages((prev) => [...prev, {
          id: Math.random().toString(),
          role: 'assistant',
          content: {
            insights: [`Critical error: ${puterError.message}`],
            sql: '',
            charts: [],
            duration_ms: 0,
            row_count: 0,
            followup_suggestions: [],
            error: puterError.message
          },
          timestamp: new Date()
        }])
      }
    }
  }

  // Helper to render AI content pieces
  const renderAIContent = (msgContent: string | BackendResponse) => {
    if (typeof msgContent === 'string') {
      return <p className="text-sm leading-relaxed whitespace-pre-wrap">{msgContent}</p>
    }

    // It's a structured response
    if (msgContent.error) {
      return <p className="text-sm text-red-400 font-mono">⚠️ {msgContent.error}</p>
    }

    return (
      <div className="space-y-4 w-full">
        {/* Metrics Row */}
        <div className="flex flex-wrap gap-2 text-xs font-mono">
          <span className="px-2 py-1 bg-indigo-900/40 rounded border border-indigo-500/30 text-indigo-200">
            ⏱ {(msgContent.duration_ms / 1000).toFixed(2)}s
          </span>
          <span className="px-2 py-1 bg-cyan-900/40 rounded border border-cyan-500/30 text-cyan-200">
            📊 {msgContent.row_count.toLocaleString()} rows
          </span>
        </div>

        {/* Reasoning Pathway */}
        {msgContent.pathway && msgContent.pathway.length > 0 && (
          <div className="mt-2 group">
            <details className="cursor-pointer">
              <summary className="text-[10px] text-cyan-400/70 font-mono flex items-center gap-2 hover:text-cyan-300 transition-colors uppercase tracking-[0.15em] py-1">
                <span className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse" />
                Neural Processing Pathway
              </summary>
              <div className="absolute inset-0 bg-linear-to-r from-primary/10 via-transparent to-primary/10 opacity-30 pointer-events-none" />
              <div className="pl-4 mt-2 border-l border-cyan-500/20 space-y-1.5 animate-in fade-in slide-in-from-top-1 duration-300">
                {msgContent.pathway.map((step, idx) => (
                  <div key={idx} className="flex gap-2 items-start group/step">
                    <span className="text-[10px] text-cyan-500 font-mono opacity-50">[{idx+1}]</span>
                    <p className="text-[11px] text-cyan-100/80 font-mono leading-tight group-hover/step:text-cyan-200 transition-colors">
                      {step}
                    </p>
                  </div>
                ))}
              </div>
            </details>
          </div>
        )}

        {/* Insights */}
        {msgContent.insights && msgContent.insights.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-indigo-300 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1 h-3 bg-indigo-500 rounded-full" />
              Intelligence Analysis
            </h4>
            <ul className="space-y-1.5">
              {msgContent.insights.map((insight, idx) => (
                <li key={idx} className="text-sm text-indigo-50/90 pl-3 border-l border-indigo-500/30 hover:border-indigo-400 transition-colors">
                  {insight}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Charts */}
        {msgContent.charts && msgContent.charts.length > 0 && (
          <div className="grid grid-cols-1 gap-4 mt-4 relative z-20">
            {msgContent.charts.map((chart, idx) => {
              if (!chart.fig_json) return null
              try {
                const fig = JSON.parse(chart.fig_json)
                // Enforce transparent background for UI theme
                if(fig.layout) {
                  fig.layout.paper_bgcolor = 'rgba(0,0,0,0)'
                  fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
                  fig.layout.font = { color: '#e0e0ff' }
                }
                return (
                  <div key={idx} className="w-full bg-black/20 rounded-xl overflow-hidden border border-indigo-500/20 shadow-inner">
                    <Plot
                      data={fig.data}
                      layout={{
                        ...fig.layout,
                        autosize: true,
                        margin: { l: 40, r: 20, t: 40, b: 40 }
                      }}
                      useResizeHandler={true}
                      style={{ width: '100%', height: '350px' }}
                      config={{ displayModeBar: false, responsive: true }}
                    />
                  </div>
                )
              } catch (e) {
                return <div key={idx} className="text-xs text-red-500">Failed to render chart data.</div>
              }
            })}
          </div>
        )}

            <div className="flex flex-wrap gap-2 pt-2">
              <Link
                href="/presentation"
                className="text-xs px-3 py-1.5 bg-purple-500/20 border border-purple-500/30 rounded-full hover:bg-purple-500/40 transition-colors text-purple-200 font-bold"
              >
                ✨ Generate Presentation
              </Link>
              {msgContent.followup_suggestions.map((sug, idx) => (
                <button 
                  key={idx}
                  onClick={() => setInput(sug)}
                  className="text-xs px-3 py-1.5 bg-indigo-500/10 border border-indigo-500/30 rounded-full hover:bg-indigo-500/30 transition-colors text-indigo-200"
                >
                  → {sug}
                </button>
              ))}
            </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-6 pr-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              'animate-slide-up',
              message.role === 'user' ? 'flex justify-end' : 'flex justify-start'
            )}
          >
            <div
              className={cn(
                'max-w-[85%] px-5 py-4 rounded-xl shadow-glow-sm',
                message.role === 'user'
                  ? 'bg-indigo-600/20 border border-cyan-400/30 text-cyan-50 self-end'
                  : 'bg-black/40 border border-indigo-500/20 text-indigo-50 glass w-full'
              )}
            >
              <div className="flex gap-3 mb-2 items-center">
                {message.role === 'assistant' && (
                  <div className="w-12 h-12 rounded-xl bg-linear-to-r from-primary to-indigo-600 flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
                    ⚡
                  </div>
                )}
                <span className="text-xs uppercase tracking-widest opacity-60 font-semibold font-mono">
                  {message.role === 'user' ? 'Operator' : 'J.A.R.V.I.S.'}
                </span>
              </div>
              
              {renderAIContent(message.content)}
              
              <span suppressHydrationWarning className="text-[10px] opacity-40 mt-3 block text-right">
                {message.timestamp.toLocaleTimeString('en-US', {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <LoadingState message="Neural analysis in progress..." size="sm" />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2 mb-3">
          {[
            'Analyze sales trends',
            'Show me growth metrics',
            'Compare regions',
          ].map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => setInput(suggestion)}
              className="text-xs px-3 py-1 rounded-full glass hover:glass-hover border border-border/50 transition-all duration-200"
            >
              {suggestion}
            </button>
          ))}
        </div>

        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSendMessage()
              }
            }}
            placeholder="Ask me anything about your data..."
            className="flex-1 px-4 py-3 rounded-lg glass border border-border/50 focus:border-indigo-500/50 focus:outline-none focus:ring-1 focus:ring-indigo-500/30 transition-all duration-200 text-sm"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !input.trim()}
            className={cn(
              'px-6 py-3 rounded-lg font-medium transition-all duration-200',
              isLoading || !input.trim()
                ? 'opacity-50 cursor-not-allowed glass'
                : 'glass-hover border-indigo-500/50 text-indigo-200 hover:shadow-glow'
            )}
          >
            {isLoading ? '...' : 'Send'}
          </button>
        </div>

        <NeonBadge variant="cyan" className="text-xs w-full text-center justify-center">
          💡 Tip: Upload your dataset or connect a data source to get started
        </NeonBadge>
      </div>
    </div>
  )
}
