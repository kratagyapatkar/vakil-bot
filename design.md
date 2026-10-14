# VakilBot — UI/UX Design System Specification (Figma Edition)
> **Updated for Latest Figma Design (`rxU9hykYlQ8XLUCiLeQ0HX`)**  
> Use this specification with plugins like *html.to.design*, *Figma Tokens*, or manually layout frames using the exact dimensions, color hexes, typography, and component specs below.

---

## 🎨 1. Design Tokens & Color Palette

### Primary Palette (Deep Navy Judiciary)
| Token Name | Hex Code | Figma Variable | Usage |
|---|---|---|---|
| `color-primary-900` | `#0b172a` | `Primary/Darkest` | Deep shadow accents |
| `color-primary-800` | `#132544` | `Primary/Main` | Sidebar background, user bubble, 3px input border, primary buttons |
| `color-primary-700` | `#1f3a6b` | `Primary/Light` | Button hover states, active category pills, header accents |
| `color-primary-100` | `#edf2f9` | `Primary/Subtle` | Subtle highlight badges, card left borders |

### Accent Palette (Judicial Warm Amber & Gold)
| Token Name | Hex Code | Figma Variable | Usage |
|---|---|---|---|
| `color-accent-600` | `#b88628` | `Accent/Dark` | Hover state for gold text and borders |
| `color-accent-500` | `#d4a347` | `Accent/Main` | Topbar brand title `⚖️ VakilBot`, Disclaimer left border, Rights card border |
| `color-accent-300` | `#f3d489` | `Accent/Light` | User bubble accent highlights, tooltip borders |
| `color-accent-100` | `#fdf8eb` | `Accent/Soft` | Bottom Disclaimer card background, Rights card background |

### Neutral & Semantic Palette
| Token Name | Hex Code | Figma Variable | Usage |
|---|---|---|---|
| `color-bg-canvas` | `#f5f7fc` | `Neutral/Background` | Main app background canvas |
| `color-surface-white` | `#ffffff` | `Neutral/Surface` | Message bubble (bot), quick cards, topbar, input dock, emergency footer card |
| `color-surface-muted` | `#edf2f9` | `Neutral/Surface-2` | Secondary surface, source chips background |
| `color-border` | `#dde4ee` | `Neutral/Border` | Card borders, dividers, subtle separators |
| `color-text-main` | `#172033` | `Text/Primary` | Body text, titles, headings |
| `color-text-muted` | `#64748b` | `Text/Secondary` | Subtitles, input placeholders, timestamp info |
| `color-success` | `#22c55e` | `Semantic/Success` | Online status dot, Helplines card border (`#f0fdf4` bg) |
| `color-emergency-red` | `#dc2626` | `Semantic/Emergency` | Emergency helpline text on white footer card |
| `color-warning` | `#eab308` | `Semantic/Warning` | In-chat warning card border (`#fefce8` bg) |
| `color-danger` | `#ef4444` | `Semantic/Danger` | Mic recording pulsing badge |

---

## 🔤 2. Typography Specification (Font Family: `Inter`)

| Style Name | Size | Weight | Line Height | Letter Spacing | Case |
|---|---|---|---|---|---|
| **Welcome Heading** | `24px` | Bold (700) | `32px` | `-0.01em` | Normal |
| **Topbar Title** | `17px` | Bold (700) | `24px` | `-0.01em` | Normal |
| **Card Title / Rights** | `13px` | Bold (700) | `18px` | `+0.04em` | ALL CAPS |
| **Body Primary** | `13.5px` | Regular (400) | `22px` | `0` | Normal |
| **Body Bold / Law** | `13.5px` | SemiBold (600) | `22px` | `0` | Normal |
| **Quick Card Text** | `12.5px` | Medium (500) | `18px` | `0` | Normal |
| **Sidebar Subtitle** | `10px` | SemiBold (600) | `14px` | `+0.08em` | ALL CAPS |
| **Section Label** | `10px` | Bold (700) | `14px` | `+0.10em` | ALL CAPS |
| **Bottom Disclaimer** | `11px` | Regular (400) | `16px` | `0` | Normal |
| **Emergency Numbers** | `10px` | SemiBold (600) | `14px` | `0` | Normal |

