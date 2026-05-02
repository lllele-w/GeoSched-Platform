# GeoSched 智策平台

> 多源数据驱动的智能调度与辅助决策系统

---

## 目录结构

```
GeoSched/
├── frontend/               ← 负责人：王晶晶
│   ├── index.html          # 首页总览（KPI仪表盘、系统状态）
│   ├── data.html           # 数据管理（任务表 + 卫星资源表）
│   ├── schedule.html       # 智能调度（参数配置、方案对比）
│   ├── analysis.html       # 结果分析（算法对比图、Pareto前沿）
│   ├── visual.html         # 可视化监控（卫星轨道态势）
│   ├── about.html          # 系统说明（背景介绍、算法说明）
│   ├── css/
│   │   └── style.css       # 全局统一样式
│   ├── js/
│   │   └── common.js       # 公共脚本（导航、API调用等）
│   └── input/              # 前端图片素材（轮播图等）
│
├── backend/                ← 负责人：覃涵
│   ├── main.py             # 所有API接口定义（FastAPI主程序）
│   ├── mock_data.py        # 当前使用的模拟数据，算法接入后替换
│   └── requirements.txt    # 后端单独部署时使用的依赖清单
│
├── model/                  ← 负责人：李玟
│   ├── greedy.py           # 贪心算法（baseline对比用）
│   ├── nsga3.py            # NSGA-III多目标进化算法
│   ├── model.py            # 统一调用入口，后端通过此文件调用算法
│   └── README.md           # 说明算法输入输出格式、如何接入后端
│
├── data/                   ← 负责人：李可颐 + 李玟
│   ├── raw/                # 原始数据，只放不改（TLE轨道数据、任务CSV）
│   ├── processed/          # 预处理后数据，算法直接读取此处文件
│   └── README.md           # 数据来源说明、字段含义（张鑫晨负责写）
│
├── results/                ← 负责人：李玟（结果）+ 李可颐（图表）
│   ├── result.csv          # 算法输出的调度结果（表格形式）
│   ├── result.json         # 算法输出的调度结果（API返回形式）
│   ├── figures/            # 算法对比图、Pareto前沿图等图表素材
│   └── README.md           # 说明各结果文件的含义与生成方式
│
├── docs/                   ← 负责人：李可颐 / 陈家祺 / 张鑫辰
│   ├── report/             # 作品报告（李可颐初稿，陈家祺排版终版）
│   ├── slides/             # 答辩PPT（徐佳玮内容，黄首诺美化）
│   ├── submit/             # 提交材料（张鑫晨：概要信息表、AI说明书）
│   └── README.md           # 说明各文档用途、当前版本状态
│
├── video/                  ← 负责人：黄首诺
│   └── README.md           # 说明视频素材内容（视频文件用网盘共享，不传仓库）
│
├── assets/                 ← 负责人：黄首诺
│                           # 封面图、logo、图标等视觉设计文件
│                           # 前端需要的图片资源也可放此处
│
├── .gitignore              # 指定不上传Git的文件（.conda、视频、缓存等）
├── README.md               # 本文件，仓库主页说明
└── requirements.txt        # 全量依赖，clone后第一步执行安装
```

---

## 各文件/文件夹详细说明

### `frontend/` — 前端页面（王晶晶）
纯静态 HTML/CSS/JS，无需任何构建工具，浏览器直接打开 `index.html` 即可运行。通过调用后端 API（`http://localhost:8000`）获取数据并渲染图表。

| 文件 | 作用 |
|------|------|
| `index.html` | 系统首页，展示 KPI 总览（待调度任务数、可用卫星数、最优收益） |
| `data.html` | 数据管理页，展示任务列表和卫星资源表，支持筛选查询 |
| `schedule.html` | 核心功能页，配置调度参数、触发优化、对比多套方案 |
| `analysis.html` | 结果分析页，展示算法对比柱状图和 Pareto 前沿散点图 |
| `visual.html` | 可视化监控页，展示卫星轨道态势和任务执行状态 |
| `about.html` | 系统说明页，介绍项目背景、算法原理、团队信息 |
| `css/style.css` | 全局样式，所有页面共用 |
| `js/common.js` | 公共 JS，包含导航逻辑和通用 API 调用函数 |
| `input/` | 前端使用的图片素材（侧边栏轮播图等） |

---

### `backend/` — 后端服务（覃涵）
基于 Python FastAPI 框架，提供 REST API 供前端调用。

| 文件 | 作用 |
|------|------|
| `main.py` | 主程序，定义全部 API 接口（`/ping` `/load_data` `/optimize` `/result`） |
| `mock_data.py` | 模拟数据模块，当前返回静态数据；**李玟算法完成后，此文件替换为真实算法调用** |
| `requirements.txt` | 后端专用依赖，单独部署后端时使用（`fastapi`、`uvicorn`） |

