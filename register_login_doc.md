注册和登录功能文档# 注册和登录功能文档

## 第一部分：已完成的代码梳理

### 1. 前端部分

#### 登录页面
- 文件位置：frontend/src/app/login/page.tsx
- 功能：
  - 用户输入用户名和密码进行登录。
  - 前端发送登录请求到后端，获取 JWT 令牌。
  - 登录成功后，用户被重定向到仪表盘页面。
  - 添加跳转到注册页面的链接。

#### 注册页面
- 文件位置：frontend/src/app/register/page.tsx
- 功能：
  - 用户输入用户名、密码，选择角色（总公司管理员、公司管理员、项目负责人）。
  - 根据角色选择，动态显示公司和项目的下拉选项。
  - 前端从后端获取公司和项目列表以供选择。
  - 提交注册信息到后端，完成注册流程。
  - 确保公司和项目名称正确显示。

#### Dashboard 页面
- 文件位置：frontend/src/app/dashboard/page.tsx
- 功能：
  - 实现基础页面布局。
  - 顶部导航栏，包含用户信息和登出功能。
  - 在岗员工名单表格(EmployeeList组件)：
    - 根据用户角色显示对应的字段。
    - 实现数据分页和排序功能。
    - 添加必要的数据加载和错误处理逻辑。

#### 根路径重定向
- 文件位置：frontend/src/app/page.tsx
- 功能：
  - 将根路径重定向到 `/login` 页面。

#### 路由守卫
- 功能：
  - 实现基础的路由守卫功能。
  - 未登录用户重定向到登录页面。
  - 根据用户角色限制页面访问权限。

### 2. 后端部分

#### 数据模型
- 文件位置：buildsense/mainapp/models.py
- 模型设计：
  - User 模型（继承自 AbstractUser）：
    - 字段包括：username、password、role（角色）、company（所属公司）、project（所属项目）等。
    - role字段使用预定义的选择项：
      - head_office_admin（总公司管理员）
      - company_admin（公司管理员）
      - project_manager（项目负责人）

#### 序列化器
- 文件位置：buildsense/mainapp/serializers.py
- 功能：
  - 定义 UserSerializer、CompanySerializer、ProjectSerializer 等，用于处理数据的序列化和反序列化。
  - 在序列化器中添加自定义字段，以匹配前端需求。

#### 视图函数
- 文件位置：buildsense/mainapp/views.py
- 功能：
  - 注册视图：处理用户注册的逻辑，验证数据，创建新用户。
  - 登录视图：使用 JWT 认证，返回访问令牌和刷新令牌。
  - 公司列表视图：提供公司列表数据给前端。
  - 项目列表视图：根据公司 ID 返回对应的项目列表。

#### URL 配置
- 文件位置：buildsense/mainapp/urls.py
- 功能：
  - 定义后端 API 的路由：
    - /api/register/：用户注册接口
    - /api/login/：用户登录接口
    - /api/companies/：获取公司列表
    - /api/companies/<int:company_id>/projects/：获取指定公司的项目列表

#### JWT 授权
- 功能：
  - 使用 djangorestframework-simplejwt 实现 JWT 认证。
  - 配置了访问令牌和刷新令牌的获取和刷新接口。
  - 在视图中使用权限装饰器，保护需要认证的接口。

### 3. 前后端交互

#### 跨域配置
- 文件位置：buildsense/buildsense/settings.py
- 功能：
  - 使用 django-cors-headers 处理跨域请求。
  - 允许来自 http://localhost:3000 的请求，以支持前端本地开发。

#### 前端环境变量
- 文件位置：frontend/.env.local
- 功能：
  - 定义后端 API 的基础 URL：
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

## 第二部分：注册和登录功能技术文档

### 1. 数据库设计

#### 1.1 用户表（User）
- 模型位置：buildsense/mainapp/models.py
- 字段说明：

