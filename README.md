# 标准工程图纸系统 (Standard Engineering Drawing System)

## 项目简介

这是一个基于Django框架开发的工程图纸管理系统，用于管理船舶制造项目中的分段、托盘、工艺流程等核心业务数据。

## 环境要求

### Python版本
- **Python 3.13** (推荐)
- 最低要求：Python 3.8+

### 操作系统
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, CentOS 7+)

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd Standard-Engineering-Drawing-System
```

### 2. 创建虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置数据库
```bash
# 创建数据库迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate
```

### 5. 创建超级用户
```bash
python manage.py createsuperuser
```

### 6. 初始化基础数据
```bash
# 初始化权限
python manage.py init_permissions

# 初始化船型
python manage.py init_ship_types

# 初始化典型分段
python manage.py init_typical_sections

# 初始化工作流程
python manage.py init_work_processes

# 初始化工作类型
python manage.py init_work_types
```

### 7. 运行开发服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 即可使用系统。

## 项目结构

```
Standard Engineering Drawing System/
├── drawings/                    # 主应用模块
│   ├── models.py               # 数据模型
│   ├── views.py                # 视图逻辑
│   ├── urls.py                 # URL配置
│   ├── admin.py                # 管理后台
│   └── management/             # 管理命令
│       └── commands/           # 自定义命令
├── engineering_drawing_system/  # 项目配置
│   ├── settings.py             # 项目设置
│   ├── urls.py                 # 主URL配置
│   └── wsgi.py                 # WSGI配置
├── templates/                   # 模板文件
│   └── drawings/               # 应用模板
├── static/                      # 静态文件
│   └── vendor/                 # 第三方库
│       └── bootstrap-5.3.3/    # Bootstrap框架
├── manage.py                    # Django管理脚本
└── README.md                    # 项目说明
```

## 主要功能模块

### 1. 人员管理
- 人员信息维护
- 角色分配
- 权限管理

### 2. 项目管理
- 项目创建与维护
- 项目状态跟踪
- 项目关联管理

### 3. 分段管理
- 分段信息维护
- 分段计划管理
- 分段状态跟踪

### 4. 托盘管理
- 托盘信息维护
- 托盘计划管理
- 托盘状态跟踪

### 5. 标准工艺流程
- 工艺流程定义
- 流程步骤管理
- 流程模板维护

### 6. 船型管理
- 船型信息维护
- 船型分类管理

### 7. 典型分段管理
- 典型分段模板
- 分段类型管理

## 技术栈

- **后端框架**: Django 4.2+
- **前端框架**: Bootstrap 5.3.3
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **模板引擎**: Django Templates
- **静态文件**: Django Static Files

## 开发说明

### 代码规范
- 遵循PEP 8 Python代码规范
- 使用中文注释和文档
- 遵循Django最佳实践

### 数据库设计
- 使用Django ORM进行数据操作
- 支持数据库迁移
- 包含完整的模型关系

### 前端开发
- 使用Bootstrap 5响应式设计
- 支持移动端和桌面端
- 统一的UI组件和样式

## 部署说明

### 生产环境配置
1. 修改 `settings.py` 中的 `DEBUG = False`
2. 配置生产数据库
3. 设置 `ALLOWED_HOSTS`
4. 配置静态文件服务
5. 使用生产级Web服务器（如Nginx + Gunicorn）

### 静态文件收集
```bash
python manage.py collectstatic
```

## 常见问题

### 1. Python版本兼容性
- 确保使用Python 3.8+版本
- 如果遇到版本冲突，建议使用Python 3.13

### 2. 依赖安装问题
- 使用虚拟环境避免包冲突
- 如果pip安装失败，可以尝试使用国内镜像源

### 3. 数据库迁移问题
- 确保数据库连接正常
- 按顺序执行迁移命令

### 4. 静态文件问题
- 确保 `STATICFILES_DIRS` 配置正确
- 运行 `collectstatic` 命令收集静态文件

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 项目讨论区

---

**注意**: 首次使用请务必按照安装步骤执行，确保所有依赖和配置正确。