---

## 📐 3. Layout Grid & Global Dimensions

```
+---------------------------------------------------------------------------------------+
|  [Sidebar: 280px Fixed]        |  [Main Chat Container: Flex Fill]                    |
|  - Brand Logo + Subtitle       |  - Topbar (Height: 58px)                             |
|    "AI LEGAL BOT · FOR INDIA   |    * Amber Brand ⚖️ VakilBot + ● Online status       |
|     · FROM INDIA"              |    * Multilingual & Accessibility Controls           |
|  - Legal Categories            |    * Dark Navy "+ New Chat" Button                   |
|  - Quick Questions Pills       |  - Scrollable Area:                                  |
|  - Footer Emergency Card:      |    * 🏛️ Namaste! I'm VakilBot                         |
|    * White card (#ffffff)      |    * Knowledge Level Selector (New/Inter/Expert)     |
|      Red text (#dc2626)        |    * 2x3 Quick Action Cards (White, 560px max)       |
|    * "Powered by Google"       |  - Floating Input Dock:                              |
|                                |    * 3px Navy Pill Input (#132544 border, 720px max) |
|                                |    * Centered Bottom Disclaimer Card (530px max)     |
+---------------------------------------------------------------------------------------+
```

- **Desktop Frame**: `1440px × 900px`
- **Mobile Frame**: `390px × 844px`
- **Radii Specs**:
  - Floating Input Pill: `36px`
  - Message Bubbles: `14px`
  - Cards & Buttons: `8px`
  - Translucent Sidebar Question Pills: `6px`
  - Emergency Footer Card: `6px`

---

## 🧩 4. Figma Component Specs

### Component A: Sidebar (`Frame 280px × 900px`)
- **Fill**: Solid `#132544` (Deep Navy)
- **Header**:
  - Scales icon `⚖️` + Title `VakilBot` (Bold 20px, `#ffffff`)
  - Subtitle: `AI LEGAL BOT · FOR INDIA · FROM INDIA` (10px, `#8a9eb8`, Letter-spacing: `0.8px`)
- **Category Navigation Item**:
  - Transparent row with emoji + label (`rgba(255,255,255,0.82)`)
  - Hover: `rgba(255, 255, 255, 0.10)`
- **Quick Question Pills**:
  - Fill: `rgba(255, 255, 255, 0.06)`
  - Stroke: `1px solid rgba(255, 255, 255, 0.10)`
  - Corner Radius: `6px`
  - Text: `11.5px`, `#ffffff` (85% opacity)
  - Hover: Fill `rgba(255, 255, 255, 0.14)`, Border `rgba(255, 255, 255, 0.25)`
- **Sidebar Footer**:
  - Border-top: `1px solid rgba(255, 255, 255, 0.08)`
  - **Emergency White Card**:
    - Fill: `#ffffff`
    - Radius: `6px`
    - Text: `🆘 Emergency: 100 | Women: 1091 | Cyber: 1930 | Legal Aid: 15100` (Red `#dc2626`, 10px bold)
  - **Powered by Google**:
    - Text: `Powered by Google` (10px, `rgba(255, 255, 255, 0.45)`, centered)

---

### Component B: Topbar (`Height: 58px`)
- **Fill**: `#ffffff`
- **Border Bottom**: `1px solid #dde4ee`
- **Left Lockup**:
  - Brand Title: `⚖️ VakilBot` (Bold 17px, Warm Amber `#d4a347`)
  - Subtitle: `● Online · gemini-1.5-flash` (Dot `#22c55e`, Text `#64748b`, 11px)
- **Right Action**:
  - `+ New Chat` Button: Fill `#132544`, Text `#ffffff`, Radius `8px`, Padding `7px 16px`
  - Language Selector dropdown & Accessibility Buttons (`A±`, `🌓`, `Aa`)

