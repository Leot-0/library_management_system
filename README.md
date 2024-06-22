
# 图书管理系统

这是一个使用 Flask 和 MySQL 构建的简单图书管理系统。它允许管理员管理图书、借阅记录和用户。系统还支持基于上传的封面图片自动获取图书信息，使用 SM.MS 和 OpenAI API。

## 功能

- 添加、编辑和删除图书
- 借阅和归还图书
- 查看借阅记录
- 基于上传的封面图片自动获取图书信息
- 根据书名、作者或 ISBN 搜索图书

## 前提条件

- Python 3.x
- MySQL

## 安装步骤

1. 克隆仓库：

    ```sh
    git clone https://github.com/your-username/library_management_system.git
    cd library_management_system
    ```

2. 创建并激活虚拟环境：

    ```sh
    python -m venv venv
    source venv/bin/activate  # Windows 上使用 `venv\Scripts\activate`
    ```

3. 安装依赖项：

    ```sh
    pip install -r requirements.txt
    ```

4. 设置 MySQL 数据库：

    ```sh
    mysql -u root -p
    CREATE DATABASE library_db;
    ```

5. 配置应用程序：

    - 在根目录创建 `.env` 文件并添加以下内容：

    ```sh
    FLASK_APP=app
    FLASK_ENV=development
    DATABASE_URL=mysql+pymysql://root:123456@localhost/library_db
    SECRET_KEY=your_secret_key
    ```

6. 初始化数据库：

    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

## 运行应用程序

1. 启动 Flask 开发服务器：

    ```sh
    flask run
    ```

2. 打开浏览器并访问 `http://127.0.0.1:5000`。

## 使用方法

### 添加图书

1. 转到“添加图书”页面。
2. 填写图书详情表单。如果启用“自动获取”选项，表单将根据上传的封面图片自动填写详细信息。
3. 点击“添加图书”按钮。

### 编辑图书

1. 转到“主页”。
2. 点击要编辑的图书旁边的“编辑”按钮。
3. 更新图书详细信息并点击“保存”按钮。

### 删除图书

1. 转到“主页”。
2. 点击要删除的图书旁边的“删除”按钮。

### 借阅图书

1. 转到“主页”。
2. 点击要借阅的图书旁边的“借阅”按钮。
3. 填写借阅人姓名并点击“借阅”按钮。

### 归还图书

1. 转到“借阅记录”页面。
2. 点击要归还的图书旁边的“归还”按钮。

## 配置

### SM.MS API

要使用自动获取功能，需要一个 SM.MS API 令牌。在 `.env` 文件中添加令牌：

```sh
SMMS_API_TOKEN=your_smms_api_token
```

### OpenAI API

要使用 OpenAI API 进行图书信息提取，请将您的 OpenAI API 密钥添加到 `.env` 文件中：

```sh
OPENAI_API_KEY=your_openai_api_key
```

## 许可证

本项目使用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
