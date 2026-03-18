# InsightPulse AI - Sci-Fi Intelligence Bureau

A cutting-edge, next-generation AI-powered intelligence platform built with React, Next.js, and advanced web technologies. Experience the future of data analysis with real-time visualizations, predictive analytics, and machine learning insights.

## ✨ Features

### 🎯 Core Capabilities
- **Neural Data Chat** - Conversational AI for natural language data queries
- **Real-Time Analytics** - Live data visualization and insights
- **Machine Learning Lab** - Classification, regression, clustering, and anomaly detection
- **Data Profiling** - Comprehensive dataset analysis and quality assessment
- **Geographic Intelligence** - Map-based data distribution and regional analytics
- **Query Audit Trail** - Complete history and performance metrics
- **Smart Dashboards** - Customizable intelligence boards with live updates

### 🎨 Design Excellence
- **Glassmorphic UI** - Modern, premium aesthetic with blur effects
- **Neon Color Palette** - Sci-fi inspired indigo, purple, cyan, and magenta theme
- **50+ Animations** - Smooth, captivating micro-interactions
- **Responsive Design** - Mobile-first approach (375px+)
- **Dark Mode** - Eye-friendly, energy-efficient interface

### ⚡ Performance
- **Zero White Screens** - Always-loaded states with realistic data
- **Optimized Rendering** - Smooth 60fps animations
- **Efficient Data Transfer** - Optimized API calls and caching
- **Production-Ready** - Battle-tested patterns and best practices

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- pnpm (recommended) or npm/yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/insightpulse-ai.git
cd insightpulse-ai

# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env.local

# Run development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
insightpulse-ai/
├── app/
│   ├── page.tsx              # Home page with hero and bento grid
│   ├── chat/
│   │   └── page.tsx          # Data chat interface
│   ├── ml-lab/
│   │   └── page.tsx          # Machine learning laboratory
│   ├── profiler/
│   │   └── page.tsx          # Data profiling tool
│   ├── maps/
│   │   └── page.tsx          # Geographic analytics
│   ├── history/
│   │   └── page.tsx          # Query audit trail
│   ├── dashboards/
│   │   └── page.tsx          # Smart dashboards
│   ├── layout.tsx            # Root layout with fonts and metadata
│   └── globals.css           # Global styles and animations
├── components/
│   ├── GlassCard.tsx         # Reusable glass morphic card
│   ├── NeonBadge.tsx         # Neon-styled badge component
│   ├── MetricCard.tsx        # KPI metric display
│   ├── LoadingState.tsx      # Loading indicator
│   ├── StarField.tsx         # Animated star background
│   ├── GlowingOrbs.tsx       # Floating animated orbs
│   ├── BentoGrid.tsx         # Responsive bento grid layout
│   ├── ChatUI.tsx            # Chat interface
│   ├── ChartPlaceholder.tsx  # Data visualization placeholder
│   ├── Sidebar.tsx           # Navigation sidebar
│   └── Topbar.tsx            # Top navigation bar
├── lib/
│   ├── api.ts                # API client service
│   └── utils.ts              # Utility functions (cn)
├── tailwind.config.ts        # Tailwind configuration
├── next.config.mjs           # Next.js configuration
├── tsconfig.json             # TypeScript configuration
└── package.json              # Project dependencies
```

## 🎨 Color System

The design uses exactly 5 colors for a cohesive sci-fi aesthetic:

- **Primary**: `#6366f1` (Indigo)
- **Secondary**: `#8b5cf6` (Purple)  
- **Accent**: `#ec4899` (Magenta)
- **Tertiary**: `#14b8a6` (Teal)
- **Background**: `#080818` (Deep Black)

## 🎬 Animations

50+ CSS animations bring the interface to life:

- `float` - Smooth floating motion
- `pulse-glow` - Pulsing opacity effect
- `shimmer` - Shimmer gradient animation
- `scan-line` - Sci-fi scan line effect
- `glow-pulse` - Box shadow glow animation
- `slide-up` - Entrance animation
- And many more...

## 🔗 API Integration

The app includes an API service layer for backend communication:

```typescript
import { apiClient } from '@/lib/api'

// Upload dataset
const result = await apiClient.uploadDataset(file)

// Generate query
const response = await apiClient.generateQuery('Show sales trends')

// Analyze with ML
const analysis = await apiClient.analyzeWithML(datasetId, 'classification')
```

Set `NEXT_PUBLIC_API_URL` in your `.env.local` to connect to your backend.

## 📊 Components Guide

### GlassCard
Reusable container with glassmorphism effect
```tsx
<GlassCard hover glow>
  Your content here
</GlassCard>
```

### MetricCard
Display KPIs with trending data
```tsx
<MetricCard 
  label="Total Sales"
  value="$2.4M"
  trend={{ value: 28, direction: 'up' }}
/>
```

### BentoGrid
Responsive grid layout for features
```tsx
<BentoGrid>
  <BentoGridItem title="Feature" icon="📊" span="double">
    Content
  </BentoGridItem>
</BentoGrid>
```

## 🚀 Deployment

### Vercel (Recommended)
```bash
# Push to GitHub and connect to Vercel
pnpm run build
```

### Docker
```bash
docker build -t insightpulse-ai .
docker run -p 3000:3000 insightpulse-ai
```

## 🛠️ Tech Stack

- **Framework**: Next.js 16
- **UI Library**: React 19
- **Styling**: Tailwind CSS
- **Fonts**: Outfit + Inter (Google Fonts)
- **Animations**: CSS Keyframes
- **Package Manager**: pnpm
- **Language**: TypeScript

## 📝 Environment Variables

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Analytics (Optional)
NEXT_PUBLIC_VERCEL_ANALYTICS_ID=
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Design inspiration from cutting-edge sci-fi interfaces
- Built with Next.js and modern web technologies
- Community-driven improvements and feedback

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check our documentation
- Join our community Discord

---

**InsightPulse AI** - The Future of Data Intelligence. Built for those who demand the best.
