# PeeweeSys Website (`peeweesys.com`)

The official public website for **PeeweeSys** (OpenPIWIS) — dealer-level and beyond Porsche diagnostics running directly in your web browser.

Built with **Astro 4**, **Tailwind CSS**, **Lucide Icons**, and **TypeScript**, styled to match the classic matte black, Guards Red, and precision typography of vintage Porsche instrument clusters.

---

## 🚀 Key Highlights & Sections

1. **Hero & Philosophy:**
   - Plug any standard **$15 FTDI USB cable** into your 986 / 996 / 987.
   - Zero $1,000 dealer multiplexers, zero Windows XP virtual machines, zero VIN locks.
   - Platform status indicators (Windows Tested & Live; macOS/iOS/Android Roadmap).
   - Direct launch CTA linking to `https://peeweesys.app`.

2. **Killer Features ("What No Other Tool Does"):**
   - Full ECU ROM & EEPROM dumps over OBD (0x23 read service on Bosch ME7.2 and Kombi 93C86).
   - Coolant gauge linearization (eradicating the factory 80°C–105°C dummy buffer).
   - Speedometer recalibration for tire changes and factory over-read.
   - Over-rev Ranges 1–6 and operating hours PPI scorecard.
   - Multi-module mileage & tamper audit (DME vs Kombi vs Tiptronic).
   - Safe pre-clear diagnostic snapshot reports.

3. **Tool Comparison Matrix (`src/data/comparisons.json`):**
   - Side-by-side comparison with Porsche OEM PIWIS, Durametric Enthusiast & Pro, Foxwell NT530, iCarsoft POR V2.0/V3.0, Launch X431 / Autel MaxiSys, and generic ELM327.

4. **Hardware & Cable Pinout Guide (`src/data/cables.json`):**
   - Blue VAG KKL FTDI FT232R cables with interactive OBD pinout (Pin 7 vs Pin 3 switch mod).
   - Tactrix OpenPort 2.0 (J2534) and OBDLink EX/SX CAN adapters.

5. **Vehicle Coverage Selector (`src/data/vehicles.json`):**
   - Interactive selector for 986 Boxster, 996 911, 987 Boxster/Cayman, 997 911, Cayenne E1, and Next-Gen roadmap.
   - Official SVG vector silhouettes from `public/assets/vehicles/`.
   - Comprehensive module support matrix (DME, Kombi, ABS/PSM, Airbag, Alarm, Climate, Tiptronic).

6. **Dynamic Feature Sync Pipeline (`tools/sync_from_app.py`):**
   - Automatically synchronizes live progress from `D:\PIWIS Reverse Engineering\docs\features.yaml` into `src/data/features.json`.
   - Proves live continuous build & deployment when new vehicle capabilities are verified.

7. **Contact & Feedback (`galballyj@hotmail.com`):**
   - Responsive inquiry form for cable advice, ECU queries, and vehicle log contributions.

---

## 🛠️ Stack & Directory Layout

```text
peeweesys-website/
├── .github/
│   └── workflows/
│       ├── deploy-pages.yml         # Cloudflare Pages build & deployment
│       └── sync-app-features.yml    # Automated feature sync trigger
├── public/
│   └── assets/
│       ├── brand/                   # Official SVG & PNG logos and wordmarks
│       └── vehicles/                # Official dark/light silhouette SVGs
├── src/
│   ├── components/
│   │   ├── ContactSection.astro     # Contact form for inquiries
│   │   ├── DynamicFeatures.astro    # Live engine progress metrics
│   │   ├── HardwareGuide.astro      # Cables, pinouts, and $1 switch mod
│   │   ├── Hero.astro               # Hero section with live terminal preview
│   │   ├── KillerFeatures.astro     # 6 exclusive deep-dive capabilities
│   │   ├── ToolComparison.astro     # Diagnostic comparison matrix
│   │   └── VehicleCoverage.astro    # Interactive vehicle & module selector
│   ├── data/
│   │   ├── cables.json              # Hardware and pinout data
│   │   ├── comparisons.json         # Matrix comparison data
│   │   ├── features.json            # Synced from core OpenPIWIS engine
│   │   ├── killer_features.json     # Killer features dataset
│   │   └── vehicles.json            # Vehicle platform & module support
│   ├── layouts/
│   │   └── Layout.astro             # Global layout, header, and footer
│   ├── pages/
│   │   └── index.astro              # Homepage
│   └── styles/
│       └── global.css               # Porsche instrument gauge theme styles
├── tools/
│   └── sync_from_app.py             # Feature ingestion script
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
└── package.json
```

---

## 💻 Development & Build

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Dev Server
```bash
npm run dev
```

### 3. Build Static Site
```bash
npm run build
```
Builds the static production bundle to `dist/`.

### 4. Sync Live Engine Features
To update `src/data/features.json` from the core diagnostic repo:
```bash
python tools/sync_from_app.py
```

---

## 🌐 Deployment to Cloudflare Pages

This site is pre-configured for automated deployment to **Cloudflare Pages**:
- Workflow: `.github/workflows/deploy-pages.yml`
- Output Directory: `dist`
- Build Command: `npm run build`
- Node Version: `20`

No external API keys are required for local compilation or static verification.
