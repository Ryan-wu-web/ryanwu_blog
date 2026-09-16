# Butterfly 第二轮质感升级实现计划

> **给代理工作者：** 在当前线程内顺序执行；未经用户授权不提交、不推送、不发布。

**目标：** 通过独立 CSS 覆盖和少量 Butterfly 配置，完成一轮可回退的深色铜棕质感升级。
**架构：** 保留 Butterfly 主题源码，通过 `_config.butterfly.yml` 的 `inject` 加载 `source/css/texture-upgrade.css`。配置只启用主题现有组件，样式文件负责统一视觉变量与组件表面。
**技术栈：** Hexo 8.1.2、Butterfly 5.7.0、CSS、Playwright 截图检查。

---

### 任务 1：锁定基线

**文件：**
- 不修改文件
- 输出：`.codex-baseline-home.png`（本地验收产物，不提交）

- [x] 从 `main@76d08a3` 创建 `codex/texture-upgrade-v2`。
- [x] 运行 `npm run build`，预期生成 84 个文件。
- [x] 截取 1440px 深色首页基线。

### 任务 2：配置 Butterfly 内置能力

**文件：**
- 修改：`_config.butterfly.yml:33-46, 927-955, 1068-1072`

- [x] 将 `code_blocks.theme` 设为 `darker`，`macStyle` 设为 `true`。
- [x] 开启 `series.enable`。
- [x] 开启 `mermaid.enable` 和 `mermaid.code_write`，保留深色 Mermaid 主题。
- [x] 在 `inject.head` 添加 `<link rel="stylesheet" href="/css/texture-upgrade.css">`。

### 任务 3：实现独立视觉覆盖

**文件：**
- 创建：`source/css/texture-upgrade.css`

- [x] 定义铜棕、暖黑、边框、阴影、圆角和动效变量。
- [x] 为首页卡片、侧栏、文章页和归档页增加一致的暖黑材质表面。
- [x] 统一正文标题、链接、引用、Note、Tabs、Gallery、Series 和代码块。
- [x] 收敛页脚、分页、滚动条、目录激活态与图片边框。
- [x] 增加移动端和 `prefers-reduced-motion` 降级规则。

### 任务 4：验证和清理

**文件：**
- 检查：`_config.butterfly.yml`
- 检查：`source/css/texture-upgrade.css`

- [x] 运行 `npm run prepublish:check`，预期无错误。
- [x] 截取首页、文章页、归档页桌面截图以及移动端首页截图。
- [x] 检查页面 `scrollWidth <= clientWidth`，避免横向溢出。
- [x] 运行 `git diff --check`，检查尾随空格和冲突标记。
- [x] 确认 `themes/butterfly/` 无本轮改动，`.codex-readme-preview/` 未触碰。
- [x] 审阅差异并删除无效或重复 CSS；未经授权不提交、不推送、不发布。
## 本轮验证结果

- `npm run prepublish:check`：通过，11 篇文章 0 错误；14 条既存 Front Matter 完整性警告，本轮未扩大范围修改文章内容。
- 桌面端与 390×844 移动端：首页、文章页、归档页均无横向溢出，浏览器页面错误为 0。
- `git diff --check`：通过；`themes/butterfly/` 无差异。
- 预览截图位于工作区外的 Codex visualizations 目录，不进入仓库。
