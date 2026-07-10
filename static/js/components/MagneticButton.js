/**
 * Magnetic Button Effect
 * Button subtly follows cursor within a radius on hover
 */

export function initMagneticButtons() {
  const buttons = document.querySelectorAll('.magnetic-btn');
  const isTouchDevice = window.matchMedia('(hover: none) and (pointer: coarse)').matches;

  if (isTouchDevice) return;

  buttons.forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      // Calculate offset from center (max 8px)
      const deltaX = (e.clientX - centerX) * 0.15;
      const deltaY = (e.clientY - centerY) * 0.15;

      // Clamp to max 8px
      const clampedX = Math.max(-8, Math.min(8, deltaX));
      const clampedY = Math.max(-8, Math.min(8, deltaY));

      btn.style.transform = `translate(${clampedX}px, ${clampedY}px)`;
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translate(0, 0)';
    });
  });
}
