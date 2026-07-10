/**
 * SplitType wrapper with cleanup
 * Provides a consistent API for splitting text into words/chars
 */

import SplitType from 'split-type';
import { isReducedMotion } from './reduced-motion.js';

const splitInstances = [];

/**
 * Split text elements for animation
 * @param {string|Element} target - CSS selector or DOM element
 * @param {Object} options - SplitType options
 * @returns {SplitType|null} The SplitType instance or null if reduced motion
 */
export function splitText(target, options = { types: 'words,chars' }) {
  if (isReducedMotion()) return null;

  const elements = typeof target === 'string' ? document.querySelectorAll(target) : [target];

  const instances = [];
  elements.forEach((el) => {
    const split = new SplitType(el, options);
    splitInstances.push(split);
    instances.push(split);
  });

  return instances.length === 1 ? instances[0] : instances;
}

/**
 * Revert all split text instances
 */
export function revertAllSplits() {
  splitInstances.forEach((split) => {
    if (split && split.revert) {
      split.revert();
    }
  });
  splitInstances.length = 0;
}

/**
 * Get split elements for animation
 * @param {SplitType} splitInstance
 * @param {string} type - 'words' or 'chars'
 * @returns {Array}
 */
export function getSplitElements(splitInstance, type = 'words') {
  if (!splitInstance) return [];
  return splitInstance[type] || [];
}
