/**
 * "Who Is HerSakhi?" Dashboard Assembly Animation
 * Cards scatter from random positions and assemble into the dashboard panel on scroll
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { isReducedMotion } from '../utils/reduced-motion.js';

gsap.registerPlugin(ScrollTrigger);

export function initDashboardAssembly() {
  if (isReducedMotion()) return;

  const section = document.querySelector('.who-is');
  const panel = document.getElementById('dashboard-panel');
  const cards = [
    document.getElementById('dash-card-1'),
    document.getElementById('dash-card-2'),
    document.getElementById('dash-card-3'),
    document.getElementById('dash-card-4'),
    document.getElementById('dash-card-5'),
    document.getElementById('dash-card-6'),
  ];

  if (!section || !panel || cards.some((c) => !c)) return;

  // Set initial scattered state for cards
  const scatterPositions = [
    { x: -300, y: -200, rotate: -15 },
    { x: 350, y: -180, rotate: 12 },
    { x: -280, y: 50, rotate: -8 },
    { x: 320, y: 80, rotate: 15 },
    { x: -250, y: 250, rotate: 10 },
    { x: 300, y: 220, rotate: -12 },
  ];

  cards.forEach((card, i) => {
    gsap.set(card, {
      x: scatterPositions[i].x,
      y: scatterPositions[i].y,
      rotation: scatterPositions[i].rotate,
      opacity: 0,
      scale: 0.8,
    });
  });

  gsap.set(panel, { scale: 0.9, opacity: 0 });

  // Create scroll-driven timeline
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: section,
      start: 'top 80%',
      end: 'center center',
      scrub: 1,
    },
  });

  // Panel scales in
  tl.to(panel, {
    scale: 1,
    opacity: 1,
    duration: 0.3,
    ease: 'expo.out',
  });

  // Cards assemble at staggered progress points
  const cardProgressPoints = [0.1, 0.25, 0.4, 0.55, 0.7, 0.85];
  cards.forEach((card, i) => {
    tl.to(
      card,
      {
        x: 0,
        y: 0,
        rotation: 0,
        opacity: 1,
        scale: 1,
        duration: 0.2,
        ease: 'expo.out',
      },
      cardProgressPoints[i]
    );
  });

  // Progress ring animation
  const ringFill = document.getElementById('progress-ring-fill');
  if (ringFill) {
    tl.to(
      ringFill,
      {
        strokeDashoffset: 314 * (1 - 0.86),
        duration: 0.5,
        ease: 'expo.out',
      },
      0.4
    );
  }

  // Radar chart scale
  const radarFill = document.getElementById('radar-fill');
  if (radarFill) {
    tl.to(
      radarFill,
      {
        scale: 1,
        duration: 0.3,
        ease: 'expo.out',
        onStart: () => radarFill.classList.add('active'),
      },
      0.5
    );
  }

  // Career score counter
  const scoreEl = document.getElementById('career-score');
  if (scoreEl) {
    const scoreObj = { value: 0 };
    tl.to(
      scoreObj,
      {
        value: 86,
        duration: 0.5,
        ease: 'expo.out',
        onUpdate: () => {
          scoreEl.textContent = Math.round(scoreObj.value);
        },
      },
      0.3
    );
  }
}
