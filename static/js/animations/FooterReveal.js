/**
 * Footer Entrance Animation
 * Simple fade in with slight translate
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { isReducedMotion } from '../utils/reduced-motion.js';

gsap.registerPlugin(ScrollTrigger);

export function initFooterReveal() {
  if (isReducedMotion()) return;

  const footer = document.querySelector('.footer');
  if (!footer) return;

  gsap.from(footer, {
    y: 20,
    opacity: 0,
    duration: 0.6,
    ease: 'expo.out',
    scrollTrigger: {
      trigger: footer,
      start: 'top 90%',
    },
  });
}
