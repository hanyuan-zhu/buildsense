# API 端点规划

## 1. 用户认证相关

### POST /api/auth/login
- 请求: { username: string, password: string }
- 响应: { token: string, user: { id: number, name: string, role: string, companyId?: number, projectId?: number } }

### POST /api/auth/register 
- 请求: { username: string, password: string, role: string, companyId?: number, projectId?: number }
- 响应: { success: boolean, message: string }

## 2. 员工管理相关

### GET /api/employees
- 查询参数: { companyId?: number, projectId?: number }
- 响应: {
    employees: [{
      id: number,
      name: string,
      position: string,
      company: { id: number, name: string },
      project: { id: number, name: string },
      status: '在岗' | '待岗' | '离职'
    }]
  }

### POST /api/employees
- 请求: { 
    name: string,
    position: string, 
    companyId: number,
    projectId: number
  }
- 响应: { success: boolean, employee: {...} }

## 3. 人事变动相关

### GET /api/changes
- 查询参数: { companyId?: number, projectId?: number }
- 响应: {
    changes: [{
      id: number,
      type: '入职' | '调岗' | '离职',
      employeeId: number,
      employeeName: string,
      fromCompany?: { id: number, name: string },
      toCompany?: { id: number, name: string },
      fromProject?: { id: number, name: string }, 
      toProject?: { id: number, name: string },
      effectiveDate: string,
      status: '待确认' | '已确认' | '已拒绝'
    }]
  }

### POST /api/changes
- 请求: {
    type: '入职' | '调岗' | '离职',
    employeeId: number,
    fromCompanyId?: number,
    toCompanyId?: number, 
    fromProjectId?: number,
    toProjectId?: number,
    effectiveDate: string
  }
- 响应: { success: boolean, change: {...} }

### PUT /api/changes/:id/confirm
- 响应: { success: boolean }

### PUT /api/changes/:id/reject  
- 响应: { success: boolean }

## 4. 公司和项目查询

### GET /api/companies
- 响应: { companies: [{ id: number, name: string }] }

### GET /api/companies/:id/projects 
- 响应: { projects: [{ id: number, name: string }] }
