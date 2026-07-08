<div align="center">

<!-- ANIMATED HERO BANNER -->
<svg width="100%" height="280" viewBox="0 0 1200 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradients -->
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#1e293b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f172a;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#8b5cf6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ec4899;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#22d3ee;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#a78bfa;stop-opacity:0.8" />
    </linearGradient>
    <!-- Glow Filter -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <!-- Pulse Animation -->
    <style>
      .pulse { animation: pulse 2s infinite; }
      @keyframes pulse {
        0% { opacity: 0.4; r: 3; }
        50% { opacity: 1; r: 6; }
        100% { opacity: 0.4; r: 3; }
      }
      .dash { stroke-dasharray: 10; animation: dash 1s linear infinite; }
      @keyframes dash { to { stroke-dashoffset: -20; } }
      .float { animation: float 6s ease-in-out infinite; }
      @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
      }
      .neon { filter: url(#glow); }
      .typewriter { animation: blink 1s infinite; }
      @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
      .spin-slow { animation: spin 8s linear infinite; transform-origin: center; }
      @keyframes spin { 100% { transform: rotate(360deg); } }
      .orbit { animation: orbit 4s linear infinite; }
      @keyframes orbit {
        0% { transform: translate(0, 0); }
        25% { transform: translate(5px, -5px); }
        50% { transform: translate(0, -8px); }
        75% { transform: translate(-5px, -5px); }
        100% { transform: translate(0, 0); }
      }
    </style>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="url(#grad1)" rx="20"/>

  <!-- Animated Grid Lines -->
  <g opacity="0.1">
    <line x1="0" y1="70" x2="1200" y2="70" stroke="#22d3ee" stroke-width="1" class="dash"/>
    <line x1="0" y1="140" x2="1200" y2="140" stroke="#a78bfa" stroke-width="1" class="dash"/>
    <line x1="0" y1="210" x2="1200" y2="210" stroke="#ec4899" stroke-width="1" class="dash"/>
  </g>

  <!-- Neural Network Nodes Background -->
  <g opacity="0.3">
    <circle cx="100" cy="50" r="3" fill="#22d3ee" class="pulse"/>
    <circle cx="250" cy="80" r="4" fill="#a78bfa" class="pulse" style="animation-delay:0.3s"/>
    <circle cx="180" cy="200" r="3" fill="#ec4899" class="pulse" style="animation-delay:0.6s"/>
    <circle cx="350" cy="150" r="4" fill="#22d3ee" class="pulse" style="animation-delay:0.9s"/>
    <circle cx="900" cy="60" r="3" fill="#a78bfa" class="pulse" style="animation-delay:1.2s"/>
    <circle cx="1050" cy="120" r="4" fill="#ec4899" class="pulse" style="animation-delay:1.5s"/>
    <circle cx="980" cy="220" r="3" fill="#22d3ee" class="pulse" style="animation-delay:1.8s"/>
    <circle cx="1100" cy="180" r="4" fill="#a78bfa" class="pulse" style="animation-delay:2.1s"/>
    <!-- Neural Connections -->
    <line x1="100" y1="50" x2="250" y2="80" stroke="#22d3ee" stroke-width="0.5" opacity="0.5" class="dash"/>
    <line x1="250" y1="80" x2="350" y2="150" stroke="#a78bfa" stroke-width="0.5" opacity="0.5" class="dash"/>
    <line x1="180" y1="200" x2="350" y2="150" stroke="#ec4899" stroke-width="0.5" opacity="0.5" class="dash"/>
    <line x1="900" y1="60" x2="1050" y2="120" stroke="#22d3ee" stroke-width="0.5" opacity="0.5" class="dash"/>
    <line x1="1050" y1="120" x2="980" y2="220" stroke="#a78bfa" stroke-width="0.5" opacity="0.5" class="dash"/>
    <line x1="980" y1="220" x2="1100" y2="180" stroke="#ec4899" stroke-width="0.5" opacity="0.5" class="dash"/>
  </g>

  <!-- Central Brain/Network Icon -->
  <g transform="translate(600, 140)" class="float">
    <circle r="50" fill="none" stroke="url(#grad2)" stroke-width="3" filter="url(#glow)" opacity="0.8"/>
    <circle r="35" fill="none" stroke="#22d3ee" stroke-width="2" opacity="0.6" class="spin-slow"/>
    <circle r="20" fill="url(#grad2)" opacity="0.3"/>
    <text x="0" y="8" text-anchor="middle" fill="#fff" font-size="24" font-weight="bold" font-family="monospace">⚕</text>
    <!-- Orbiting dots -->
    <circle r="4" fill="#22d3ee" class="orbit">
      <animateMotion dur="4s" repeatCount="indefinite" path="M 50,0 A 50,50 0 1,1 50,0.1"/>
    </circle>
    <circle r="3" fill="#ec4899" class="orbit" style="animation-delay:1.3s">
      <animateMotion dur="3s" repeatCount="indefinite" path="M 0,50 A 50,50 0 1,1 0.1,50"/>
    </circle>
  </g>

  <!-- Title -->
  <text x="600" y="60" text-anchor="middle" fill="url(#grad2)" font-size="42" font-weight="bold" font-family="Segoe UI, sans-serif" filter="url(#glow)" class="neon">CLINIC MANAGEMENT SYSTEM</text>
  <text x="600" y="95" text-anchor="middle" fill="#94a3b8" font-size="18" font-family="Segoe UI, sans-serif">Multi-Tenant Neural Architecture</text>

  <!-- Animated Underline -->
  <line x1="400" y1="110" x2="800" y2="110" stroke="url(#grad2)" stroke-width="3" stroke-linecap="round" filter="url(#glow)">
    <animate attributeName="x2" values="400;800;400" dur="3s" repeatCount="indefinite"/>
  </line>

  <!-- Bottom Stats -->
  <g transform="translate(0, 240)">
    <text x="300" y="0" text-anchor="middle" fill="#22d3ee" font-size="14" font-family="monospace">◉ Multi-Tenant</text>
    <text x="600" y="0" text-anchor="middle" fill="#a78bfa" font-size="14" font-family="monospace">◉ Role-Based</text>
    <text x="900" y="0" text-anchor="middle" fill="#ec4899" font-size="14" font-family="monospace">◉ Real-Time</text>
  </g>
</svg>

<!-- Animated Subtitle -->
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=22D3EE&center=true&vCenter=true&width=600&lines=Multi-Tenant+Clinic+Platform;Neural+Workflow+Architecture;Real-Time+Appointment+System;Role-Based+Access+Control" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-0f172a?style=for-the-badge&logo=python&logoColor=22d3ee&labelColor=1e293b"/>
  <img src="https://img.shields.io/badge/Flask-2.3+-0f172a?style=for-the-badge&logo=flask&logoColor=a78bfa&labelColor=1e293b"/>
  <img src="https://img.shields.io/badge/SQLite-3.0+-0f172a?style=for-the-badge&logo=sqlite&logoColor=ec4899&labelColor=1e293b"/>
  <img src="https://img.shields.io/badge/Jinja2-Templates-0f172a?style=for-the-badge&logo=jinja&logoColor=22d3ee&labelColor=1e293b"/>
</p>

</div>

---

## 🚀 Quick Installation

> **Get the system running in under 2 minutes**

```bash
# 1. Clone the repository
git clone <repository-url>
cd clinic-management

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Initialize database (auto-creates instance/clinic.db)
python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"

# 6. Run the application
python run.py
```

**Access the application:**
- 🌐 **Web App:** `http://localhost:5000`
- 🔑 **Login:** Use your configured credentials

---

## 📋 Project Overview

<div align="center">

<!-- ANIMATED OVERVIEW BANNER -->
<svg width="100%" height="120" viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ovGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0f172a"/>
      <stop offset="100%" style="stop-color:#1e293b"/>
    </linearGradient>
    <style>
      .ov-pulse { animation: ovPulse 2s infinite; }
      @keyframes ovPulse { 0%,100% { opacity:0.3; } 50% { opacity:1; } }
      .ov-slide { animation: ovSlide 3s ease-in-out infinite; }
      @keyframes ovSlide { 0%,100% { transform:translateX(0); } 50% { transform:translateX(10px); } }
    </style>
  </defs>
  <rect width="100%" height="100%" fill="url(#ovGrad)" rx="12"/>
  <g transform="translate(100, 60)">
    <rect x="-40" y="-30" width="80" height="60" rx="10" fill="#22d3ee" opacity="0.2" stroke="#22d3ee" stroke-width="2"/>
    <text x="0" y="5" text-anchor="middle" fill="#22d3ee" font-size="12" font-family="monospace">PATIENT</text>
    <circle cx="50" cy="0" r="3" fill="#22d3ee" class="ov-pulse"/>
    <line x1="50" y1="0" x2="150" y2="0" stroke="#22d3ee" stroke-width="2" stroke-dasharray="5,5">
      <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1s" repeatCount="indefinite"/>
    </line>
  </g>
  <g transform="translate(350, 60)">
    <rect x="-40" y="-30" width="80" height="60" rx="10" fill="#a78bfa" opacity="0.2" stroke="#a78bfa" stroke-width="2"/>
    <text x="0" y="5" text-anchor="middle" fill="#a78bfa" font-size="12" font-family="monospace">CLINIC</text>
    <circle cx="50" cy="0" r="3" fill="#a78bfa" class="ov-pulse" style="animation-delay:0.5s"/>
    <line x1="50" y1="0" x2="150" y2="0" stroke="#a78bfa" stroke-width="2" stroke-dasharray="5,5">
      <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1s" repeatCount="indefinite"/>
    </line>
  </g>
  <g transform="translate(600, 60)">
    <rect x="-40" y="-30" width="80" height="60" rx="10" fill="#ec4899" opacity="0.2" stroke="#ec4899" stroke-width="2"/>
    <text x="0" y="5" text-anchor="middle" fill="#ec4899" font-size="12" font-family="monospace">ADMIN</text>
    <circle cx="50" cy="0" r="3" fill="#ec4899" class="ov-pulse" style="animation-delay:1s"/>
    <line x1="50" y1="0" x2="150" y2="0" stroke="#ec4899" stroke-width="2" stroke-dasharray="5,5">
      <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1s" repeatCount="indefinite"/>
    </line>
  </g>
  <g transform="translate(850, 60)">
    <rect x="-50" y="-30" width="100" height="60" rx="10" fill="#f59e0b" opacity="0.2" stroke="#f59e0b" stroke-width="2"/>
    <text x="0" y="5" text-anchor="middle" fill="#f59e0b" font-size="12" font-family="monospace">SUPER ADMIN</text>
    <circle cx="60" cy="0" r="3" fill="#f59e0b" class="ov-pulse" style="animation-delay:1.5s"/>
  </g>
</svg>

</div>

A **multi-tenant clinic management platform** built with Flask and SQLite. Features role-based access control, appointment scheduling, patient management, and company-level data isolation. Designed for healthcare providers managing multiple clinics under a single unified platform.

---

## 🏗️ System Architecture

<div align="center">

```mermaid
graph TB
    subgraph CLIENT["🖥️ CLIENT LAYER"]
        A[Browser/HTML5]
        B[Mobile Responsive]
    end

    subgraph APPLICATION["⚡ APPLICATION LAYER"]
        C[Flask App Server]
        D[Jinja2 Templates]
        E[WTForms Validation]
        F[Flask-Login Sessions]
    end

    subgraph ROUTES["🛣️ ROUTE CONTROLLERS"]
        G[Auth Routes]
        H[Patient Routes]
        I[Admin Routes]
        J[Super Admin Routes]
        K[Main Routes]
    end

    subgraph DATA["🗄️ DATA LAYER"]
        L[(SQLite clinic.db)]
        M[SQLAlchemy ORM]
        N[User Model]
        O[Company Model]
        P[PatientProfile Model]
        Q[Appointment Model]
    end

    A -->|HTTP/HTTPS| C
    B -->|HTTP/HTTPS| C
    C --> D
    C --> E
    C --> F
    C --> G
    C --> H
    C --> I
    C --> J
    C --> K
    G --> M
    H --> M
    I --> M
    J --> M
    K --> M
    M --> L
    M --> N
    M --> O
    M --> P
    M --> Q

    style CLIENT fill:#0f172a,stroke:#22d3ee,stroke-width:3px,color:#fff
    style APPLICATION fill:#0f172a,stroke:#a78bfa,stroke-width:3px,color:#fff
    style ROUTES fill:#0f172a,stroke:#ec4899,stroke-width:3px,color:#fff
    style DATA fill:#0f172a,stroke:#f59e0b,stroke-width:3px,color:#fff
    style A fill:#1e293b,stroke:#22d3ee,color:#22d3ee
    style B fill:#1e293b,stroke:#22d3ee,color:#22d3ee
    style C fill:#1e293b,stroke:#a78bfa,color:#a78bfa
    style L fill:#1e293b,stroke:#f59e0b,color:#f59e0b
```

</div>

---

## 🧠 Neural Workflow Engine

<div align="center">

<!-- ANIMATED NEURAL NETWORK DIAGRAM -->
<svg width="100%" height="500" viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="nGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a"/>
      <stop offset="100%" style="stop-color:#1e293b"/>
    </linearGradient>
    <radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#22d3ee;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#22d3ee;stop-opacity:0"/>
    </radialGradient>
    <radialGradient id="nodeGlow2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#a78bfa;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#a78bfa;stop-opacity:0"/>
    </radialGradient>
    <radialGradient id="nodeGlow3" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#ec4899;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#ec4899;stop-opacity:0"/>
    </radialGradient>
    <style>
      .n-bg { fill: url(#nGrad1); }
      .n-line { stroke-width: 2; fill: none; opacity: 0.6; }
      .n-line-anim { stroke-dasharray: 10; animation: nDash 1s linear infinite; }
      @keyframes nDash { to { stroke-dashoffset: -20; } }
      .n-node { r: 8; }
      .n-pulse { animation: nPulse 2s infinite; }
      @keyframes nPulse { 0%,100% { r: 8; opacity: 0.8; } 50% { r: 12; opacity: 1; } }
      .n-label { fill: #e2e8f0; font-family: 'Segoe UI', sans-serif; font-size: 11px; font-weight: 600; text-anchor: middle; }
      .n-title { fill: #22d3ee; font-family: 'Segoe UI', sans-serif; font-size: 24px; font-weight: bold; text-anchor: middle; filter: drop-shadow(0 0 8px #22d3ee); }
      .n-layer-label { fill: #94a3b8; font-family: monospace; font-size: 10px; text-anchor: middle; }
    </style>
  </defs>

  <rect width="100%" height="100%" class="n-bg" rx="16"/>

  <!-- Title -->
  <text x="500" y="40" class="n-title">NEURAL WORKFLOW ENGINE</text>

  <!-- Layer Labels -->
  <text x="100" y="80" class="n-layer-label">◉ INPUT LAYER</text>
  <text x="350" y="80" class="n-layer-label">◉ HIDDEN LAYER 1</text>
  <text x="600" y="80" class="n-layer-label">◉ HIDDEN LAYER 2</text>
  <text x="850" y="80" class="n-layer-label">◉ OUTPUT LAYER</text>

  <!-- INPUT LAYER -->
  <g transform="translate(100, 130)">
    <circle class="n-node n-pulse" fill="#22d3ee"/>
    <circle r="20" fill="url(#nodeGlow)" class="n-pulse"/>
    <text y="35" class="n-label">Auth Request</text>
  </g>
  <g transform="translate(100, 220)">
    <circle class="n-node n-pulse" fill="#22d3ee" style="animation-delay:0.3s"/>
    <circle r="20" fill="url(#nodeGlow)" class="n-pulse" style="animation-delay:0.3s"/>
    <text y="35" class="n-label">Form Data</text>
  </g>
  <g transform="translate(100, 310)">
    <circle class="n-node n-pulse" fill="#22d3ee" style="animation-delay:0.6s"/>
    <circle r="20" fill="url(#nodeGlow)" class="n-pulse" style="animation-delay:0.6s"/>
    <text y="35" class="n-label">File Upload</text>
  </g>
  <g transform="translate(100, 400)">
    <circle class="n-node n-pulse" fill="#22d3ee" style="animation-delay:0.9s"/>
    <circle r="20" fill="url(#nodeGlow)" class="n-pulse" style="animation-delay:0.9s"/>
    <text y="35" class="n-label">API Call</text>
  </g>

  <!-- HIDDEN LAYER 1 -->
  <g transform="translate(350, 130)">
    <circle class="n-node n-pulse" fill="#a78bfa" style="animation-delay:0.2s"/>
    <circle r="20" fill="url(#nodeGlow2)" class="n-pulse" style="animation-delay:0.2s"/>
    <text y="35" class="n-label">Validation</text>
  </g>
  <g transform="translate(350, 220)">
    <circle class="n-node n-pulse" fill="#a78bfa" style="animation-delay:0.5s"/>
    <circle r="20" fill="url(#nodeGlow2)" class="n-pulse" style="animation-delay:0.5s"/>
    <text y="35" class="n-label">Sanitization</text>
  </g>
  <g transform="translate(350, 310)">
    <circle class="n-node n-pulse" fill="#a78bfa" style="animation-delay:0.8s"/>
    <circle r="20" fill="url(#nodeGlow2)" class="n-pulse" style="animation-delay:0.8s"/>
    <text y="35" class="n-label">Encryption</text>
  </g>
  <g transform="translate(350, 400)">
    <circle class="n-node n-pulse" fill="#a78bfa" style="animation-delay:1.1s"/>
    <circle r="20" fill="url(#nodeGlow2)" class="n-pulse" style="animation-delay:1.1s"/>
    <text y="35" class="n-label">Rate Limit</text>
  </g>

  <!-- HIDDEN LAYER 2 -->
  <g transform="translate(600, 160)">
    <circle class="n-node n-pulse" fill="#ec4899" style="animation-delay:0.4s"/>
    <circle r="20" fill="url(#nodeGlow3)" class="n-pulse" style="animation-delay:0.4s"/>
    <text y="35" class="n-label">Role Check</text>
  </g>
  <g transform="translate(600, 260)">
    <circle class="n-node n-pulse" fill="#ec4899" style="animation-delay:0.7s"/>
    <circle r="20" fill="url(#nodeGlow3)" class="n-pulse" style="animation-delay:0.7s"/>
    <text y="35" class="n-label">Tenant Filter</text>
  </g>
  <g transform="translate(600, 360)">
    <circle class="n-node n-pulse" fill="#ec4899" style="animation-delay:1.0s"/>
    <circle r="20" fill="url(#nodeGlow3)" class="n-pulse" style="animation-delay:1.0s"/>
    <text y="35" class="n-label">Permission</text>
  </g>

  <!-- OUTPUT LAYER -->
  <g transform="translate(850, 200)">
    <circle class="n-node n-pulse" fill="#f59e0b" style="animation-delay:0.6s"/>
    <circle r="20" fill="url(#nodeGlow)" class="n-pulse" style="animation-delay:0.6s"/>
    <text y="35" class="n-label">HTML Render</text>
  </g>
  <g transform="translate(850, 320)">
    <circle class="n-node n-pulse" fill="#f59e0b" style="animation-delay:0.9s"/>
    <circle r="20" fill="url(#nodeGlow)" class="n-pulse" style="animation-delay:0.9s"/>
    <text y="35" class="n-label">JSON Response</text>
  </g>

  <!-- CONNECTIONS (Animated) -->
  <!-- Input to Hidden 1 -->
  <line x1="108" y1="130" x2="342" y2="130" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="108" y1="130" x2="342" y2="220" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="108" y1="220" x2="342" y2="130" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="108" y1="220" x2="342" y2="220" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="108" y1="220" x2="342" y2="310" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="108" y1="310" x2="342" y2="220" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="108" y1="310" x2="342" y2="310" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="108" y1="310" x2="342" y2="400" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="108" y1="400" x2="342" y2="310" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="108" y1="400" x2="342" y2="400" stroke="#22d3ee" class="n-line n-line-anim" opacity="0.4"/>

  <!-- Hidden 1 to Hidden 2 -->
  <line x1="358" y1="130" x2="592" y2="160" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="358" y1="130" x2="592" y2="260" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="358" y1="220" x2="592" y2="160" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="358" y1="220" x2="592" y2="260" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="358" y1="220" x2="592" y2="360" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="358" y1="310" x2="592" y2="260" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="358" y1="310" x2="592" y2="360" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="358" y1="400" x2="592" y2="360" stroke="#a78bfa" class="n-line n-line-anim" opacity="0.3"/>

  <!-- Hidden 2 to Output -->
  <line x1="608" y1="160" x2="842" y2="200" stroke="#ec4899" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="608" y1="160" x2="842" y2="320" stroke="#ec4899" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="608" y1="260" x2="842" y2="200" stroke="#ec4899" class="n-line n-line-anim" opacity="0.3"/>
  <line x1="608" y1="260" x2="842" y2="320" stroke="#ec4899" class="n-line n-line-anim" opacity="0.4"/>
  <line x1="608" y1="360" x2="842" y2="320" stroke="#ec4899" class="n-line n-line-anim" opacity="0.3"/>

  <!-- Animated Data Packets -->
  <circle r="3" fill="#fff">
    <animateMotion dur="1.5s" repeatCount="indefinite" path="M 108,130 Q 225,130 342,130"/>
  </circle>
  <circle r="3" fill="#fff">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 108,220 Q 225,275 342,310"/>
  </circle>
  <circle r="3" fill="#fff">
    <animateMotion dur="1.8s" repeatCount="indefinite" path="M 358,220 Q 475,290 592,360"/>
  </circle>
  <circle r="3" fill="#fff">
    <animateMotion dur="2.2s" repeatCount="indefinite" path="M 608,260 Q 725,260 842,200"/>
  </circle>
</svg>

</div>

---

## 🗄️ Database Schema (Entity Relationship)

<div align="center">

```mermaid
erDiagram
    USERS ||--o{ COMPANIES : "manages"
    USERS ||--o| PATIENT_PROFILES : "has"
    USERS ||--o{ APPOINTMENTS : "books"
    USERS ||--o{ APPOINTMENTS : "diagnoses"
    COMPANIES ||--o{ PATIENT_PROFILES : "contains"
    COMPANIES ||--o{ APPOINTMENTS : "schedules"

    USERS {
        int id PK
        string username UK
        string password
        string email UK
        string phone
        string role
        string profile_picture
        boolean is_active
        datetime created_at
    }

    COMPANIES {
        int id PK
        string name
        int admin_id FK
        string country
        string city
        string currency
        string timezone
        string address
        string phone
        string email
        string logo
        text description
        datetime created_at
    }

    PATIENT_PROFILES {
        int id PK
        int user_id FK
        int company_id FK
        string full_name
        int age
        string gender
        text address
        string emergency_contact
        text medical_history
        datetime created_at
    }

    APPOINTMENTS {
        int id PK
        int patient_id FK
        int company_id FK
        int doctor_id FK
        date appointment_date
        string time_slot
        text notes
        string status
        float amount
        string payment_method
        string payment_status
        datetime created_at
        datetime updated_at
    }
```

</div>

---

## 🔄 User Role Flow Matrix

<div align="center">

<!-- ANIMATED ROLE FLOW DIAGRAM -->
<svg width="100%" height="400" viewBox="0 0 1000 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rfGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a"/>
      <stop offset="100%" style="stop-color:#1e293b"/>
    </linearGradient>
    <style>
      .rf-bg { fill: url(#rfGrad); }
      .rf-box { rx: 12; }
      .rf-title { fill: #fff; font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: bold; text-anchor: middle; }
      .rf-item { fill: #cbd5e1; font-family: 'Segoe UI', sans-serif; font-size: 11px; }
      .rf-connector { stroke-width: 2; fill: none; stroke-dasharray: 8; animation: rfDash 1s linear infinite; }
      @keyframes rfDash { to { stroke-dashoffset: -16; } }
      .rf-node { animation: rfPulse 2s infinite; }
      @keyframes rfPulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }
    </style>
  </defs>

  <rect width="100%" height="100%" class="rf-bg" rx="16"/>

  <!-- Super Admin Box -->
  <g transform="translate(50, 80)">
    <rect width="200" height="240" class="rf-box" fill="#f59e0b" opacity="0.15" stroke="#f59e0b" stroke-width="2"/>
    <text x="100" y="30" class="rf-title" fill="#f59e0b">👑 SUPER ADMIN</text>
    <text x="20" y="60" class="rf-item">◉ Manage All Companies</text>
    <text x="20" y="85" class="rf-item">◉ View All Users</text>
    <text x="20" y="110" class="rf-item">◉ System Configuration</text>
    <text x="20" y="135" class="rf-item">◉ Global Analytics</text>
    <text x="20" y="160" class="rf-item">◉ Role Assignment</text>
    <text x="20" y="185" class="rf-item">◉ Database Access</text>
    <text x="20" y="210" class="rf-item">◉ Audit Logs</text>
    <circle cx="200" cy="120" r="6" fill="#f59e0b" class="rf-node"/>
  </g>

  <!-- Admin Box -->
  <g transform="translate(350, 80)">
    <rect width="200" height="240" class="rf-box" fill="#ec4899" opacity="0.15" stroke="#ec4899" stroke-width="2"/>
    <text x="100" y="30" class="rf-title" fill="#ec4899">🔧 ADMIN</text>
    <text x="20" y="60" class="rf-item">◉ Manage Own Company</text>
    <text x="20" y="85" class="rf-item">◉ View Patients</text>
    <text x="20" y="110" class="rf-item">◉ Manage Appointments</text>
    <text x="20" y="135" class="rf-item">◉ Doctor Assignment</text>
    <text x="20" y="160" class="rf-item">◉ Company Settings</text>
    <text x="20" y="185" class="rf-item">◉ Payment Tracking</text>
    <text x="20" y="210" class="rf-item">◉ Reports &amp; Records</text>
    <circle cx="0" cy="120" r="6" fill="#ec4899" class="rf-node" style="animation-delay:0.5s"/>
    <circle cx="200" cy="120" r="6" fill="#ec4899" class="rf-node" style="animation-delay:0.5s"/>
  </g>

  <!-- Doctor Box -->
  <g transform="translate(650, 80)">
    <rect width="200" height="240" class="rf-box" fill="#a78bfa" opacity="0.15" stroke="#a78bfa" stroke-width="2"/>
    <text x="100" y="30" class="rf-title" fill="#a78bfa">👨‍⚕️ DOCTOR</text>
    <text x="20" y="60" class="rf-item">◉ View Assigned Patients</text>
    <text x="20" y="85" class="rf-item">◉ Update Diagnoses</text>
    <text x="20" y="110" class="rf-item">◉ Manage Schedule</text>
    <text x="20" y="135" class="rf-item">◉ Write Prescriptions</text>
    <text x="20" y="160" class="rf-item">◉ Medical Records</text>
    <text x="20" y="185" class="rf-item">◉ Appointment Notes</text>
    <text x="20" y="210" class="rf-item">◉ Patient History</text>
    <circle cx="0" cy="120" r="6" fill="#a78bfa" class="rf-node" style="animation-delay:1s"/>
    <circle cx="200" cy="120" r="6" fill="#a78bfa" class="rf-node" style="animation-delay:1s"/>
  </g>

  <!-- Patient Box -->
  <g transform="translate(350, 340)">
    <rect width="300" height="40" class="rf-box" fill="#22d3ee" opacity="0.15" stroke="#22d3ee" stroke-width="2"/>
    <text x="150" y="25" class="rf-title" fill="#22d3ee">🧑‍⚕️ PATIENT</text>
    <circle cx="0" cy="20" r="6" fill="#22d3ee" class="rf-node" style="animation-delay:1.5s"/>
  </g>

  <!-- Flow Lines -->
  <line x1="256" y1="200" x2="344" y2="200" stroke="#f59e0b" class="rf-connector"/>
  <line x1="556" y1="200" x2="644" y2="200" stroke="#ec4899" class="rf-connector"/>
  <line x1="750" y1="320" x2="500" y2="340" stroke="#a78bfa" class="rf-connector"/>
  <line x1="500" y1="320" x2="500" y2="340" stroke="#22d3ee" class="rf-connector"/>

  <!-- Animated Dots on Lines -->
  <circle r="4" fill="#f59e0b">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 256,200 L 344,200"/>
  </circle>
  <circle r="4" fill="#ec4899">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 556,200 L 644,200"/>
  </circle>
  <circle r="4" fill="#a78bfa">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 750,320 L 500,340"/>
  </circle>
</svg>

</div>

---

## 🌊 Patient Journey Flowchart

<div align="center">

```mermaid
flowchart LR
    A[🧑 Patient Login] -->|Auth Success| B{🔐 Role Check}
    B -->|Patient| C[🏥 Select Clinic]
    C --> D[📋 View Company Details]
    D --> E[📅 Book Appointment]
    E --> F[⏰ Choose Time Slot]
    F --> G[💳 Payment Info]
    G --> H[✅ Confirm Booking]
    H --> I[📊 Dashboard]
    I --> J[📝 My Appointments]

    B -->|Admin| K[⚙️ Admin Dashboard]
    K --> L[👥 Manage Patients]
    K --> M[📅 Manage Appointments]
    K --> N[📈 View Records]

    B -->|Super Admin| O[👑 Super Dashboard]
    O --> P[🏢 All Companies]
    O --> Q[👤 All Users]
    O --> R[🌍 Global Settings]

    style A fill:#0f172a,stroke:#22d3ee,stroke-width:3px,color:#22d3ee
    style B fill:#0f172a,stroke:#f59e0b,stroke-width:3px,color:#f59e0b
    style C fill:#0f172a,stroke:#a78bfa,stroke-width:2px,color:#a78bfa
    style E fill:#0f172a,stroke:#22d3ee,stroke-width:2px,color:#22d3ee
    style H fill:#0f172a,stroke:#22d3ee,stroke-width:3px,color:#22d3ee
    style K fill:#0f172a,stroke:#ec4899,stroke-width:3px,color:#ec4899
    style O fill:#0f172a,stroke:#f59e0b,stroke-width:3px,color:#f59e0b
```

</div>

---

## 🔐 Security & Authentication Flow

<div align="center">

<!-- ANIMATED SECURITY FLOW -->
<svg width="100%" height="350" viewBox="0 0 1000 350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="secGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0f172a"/>
      <stop offset="100%" style="stop-color:#1e293b"/>
    </linearGradient>
    <style>
      .sec-bg { fill: url(#secGrad); }
      .sec-hex { stroke-width: 3; fill-opacity: 0.1; }
      .sec-text { fill: #e2e8f0; font-family: 'Segoe UI', sans-serif; font-size: 13px; font-weight: 600; text-anchor: middle; }
      .sec-line { stroke-width: 2.5; fill: none; stroke-dasharray: 12; animation: secDash 1.2s linear infinite; }
      @keyframes secDash { to { stroke-dashoffset: -24; } }
      .sec-shield { animation: secShield 3s ease-in-out infinite; }
      @keyframes secShield { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
      .sec-glow { filter: drop-shadow(0 0 6px currentColor); }
    </style>
  </defs>

  <rect width="100%" height="100%" class="sec-bg" rx="16"/>

  <!-- Title -->
  <text x="500" y="40" fill="#22d3ee" font-family="Segoe UI" font-size="22" font-weight="bold" text-anchor="middle" class="sec-glow">🔐 SECURITY AUTHENTICATION PIPELINE</text>

  <!-- Step 1: Request -->
  <g transform="translate(100, 200)">
    <path d="M 0,-50 L 43,-25 L 43,25 L 0,50 L -43,25 L -43,-25 Z" class="sec-hex" stroke="#22d3ee" fill="#22d3ee"/>
    <text y="5" class="sec-text" fill="#22d3ee">REQUEST</text>
  </g>

  <!-- Step 2: Validate -->
  <g transform="translate(300, 200)">
    <path d="M 0,-50 L 43,-25 L 43,25 L 0,50 L -43,25 L -43,-25 Z" class="sec-hex" stroke="#a78bfa" fill="#a78bfa"/>
    <text y="5" class="sec-text" fill="#a78bfa">VALIDATE</text>
  </g>

  <!-- Step 3: Session -->
  <g transform="translate(500, 200)">
    <path d="M 0,-50 L 43,-25 L 43,25 L 0,50 L -43,25 L -43,-25 Z" class="sec-hex" stroke="#ec4899" fill="#ec4899"/>
    <text y="5" class="sec-text" fill="#ec4899">SESSION</text>
  </g>

  <!-- Step 4: Role Check -->
  <g transform="translate(700, 200)">
    <path d="M 0,-50 L 43,-25 L 43,25 L 0,50 L -43,25 L -43,-25 Z" class="sec-hex" stroke="#f59e0b" fill="#f59e0b"/>
    <text y="5" class="sec-text" fill="#f59e0b">ROLE CHECK</text>
  </g>

  <!-- Step 5: Access -->
  <g transform="translate(900, 200)">
    <path d="M 0,-50 L 43,-25 L 43,25 L 0,50 L -43,25 L -43,-25 Z" class="sec-hex" stroke="#22d3ee" fill="#22d3ee"/>
    <text y="5" class="sec-text" fill="#22d3ee">ACCESS</text>
  </g>

  <!-- Connection Lines -->
  <line x1="143" y1="200" x2="257" y2="200" stroke="#22d3ee" class="sec-line"/>
  <line x1="343" y1="200" x2="457" y2="200" stroke="#a78bfa" class="sec-line"/>
  <line x1="543" y1="200" x2="657" y2="200" stroke="#ec4899" class="sec-line"/>
  <line x1="743" y1="200" x2="857" y2="200" stroke="#f59e0b" class="sec-line"/>

  <!-- Animated Data Packets -->
  <circle r="5" fill="#fff" class="sec-shield">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 143,200 L 257,200"/>
  </circle>
  <circle r="5" fill="#fff" class="sec-shield" style="animation-delay:0.4s">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 343,200 L 457,200"/>
  </circle>
  <circle r="5" fill="#fff" class="sec-shield" style="animation-delay:0.8s">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 543,200 L 657,200"/>
  </circle>
  <circle r="5" fill="#fff" class="sec-shield" style="animation-delay:1.2s">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 743,200 L 857,200"/>
  </circle>

  <!-- Bottom Labels -->
  <text x="100" y="290" fill="#64748b" font-family="monospace" font-size="10" text-anchor="middle">HTTP POST /login</text>
  <text x="300" y="290" fill="#64748b" font-family="monospace" font-size="10" text-anchor="middle">WTForms + Hash</text>
  <text x="500" y="290" fill="#64748b" font-family="monospace" font-size="10" text-anchor="middle">Flask-Login</text>
  <text x="700" y="290" fill="#64748b" font-family="monospace" font-size="10" text-anchor="middle">@role_required</text>
  <text x="900" y="290" fill="#64748b" font-family="monospace" font-size="10" text-anchor="middle">Render Template</text>
</svg>

</div>

---

## 📁 Project Structure

```
clinic-management/
│
├── 📄 run.py                    # Application entry point
├── 📄 db.py                     # Database utilities
├── 📄 fix.py                    # Maintenance scripts
├── 📄 requirements.txt          # Python dependencies
│
├── 📂 app/
│   ├── 📄 __init__.py          # App factory & initialization
│   ├── 📄 config.py            # Configuration settings
│   ├── 📄 extensions.py        # Flask extensions (db, login, etc.)
│   ├── 📄 models.py            # SQLAlchemy database models
│   │
│   ├── 📂 routes/              # Blueprint controllers
│   │   ├── 📄 auth.py          # Authentication (login/register)
│   │   ├── 📄 main.py          # Public/main pages
│   │   ├── 📄 patient.py       # Patient dashboard & booking
│   │   ├── 📄 admin.py         # Admin clinic management
│   │   └── 📄 super_admin.py   # Super admin global control
│   │
│   ├── 📂 static/              # Static assets
│   │   ├── 📂 css/             # Stylesheets
│   │   ├── 📂 js/              # JavaScript files
│   │   └── 📂 uploads/         # User uploads
│   │       ├── 📂 logos/       # Company logos
│   │       └── 📂 profiles/    # Profile pictures
│   │
│   ├── 📂 templates/           # Jinja2 HTML templates
│   │   ├── 📄 base.html        # Base layout
│   │   ├── 📄 index.html       # Landing page
│   │   ├── 📂 auth/            # Login & register pages
│   │   ├── 📂 patient/         # Patient views
│   │   ├── 📂 admin/           # Admin dashboard views
│   │   └── 📂 super_admin/     # Super admin views
│   │
│   └── 📂 utils/               # Utility modules
│       ├── 📄 decorators.py    # Custom decorators (@role_required)
│       ├── 📄 helpers.py       # Helper functions
│       └── 📄 __init__.py
│
└── 📂 instance/
    └── 🗄️ clinic.db            # SQLite database file
```

---

## 🛠️ Technology Stack

<div align="center">

<!-- ANIMATED TECH STACK -->
<svg width="100%" height="200" viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="tsGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0f172a"/>
      <stop offset="100%" style="stop-color:#1e293b"/>
    </linearGradient>
    <style>
      .ts-bg { fill: url(#tsGrad); }
      .ts-card { rx: 10; }
      .ts-text { fill: #e2e8f0; font-family: 'Segoe UI', sans-serif; font-size: 12px; font-weight: 600; text-anchor: middle; }
      .ts-icon { font-size: 28px; text-anchor: middle; }
      .ts-pulse { animation: tsPulse 2s infinite; }
      @keyframes tsPulse { 0%,100% { opacity: 0.7; } 50% { opacity: 1; } }
    </style>
  </defs>

  <rect width="100%" height="100%" class="ts-bg" rx="16"/>

  <!-- Card 1: Python -->
  <g transform="translate(80, 50)" class="ts-pulse">
    <rect width="120" height="100" class="ts-card" fill="#22d3ee" opacity="0.15" stroke="#22d3ee" stroke-width="2"/>
    <text x="60" y="40" class="ts-icon">🐍</text>
    <text x="60" y="75" class="ts-text" fill="#22d3ee">Python 3.10+</text>
  </g>

  <!-- Card 2: Flask -->
  <g transform="translate(240, 50)" class="ts-pulse" style="animation-delay:0.3s">
    <rect width="120" height="100" class="ts-card" fill="#a78bfa" opacity="0.15" stroke="#a78bfa" stroke-width="2"/>
    <text x="60" y="40" class="ts-icon">⚗️</text>
    <text x="60" y="75" class="ts-text" fill="#a78bfa">Flask 2.3+</text>
  </g>

  <!-- Card 3: SQLite -->
  <g transform="translate(400, 50)" class="ts-pulse" style="animation-delay:0.6s">
    <rect width="120" height="100" class="ts-card" fill="#ec4899" opacity="0.15" stroke="#ec4899" stroke-width="2"/>
    <text x="60" y="40" class="ts-icon">🗄️</text>
    <text x="60" y="75" class="ts-text" fill="#ec4899">SQLite3</text>
  </g>

  <!-- Card 4: SQLAlchemy -->
  <g transform="translate(560, 50)" class="ts-pulse" style="animation-delay:0.9s">
    <rect width="120" height="100" class="ts-card" fill="#f59e0b" opacity="0.15" stroke="#f59e0b" stroke-width="2"/>
    <text x="60" y="40" class="ts-icon">🔄</text>
    <text x="60" y="75" class="ts-text" fill="#f59e0b">SQLAlchemy</text>
  </g>

  <!-- Card 5: Jinja2 -->
  <g transform="translate(720, 50)" class="ts-pulse" style="animation-delay:1.2s">
    <rect width="120" height="100" class="ts-card" fill="#22d3ee" opacity="0.15" stroke="#22d3ee" stroke-width="2"/>
    <text x="60" y="40" class="ts-icon">📝</text>
    <text x="60" y="75" class="ts-text" fill="#22d3ee">Jinja2</text>
  </g>

  <!-- Card 6: Bootstrap -->
  <g transform="translate(880, 50)" class="ts-pulse" style="animation-delay:1.5s">
    <rect width="120" height="100" class="ts-card" fill="#a78bfa" opacity="0.15" stroke="#a78bfa" stroke-width="2"/>
    <text x="60" y="40" class="ts-icon">🎨</text>
    <text x="60" y="75" class="ts-text" fill="#a78bfa">Bootstrap 5</text>
  </g>
</svg>

</div>

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.10+ | Core runtime |
| **Framework** | Flask 2.3+ | Web application framework |
| **ORM** | SQLAlchemy | Database abstraction |
| **Database** | SQLite | Lightweight file-based storage |
| **Auth** | Flask-Login | Session management |
| **Forms** | WTForms | Form validation & CSRF |
| **Templates** | Jinja2 | Server-side HTML rendering |
| **Frontend** | Bootstrap 5 | Responsive UI components |
| **Styling** | Custom CSS | Theme & animations |

---

## 🎯 API Route Overview

<div align="center">

```mermaid
mindmap
  root((🌐 ROUTES))
    Auth
      🔑 /login
      📝 /register
      🚪 /logout
    Patient
      🏠 /patient/dashboard
      🏥 /patient/companies
      📅 /patient/book
      📋 /patient/appointments
    Admin
      ⚙️ /admin/dashboard
      👥 /admin/patients
      📅 /admin/appointments
      📈 /admin/records
      🏢 /admin/select-company
    SuperAdmin
      👑 /super-admin/dashboard
      🏢 /super-admin/companies
      👤 /super-admin/users
```

</div>

---

## 🚀 Deployment Checklist

```bash
# Production preparation
export FLASK_ENV=production
export SECRET_KEY="your-secure-secret-key"

# Optional: Use Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Or use Waitress (Windows-friendly)
pip install waitress
waitress-serve --port=5000 --call app:create_app
```

---

<div align="center">

<!-- FOOTER BANNER -->
<svg width="100%" height="100" viewBox="0 0 1200 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ftGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0f172a"/>
      <stop offset="100%" style="stop-color:#1e293b"/>
    </linearGradient>
    <style>
      .ft-text { fill: #64748b; font-family: 'Segoe UI', sans-serif; font-size: 14px; text-anchor: middle; }
      .ft-line { stroke: #334155; stroke-width: 1; }
      .ft-dot { animation: ftBlink 2s infinite; }
      @keyframes ftBlink { 0%,100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
  </defs>
  <rect width="100%" height="100%" fill="url(#ftGrad)" rx="12"/>
  <line x1="100" y1="50" x2="500" y2="50" class="ft-line"/>
  <line x1="700" y1="50" x2="1100" y2="50" class="ft-line"/>
  <text x="600" y="45" class="ft-text">Built with 💙 for Healthcare Innovation</text>
  <text x="600" y="70" class="ft-text" style="font-size:12px;">Multi-Tenant Clinic Management System</text>
  <circle cx="600" cy="25" r="3" fill="#22d3ee" class="ft-dot"/>
  <circle cx="600" cy="85" r="3" fill="#ec4899" class="ft-dot" style="animation-delay:1s"/>
</svg>

</div>
