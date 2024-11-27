'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmployeeList } from '@/components/employee-list'
import { AddEmployeeModal } from '@/components/add-employee-modal'
import { PendingChangesList } from '@/components/pending-changes-list'
import { logout, fetchEmployees } from '@/lib/api';
import { User, Employee } from '@/lib/types';
import axios from 'axios';
import { api } from '@/lib/api';

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [isAddEmployeeModalOpen, setIsAddEmployeeModalOpen] = useState(false)
  const [employees, setEmployees] = useState<Employee[]>([])
  const router = useRouter();

  useEffect(() => {
    async function fetchUserData() {
      try {
        const response = await api.get<User>('/custom_auth/user/');
        setUser(response.data);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    }

    fetchUserData();
  }, [])

  useEffect(() => {
    async function loadEmployees() {
      try {
        const response = await fetchEmployees()
        setEmployees(response.data)
      } catch (error) {
        console.error('Failed to fetch employees:', error)
      }
    }

    loadEmployees()
  }, [])

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
      await logout(refreshToken);
    }
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('refreshToken');
    router.push('/login');
  };

  const handleEmployeeAdded = (newEmployee: Employee) => {
    setEmployees((prevEmployees) => [...prevEmployees, newEmployee])
  }

  if (!user) return <div>Loading...</div>

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">欢迎，{user.name}！</h1>
        {user.role === '总公司管理员' && (
          <Button onClick={() => setIsAddEmployeeModalOpen(true)}>
            添加新员工
          </Button>
        )}
        <Button onClick={handleLogout}>登出</Button>
      </div>
      
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>在岗人员名单</CardTitle>
          </CardHeader>
          <CardContent>
            <EmployeeList employees={employees} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>待确认变动名单</CardTitle>
          </CardHeader>
          <CardContent>
            <PendingChangesList role={user.role} />
          </CardContent>
        </Card>
      </div>

      <AddEmployeeModal 
        isOpen={isAddEmployeeModalOpen} 
        onClose={() => setIsAddEmployeeModalOpen(false)} 
        onEmployeeAdded={handleEmployeeAdded}
      />
    </div>
  )
}

