'use client'

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { fetchCompanies, fetchProjects, register, fetchRoles } from '@/lib/api';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('');
  const [company, setCompany] = useState<number | null>(null);
  const [project, setProject] = useState<number | null>(null);
  const router = useRouter();

  const [companies, setCompanies] = useState<Array<{ id: number; name: string }>>([]);
  const [projects, setProjects] = useState<Array<{ id: number; name: string }>>([]);
  const [roles, setRoles] = useState<Array<{ id: number; name: string }>>([]);
  const [error, setError] = useState('');

  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);
  const [roleName, setRoleName] = useState('');

  useEffect(() => {
    if (roleName === '公司管理员' || roleName === '项目负责人') {
      fetchCompanies()
        .then(response => {
          setCompanies(response.data.companies);
        })
        .catch(() => {
          setError('无法获取公司列表');
        });
    }
  }, [roleName]);

  useEffect(() => {
    if (company) {
      fetchProjects(company)
        .then(response => {
          setProjects(response.data.projects);
        })
        .catch(() => {
          setError('无法获取项目列表');
        });
    }
  }, [company]);

  useEffect(() => {
    fetchRoles()
        .then(response => {
            setRoles(response.data.roles);
        })
        .catch(() => {
            setError('无法获取角色列表');
        });
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('密码和确认密码不一致');
      return;
    }

    const data = {
      username,
      password,
      role_id: selectedRoleId,
      company,
      project,
    };

    try {
      await register(data);
      router.push('/login');
    } catch (error) {
      setError('注册失败，请重试');
    }
  };

  const isFormValid =
    username.trim() !== '' &&
    password.trim() !== '' &&
    confirmPassword === password &&
    selectedRoleId !== null &&
    (roleName !== '公司管理员' || company !== null) &&
    (roleName !== '项目负责人' || project !== null);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle>注册</CardTitle>
          <CardDescription>创建您的新账号</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRegister} className="space-y-4">
            {error && <div className="text-red-500">{error}</div>}
            <Input
              placeholder="账号"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              type="password"
              placeholder="密码"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Input
              type="password"
              placeholder="确认密码"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <Select onValueChange={(value) => {
              setSelectedRoleId(Number(value));
              const selectedRole = roles.find(r => r.id === Number(value));
              setRoleName(selectedRole?.name || '');
            }}>
              <SelectTrigger>
                <SelectValue placeholder="选择角色" />
              </SelectTrigger>
              <SelectContent>
                {roles.map((role) => (
                  <SelectItem key={role.id} value={role.id.toString()}>
                    {role.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {(roleName === '公司管理员' || roleName === '项目负责人') && (
              <Select onValueChange={(value) => setCompany(Number(value))}>
                <SelectTrigger>
                  <SelectValue placeholder="选择公司" />
                </SelectTrigger>
                <SelectContent>
                  {companies.map((company) => (
                    <SelectItem key={company.id} value={company.id.toString()}>
                      {company.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
            {roleName === '项目负责人' && (
              <Select onValueChange={(value) => setProject(Number(value))}>
                <SelectTrigger>
                  <SelectValue placeholder="选择项目" />
                </SelectTrigger>
                <SelectContent>
                  {projects.map((project) => (
                    <SelectItem key={project.id} value={project.id.toString()}>
                      {project.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
            <Button type="submit" className="w-full" disabled={!isFormValid}>
              注册
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-gray-600">
            已有账号？
            <Link href="/login" className="text-blue-600 hover:underline ml-1">
              立即登录
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}

