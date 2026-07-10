# HerSakhi — Technical Specification

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `vite` | ^5.0 | Build tool, dev server, module bundling |
| `three` | ^0.160 | 3D glass orb scene, particles, orbiting cards |
| `gsap` | ^3.12 | Core animation engine, timelines, tweens |
| `lenis` | ^1.1 | Smooth scroll with inertia |
| `split-type` | ^0.3 | Text splitting for character/word animations |

**CDN Resources (loaded via `<link>` in HTML)**:
- Google Fonts: Sora (400, 500, 600, 700) + Inter (400, 500, 600)
- Lucide Icons (loaded as ES module via `vite`)

## File Structure

```
├── index.html              # Entry point, font links, main HTML structure
├── src/
│   ├── main.js             # Entry: initializes all systems in order
│   ├── styles/
│   │   └── main.css        # All styles: tokens, reset, utilities, sections
│   ├── three/
│   │   ├── HeroScene.js    # Three.js scene: orb, cards, particles, bloom
│   │   ├── GlassOrb.js     # Orb mesh creation and animation
│   │   ├── OrbitCards.js   # 8 floating UI card meshes + orbit logic
│   │   └── Particles.js    # Background energy particles
│   ├── animations/
│   │   ├── LoadingOverlay.js   # Loading screen + exit
│   │   ├── Navigation.js       # Scroll-based glass nav transformation
│   │   ├── HeroEntrance.js     # Hero text + orb entrance timeline
│   │   ├── TextCycle.js        # Headline word cycling (Empowering→Dreams→...)
│   │   ├── DashboardAssembly.js # "Who Is" section card scatter→assembly
│   │   ├── ScrollStory.js      # AI Companion 4-phase scroll timeline
│   │   ├── FeaturesGrid.js     # Feature cards stagger entrance
│   │   ├── HowItWorks.js       # Step cards slide-in + connecting line
│   │   ├── FinalCTA.js         # CTA panel entrance
│   │   └── FooterReveal.js     # Footer entrance
│   ├── components/
│   │   ├── MeshGradient.js     # Canvas-based animated mesh gradient
│   │   ├── CustomCursor.js     # Glass cursor dot with hover expand
│   │   ├── MagneticButton.js   # Button magnetic hover effect
│   │   └── GlassCard.js        # Reusable glass card DOM helper
│   └── utils/
│       ├── lenis-init.js       # Lenis instance + ScrollTrigger sync
│       ├── reduced-motion.js   # prefers-reduced-motion detection
│       └── split-text.js       # SplitType wrapper with cleanup
├── public/
│   └── logo.png            # HerSakhi logo (uploaded asset)
├── vite.config.js
└── package.json
```

## Animation Implementation Table