---

### Component C: Welcome Screen Quick Action Cards (`2x3 Grid`)
- **Grid Layout**: 2 Columns, gap `12px`, max-width `560px`
- **Card**:
  - Fill: `#ffffff`
  - Stroke: `1px solid #e2e8f0`
  - Radius: `8px`
  - Padding: `14px 18px`
  - Emoji: Top left, size `20px`
  - Text: `12.5px Medium #1e293b`
  - Hover: Border `#cbd5e1`, Elevation `0 4px 14px rgba(19, 37, 68, 0.08)`, `translateY(-1px)`
- **Cards Content**:
  1. 🚔 **Rights when arrested by police**
  2. 🏚️ **Illegal eviction by landlord**
  3. 💻 **Report online fraud / cybercrime**
  4. 👩‍⚖️ **Get free legal aid / lawyer**
  5. 📋 **How to file RTI application**
  6. 🛒 **Consumer complaint process**

---

### Component D: Knowledge Level Selector Tabs
- **Location**: Centered above Quick Cards
- **Container**: White pill container with border `#dde4ee`, padding `3px`
- **Tabs**:
  - `🌱 New to Law` (Active: `#132544` fill, white text)
  - `⚖️ Intermediate`
  - `🎓 Expert / Advocate`

---

### Component E: Floating Pill Input Bar with 3px Navy Border
- **Container**:
  - Width: `90%`, Max-width: `720px`
  - Fill: `#ffffff`
  - **Stroke**: `3px solid #132544`
  - **Corner Radius**: `36px` (Pill)
  - Box Shadow: `0 4px 18px rgba(19, 37, 68, 0.08)`
  - Padding: `8px 16px 8px 22px`
- **Children**:
  - Textarea: Transparent, 13.5px, placeholder `#8c9bb5`
  - Outline Mic Button: 36px circular, color `#132544`
  - Send Button: 36px circular, fill `#132544`, white arrow icon

---

### Component F: Centered Bottom Disclaimer Card
- **Location**: Centered directly below the floating pill input bar
- **Dimensions**: Max-width `530px`, Width `90%`
- **Fill**: `#fdf8eb` (Warm Light Cream)
- **Stroke**: `1px solid #f6e8c7`
- **Left Accent Border**: `4px solid #d4a347` (Gold/Amber)
- **Corner Radius**: `6px`
- **Padding**: `9px 14px`
- **Text**: `⚠️ Disclaimer: This bot provides general legal information based on publicly available Indian laws. It is not a substitute for professional legal advice. For serious matters, consult a qualified lawyer.`
- **Typography**: 11px, Line-height 1.45, Color `#78521a`

---

## 📱 5. Responsive Restructuring: Tablet Specification (768px – 1024px)
> **Target Devices**: iPad 9th/10th gen (`810 × 1080`), iPad Mini (`768 × 1024`), iPad Air & Pro 11" (`820 × 1180`), Android Tablets (Galaxy Tab, Lenovo Tab).

```
+---------------------------------------------------------------------------------------+
|  [☰ Menu] ⚖️ VakilBot  ● Online · gemini-1.5-flash     [🌐 English ▼] [A±] [🌓] [Aa] [+ New] |
|---------------------------------------------------------------------------------------|
|                                                                                       |
|                                🏛️ Namaste! I'm VakilBot                              |
|                   Your AI legal helper for Indian legal rights, laws...               |
|                                                                                       |
|                         [ 🌱 New to Law ] [ ⚖️ Intermediate ] [ 🎓 Expert / Advocate ]|
|                                                                                       |
|              +-----------------------------------+-----------------------------------+ |
|              | 🚔 Rights when arrested by police | 🏚️ Illegal eviction by landlord   | |
|              +-----------------------------------+-----------------------------------+ |
|              | 💻 Report cybercrime / fraud      | 👩‍⚖️ Get free legal aid / lawyer   | |
|              +-----------------------------------+-----------------------------------+ |
|              | 📋 How to file RTI application    | 🛒 Consumer complaint process     | |
|              +-----------------------------------+-----------------------------------+ |
|                                                                                       |
|                 +-------------------------------------------------------------+       |
|                 | Ask about FIR, bail, tenant rights, consumer court... 🎙️ [➤] |       |
|                 +-------------------------------------------------------------+       |
|                 | ⚠️ Disclaimer: Provides general legal information...         |       |
|                 +-------------------------------------------------------------+       |
+---------------------------------------------------------------------------------------+
```

