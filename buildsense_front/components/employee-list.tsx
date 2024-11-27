'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { TransferModal } from './transfer-modal'
import { ResignModal } from './resign-modal'
import { Employee } from '@/lib/types'

interface EmployeeListProps {
  employees: Employee[];
}

export function EmployeeList({ employees }: EmployeeListProps) {
  const [isTransferModalOpen, setIsTransferModalOpen] = useState(false)
  const [isResignModalOpen, setIsResignModalOpen] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null)

  const handleTransfer = (employee: Employee) => {
    setSelectedEmployee(employee)
    setIsTransferModalOpen(true)
  }

  const handleResign = (employee: Employee) => {
    setSelectedEmployee(employee)
    setIsResignModalOpen(true)
  }

  return (
    <div className="space-y-4">
      <div className="max-h-64 overflow-y-auto">
        {employees.map((employee) => (
          <div key={employee.id} className="flex justify-between items-center p-2 border-b">
            <div>
              <p className="font-semibold">{employee.name}</p>
              <p className="text-sm text-gray-500">{employee.position} | {employee.company} | {employee.project}</p>
            </div>
            <div>
              <Button size="sm" onClick={() => handleTransfer(employee)}>调岗</Button>
              <Button size="sm" variant="destructive" onClick={() => handleResign(employee)} className="ml-2">离职</Button>
            </div>
          </div>
        ))}
      </div>

      <TransferModal 
        isOpen={isTransferModalOpen} 
        onClose={() => setIsTransferModalOpen(false)}
        employee={selectedEmployee}
      />

      <ResignModal
        isOpen={isResignModalOpen}
        onClose={() => setIsResignModalOpen(false)}
        employee={selectedEmployee}
      />
    </div>
  )
}

