/**
 * Hero Entrance Animation
 * Orchestrated sequence of left column text and right column orb/cards
 */

import { gsap } from 'gsap';
import { isReducedMotion } from '../utils/reduced-motion.js';

export function initHeroEntrance() {
  if (isReducedMotion()) {
    // Show everything immediately
    const elements = document.querySelectorAll(
      '.hero__logo, .hero__label, .hero__headline, .hero__description, .hero__ctas, .hero__scroll-indicator'
    );
    elements.forEach((el) => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  const tl = gsap.timeline({ delay: 0.2 });

  // Left column elements
  tl.to('.hero__logo', {
    y: 0,
    opacity: 1,
    duration: 0.8,
    ease: 'expo.out',
  })
    .to(
      '.hero__label',
      {
        y: 0,
        opacity: 1,
        duration: 0.6,
        ease: 'expo.out',
      },
      0.4
    )
    .to(
      '.hero__headline',
      {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'expo.out',
      },
      0.5
    )
    .to(
      '.hero__description',
      {
        y: 0,
        opacity: 1,
        duration: 0.6,
        ease: 'expo.out',
      },
      0.9
    )
    .to(
      '.hero__ctas',
      {
        y: 0,
        opacity: 1,
        duration: 0.5,
        ease: 'expo.out',
      },
      1.1
    )
    .to(
      '.hero__scroll-indicator',
      {
        opacity: 1,
        duration: 1,
        ease: 'expo.out',
      },
      1.5
    );

  return tl;
}
