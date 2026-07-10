/**
 * Final CTA Section Animation
 * Glass panel scales in, headline splits, CTA fades up
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { isReducedMotion } from '../utils/reduced-motion.js';

gsap.registerPlugin(ScrollTrigger);

export function initFinalCTA() {
  if (isReducedMotion()) return;

  const panel = document.getElementById('cta-panel');
  const headline = panel?.querySelector('.final-cta__headline');
  const subhead = panel?.querySelector('.final-cta__subhead');
  const btn = document.getElementById('cta-btn');
  const note = panel?.querySelector('.final-cta__note');

  if (!panel) return;

  // Set initial state
  gsap.set(panel, { scale: 0.9, opacity: 0 });
  if (headline) gsap.set(headline, { y: 30, opacity: 0 });
  if (subhead) gsap.set(subhead, { y: 20, opacity: 0 });
  if (btn) gsap.set(btn, { y: 20, opacity: 0 });
  if (note) gsap.set(note, { y: 10, opacity: 0 });

  ScrollTrigger.create({
    trigger: panel,
    start: 'top 80%',
    onEnter: () => {
      const tl = gsap.timeline();

      tl.to(panel, {
        scale: 1,
        opacity: 1,
        duration: 1,
        ease: 'expo.out',
      })
        .to(
          headline,
          {
            y: 0,
            opacity: 1,
            duration: 0.8,
            ease: 'expo.out',
          },
          '-=0.6'
        )
        .to(
          subhead,
          {
            y: 0,
            opacity: 1,
            duration: 0.6,
            ease: 'expo.out',
          },
          '-=0.5'
        )
        .to(
          btn,
          {
            y: 0,
            opacity: 1,
            duration: 0.6,
            ease: 'expo.out',
          },
          '-=0.4'
        )
        .to(
          note,
          {
            y: 0,
            opacity: 1,
            duration: 0.5,
            ease: 'expo.out',
          },
          '-=0.3'
        );
    },
    once: true,
  });
}
