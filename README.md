# ☘ 簡易接口模板

自用的 簡易的 restful api demo 模板。

接口頻率限制依賴 redis，自用不需要時可以卸掉這個功能

[![python](https://img.shields.io/badge/python-3.12.6-ffd343.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.115.2-009485.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.36-778877.svg?style=for-the-badge&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![pgsql](https://img.shields.io/badge/pgsql-16.4.0-336791.svg?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![redis](https://img.shields.io/badge/redis-7.4.1-ff4438.svg?style=for-the-badge&logo=redis)](https://redis.io/)

---

## 初始運轉

記得先進入虛擬環境

```bash

# 安裝依賴
pip install -r requirements.txt

# 配置好./config.ini后創建空白資料表
python db_create.py

# 運轉項目
python app.py

```

## API demo

增刪改查完備，啓動后見[swagger 文档](http://127.0.0.1:8080/docs)

- GET /demo/{id} 指定獲取單條
- PUT /demo/{id} 修改指定單條
- POST /demo 新增單條
- GET /demos 分頁獲取多條
- DELETE /demos 刪除指定多條

## 目錄結構

```python
/nanarino/nanarinorest # cwd
│
├── app.py             # 程式入口
├── config.ini         # 配置文件
├── api
│   ├── __init__.py
│   ├── auth.py        # Oauth2授權 登錄注冊的api
│   ├── schemas.py     # 類型檢查以及DTO
│   └── demo.py        # 一組增刪改查的 Demo api
├── db
│   ├── __init__.py
│   ├── base.py        # 資料物件基類
│   └── models.py      # 資料庫模型
├── util               # 工具函式
└── requirements.txt   # 依賴的pip包

│
static/index.html      # 爲 Demo api 編撰的 增删改查Demo界面

```

---

## 示例界面

運行後訪問： http://127.0.0.1:8080/

UI 組件：![UI5 Web Components](./static/favicon.ico) [UI5 Web Components](https://sap.github.io/ui5-webcomponents/)

組件依賴使用[JSPM 工具](https://generator.jspm.io/)从 cdn 獲取`importmap`，所以無需 nodejs 環境
