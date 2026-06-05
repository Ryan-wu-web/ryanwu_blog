/**
 * Page-level typewriter effect - replaces page title with cycling slogans
 * Robust version with retry for PJAX pages
 */
(function() {
  'use strict';

  const pageTypewriters = {
    '/categories/tech/': {
      strings: [
        '向上学习，向下扎根，技术改变世界',
        'Keep learning, keep building, tech changes the world'
      ],
      speed: 80
    },
    '/categories/life/': {
      strings: [
        '热爱生活，记录美好，追寻真实的自我',
        'Love life, record moments, chase the real you'
      ],
      speed: 80
    },
    '/archives/': {
      strings: [
        '路很长，我们慢慢走',
        'The road is long, we walk slowly'
      ],
      speed: 100
    },
    '/tags/': {
      strings: [
        '钻研技术栈，落地项目，追逐创新',
        'Learn stacks, build projects, chase innovation'
      ],
      speed: 80
    }
  };

  const path = window.location.pathname;
  const config = pageTypewriters[path];
  if (!config) return;

  // Track if we've already initialized on this element
  let initialized = false;

  function initTypewriter() {
    if (initialized) return;

    const titleEl = document.querySelector('#site-title');
    if (!titleEl) {
      // Retry after delay if element not ready (PJAX still loading)
      setTimeout(initTypewriter, 500);
      return;
    }

    initialized = true;

    // Clear original text and set up container inside h1#site-title
    titleEl.innerHTML = '';

    const textSpan = document.createElement('span');
    textSpan.className = 'typed-page-title';

    const cursor = document.createElement('span');
    cursor.className = 'typed-cursor';
    cursor.textContent = '|';
    cursor.style.cssText = 'animation: typedBlink 1s infinite; font-weight: 100;';

    titleEl.appendChild(textSpan);
    titleEl.appendChild(cursor);

    // Add cursor blink animation
    if (!document.getElementById('typed-cursor-style')) {
      const style = document.createElement('style');
      style.id = 'typed-cursor-style';
      style.textContent = '@keyframes typedBlink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }';
      document.head.appendChild(style);
    }

    // Typewriter logic
    let stringIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
      const currentString = config.strings[stringIndex];

      if (isDeleting) {
        textSpan.textContent = currentString.substring(0, charIndex - 1);
        charIndex--;
      } else {
        textSpan.textContent = currentString.substring(0, charIndex + 1);
        charIndex++;
      }

      let typeSpeed = config.speed;

      if (isDeleting) {
        typeSpeed = config.speed / 2;
      }

      if (!isDeleting && charIndex === currentString.length) {
        typeSpeed = 2500;
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        stringIndex = (stringIndex + 1) % config.strings.length;
        typeSpeed = 500;
      }

      setTimeout(type, typeSpeed);
    }

    setTimeout(type, 800);
  }

  // Try immediately
  initTypewriter();

  // Also retry on window load (after all resources including PJAX content)
  window.addEventListener('load', initTypewriter);

  // Retry on PJAX complete if supported
  document.addEventListener('pjax:complete', function() {
    initialized = false;
    initTypewriter();
  });

  // Fallback: keep retrying for up to 5 seconds
  let retries = 0;
  const fallbackInterval = setInterval(function() {
    if (initialized || retries > 10) {
      clearInterval(fallbackInterval);
      return;
    }
    initTypewriter();
    retries++;
  }, 500);
})();
