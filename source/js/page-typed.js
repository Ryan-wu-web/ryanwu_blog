/**
 * Page-level typewriter effect for category/tag/archive pages
 * Injected via Butterfly inject configuration
 */
(function() {
  'use strict';

  // Page-specific typewriter configurations
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

  // Wait for DOM ready
  function initTypewriter() {
    // Find the page title element - try multiple selectors
    const titleEl = document.querySelector('.page-title, #site-title, .site-page-title, h1.page-title, .article-title, #page-header-title');
    if (!titleEl) {
      // Retry after a short delay if element not found
      setTimeout(initTypewriter, 300);
      return;
    }

    // Create typewriter container
    const container = document.createElement('div');
    container.className = 'page-typed-subtitle';
    container.style.cssText = 'font-size: 1.1rem; margin-top: 12px; opacity: 0.95; min-height: 1.6em; font-weight: 400; letter-spacing: 1px;';

    const textSpan = document.createElement('span');
    textSpan.className = 'typed-text';

    const cursor = document.createElement('span');
    cursor.className = 'typed-cursor';
    cursor.textContent = '|';

    container.appendChild(textSpan);
    container.appendChild(cursor);

    // Insert after title
    titleEl.parentNode.insertBefore(container, titleEl.nextSibling);

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
        typeSpeed = 2500; // Pause before deleting
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        stringIndex = (stringIndex + 1) % config.strings.length;
        typeSpeed = 500;
      }

      setTimeout(type, typeSpeed);
    }

    // Start typing after a brief delay
    setTimeout(type, 800);
  }

  // Add cursor blink animation
  const style = document.createElement('style');
  style.textContent = `
    .typed-cursor {
      animation: typedBlink 1s infinite;
      font-weight: 100;
    }
    @keyframes typedBlink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }
  `;
  document.head.appendChild(style);

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTypewriter);
  } else {
    initTypewriter();
  }
})();
