/**
 * Lenis Smooth Scroll + ScrollTrigger Sync
 */

import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { isReducedMotion } from './reduced-motion.js';

gsap.registerPlugin(ScrollTrigger);

let lenis = null;

export function initLenis() {
  if (isReducedMotion()) {
    // Disable smooth scroll for reduced motion
    ScrollTrigger.defaults({
      scroller: window,
    });
    return null;
  }

  lenis = new Lenis({
    lerp: 0.1,
    smoothWheel: true,
    wheelMultiplier: 0.8,
  });

  // Sync Lenis with ScrollTrigger
  lenis.on('scroll', ScrollTrigger.update);

  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });

  gsap.ticker.lagSmoothing(0);

  return lenis;
}

export function getLenis() {
  return lenis;
}

export function scrollTo(target, options = {}) {
  if (lenis) {
    lenis.scrollTo(target, options);
  } else {
    // Fallback for reduced motion
    const el = typeof target === 'string' ? document.querySelector(target) : target;
    if (el) {
      el.scrollIntoView({ behavior: 'auto', ...options });
    }
  }
}
