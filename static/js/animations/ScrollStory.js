/**
 * AI Career Companion — Scroll-Driven Story
 * 4-phase animation: Orb → Transformation → Dashboard Assembly → Live Demo
 * Uses GSAP ScrollTrigger with scrub
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { isReducedMotion } from '../utils/reduced-motion.js';

gsap.registerPlugin(ScrollTrigger);

export function initScrollStory() {
  if (isReducedMotion()) {
    // Show final state
    const dashboard = document.getElementById('ai-dashboard');
    const orb = document.getElementById('ai-orb-wrapper');
    if (dashboard) dashboard.style.opacity = '1';
    if (orb) orb.style.opacity = '0';
    return;
  }

  const runway = document.getElementById('ai-scroll-runway');
  const orbWrapper = document.getElementById('ai-orb-wrapper');
  const orb = document.getElementById('ai-orb');
  const dashboard = document.getElementById('ai-dashboard');

  if (!runway || !orbWrapper || !orb || !dashboard) return;

  // Get dashboard elements
  const dashHeader = document.getElementById('ai-dash-header');
  const dashLeft = document.getElementById('ai-dash-left');
  const dashRight = document.getElementById('ai-dash-right');
  const analyzerCard = document.getElementById('ai-analyzer-card');
  const oppsCard = document.getElementById('ai-opps-card');

  // Set initial states
  gsap.set(orbWrapper, { opacity: 1, scale: 0.6 });
  gsap.set(orb, { scaleX: 1, scaleY: 1 });
  gsap.set(dashboard, { opacity: 0, pointerEvents: 'none' });
  gsap.set(dashHeader, { y: -30, opacity: 0 });
  gsap.set(dashLeft, { x: -60, opacity: 0 });
  gsap.set(dashRight, { x: 60, opacity: 0 });
  gsap.set(analyzerCard, { scale: 0.8, opacity: 0 });
  gsap.set(oppsCard, { y: 40, opacity: 0 });

  // Create master timeline
  const masterTl = gsap.timeline({
    scrollTrigger: {
      trigger: runway,
      start: 'top top',
      end: 'bottom bottom',
      scrub: 1,
      pin: false,
    },
  });

  // Phase 1 (0-0.15): Orb visible, slight glow intensification
  masterTl.to(orb, {
    boxShadow: '0 0 100px rgba(124, 92, 252, 0.5), 0 0 200px rgba(79, 140, 255, 0.25), inset 0 0 60px rgba(255, 255, 255, 0.3)',
    duration: 0.15,
  });

  // Phase 2 (0.15-0.35): Orb transformation
  masterTl.to(
    orbWrapper,
    {
      opacity: 0,
      scale: 0.3,
      x: '-30%',
      y: '-30%',
      duration: 0.2,
      ease: 'expo.in',
    },
    0.15
  );

  masterTl.to(
    orb,
    {
      scaleX: 1.6,
      scaleY: 1.4,
      duration: 0.2,
      ease: 'expo.inOut',
    },
    0.15
  );

  // Dashboard fades in
  masterTl.to(
    dashboard,
    {
      opacity: 1,
      pointerEvents: 'all',
      duration: 0.15,
    },
    0.25
  );

  // Phase 3 (0.35-0.7): Dashboard assembly
  masterTl.to(
    dashHeader,
    {
      y: 0,
      opacity: 1,
      duration: 0.1,
      ease: 'expo.out',
    },
    0.35
  );

  masterTl.to(
    dashLeft,
    {
      x: 0,
      opacity: 1,
      duration: 0.12,
      ease: 'expo.out',
    },
    0.4
  );

  masterTl.to(
    analyzerCard,
    {
      scale: 1,
      opacity: 1,
      duration: 0.12,
      ease: 'expo.out',
    },
    0.45
  );

  masterTl.to(
    dashRight,
    {
      x: 0,
      opacity: 1,
      duration: 0.12,
      ease: 'expo.out',
    },
    0.5
  );

  masterTl.to(
    oppsCard,
    {
      y: 0,
      opacity: 1,
      duration: 0.1,
      ease: 'expo.out',
    },
    0.6
  );

  // Phase 4 (0.7-1.0): Live demo animations
  // Score counter: 72 → 86 → 91
  const scoreEl = document.getElementById('ai-score-number');
  const scoreRing = document.getElementById('ai-score-ring-fill');
  const analyzerScore = document.getElementById('ai-analyzer-score');
  const analyzerStatus = document.getElementById('ai-analyzer-status');

  const scoreObj = { value: 72 };
  masterTl.to(
    scoreObj,
    {
      value: 86,
      duration: 0.1,
      ease: 'power2.out',
      onUpdate: () => {
        const val = Math.round(scoreObj.value);
        if (scoreEl) scoreEl.textContent = val;
        if (analyzerScore) analyzerScore.textContent = val;
        if (scoreRing) {
          scoreRing.style.strokeDashoffset = 314 * (1 - val / 100);
        }
      },
    },
    0.7
  );

  masterTl.to(
    scoreObj,
    {
      value: 91,
      duration: 0.1,
      ease: 'power2.out',
      onUpdate: () => {
        const val = Math.round(scoreObj.value);
        if (scoreEl) scoreEl.textContent = val;
        if (analyzerScore) analyzerScore.textContent = val;
        if (scoreRing) {
          scoreRing.style.strokeDashoffset = 314 * (1 - val / 100);
        }
      },
    },
    0.85
  );

  // Status change
  if (analyzerStatus) {
    masterTl.call(
      () => {
        analyzerStatus.textContent = 'Analyzing';
      },
      [],
      0.72
    );
    masterTl.call(
      () => {
        analyzerStatus.textContent = 'Optimized';
        analyzerStatus.style.color = '#22c55e';
      },
      [],
      0.88
    );
  }

  // Check items
  const checks = document.querySelectorAll('.ai-check');
  checks.forEach((check, i) => {
    masterTl.call(
      () => check.classList.add('checked'),
      [],
      0.75 + i * 0.04
    );
  });

  // Roadmap nodes activate
  for (let i = 1; i <= 5; i++) {
    const node = document.getElementById(`ai-rm-${i}`);
    const connector = document.getElementById(`ai-rm-conn-${i}`);
    if (node) {
      masterTl.call(
        () => node.classList.add('active'),
        [],
        0.7 + i * 0.05
      );
    }
    if (connector) {
      masterTl.call(
        () => connector.classList.add('active'),
        [],
        0.7 + i * 0.05
      );
    }
  }

  // Goals check
  const goals = document.querySelectorAll('.ai-goal');
  goals.forEach((goal, i) => {
    masterTl.call(
      () => goal.classList.add('checked'),
      [],
      0.78 + i * 0.04
    );
  });

  // Goals progress bar
  const goalsBar = document.getElementById('ai-goals-bar');
  if (goalsBar) {
    masterTl.call(
      () => {
        goalsBar.style.width = '100%';
      },
      [],
      0.92
    );
  }

  // Opportunity items slide in
  const oppItems = document.querySelectorAll('.ai-opp-item');
  oppItems.forEach((item, i) => {
    gsap.set(item, { x: 40, opacity: 0 });
    masterTl.to(
      item,
      {
        x: 0,
        opacity: 1,
        duration: 0.05,
        ease: 'expo.out',
      },
      0.8 + i * 0.05
    );
  });
}
