/**
 * Hero Headline Word Cycling
 * Cycles through: Empowering → Dreams → Skills → Careers → Leaders
 * Each character animates individually
 */

import { gsap } from 'gsap';
import { isReducedMotion } from '../utils/reduced-motion.js';

const WORDS = ['Dreams', 'Skills', 'Careers', 'Future', 'Leader'];
const CYCLE_INTERVAL = 3000; // ms

export function initTextCycle() {
  const cycleEl = document.getElementById('headline-cycle');
  if (!cycleEl) return;

  if (isReducedMotion()) {
    cycleEl.textContent = WORDS[0];
    return;
  }

  let currentIndex = 0;
  let isAnimating = false;

  function animateWordChange(newWord) {
    if (isAnimating) return;
    isAnimating = true;

    const oldText = cycleEl.textContent;
    const maxLen = Math.max(oldText.length, newWord.length);

    // Build character spans
    let html = '';
    for (let i = 0; i < maxLen; i++) {
      const oldChar = oldText[i] || '';
      const newChar = newWord[i] || '';
      html += `<span class="cycle-char" data-old="${oldChar}" data-new="${newChar}" style="display:inline-block;position:relative;">`;
      html += `<span class="cycle-old" style="display:inline-block;">${oldChar}</span>`;
      html += `<span class="cycle-new" style="display:inline-block;position:absolute;left:0;top:0;opacity:0;transform:translateY(100%);">${newChar}</span>`;
      html += `</span>`;
    }
    cycleEl.innerHTML = html;

    const chars = cycleEl.querySelectorAll('.cycle-char');

    const tl = gsap.timeline({
      onComplete: () => {
        cycleEl.textContent = newWord;
        isAnimating = false;
      },
    });

    // Animate out old characters
    tl.to(chars.querySelectorAll ? chars[0].parentElement.querySelectorAll('.cycle-old') : [], {
      y: '-100%',
      opacity: 0,
      duration: 0.4,
      stagger: 0.03,
      ease: 'expo.in',
    });

    // Animate in new characters
    tl.to(
      cycleEl.querySelectorAll('.cycle-new'),
      {
        y: '0%',
        opacity: 1,
        duration: 0.5,
        stagger: 0.03,
        ease: 'expo.out',
      },
      '-=0.2'
    );
  }

  // Simple version: fade/slide the whole word
  function cycleWord() {
    if (isAnimating) return;
    isAnimating = true;

    const nextIndex = (currentIndex + 1) % WORDS.length;
    const nextWord = WORDS[nextIndex];

    // Animate out
    gsap.to(cycleEl, {
      y: -20,
      opacity: 0,
      duration: 0.3,
      ease: 'expo.in',
      onComplete: () => {
        cycleEl.textContent = nextWord;
        currentIndex = nextIndex;

        // Animate in
        gsap.fromTo(
          cycleEl,
          { y: 20, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            duration: 0.4,
            ease: 'expo.out',
            onComplete: () => {
              isAnimating = false;
            },
          }
        );
      },
    });
  }

  // Set initial word
  cycleEl.textContent = WORDS[0];

  // Start cycling
  setInterval(cycleWord, CYCLE_INTERVAL);
}
