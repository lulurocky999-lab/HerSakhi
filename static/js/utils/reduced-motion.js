/**
 * Reduced Motion Detection Utility
 * Checks for prefers-reduced-motion and returns a reactive boolean
 */

let reducedMotion = false;

export function initReducedMotion() {
  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  reducedMotion = mediaQuery.matches;

  mediaQuery.addEventListener('change', (e) => {
    reducedMotion = e.matches;
  });

  return reducedMotion;
}

export function isReducedMotion() {
  return reducedMotion;
}
