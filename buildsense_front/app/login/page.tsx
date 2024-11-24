'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { login } from '@/lib/api';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await login(username, password);
      const { token, user } = response.data;
      localStorage.setItem('token', token);  // 保存令牌
      localStorage.setItem('user', JSON.stringify(user));  // 保存用户信息
      router.push('/dashboard');
    } catch (error) {
      setError('登录失败，请检查用户名和密码是否正确');
    }
  };

  const isFormValid = username.trim() !== '' && password.trim() !== '';

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>登录</CardTitle>
          <CardDescription>请输入您的账号和密码</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            {error && <div className="text-red-500">{error}</div>}
            <Input
              id="username"
              placeholder="账号"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              id="password"
              type="password"
              placeholder="密码"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button 
              type="submit" 
              className="w-full" 
              disabled={!isFormValid}
            >
              登录
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-gray-600">
            还没有账号？
            <Link href="/register" className="text-blue-600 hover:underline ml-1">
              立即注册
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}