| Animation | Library / Addons | Implementation Approach | Complexity |
|-----------|-----------------|------------------------|------------|
| Loading overlay breathing orb | CSS @keyframes | `scale(0.95) ↔ (1.05)` over 3s infinite, radial-gradient glass effect | Low |
| Loading overlay exit | GSAP | `opacity: 1→0` over 600ms on window.load, then display:none | Low |
| Nav scroll transformation | GSAP + ScrollTrigger | ScrollTrigger at 80px toggles class; CSS transitions handle morph (width, border-radius, bg, shadow). IntersectionObserver for active link. | Medium |
| Nav link hover dot | CSS | `::after` pseudo-element, scale + opacity transition | Low |
| Mobile menu open/close | GSAP | Fullscreen overlay fade 0.4s + links stagger from bottom 0.1s | Medium |
| **Mesh gradient background** | **Custom Canvas (MeshGradient.js)** | **🔒 Non-degradable.** 4 control points moved by simplex noise, bilinear interpolation on 20×20 grid, CSS blur(80px). Two gradient contexts (hero=more violet, companion=more blue) on separate canvas layers with opacity transitions. | **High** |
| Custom cursor | requestAnimationFrame | Lerp-following div (0.15 factor), expand to 40px on interactive hover via mouseenter/mouseleave delegation, mix-blend-mode:difference | Medium |
| Button magnetic effect | Custom JS | mousemove within 50px radius → calculate offset → rAF lerp 0.2. Desktop only. | Medium |
| **Hero Glass Orb** | **Three.js + MeshPhysicalMaterial** | **🔒 Non-degradable.** IcosahedronGeometry(1, 64), transmission:0.98, thickness:1.5, ior:1.7, dispersion:0.4, clearcoat:1.0. Slow Y rotation (0.001 rad/f), breathing scale via sin(time*0.8), mouse-tilt via lerped rotation.x/y. | **High** |
| **Orb post-processing bloom** | **Three.js EffectComposer + UnrealBloomPass** | **🔒 Non-degradable.** Bloom: strength 0.4, radius 0.5, threshold 0.85. ACESFilmic tone mapping, exposure 1.2. | **High** |
| **Floating orbit cards** | **Three.js PlaneGeometry + CanvasTexture** | **🔒 Non-degradable.** 8 cards with unique radius/speed/tilt/phase. Elliptical orbits. Cards always face camera (lookAt). Mouse shifts orbit center (lerp 0.03). Opacity pulse via sin. | **High** |
| Background energy particles | Three.js | 50 spheres (radius 0.01-0.03), drift via sin(time*0.1+seed), opacity oscillation, depth-sorted | Medium |
| **Hero entrance sequence** | **GSAP timeline** | **🔒 Non-degradable.** Master timeline: left column elements stagger from below (0.8s, expo.out, staggered delays 0.2-1.5s). Right column: orb scale 0→1 (1.2s, elastic, delay 0.3s) with transmission ramp 0→0.98. Cards scale+fade stagger 0.08s from 0.8s. Particles fade 2s from 1s. | **High** |
| Headline word cycling | GSAP + SplitType | Split cycling word into chars. Every 3s: outgoing chars slide up translateY(-100%) stagger 0.03s, duration 0.6s; incoming chars slide from translateY(100%)→0. 5-word loop. | Medium |
| Hero mouse reaction | Custom JS (rAF) | Mouse normalized -1→1. Orb rotation accelerates, tilt lerps. Cards orbit center shifts. Mesh gradient focal shifts (CSS vars). Buttons lift in right half. Shadow intensity changes. All lerped for smoothness. | Medium |
| **"Who Is" dashboard assembly** | **GSAP + ScrollTrigger scrub** | **🔒 Non-degradable.** ScrollTrigger scrub over section. 6 cards start scattered (random positions, ±15deg rotate, opacity 0). Scrub: cards animate to final positions, rotate→0, opacity→1 at staggered progress points (0.1, 0.25, 0.4, 0.55, 0.7, 0.85). Dashboard panel scale 0.9→1, opacity 0→1 over first 30%. Progress ring 0→86%, radar scale 0→1, roadmap nodes sequential. | **High** |
| **AI Companion scroll story** | **GSAP + ScrollTrigger scrub** | **🔒 Non-degradable.** Section min-height 300vh. Sticky container 80vh. Master timeline scrubbed 0→1. Phase 1 (0-0.15): orb at scale 0.6. Phase 2 (0.15-0.35): orb flattens (scaleY 1→1.4, scaleX 1→1.6), moves to header position, transmission 0.98→0.3, cards detach. Phase 3 (0.35-0.7): dashboard cards slide from edges. Phase 4 (0.7-1.0): resume score counter 72→86→91, roadmap nodes pulse sequentially, SVG line draws, opportunities slide in. | **High** |
| Feature cards entrance | GSAP + ScrollTrigger | Stagger from below: translateY(60px), opacity 0→1, stagger 0.12s, duration 0.8s. Trigger at 20% from viewport bottom. | Medium |
| Card hover micro-interactions | CSS transitions | Border brighten, bg lighten, shadow deepen, translateY(-4px), icon micro-anim (rotate/pulse/scale). `all 0.4s cubic-bezier(0.16,1,0.3,1)` | Low |
| How It Works step cards | GSAP + ScrollTrigger | Each card: translateX(60px)→0, opacity 0→1, stagger 0.2s. Connecting line: height 0→100% as cards appear. Internal visuals micro-animate. | Medium |
| Final CTA entrance | GSAP + ScrollTrigger | Panel: scale 0.9→1, opacity 0→1, 1s expo.out. Headline: SplitType word stagger 0.05s. CTA: translateY(20px)→0, delay 0.4s. | Medium |
| Text entrance (global) | GSAP + SplitType + ScrollTrigger | Default: words translateY(40px), opacity 0→1, stagger 0.08s, 0.8s, expo.out. Trigger at 85% from top. Reusable helper function. | Low |
| Orb entrance transmission ramp | GSAP | tween orb.material.transmission from 0 to 0.98 over 1.2s synced with scale animation | Low |
| Dashboard hover straighten | CSS | perspective container: rotateY(-5deg) rotateX(2deg) → rotateY(0) rotateX(0) on hover, 0.6s transition | Low |
| CTA panel hover | CSS | rotateX(2deg) → rotateX(0) on hover, 0.6s transition | Low |
| Scroll indicator loop | CSS @keyframes | Circle moves down 40px line over 2s, infinite | Low |
| Footer entrance | GSAP + ScrollTrigger | Fade in with slight translateY(20px), 0.6s | Low |

## State & Logic Plan

### Lenis ↔ ScrollTrigger Sync
Lenis must feed its scroll position directly into ScrollTrigger for all scrub-based animations to work. On every Lenis scroll event, call `ScrollTrigger.update()`. This is the backbone of the entire scroll experience.

```
Lenis onScroll → ScrollTrigger.update()
```

### Three.js ↔ DOM Coordinate Bridge
The hero scene reacts to mouse position. Mouse events are captured on the hero container DOM element. Coordinates are normalized to [-1, 1] and passed into the Three.js animation loop as target values. The render loop lerps actual values toward targets each frame.

