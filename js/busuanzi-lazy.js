// 不蒜子官方服务器响应慢（约 2.5s）。此桩经 CDN.option.busuanzi 替换原脚本标签，
// 推迟到页面 load 事件结束后空闲时再请求真实脚本，避免拖住标签页加载状态。
;(() => {
  const real = '//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js'
  const whenIdle = fn => (window.requestIdleCallback || (f => setTimeout(f, 200)))(fn)
  const load = () => {
    const s = document.createElement('script')
    s.async = true
    s.src = real
    document.body.appendChild(s)
  }
  if (document.readyState === 'complete') whenIdle(load)
  else window.addEventListener('load', () => whenIdle(load))
})()
