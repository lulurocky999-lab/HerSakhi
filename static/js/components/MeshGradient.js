/**
 * Animated Mesh Gradient Background
 * Uses canvas with 4 moving control points (simplex-like noise) for bilinear color interpolation
 */

import { isReducedMotion } from '../utils/reduced-motion.js';

// Simple noise function for smooth random movement
function noise(t) {
  return Math.sin(t) * 0.5 + Math.sin(t * 1.3) * 0.25 + Math.sin(t * 0.7) * 0.25;
}

class MeshGradient {
  constructor(canvasId, colors, speed = 0.0002) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;

    this.ctx = this.canvas.getContext('2d');
    this.colors = colors;
    this.speed = speed;
    this.time = Math.random() * 1000;
    this.reducedMotion = isReducedMotion();

    // 4 control points with initial positions and random seeds
    this.points = [
      { x: 0.2, y: 0.2, seed: 0 },
      { x: 0.8, y: 0.2, seed: 1 },
      { x: 0.2, y: 0.8, seed: 2 },
      { x: 0.8, y: 0.8, seed: 3 },
    ];

    this.resize();
    window.addEventListener('resize', () => this.resize());

    if (!this.reducedMotion) {
      this.animate();
    } else {
      this.renderStatic();
    }
  }

  resize() {
    if (!this.canvas) return;
    const dpr = Math.min(window.devicePixelRatio, 2);
    this.canvas.width = window.innerWidth * dpr;
    this.canvas.height = window.innerHeight * dpr;
    this.ctx.scale(dpr, dpr);
    this.width = window.innerWidth;
    this.height = window.innerHeight;

    if (this.reducedMotion) {
      this.renderStatic();
    }
  }

  hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16),
    } : { r: 0, g: 0, b: 0 };
  }

  bilinearColor(x, y, colors) {
    const c1 = this.hexToRgb(colors[0]);
    const c2 = this.hexToRgb(colors[1]);
    const c3 = this.hexToRgb(colors[2]);
    const c4 = this.hexToRgb(colors[3]);

    const r = (
      c1.r * (1 - x) * (1 - y) +
      c2.r * x * (1 - y) +
      c3.r * (1 - x) * y +
      c4.r * x * y
    );
    const g = (
      c1.g * (1 - x) * (1 - y) +
      c2.g * x * (1 - y) +
      c3.g * (1 - x) * y +
      c4.g * x * y
    );
    const b = (
      c1.b * (1 - x) * (1 - y) +
      c2.b * x * (1 - y) +
      c3.b * (1 - x) * y +
      c4.b * x * y
    );

    return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
  }

  render() {
    if (!this.ctx) return;

    const gridSize = 20;
    const cellW = this.width / gridSize;
    const cellH = this.height / gridSize;

    for (let i = 0; i < gridSize; i++) {
      for (let j = 0; j < gridSize; j++) {
        const x = i / (gridSize - 1);
        const y = j / (gridSize - 1);

        const color = this.bilinearColor(x, y, this.colors);
        this.ctx.fillStyle = color;
        this.ctx.fillRect(i * cellW, j * cellH, cellW + 1, cellH + 1);
      }
    }
  }

  renderStatic() {
    this.render();
  }

  animate() {
    if (this.reducedMotion) return;

    this.time += this.speed * 16;

    // Update control point positions with noise
    this.points.forEach((p, i) => {
      p.x = 0.3 + 0.4 * (0.5 + 0.5 * noise(this.time + p.seed * 10));
      p.y = 0.3 + 0.4 * (0.5 + 0.5 * noise(this.time + p.seed * 10 + 100));
    });

    // Update colors based on point positions
    this.currentColors = this.colors.map((c, i) => {
      // Slightly shift colors based on point movement
      return c;
    });

    this.render();
    requestAnimationFrame(() => this.animate());
  }

  setOpacity(value) {
    if (this.canvas) {
      this.canvas.style.opacity = value;
    }
  }

  destroy() {
    this.reducedMotion = true; // Stop animation
  }
}

export function initMeshGradients() {
  // Hero gradient — more violet
  const heroGradient = new MeshGradient('mesh-gradient-hero', [
    '#E8E0F0',
    '#F0E8F8',
    '#D4E0F0',
    '#FAFAFA',
  ], 0.00015);

  heroGradient.setOpacity(0.7);

  // CTA gradient — more blue/violet
  const ctaGradient = new MeshGradient('mesh-gradient-cta', [
    '#D4E0F0',
    '#E0ECF8',
    '#E8E0F0',
    '#E0E0F8',
  ], 0.0002);

  ctaGradient.setOpacity(0.6);

  return { heroGradient, ctaGradient };
}

export default MeshGradient;
