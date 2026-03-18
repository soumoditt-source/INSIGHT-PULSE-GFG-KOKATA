import type { Metadata, Viewport } from 'next'
import { Outfit, Inter } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

const outfit = Outfit({
  subsets: ["latin"],
  variable: '--font-outfit',
  weight: ['400', '500', '600', '700', '800'],
})

const inter = Inter({
  subsets: ["latin"],
  variable: '--font-inter',
  weight: ['400', '500', '600'],
})

export const viewport: Viewport = {
  themeColor: '#080818',
  colorScheme: 'dark',
  userScalable: false,
}

export const metadata: Metadata = {
  title: 'InsightPulse AI - Sci-Fi Intelligence Bureau',
  description: 'The world\'s most advanced AI-powered intelligence bureau with real-time data visualization and predictive analytics',
  generator: 'v0.app',
  icons: {
    icon: [
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${outfit.variable} ${inter.variable} font-sans antialiased bg-background text-foreground`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
