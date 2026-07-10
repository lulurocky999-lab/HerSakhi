/**
 * Navigation Animation
 * - Scroll-based glass transformation
 * - Mobile hamburger menu
 * - Active link tracking via IntersectionObserver
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { scrollTo } from '../utils/lenis-init.js';

gsap.registerPlugin(ScrollTrigger);

export function initNavigation() {
  const nav = document.getElementById('nav');
  if (!nav) return;

  // Scroll-based glass transformation
  ScrollTrigger.create({
    start: 80,
    onUpdate: (self) => {
      if (self.scroll() > 80) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
    },
  });

  // Mobile hamburger
  const hamburger = nav.querySelector('.nav__hamburger');
  const mobileMenu = nav.querySelector('.nav__mobile-menu');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Close mobile menu on link click
    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  // Smooth scroll for nav links
  nav.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = link.getAttribute('href');
      scrollTo(target, { offset: -80 });
    });
  });

  // Active link tracking via IntersectionObserver
  const sections = document.querySelectorAll('section[id]');
  const navLinks = nav.querySelectorAll('.nav__link');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach((link) => {
            link.classList.remove('nav__link--active');
            if (link.getAttribute('href') === `#${id}`) {
              link.classList.add('nav__link--active');
            }
          });
        }
      });
    },
    {
      rootMargin: '-40% 0px -40% 0px',
    }
  );

  sections.forEach((section) => observer.observe(section));

  // Nav entrance animation
  gsap.from(nav, {
    y: -20,
    opacity: 0,
    duration: 0.5,
    delay: 0.1,
    ease: 'expo.out',
  });
}