| 字段名     | 类型         | 说明               |
|------------|--------------|--------------------|
| id         | AutoField    | 用户 ID，自增主键 |
| username   | CharField    | 用户名，唯一       |
| password   | CharField    | 密码，使用加密方式存储 |
| role       | CharField    | 角色，选择项       |
| company    | ForeignKey   | 所属公司，外键，可为空 |
| project    | ForeignKey   | 所属项目，外键，可为空 |
| is_active  | BooleanField | 账户是否激活       |
| date_joined| DateTimeField| 注册日期           |

- 角色选择项（ROLE_CHOICES）：
  - head_office_admin：总公司管理员
  - company_admin：公司管理员
  - project_manager：项目负责人

#### 1.2 公司表（Company）
- 模型位置：buildsense/mainapp/models.py
- 字段说明：

| 字段名     | 类型         | 说明               |
|------------|--------------|--------------------|
| id         | AutoField    | 公司 ID，自增主键 |
| company_name | CharField  | 公司名称           |

- 方法：
  - `__str__`：返回公司名称

#### 1.3 项目表（Project）
- 模型位置：buildsense/mainapp/models.py
- 字段说明：

| 字段名     | 类型         | 说明               |
|------------|--------------|--------------------|
| id         | AutoField    | 项目 ID，自增主键 |
| project_name | CharField  | 项目名称           |
| company    | ForeignKey   | 所属公司，外键     |

- 方法：
  - `__str__`：返回项目名称

### 2. 后端接口设计

#### 2.1 注册 API
- 请求方式：POST
- 接口地址：/api/register/
- 请求参数（JSON 格式）：

| 参数名     | 类型   | 必填 | 说明                       |
|------------|--------|------|----------------------------|
| username   | String | 是   | 用户名，必须唯一           |
| password   | String | 是   | 密码                       |
| role       | String | 是   | 角色，需为预定义角色之一   |
| company_id | Int    | 否   | 公司 ID，company_admin 和 project_manager 角色必填 |
| project_id | Int    | 否   | 项目 ID，project_manager 角色必填 |

- 响应结果：
  - 成功：
    - 状态码：201 Created
    - 内容：
      ```json
      {
        "message": "注册成功"
      }
      ```
  - 失败：
    - 状态码：400 Bad Request
    - 内容：
      ```json
      {
        "error": "错误信息"
      }
      ```

#### 2.2 登录 API
- 请求方式：POST
- 接口地址：/api/token/
- 请求参数（JSON 格式）：

| 参数名     | 类型   | 必填 | 说明                       |
|------------|--------|------|----------------------------|
| username   | String | 是   | 用户名                     |
| password   | String | 是   | 密码                       |

- 响应结果：
  - 成功：
    - 状态码：200 OK
    - 内容：
      ```json
      {
        "refresh": "刷新令牌",
        "access": "访问令牌"
      }
      ```
  - 失败：
    - 状态码：401 Unauthorized
    - 内容：
      ```json
      {
        "detail": "认证凭据无效"
      }
      ```

### 3. 前端页面设计

#### 3.1 注册页面
- 文件位置：frontend/src/app/register/page.tsx
- 功能描述：
  - 用户输入用户名和密码。
  - 用户选择角色，角色包括：
    - 总公司管理员
    - 公司管理员
    - 项目负责人
  - 根据所选角色：
    - 如果是公司管理员或项目负责人，需选择所属公司。
    - 如果是项目负责人，需在选择公司后选择所属项目。
  - 前端在组件加载时，向后端请求公司列表。
  - 当选择公司后，若角色为项目负责人，前端请求该公司的项目列表。
  - 提交注册信息到后端，处理响应结果。
- 主要交互流程：
  1. 用户访问注册页面，页面加载公司列表。
  2. 用户输入用户名、密码，选择角色。
  3. 根据角色要求，选择公司和项目。
  4. 点击注册，前端将数据发送至后端 API。
  5. 根据后端返回结果，提示用户注册成功或失败。