### Tablet Frame & Layout Specs
| Element | Tablet Spec (`768px – 1024px`) | Differences from Desktop |
|---|---|---|
| **Canvas Frame** | `768px × 1024px` / `820px × 1180px` | Full screen width utilized for chat |
| **Sidebar** | `320px` sliding off-canvas drawer (`transform: translateX(-100%)`) | Hidden by default; toggled via `☰` button; dark backdrop blur overlay (`rgba(19, 37, 68, 0.45)`) |
| **Sidebar Close Button** | `32px` circular button (`✕`), top-right of sidebar header | Replaces static header on desktop; provides direct touch dismissal |
| **Topbar** | `Height: 58px`, padding `12px 20px`, flex layout | Hamburger `☰` button added (`38px × 38px`, `#edf2f9` surface); keeps full language dropdown & a11y buttons |
| **Level Selector** | Centered pill container, all 3 labels displayed in full | Maintained with generous padding (`6px 16px`) |
| **Quick Action Cards** | 2-column grid (`repeat(2, 1fr)`), max-width `620px`, gap `12px` | Slightly expanded width for comfortable touch tap targets (`min-height: 64px`) |
| **Floating Input Bar** | `Width: 92%`, `max-width: 640px`, `3px solid #132544` border | Re-centered floating dock above disclaimer |
| **Disclaimer Card** | `Max-width: 540px`, centered, 11px font | Proportionate to 640px input pill |
| **Auto-Dismiss Drawer** | Auto-closes upon selecting category or question | Touch navigation flow optimization |

---

## 📲 6. Responsive Restructuring: Mobile Specification (≤767px, 360px – 480px)
> **Target Devices**: iPhone 13/14/15/16 (`390 × 844`), iPhone SE / Mini (`375 × 812`), Android Standard (`360 × 800`), Galaxy S22/S23/S24 (`360 × 780`).

```
+----------------------------------------------------+
| [☰] ⚖️ VakilBot                  [🌐 EN] [+ New]   |
|----------------------------------------------------|
|                       🏛️                           |
|              Namaste! I'm VakilBot                 |
|       Legal helper for Indian rights & laws        |
|                                                    |
|           KNOWLEDGE LEVEL: HOW SHOULD I EXPLAIN?    |
|       +------------------------------------+       |
|       |  🌱 New  |  ⚖️ Medium  |  🎓 Expert |       |
|       +------------------------------------+       |
|                                                    |
|       +--------------------+--------------------+  |
|       | 🚔 Police Arrest   | 🏚️ Landlord Evict  |  |
|       +--------------------+--------------------+  |
|       | 💻 Cyber Fraud     | 👩‍⚖️ Legal Aid      |  |
|       +--------------------+--------------------+  |
|       | 📋 File RTI        | 🛒 Consumer Court  |  |
|       +--------------------+--------------------+  |
|                                                    |
|====================================================|
| [ Ask legal question...                       🎙️ ➤]|
| [⚠️ Disclaimer: General info only. Consult lawyer. ]|
+----------------------------------------------------+
```

