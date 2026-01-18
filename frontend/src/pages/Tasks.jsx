import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { Calendar, Clock, CheckCircle, XCircle } from 'lucide-react'
import { format } from 'date-fns'

export default function Tasks() {
  const [statusFilter, setStatusFilter] = useState('')
  const [dateFilter, setDateFilter] = useState('today')
  const navigate = useNavigate()

  const getQueryParams = () => {
    const params = new URLSearchParams()
    if (statusFilter) params.append('status', statusFilter)
    if (dateFilter === 'today') {
      params.append('today', 'true')
    } else if (dateFilter === 'overdue') {
      params.append('overdue', 'true')
    }
    return params.toString()
  }

  const { data, isLoading } = useQuery({
    queryKey: ['tasks', statusFilter, dateFilter],
    queryFn: async () => {
      const res = await api.get(`/tasks/tasks/?${getQueryParams()}`)
      return res.data.results || res.data
    },
  })

  const getTaskIcon = (type) => {
    const icons = {
      visit: Calendar,
      call: Clock,
      online_meeting: Calendar,
      whatsapp: Clock,
    }
    return icons[type] || Calendar
  }

  const getStatusIcon = (status) => {
    if (status === 'completed') return CheckCircle
    if (status === 'missed') return XCircle
    return Clock
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center mb-6">
        <div className="sm:flex-auto">
          <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
          <p className="mt-2 text-sm text-gray-700">Manage your visits, calls, and follow-ups</p>
        </div>
      </div>

      <div className="mb-6 flex gap-4">
        <select
          value={dateFilter}
          onChange={(e) => setDateFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="today">Today</option>
          <option value="overdue">Overdue</option>
          <option value="all">All</option>
        </select>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">All Status</option>
          <option value="planned">Planned</option>
          <option value="completed">Completed</option>
          <option value="missed">Missed</option>
        </select>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Loading...</div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {data && data.length > 0 ? (
              data.map((task) => {
                const TaskIcon = getTaskIcon(task.task_type)
                const StatusIcon = getStatusIcon(task.status)
                return (
                  <li
                    key={task.id}
                    onClick={() => navigate(`/leads/${task.lead}`)}
                    className="px-6 py-4 hover:bg-gray-50 cursor-pointer"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center flex-1">
                        <TaskIcon className="h-5 w-5 text-gray-400 mr-4" />
                        <div className="flex-1">
                          <div className="flex items-center">
                            <p className="text-sm font-medium text-gray-900">
                              {task.lead_detail?.company_name || 'Unknown Lead'}
                            </p>
                            <span className="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              {task.task_type.replace('_', ' ')}
                            </span>
                          </div>
                          <div className="mt-1 flex items-center text-sm text-gray-500">
                            <Clock className="h-4 w-4 mr-1" />
                            <span>{format(new Date(task.scheduled_at), 'MMM d, yyyy h:mm a')}</span>
                            {task.outcome_notes && (
                              <>
                                <span className="mx-2">•</span>
                                <span className="truncate">{task.outcome_notes}</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="ml-4 flex items-center">
                        <StatusIcon
                          className={`h-5 w-5 ${
                            task.status === 'completed' ? 'text-green-500' :
                            task.status === 'missed' ? 'text-red-500' :
                            'text-yellow-500'
                          }`}
                        />
                      </div>
                    </div>
                  </li>
                )
              })
            ) : (
              <li className="px-6 py-12 text-center text-gray-500">No tasks found</li>
            )}
          </ul>
        </div>
      )}
    </div>
  )
}
