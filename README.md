# Swarms Marketplace

按 Figma 设计稿（node-id 1575:3560）开发的首页静态原型。

---

## 快速上手

1. 把整个 `swarms-marketplace` 文件夹放到本地任何位置（你提到的 `C:\Users\13270\Desktop\swarms-marketplace` 就行）。
2. 双击 `index.html` 用浏览器打开，即可看到效果。

页面在最新版 Chrome / Edge / Firefox / Safari 中均可正常显示。

---

## ⚠️ 关于图片：建议立即跑一下本地化脚本

`index.html` 当前引用的图片都来自 Figma 的临时 CDN：

```
https://www.figma.com/api/mcp/asset/<uuid>
```

**这些 URL 会在生成后约 7 天过期。** 过期之后页面会显示破图。

为了让页面长期稳定、并且支持完全离线打开，请在拿到这份代码后**尽快**执行下面这一步：

### Windows

打开 PowerShell 或 CMD，进入项目目录然后跑：

```bash
cd C:\Users\13270\Desktop\swarms-marketplace
python localize-images.py
```

脚本会做三件事：

1. 创建 `./images/` 文件夹
2. 把 13 张图片下载下来（Hero × 1，卡片 × 12），用易识别的文件名（`yuki.png`、`clawpay-s1.png`、`rok.png` ...）
3. 把 HTML 里所有 `https://www.figma.com/api/mcp/asset/...` 替换为本地相对路径 `images/xxx.png`

跑完一次就行了。之后页面完全离线、不再依赖 Figma。

> 需要 Python 3.6+。如果系统没装 Python，到 [python.org](https://www.python.org/downloads/) 下载安装即可，安装时记得勾选 "Add Python to PATH"。

---

## 文件结构

```
swarms-marketplace/
├── index.html              ← 主页面（含全部 CSS 和 JS）
├── localize-images.py      ← 图片本地化脚本（建议跑一次）
├── README.md               ← 这份说明
└── images/                 ← 跑完脚本后会出现，存放下载好的图片
```

---

## 设计要点回顾

整体结构遵循 Centered Single-Column Layout：

- **Sidebar**（左侧 84px）— 7 个一级导航 + WAI Credits 余额 + 用户头像
- **Hero**（460px）— 三屏轮播，第三屏使用真实机器人图（Quant Trader Agent）
- **Search + Tags** — 搜索栏与可点击的分类标签
- **04 个产品板块**：
  - `01 / Capital Performance` → Most Profitable Agents（红色收益条带）
  - `02 / Speed Mode` → Top Frenzy Agents & Prompts（mini-tags 能力标签）
  - `03 / Community Favorites` → Highest Rated Products
  - `04 / On-Chain` → Tokenized Products（绿色 token 价格条带）

每个板块右上角都有 ◀ ▶ Chevron 翻页按钮。卡片采用 scroll-snap，鼠标可以横向拖拽，到达边界时按钮自动 disable。

设计语言：

- 字体：Montserrat（标题/正文）+ JetBrains Mono（数字/价格/编号）
- 主色：Swarms 品牌红 `#ED1717`，深色基底 `#0A0A0A`
- 卡片悬停：白色描边 + 标题变白 + 上移 2px

---

## 技术说明

- 单文件应用，无构建步骤
- 不依赖任何前端框架，纯原生 HTML / CSS / JS
- 字体通过 Google Fonts CDN 加载（首次打开需要联网）
- 浏览器存储：完全使用内存状态，不写 localStorage / cookie

如果你想要离线字体，可以下载 Montserrat 与 JetBrains Mono 的 woff2 文件放到 `./fonts/` 目录，并替换 `<head>` 里的 Google Fonts 链接。

---

## 后续改动建议

如果要在这份原型上继续工作：

- 修改 Hero 文案：搜索 `Quant Trader Agent` 即可定位
- 添加新卡片：复制现有 `<article class="card">...</article>` 块即可，注意每个 section 至少 6 张才能让翻页有意义
- 调整品牌色：改 `:root` 里的 `--brand-600` 即可全局生效
- 调整间距/圆角：改 `:root` 里 `--r-*`、`--spacing-*` 系列变量

任何问题随时找我继续迭代。