#### 3.2 登录页面
- 文件位置：frontend/src/app/login/page.tsx
- 功能描述：
  - 用户输入用户名和密码进行登录。
  - 前端将用户名和密码发送至后端登录 API。
  - 登录成功后，后端返回 JWT 访问令牌和刷新令牌。
  - 前端保存令牌至本地存储，以便后续请求使用。
  - 用户被重定向至仪表盘页面。
  - 添加跳转到注册页面的链接。
- 主要交互流程：
  1. 用户访问登录页面。
  2. 用户输入用户名和密码。
  3. 点击登录，前端将数据发送至后端 API。
  4. 登录成功，保存令牌并重定向；登录失败，提示错误信息。

### 4. JWT 授权机制
- 后端配置：
  - 使用 djangorestframework-simplejwt 库。
  - 在 settings.py 中配置认证后端和简单 JWT 设置。
  - 定义令牌过期时间、签名算法等。
- 令牌获取和刷新：
  - 获取令牌：
    - 用户通过登录 API 获取 access和 refresh 令牌。
  - 刷新令牌：
    - 当 access令牌过期时，前端可使用 refresh 令牌获取新的 access令牌。
- 前端处理：
  - 存储令牌：
    - 登录成功后，前端将令牌保存到 localStorage。
  - 请求拦截：
    - 在发送请求时，前端在请求头中加入 Authorization:  <Beareraccess_token>。
  - 令牌刷新：
    - 在检测到令牌过期后，前端自动调用刷新令牌的 API，更新 access 令牌。

- 权限控制：
  - 后端在需要保护的视图中使用权限装饰器，限制未认证用户的访问。
  - 根据用户角色，控制其可访问的资源和执行的操作。

### 5. 接口列表汇总

| 接口名称       | 方法 | 路径                                | 描述               |
|----------------|------|-------------------------------------|--------------------|
| 注册接口       | POST | /api/register/                      | 用户注册           |
| 登录接口       | POST | /api/token/                         | 用户登录，获取令牌 |
| 刷新令牌接口   | POST | /api/token/refresh/                 | 刷新访问令牌       |
| 获取公司列表   | GET  | /api/companies/                     | 获取所有公司       |
| 获取公司下的项目 | GET  | /api/companies/<company_id>/projects/ | 获取指定公司下的项目 |

### 6. 注意事项
- 数据验证：
  - 后端对接收到的数据进行验证，确保字段完整性和正确性。
  - 对密码进行加密存储，确保安全性。
- 错误处理：
  - 前后端均需对可能出现的错误进行处理，提供友好的错误提示。
  - 前端在接口失败时，显示错误信息，不泄露敏感信息。
- 跨域问题：
  - 已在后端配置了 CORS，允许来自前端本地开发环境的请求。
- 安全性：
  - 使用 HTTPS（在生产环境）确保数据传输安全。
  - 对敏感信息进行妥善处理，不在前端暴露密码等敏感数据。

## 第三部分：测试与运行指南

### 1. 环境配置

#### 后端环境：
- Python 版本：3.x
- 安装依赖：
  ```sh
  pip install -r requirements.txt
  ```
- 数据库迁移：
```python manage.py migrate```

- 前端环境：
  - Node.js 版本：16.x 或以上
  - 安装依赖：
```cd frontend
npm install```
  - 配置环境变量：
    - 创建 .env.local 文件，内容如下：
            ```NEXT_PUBLIC_API_URL=http://localhost:8000```

2. 运行项目
- 启动后端服务器：
```cd buildsense
python manage.py runserver```

- 启动前端服务器：
```cd frontend
npm run dev```
- 访问应用程序：
  - 前端地址：http://localhost:3000
  - 后端地址：http://localhost:8000

3. 测试流程
- 注册新用户：
  1. 访问 http://localhost:3000/register
  2. 填写用户名、密码，选择角色。
  3. 根据角色要求，选择公司和项目。
  4. 点击注册，注册成功后将提示成功信息。

- 登录已有用户：
  1. 访问 http://localhost:3000/login
  2. 输入注册时的用户名和密码。
  3. 点击登录，登录成功后将重定向至仪表盘页面。