---

### `model/` — 算法模块（李玟）
实现所有优化算法，通过 `model.py` 统一对外暴露接口，后端 `main.py` 只调用 `model.py`。

| 文件 | 作用 |
|------|------|
| `greedy.py` | 贪心算法，作为 baseline 对比基准 |
| `nsga3.py` | NSGA-III 多目标进化算法 |
| `model.py` | 统一入口，接收调度参数，调用对应算法，返回标准格式结果 |
| `README.md` | 说明输入输出数据格式，方便覃涵对接 |

---

### `data/` — 数据集（李可颐 + 李玟）
严格区分原始数据和处理后数据，**`raw/` 中的文件只读不改**。

| 目录/文件 | 作用 |
|-----------|------|
| `raw/` | 原始数据原始存放处（TLE 卫星轨道文件、任务原始 CSV） |
| `processed/` | 预处理后数据，算法和后端直接读取此目录 |
| `README.md` | 说明数据来源、字段含义、预处理方法（张鑫晨负责撰写） |

---

### `results/` — 实验结果（李玟 + 李可颐）
算法运行产出的所有结果文件和图表，后端从此处读取数据返回给前端。

| 文件 | 作用 |
|------|------|
| `result.csv` | 调度结果表格，含每个任务的分配方案和指标 |
| `result.json` | 同上，JSON 格式，供后端 API 直接读取返回 |
| `figures/` | 所有图表图片（算法对比柱状图、Pareto 散点图、资源利用率图等） |
| `README.md` | 说明各结果文件含义、图表生成方法 |

---

### `docs/` — 文档（李可颐 / 陈家祺 / 张鑫晨）
所有非代码提交材料，**按类型拆分子文件夹，不要混放**。

| 目录 | 内容 | 负责人 |
|------|------|--------|
| `report/` | 作品报告（Word/PDF） | 李可颐写初稿，陈家祺排版 |
| `slides/` | 答辩 PPT | 徐佳玮写内容，黄首诺美化 |
| `submit/` | 作品概要信息表、AI使用说明表等提交材料 | 张鑫晨 |
| `README.md` | 说明各文档当前版本状态和修改记录 | 张鑫晨 |

---

### `video/` — 演示视频（黄首诺）
视频剪辑素材和最终成品。**注意：视频文件体积大，不传 GitHub，用网盘共享链接，在 `README.md` 里注明网盘地址。**

---

### `assets/` — 视觉资源（黄首诺）
封面图、项目 logo、图标设计文件、PPT 模板素材等。前端页面需要使用的图片也可放在此处。

---

### 根目录文件

| 文件 | 作用 |
|------|------|
| `README.md` | 本文件，仓库主页，所有人的入口文档 |
| `requirements.txt` | 全量依赖，clone 后执行 `pip install -r requirements.txt` 一键安装 |
| `.gitignore` | 排除不上传的文件（`.conda/`、`__pycache__/`、视频大文件等） |

---

## 快速启动

### 1. 克隆仓库

```bash
git clone <仓库地址>
cd GeoSched
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动后端

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. 打开前端

直接用浏览器打开 `frontend/index.html` 即可，无需任何构建工具。

### 5. 查看 API 文档

后端启动后访问：[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 团队分工与目录对应关系

| 模块 | 负责目录 | 说明 |
|------|----------|------|
| 前端 | `frontend/` | 页面开发、样式、交互 |
| 后端 | `backend/` | API 接口、数据对接 |
| 算法 | `model/` | 优化算法实现 |
| 数据 | `data/` | 数据采集、清洗、预处理 |
| 实验 | `results/` | 算法对比图表、实验记录 |
| 文档 | `docs/` | 报告、PPT、说明材料 |

---

## 协作规范

- **不要把大文件（数据集、视频）直接 push 到仓库**，放到 `data/` 和 `video/` 后在 `.gitignore` 中排除，通过网盘共享
- 每人在自己负责的目录下工作，不随意修改他人模块
- 提交信息格式：`[模块] 说明`，例如：`[frontend] 完成调度页参数面板` / `[model] 添加NSGA3算法初版`
- 主分支（`main`）保持可运行状态，开发新功能请新建分支

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | HTML5 / CSS3 / JavaScript / Bootstrap Icons |
| 后端 | Python 3 / FastAPI / Uvicorn |
| 算法 | Python 3（多目标优化） |
| 数据 | TLE 轨道根数 / CSV 任务数据 |

---

## 版本信息

- 当前版本：v1.0.0
- 最后更新：2026-04-29
