/**
 * Custom Cursor — Glass dot with hover expand
 * Desktop only, follows cursor with slight lag
 */

import { isReducedMotion } from '../utils/reduced-motion.js';

class CustomCursor {
  constructor() {
    this.cursor = document.getElementById('custom-cursor');
    if (!this.cursor) return;

    // Hide on touch devices
    if (window.matchMedia('(hover: none) and (pointer: coarse)').matches) {
      this.cursor.style.display = 'none';
      return;
    }

    if (isReducedMotion()) {
      this.cursor.style.display = 'none';
      return;
    }

    this.x = 0;
    this.y = 0;
    this.targetX = 0;
    this.targetY = 0;

    this.isHovering = false;

    this.init();
  }

  init() {
    // Track mouse position
    document.addEventListener('mousemove', (e) => {
      this.targetX = e.clientX;
      this.targetY = e.clientY;
    });

    // Expand on interactive elements
    const interactiveSelectors = 'a, button, .magnetic-btn, .glass-card, .nav__link';
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(interactiveSelectors)) {
        this.isHovering = true;
        this.cursor.classList.add('expanded');
      }
    });

    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(interactiveSelectors)) {
        this.isHovering = false;
        this.cursor.classList.remove('expanded');
      }
    });

    // Start animation loop
    this.animate();

    // Hide default cursor
    document.body.style.cursor = 'none';

    // Re-show on leave
    document.addEventListener('mouseleave', () => {
      this.cursor.style.opacity = '0';
    });
    document.addEventListener('mouseenter', () => {
      this.cursor.style.opacity = '1';
    });
  }

  animate() {
    // Lerp toward target
    this.x += (this.targetX - this.x) * 0.15;
    this.y += (this.targetY - this.y) * 0.15;

    this.cursor.style.transform = `translate(${this.x}px, ${this.y}px)`;

    requestAnimationFrame(() => this.animate());
  }
}

export function initCustomCursor() {
  return new CustomCursor();
}

export default CustomCursor;
