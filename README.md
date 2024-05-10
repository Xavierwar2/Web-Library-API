# Web-Library-API

### 介绍

基于Flask框架的智能图书借阅系统后端部分



### 工具版本

- Python: 3.11
- Flask: 2.3.2



### 项目目录结构

```
/
├── .venv/
├── app/
│   └── api/ # api 接口模块
│       └── __init__.py # 注册以及生成蓝图
│       └── common/ # 公共方法
│       └── models/ # 模型
│       └── resources/ # 接口
│       └── schema/ # 校验
│   └── __init__.py # 整个应用的初始化
│   └── config.py # 配置项
│   └── manage.py # 数据库迁移工具管理
├── .env # 环境变量
├── run.py # 入口文件
```



### 安装依赖项

终端输入

```
pip install -r requirements.txt
```



### 数据库迁移与更新

终端输入

```
python -m flask db migrate
python -m flask db upgrade
```



### 运行

终端输入

```
python -m flask run
```