```
mousemove on hero container → normalize to [-1, 1] → store as targets → rAF loop lerps actual values
```

### Scroll Story State Machine
The AI Career Companion section is a 4-phase state machine driven by scroll progress (0→1). Each phase triggers specific animation groups:

- **Phase 1** (0–0.15): Orb-only view
- **Phase 2** (0.15–0.35): Orb-to-panel morph
- **Phase 3** (0.35–0.7): Dashboard assembly
- **Phase 4** (0.7–1.0): Live demo animations

Each phase's animations are defined as GSAP timeline segments with specific progress ranges. The master timeline uses `scrub: 1` for 1-second smoothing.

Key state transitions:
- Phase 1→2: Orb begins flattening, cards start detaching
- Phase 2→3: Orb becomes opaque panel, dashboard cards begin sliding in
- Phase 3→4: All cards in position, internal micro-animations begin

### Reduced Motion Detection
A single utility checks `prefers-reduced-motion: reduce` at init and returns a boolean. All animation systems read this flag:
- If true: show all elements in final state immediately (opacity 1, transform none)
- Disable Lenis smooth scroll (use native scroll)
- Hide custom cursor
- Three.js: stop orb rotation/breathing, freeze card orbits, static particles
- ScrollTrigger: show final states of all scrub animations
- Mesh gradient: render once, do not animate

### Text Cycle Word State
The hero headline cycles through 5 words on a 3-second interval. State:
- `currentIndex`: 0–4, tracks which word is showing
- `isAnimating`: boolean, prevents overlap if transition takes longer than interval
- On each tick: SplitType splits both outgoing and incoming words into chars, GSAP animates char groups

### Loading → Hero Orchestration
Strict init sequence:
1. Loading overlay renders immediately (inline CSS, no JS)
2. JS loads, initializes Lenis, ScrollTrigger, Three.js scene (offscreen)
3. `window.onload` fires → overlay fade-out GSAP tween starts
4. On overlay fade complete → hero entrance timeline starts
5. Navigation entrance starts slightly before hero (0.1s delay)

This sequence is managed by a single init function in `main.js` with explicit callbacks between stages.

### Three.js Scene Lifecycle
- **Init**: Create renderer, scene, camera, composer. Append canvas to hero right column container.
- **Resize**: Observe container size via ResizeObserver. Update camera.aspect, renderer.setSize, composer.setSize.
- **Animate**: requestAnimationFrame loop. Update orb (rotation, breathing, mouse tilt), update card orbits, update particles, render via composer.
- **Visibility**: Use Page Visibility API. Pause rAF when tab hidden, resume when visible.
- **Cleanup**: On page unload (or if implementing hot reload), dispose geometries, materials, textures, renderer, composer.

## CSS Architecture

All styles live in a single `main.css` file organized in layers:

1. **Reset & Base**: Normalize, box-sizing, font smoothing, selection colors
2. **Design Tokens**: CSS custom properties for all colors, spacing, typography, easing
3. **Typography**: Font loading, heading/body/caption/label classes
4. **Utilities**: `.glass`, `.glass-hover`, `.container`, `.section`, `.btn-primary`, `.btn-glass`
5. **Layout**: Grid system, responsive breakpoints
6. **Components**: Loading overlay, navigation, hero, sections, footer
7. **Animations**: Keyframes (breathing, scroll indicator), transition utilities
8. **Responsive**: Mobile-first overrides at 768px and 1024px
9. **Reduced Motion**: `prefers-reduced-motion` overrides at the bottom

## Responsive Breakpoints

| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | ≤767px | Single column, stacked layouts, simplified Three.js (32 subdivisions, 20 particles, 4 orbit cards, no bloom), hamburger nav, shorter scroll runway (200vh) |
| Tablet | 768–1023px | 2-column grids, side-by-side hero (50/50), full Three.js scene, hamburger nav |
| Desktop | ≥1024px | Full layout as designed, all animations at full fidelity |

## Performance Checklist

- [ ] Three.js: Use `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` to cap DPR
- [ ] Three.js: Dispose unused geometries/materials/textures on cleanup
- [ ] Three.js: Use `BufferGeometry` (all built-in geometries are already buffered)
- [ ] GSAP: Use `will-change: transform` on animated elements sparingly, remove after animation
- [ ] GSAP: Prefer `transform` and `opacity` only — avoid animating layout properties
- [ ] ScrollTrigger: Use `refreshPriority` for elements that change size during animation
- [ ] Images: Logo should be optimized PNG or SVG
- [ ] Fonts: Use `font-display: swap` to prevent FOIT
- [ ] Canvas: Mesh gradient canvas uses `will-change: transform` for compositor promotion
- [ ] Mobile: Conditionally disable bloom post-processing, reduce geometry subdivisions
- [ ] rAF: Pause Three.js render loop when tab is hidden (Page Visibility API)
- [ ] CSS: Use `contain: layout style paint` on glass card containers
