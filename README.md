# 先看看 - 高考择校助手

一个基于 AI 的高考择校辅助工具，帮助考生和家长了解高校宿舍环境、交通出行等校园生活信息，为志愿填报提供参考。

## 功能特性

- **AI 校园生活分析**：基于大语言模型，智能分析高校的宿舍条件、校园交通等信息
- **高校数据查询**：提供全国高校的基础数据，包括录取分数线、招生计划等
- **收藏管理**：支持收藏感兴趣的高校，方便对比和回顾
- **宿舍信息**：详细的宿舍环境数据，包含住宿条件、设施配置等
- **交通出行**：校园周边交通信息，帮助了解出行便利程度
- **管理后台**：支持管理员配置 API Key 和数据管理

## 技术栈

- **后端框架**：FastAPI
- **AI 能力**：Claude / OpenAI 兼容 API
- **数据处理**：Pandas、OpenPyXL
- **数据库**：SQLite
- **前端**：原生 HTML/CSS/JavaScript
- **部署**：Uvicorn，支持 PaaS 平台部署（Procfile）

## 项目结构

```
gaokao-helper/
├── main.py              # FastAPI 应用入口
├── requirements.txt     # Python 依赖
├── Procfile             # PaaS 部署配置
├── ai/                  # AI 客户端模块
│   └── claude_client.py
├── core/                # 核心业务逻辑
│   ├── config.py        # 配置管理
│   ├── data_loader.py   # 数据加载器
│   ├── database.py      # 数据库操作
│   └── favorites.py     # 收藏管理
├── data/                # 数据文件
│   ├── universities.csv
│   ├── admission_scores.csv
│   ├── seed_data.json
│   └── ...
├── db/                  # SQLite 数据库
├── static/              # 静态资源
│   ├── css/style.css
│   └── js/
├── templates/           # HTML 模板
└── scripts/             # 数据处理脚本
```

## 安装与运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd gaokao-helper
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
export MIMO_API_KEY="your-api-key"      # AI API Key
export MIMO_BASE_URL="https://..."      # API Base URL（可选）
export ADMIN_PASSWORD="your-password"   # 管理员密码
```

### 5. 启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

访问 `http://localhost:8000` 即可使用。

## 部署

项目支持通过 Procfile 部署到 Railway、Heroku 等 PaaS 平台：

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## License

[MIT](LICENSE)