### Mobile Frame & Component Specs
| Component | Mobile Implementation (`≤767px`) | Rationale / Touch UX Behavior |
|---|---|---|
| **Viewport & Height** | `height: 100dvh`, `viewport-fit=cover` | Prevents mobile Safari / Chrome browser address bar jumpiness; supports bottom safe-area insets (`env(safe-area-inset-bottom)`) |
| **Sidebar Drawer** | `Width: 86vw` (max `330px`), sliding off-canvas drawer | Leaves visible right edge touch-dismiss zone; closes on item selection |
| **Topbar Header** | `Height: 52px`, padding `10px 14px` | Zero horizontal scroll; hides lengthy subtitle and large desktop controls |
| **Topbar Brand** | Icon `⚖️` + Title `VakilBot` (`15.5px` Bold Gold `#d4a347`) | Clean compact lockup |
| **Mobile Settings Pill** | Button `🌐 EN` (`12px` font, border `#dde4ee`, radius `8px`) | Replaces bulky desktop `<select>` and 3 separate a11y buttons; opens `#mobileSettingsSheet` |
| **New Chat Button** | Compact button: icon `+` or `+ New` (`padding: 6px 12px`, `11.5px`) | Easily reachable with thumb |
| **Knowledge Level Tabs** | 3-way segmented control (`flex: 1`, `max-width: 340px`) | Uses responsive text span: hides `Intermediate`, displays `Medium` (`🌱 New`, `⚖️ Medium`, `🎓 Expert`) to guarantee zero line-wrapping |
| **Quick Action Cards** | 2-column compact grid, gap `8px`, width `100%` | Card padding `9px 11px`, emoji `16px`, text `11px` (line-height `1.3`). Fits all 6 cards above the fold |
| **Docked Bottom Input** | Fixed dock (`border-top: 1px solid #dde4ee`, `#ffffff` bg) | Anchored to bottom screen with safe-area support; eliminates float gaps on small screens |
| **Input Pill Stroke** | `2.5px solid #132544`, radius `26px`, padding `5px 8px 5px 14px` | Scaled down for mobile proportions while retaining signature navy stroke |
| **Input Textarea** | `font-size: 14px`, `min-height: 20px`, `line-height: 1.4` | `14px` base prevents iOS Safari from automatically zooming into the page on focus |
| **Mic & Send Touch Buttons** | Circular `34px × 34px` touch targets | Comfortable 34-44px tap targets |
| **Mobile Disclaimer** | Full-width (`100%`), padding `6px 10px`, `9.5px` text, 3px left gold bar | Compact 2-line layout that does not push input out of view |
| **Extra Small Devices (`≤380px`)**| Scaled font `10px` on cards, compact padding `5px 9px` | Guaranteed compatibility down to 320px devices (Galaxy Fold outer display, iPhone SE 1st gen) |

---

## 📑 7. Mobile-Specific Sheets & Touch Overlays

### A. Mobile Settings & Accessibility Bottom Sheet (`#mobileSettingsSheet`)
- **Trigger**: Tapping `🌐 EN` button in the mobile topbar.
- **Surface**: Slide-up modal (`transform: translateY(0)`), fill `#ffffff`, top border `3px solid #d4a347`, corner radius `20px 20px 0 0`.
- **Z-Index**: `1100` (above chat, below system alerts).
- **Handle**: Centered bar (`44px × 4px`, radius `2px`, color `#dde4ee`).
- **Sections**:
  1. **Language Selection**: Full-width native styled dropdown supporting all 16 Indian and International languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Spanish, French, German, Arabic, Japanese, English).
  2. **Accessibility Quick Grid (`3 columns`)**:
     - `A±` Text Size (cycles Normal → Large → X-Large).
     - `🌓` High Contrast (toggles WCAG AAA black/gold high contrast theme).
     - `Aa` Dyslexia Font (toggles high-readability weighted letter spacing).

### B. Interactive Legal Terminology Touch Sheet (`#termSheet`)
- **Problem Solved**: Desktop tooltips rely on CSS `:hover`, which fails or causes sticky hover bugs on touch devices.
- **Trigger**: Tapping any highlighted legal term (`.legal-term`, e.g. *Bail*, *Cognizable Offence*, *FIR*, *BNSS*, *BNS*, *CPC*, *RTI*).
- **Surface**: Smooth bottom sheet sliding up from bottom (`transform: translateY(0)`), corner radius `16px 16px 0 0`, top border `3px solid #d4a347`.
- **Contents**:
  - Header with Scales icon `⚖️`, bold term title, and circular `✕` close button.
  - Body text with plain-language definition of the legal term.
