# 🌌 InsightPulse AI: The Forensic Data Revolution
### 🏆 Official Submission for GFG Kolkata Hackathon 2026
**LIVE DASHBOARD**: [https://insight-pulse-gfg-kokata.vercel.app/](https://insight-pulse-gfg-kokata.vercel.app/)

**Project ID**: GFGK-2026-IPAI  
**Lead Architect**: Soumoditya Das  
**Advisory**: Sounak Mondal  

---

## 🌟 Vision
InsightPulse AI is a high-fidelity, Conversational Business Intelligence engine designed to eliminate the "Last Mile" problem in data analysis. It turns massive datasets into actionable intelligence through a **No-Fail Neural Pipeline**.

## 🚀 Key Innovation: The "No-Fail" 4-Stage Fallback
Unlike standard AI dashboards that break during high traffic or API downtime, our and architecture uses a **Neural Load Balancer**:
1.  **Stage 1 (Primary)**: Google Gemini 2.0 Flash (Optimized for Speed)
2.  **Stage 2 (Scale)**: Gemini 1.5 Pro (Deep Reasoning)
3.  **Stage 3 (Performance)**: OpenRouter/Claude 3.5 Sonnet
4.  **Stage 4 (Emergency)**: Free-Tier Neural Models (Fail-Safe)

## 🏗️ Technical Architecture
-   **Frontend**: Next.js 16 (Turbopack), Tailwind CSS, Framer Motion.
-   **Backend**: FastAPI (Python 3.12) Serverless Runtime.
-   **Data Engine**: DuckDB In-Memory OLAP (Sub-30ms execution on 50k+ rows).
-   **Visualization**: Plotly.js Georeferenced Mapping & Starfield UX.

## 🛠️ Deployment Configuration (Vercel)
The project is architected for **Automatic Full-Stack Initialization**.
-   **Frontend**: Deployed via `@vercel/next`
-   **Backend**: Deployed via `@vercel/python` (Serverless Functions)
-   **Route Orchestration**: Unified through a central `vercel.json` at the root.

## 📦 Getting Started
### 1. Requirements
-   Python 3.9+
-   Node.js 18+
-   Google AI Studio API Key

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/soumoditt-source/INSIGHT-PULSE-GFG-KOKATA.git

# Initialize Backend
cd InsightPulse_AI
pip install -r requirements.txt
python backend.py

# Initialize Frontend
cd ../frontend_extracted
npm install
npm run dev
```

## 🗺️ Live Showcase Visuals
| Feature | Capability |
| :--- | :--- |
| **Data Profiler** | Intelligent missing value detection & bplist00 binary guarding. |
| **Forensic Maps** | Dynamic dot-mapping and hotspot clustering. |
| **AI Forecasts** | Predictive linear regression for future trend projection. |

---
*Created for excellence at GFG Kolkata 2026. The 11/10 Standard.* 🚀
