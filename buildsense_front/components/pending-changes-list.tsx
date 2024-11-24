'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { UserPlus, UserMinus, UserCog } from 'lucide-react'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { useToast } from "@/hooks/use-toast"

export function PendingChangesList({ role }) {
  const [pendingChanges, setPendingChanges] = useState([])
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false)
  const [rejectDialogOpen, setRejectDialogOpen] = useState(false)
  const [selectedChange, setSelectedChange] = useState(null)
  const { toast } = useToast()

  useEffect(() => {
    // TODO: Fetch pending changes from API based on role
    setPendingChanges([
      { id: 1, type: '调岗', name: '张三', fromCompany: '公司A', toCompany: '公司B', fromProject: '项目X', toProject: '项目Y', effectiveDate: '2023-06-01' },
      { id: 2, type: '入职', name: '李四', toCompany: '公司C', toProject: '项目Z', effectiveDate: '2023-06-15' },
      { id: 3, type: '离职', name: '王五', fromCompany: '公司B', fromProject: '项目Y', effectiveDate: '2023-06-30' },
    ])
  }, [role])

  const handleConfirm = async () => {
    try {
      // TODO: Implement actual confirmation logic
      console.log('Confirmed change:', selectedChange.id)
      
      // Simulating an API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: "变动已确认",
        description: `${selectedChange.name}的${selectedChange.type}申请已确认。`,
      })
      // Remove the confirmed change from the list
      setPendingChanges(pendingChanges.filter(change => change.id !== selectedChange.id))
    } catch (error) {
      toast({
        title: "确认失败",
        description: "发生错误，请稍后重试。",
        variant: "destructive",
      })
    } finally {
      setConfirmDialogOpen(false)
      setSelectedChange(null)
    }
  }

  const handleReject = async () => {
    try {
      // TODO: Implement actual rejection logic
      console.log('Rejected change:', selectedChange.id)
      
      // Simulating an API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: "变动已拒绝",
        description: `${selectedChange.name}的${selectedChange.type}申请已拒绝。`,
      })
      // Remove the rejected change from the list
      setPendingChanges(pendingChanges.filter(change => change.id !== selectedChange.id))
    } catch (error) {
      toast({
        title: "拒绝失败",
        description: "发生错误，请稍后重试。",
        variant: "destructive",
      })
    } finally {
      setRejectDialogOpen(false)
      setSelectedChange(null)
    }
  }

  const getChangeIcon = (type) => {
    switch (type) {
      case '入职': return <UserPlus className="text-emerald-500" />
      case '离职': return <UserMinus className="text-rose-500" />
      case '调岗': return <UserCog className="text-sky-500" />
      default: return null
    }
  }

  const getChangeBgColor = (type) => {
    switch (type) {
      case '入职': return 'bg-emerald-50'
      case '离职': return 'bg-rose-50'
      case '调岗': return 'bg-sky-50'
      default: return ''
    }
  }

  return (
    <div className="space-y-2">
      <div className="max-h-64 overflow-y-auto">
        {pendingChanges.map((change) => (
          <div key={change.id} className={`flex justify-between items-center p-2 rounded-lg mb-2 ${getChangeBgColor(change.type)}`}>
            <div className="flex items-center">
              {getChangeIcon(change.type)}
              <div className="ml-2">
                <p className="font-semibold text-sm">{change.name}</p>
                <p className="text-xs">
                  {change.type === '调岗' && `${change.fromCompany} → ${change.toCompany}`}
                  {change.type === '入职' && `加入 ${change.toCompany}`}
                  {change.type === '离职' && `离开 ${change.fromCompany}`}
                </p>
                <p className="text-xs text-gray-500">生效日期: {change.effectiveDate}</p>
              </div>
            </div>
            <div className="space-x-1">
              <Button 
                size="sm" 
                variant="outline" 
                className="text-xs py-1 h-7" 
                onClick={() => {
                  setSelectedChange(change)
                  setConfirmDialogOpen(true)
                }}
              >
                确认
              </Button>
              <Button 
                size="sm" 
                variant="outline" 
                className="text-xs py-1 h-7" 
                onClick={() => {
                  setSelectedChange(change)
                  setRejectDialogOpen(true)
                }}
              >
                拒绝
              </Button>
            </div>
          </div>
        ))}
      </div>

      <AlertDialog open={confirmDialogOpen} onOpenChange={setConfirmDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认变动</AlertDialogTitle>
            <AlertDialogDescription>
              您确定要确认 {selectedChange?.name} 的{selectedChange?.type}申请吗？
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={handleConfirm}>确认</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <AlertDialog open={rejectDialogOpen} onOpenChange={setRejectDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>拒绝变动</AlertDialogTitle>
            <AlertDialogDescription>
              您确定要拒绝 {selectedChange?.name} 的{selectedChange?.type}申请吗？
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={handleReject}>拒绝</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