- **Dismiss**: Tapping the `✕` close button, tapping anywhere outside, or dragging down.

---

## 🛠️ 8. Step-by-Step: How to Import Into Figma (Fix for Localhost)

> [!NOTE]  
> **Why `http://localhost:8000` fails in the plugin's "URL" tab:**  
> The `html.to.design` plugin runs on Figma's remote cloud servers. Those cloud servers cannot access your private machine (`localhost` / `127.0.0.1`).  
> Use **Method 1** (Chrome Extension) or **Method 2** (File Drag & Drop) to import localhost designs into Figma seamlessly.

### Method 1: Instant 1-Click via the `html.to.design` Chrome Extension (Easiest)
1. Install the official free [html.to.design Chrome Extension](https://chromewebstore.google.com/detail/htmltodesign/pmcpkicppkdmclhfeclpbeijpfdgfeha) from the Chrome Web Store.
2. In your browser (Chrome, Edge, Brave, Arc), open:
   ```text
   http://localhost:8000
   ```
3. Click the **html.to.design** extension icon in your browser top bar.
4. Select the viewports you want (**Desktop 1440**, **Tablet 768**, or **Mobile 390**) and click **Capture**.
5. Click **Copy to clipboard** (or save the `.h2d` file).
6. Go into your Figma file and press **`Ctrl + V`** (Windows) or **`Cmd + V`** (Mac).
7. The page is instantly pasted as editable vector frames, text styles, and auto-layout groups!

---

### Method 2: Drag & Drop `index.html` File in the Plugin (No Extension Needed)
1. In Figma, open the **html.to.design** plugin.
2. At the top of the plugin window, switch from the **URL** tab to the **File** (or **HTML Code**) tab.
3. Drag and drop the self-contained file directly into the plugin:
   ```text
   C:\Users\ACER\Documents\antigravity\brave-raman\legal-bot\frontend\index.html
   ```
4. Choose **Desktop (`1440px`)**, **Tablet (`768px`)**, or **Mobile (`390px`)** from the viewport dropdown.
5. Click **Import**.

---

### Method 3: Copy-Paste HTML Code Directly
1. Open [`frontend/index.html`](file:///c:/Users/ACER/Documents/antigravity/brave-raman/legal-bot/frontend/index.html) in your code editor.
2. Copy all code (`Ctrl + A`, then `Ctrl + C`).
3. In Figma, open the **html.to.design** plugin → Click the **HTML Code** tab.
4. Paste the code and click **Import**.

---

### Method 4: Manual Frame Setup with Provided Tokens
If building or refining frames natively in Figma without plugins:
1. **Desktop Frame (`1440 × 900`)**:
   - Sidebar `280px` fixed navy `#132544`.
   - Floating pill input `720px` max-width, `3px solid #132544` border.
2. **Tablet Frame (`768 × 1024` or `820 × 1180`)**:
   - Full-width canvas `768px` (or `820px`).
   - Topbar with hamburger `☰` on left, full controls on right.
   - Quick cards in 2 columns (`max-width: 620px`).
   - Floating pill input `640px` max-width.
   - Off-canvas sidebar drawer placed as an interactive overlay with dark backdrop blur.
3. **Mobile Frame (`390 × 844` or `375 × 812`)**:
   - Topbar height `52px` with `☰`, `⚖️ VakilBot`, `🌐 EN` pill, and `+ New` button.
   - Knowledge level tabs width `340px` max (`🌱 New`, `⚖️ Medium`, `🎓 Expert`).
   - 2-column quick cards (`8px` gap, `11px` text) fitting above the fold.
   - Docked bottom bar with `2.5px` border input pill and full-width compact disclaimer.
   - Bottom Sheet frames for `#mobileSettingsSheet` and `#termSheet` positioned as interactive overlay variants.


