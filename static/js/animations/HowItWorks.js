/**
 * How It Works — Step Cards Animation
 * Cards slide in from right with connecting line drawing
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { isReducedMotion } from '../utils/reduced-motion.js';

gsap.registerPlugin(ScrollTrigger);

export function initHowItWorks() {
  if (isReducedMotion()) return;

  const stepCards = document.querySelectorAll('.step-card');
  const connectorLine = document.getElementById('connector-line');

  if (!stepCards.length) return;

  // Set initial states
  stepCards.forEach((card) => {
    gsap.set(card, { x: 60, opacity: 0 });
  });

  if (connectorLine) {
    gsap.set(connectorLine, { height: 0 });
  }

  // Create scroll trigger for the section
  ScrollTrigger.create({
    trigger: '.how-it-works__steps',
    start: 'top 75%',
    onEnter: () => {
      // Stagger cards
      gsap.to(stepCards, {
        x: 0,
        opacity: 1,
        duration: 0.8,
        stagger: 0.2,
        ease: 'expo.out',
      });

      // Draw connector line
      if (connectorLine) {
        const stepsHeight = document.querySelector('.how-it-works__steps').offsetHeight;
        gsap.to(connectorLine, {
          height: stepsHeight - 100,
          duration: 2,
          ease: 'expo.out',
          delay: 0.3,
        });
      }
    },
    once: true,
  });
}
