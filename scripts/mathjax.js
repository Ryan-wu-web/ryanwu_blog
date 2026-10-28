'use strict'

// Butterfly 的 overflow-y:hidden 会裁掉 ui/lazy 的观测占位，导致公式滚动入屏后仍为空白。
hexo.extend.filter.register('after_render:html', html => {
  if (!html || !html.includes("script.id = 'MathJax-script'")) return html
  return html.replace(/(['"])ui\/lazy\1\s*,?/g, '')
})
