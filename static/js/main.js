/**
 * HerSakhi — Main Entry Point
 * Orchestrates initialization in strict order:
 * 1. Reduced motion detection
 * 2. Loading overlay (hides on load)
 * 3. Lenis smooth scroll
 * 4. Mesh gradient backgrounds
 * 5. Custom cursor
 * 6. Navigation
 * 7. Three.js hero scene
 * 8. Hero entrance animations
 * 9. Text cycle
 * 10. Scroll-driven sections
 * 11. Magnetic buttons
 */



import { initReducedMotion } from './utils/reduced-motion.js';
import { initLenis } from './utils/lenis-init.js';
import { initMeshGradients } from './components/MeshGradient.js';
import { initCustomCursor } from './components/CustomCursor.js';
import { initMagneticButtons } from './components/MagneticButton.js';
import { initNavigation } from './animations/Navigation.js';
import { initLoadingOverlay } from './animations/LoadingOverlay.js';
import { initHeroEntrance } from './animations/HeroEntrance.js';
import { initTextCycle } from './animations/TextCycle.js';
import { initHeroScene } from './three/HeroScene.js';
import { initDashboardAssembly } from './animations/DashboardAssembly.js';
import { initScrollStory } from './animations/ScrollStory.js';
import { initFeaturesGrid } from './animations/FeaturesGrid.js';
import { initHowItWorks } from './animations/HowItWorks.js';
import { initFinalCTA } from './animations/FinalCTA.js';
import { initFooterReveal } from './animations/FooterReveal.js';

// Strict initialization order
function init() {
  // 1. Detect reduced motion preference
  initReducedMotion();

  // 2. Show loading overlay, hide on load, then initialize everything else
  initLoadingOverlay(() => {
    // 3. Initialize Lenis smooth scroll
    initLenis();

    // 4. Mesh gradient backgrounds
    initMeshGradients();

    // 5. Custom cursor (desktop only)
    initCustomCursor();

    // 6. Navigation
    initNavigation();

    // 7. Three.js hero scene
    const heroScene = initHeroScene();

    // 8. Hero entrance animations
    initHeroEntrance();

    // 9. Text cycle
    initTextCycle();

    // 10. Scroll-driven sections
    initDashboardAssembly();
    initScrollStory();
    initFeaturesGrid();
    initHowItWorks();
    initFinalCTA();
    initFooterReveal();

    // 11. Magnetic buttons
    initMagneticButtons();

    // Make hero scene available globally for debugging
    window.heroScene = heroScene;
  });
}

// Start initialization when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
