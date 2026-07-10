/**
 * Loading Overlay
 * Minimal fullscreen overlay with breathing glass orb
 * Fades out immediately on window.load
 */

import { gsap } from 'gsap';

export function initLoadingOverlay(onComplete) {
  const overlay = document.getElementById('loading-overlay');
  if (!overlay) {
    if (onComplete) onComplete();
    return;
  }

  const hideOverlay = () => {
    gsap.to(overlay, {
      opacity: 0,
      duration: 0.6,
      ease: 'expo.out',
      onComplete: () => {
        overlay.style.display = 'none';
        if (onComplete) onComplete();
      },
    });
  };

  // If already loaded, hide immediately
  if (document.readyState === 'complete') {
    hideOverlay();
  } else {
    window.addEventListener('load', hideOverlay);
  }
}
