/** Page-specific typewriter titles. PJAX is disabled, so each page initializes once. */
(() => {
  'use strict'

  const TYPEWRITER_BY_PATH = {
    '/categories/tech/': {
      strings: ['向上学习，向下扎根，技术改变世界', 'Keep learning, keep building, tech changes the world'],
      speed: 80
    },
    '/categories/life/': {
      strings: ['热爱生活，记录美好，追寻真实的自我', 'Love life, record moments, chase the real you'],
      speed: 80
    },
    '/archives/': {
      strings: ['路很长，我们慢慢走', 'The road is long, we walk slowly'],
      speed: 100
    },
    '/tags/': {
      strings: ['钻研技术栈，落地项目，追逐创新', 'Learn stacks, build projects, chase innovation'],
      speed: 80
    }
  }

  const START_DELAY = 800
  const HOLD_DELAY = 2500
  const BETWEEN_STRINGS_DELAY = 500
  const MAX_TITLE_WAIT_ATTEMPTS = 10
  const TITLE_WAIT_INTERVAL = 250

  function addCursorStyle() {
    if (document.getElementById('typed-cursor-style')) return

    const style = document.createElement('style')
    style.id = 'typed-cursor-style'
    style.textContent = '@keyframes typedBlink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }'
    document.head.appendChild(style)
  }

  function startTypewriter(title, config) {
    title.replaceChildren()

    const text = document.createElement('span')
    text.className = 'typed-page-title'

    const cursor = document.createElement('span')
    cursor.className = 'typed-cursor'
    cursor.textContent = '|'
    cursor.style.cssText = 'animation: typedBlink 1s infinite; font-weight: 100;'

    title.append(text, cursor)
    addCursorStyle()

    let stringIndex = 0
    let characterIndex = 0
    let deleting = false

    const renderNextCharacter = () => {
      const current = config.strings[stringIndex]
      characterIndex += deleting ? -1 : 1
      text.textContent = current.slice(0, characterIndex)

      let delay = deleting ? config.speed / 2 : config.speed
      if (!deleting && characterIndex === current.length) {
        deleting = true
        delay = HOLD_DELAY
      } else if (deleting && characterIndex === 0) {
        deleting = false
        stringIndex = (stringIndex + 1) % config.strings.length
        delay = BETWEEN_STRINGS_DELAY
      }
      window.setTimeout(renderNextCharacter, delay)
    }

    window.setTimeout(renderNextCharacter, START_DELAY)
  }

  function initialize(attempt = 0) {
    const config = TYPEWRITER_BY_PATH[window.location.pathname]
    if (!config) return

    const title = document.querySelector('#site-title')
    if (title) {
      startTypewriter(title, config)
    } else if (attempt < MAX_TITLE_WAIT_ATTEMPTS) {
      window.setTimeout(() => initialize(attempt + 1), TITLE_WAIT_INTERVAL)
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true })
  } else {
    initialize()
  }
})()
