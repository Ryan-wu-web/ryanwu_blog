'use strict'

// 列表页/侧栏/推荐位的封面卡片（<img class="post-bg">）改用 800px 变体；
// 文章页横幅走 CSS background，不受此过滤器影响，仍用原图。
// 变体由 tools/gen_cover_thumbs.py 生成，新增文章后需重新执行。

hexo.extend.filter.register('after_render:html', html => {
  if (!html) return html
  return html.replace(/<img\b[^>]*\bpost-bg\b[^>]*>/gi, tag =>
    tag.replace(/((?:data-lazy-)?src=")(\/images\/posts\/[^"]+\/cover)\.(?:webp|jpe?g|png)(")/gi, '$1$2-800.webp$3')
  )
})
