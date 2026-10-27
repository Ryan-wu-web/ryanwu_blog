# AGENTS.md

## 常用命令

- 构建检查：`npm run prepublish:check`（内容检查 + clean + generate，不写 Git）
- 本地预览：`npm run server -- --ip 127.0.0.1 --port 4000 --static`（直接服务 `public/`，改动后需重新 build）
- 发布：`python tools/publish.py`（main 分支上检查、构建、提交并推送；推送 main 触发 GitHub Actions 部署）
- 生成封面：`python tools/gen_cover.py --slug <slug> --series <栏目> --title1 "..." --title2 "..." --source burst --query "..."`（内置行位/宽度/卡片自检，不过即不落盘）
- 新增文章封面后：`python tools/gen_cover_thumbs.py`（生成 `cover-800.webp` 供列表页使用）

## 本仓库的坑

- `themes/butterfly` 是指向 `node_modules/hexo-theme-butterfly` 的符号链接，不要直接修改。
- 不手改 `public/` 和 `.deploy_git/`，它们是生成产物。
- 第三方库走 npmmirror（`_config.butterfly.yml` 的 `CDN.custom_format`）；例外：snackbar 走 fastly 镜像（npmmirror 403），busuanzi 走本地延迟加载桩 `source/js/busuanzi-lazy.js`。
- 封面引用由 `scripts/covers.js` 在构建时改写为 800px 变体；文章页横幅仍用原图，删除任何 `cover-800.webp` 前先跑一次生成脚本确认引用闭合。
- 图片引用必须指向 `source/` 中实际存在的文件，构建不校验背景图路径。
