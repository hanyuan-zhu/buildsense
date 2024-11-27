import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { addEmployee } from '@/lib/api'
import { Employee } from '@/lib/types';

interface AddEmployeeModalProps {
  isOpen: boolean
  onClose: () => void
  onEmployeeAdded: (employee: Employee) => void
}

export function AddEmployeeModal({ isOpen, onClose, onEmployeeAdded }: AddEmployeeModalProps) {
  const [name, setName] = useState('')
  const [position, setPosition] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await addEmployee({ name, position, employment_status: '待岗' })  // 添加 employment_status 字段
      console.log('Employee added:', response.data)
      onEmployeeAdded(response.data)  // 通知父组件刷新员工列表
      onClose()
    } catch (error) {
      console.error('Failed to add employee:', error)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>添加新员工</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="姓名"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Input
            placeholder="岗位"
            value={position}
            onChange={(e) => setPosition(e.target.value)}
          />
          <Button type="submit">添加</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

