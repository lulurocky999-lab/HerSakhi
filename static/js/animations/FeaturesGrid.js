/**
 * Features Grid Entrance Animation
 * Cards stagger in from below
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { isReducedMotion } from '../utils/reduced-motion.js';

gsap.registerPlugin(ScrollTrigger);

export function initFeaturesGrid() {
  if (isReducedMotion()) return;

  const cards = document.querySelectorAll('.feature-card');
  if (!cards.length) return;

  gsap.from(cards, {
    y: 60,
    opacity: 0,
    duration: 0.8,
    stagger: 0.12,
    ease: 'expo.out',
    scrollTrigger: {
      trigger: cards[0],
      start: 'top 80%',
    },
  });
}
