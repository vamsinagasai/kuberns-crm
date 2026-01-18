import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import { Users, Calendar, AlertCircle, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'
import { format } from 'date-fns'

export default function Dashboard() {
  const { user } = useAuth()

  const { data: leadStats } = useQuery({
    queryKey: ['leads', 'stats'],
    queryFn: async () => {
      const res = await api.get('/leads/leads/stats/')
      return res.data
    },
  })

  const { data: todayTasks } = useQuery({
    queryKey: ['tasks', 'today'],
    queryFn: async () => {
      const res = await api.get('/tasks/tasks/?today=true&status=planned')
      return res.data.results || res.data
    },
  })

  const { data: overdueTasks } = useQuery({
    queryKey: ['tasks', 'overdue'],
    queryFn: async () => {
      const res = await api.get('/tasks/tasks/?overdue=true')
      return res.data.results || res.data
    },
  })

  const { data: atRiskLeads } = useQuery({
    queryKey: ['leads', 'at-risk'],
    queryFn: async () => {
      const res = await api.get('/leads/leads/at_risk/')
      return res.data.results || res.data
    },
  })

  const stats = [
    {
      name: 'Total Leads',
      value: leadStats?.total || 0,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      name: "Today's Tasks",
      value: todayTasks?.length || 0,
      icon: Calendar,
      color: 'bg-green-500',
    },
    {
      name: 'Overdue Tasks',
      value: overdueTasks?.length || 0,
      icon: AlertCircle,
      color: 'bg-red-500',
    },
    {
      name: 'At Risk Leads',
      value: atRiskLeads?.length || 0,
      icon: TrendingUp,
      color: 'bg-yellow-500',
    },
  ]

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.first_name || user?.username}!
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          {user?.role_display || user?.role === 'sales_executive' ? 'Sales Executive' : 'Sales Manager'} Dashboard
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 ${stat.color} rounded-md p-3`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{stat.name}</dt>
                    <dd className="text-lg font-semibold text-gray-900">{stat.value}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Today's Tasks</h3>
            <div className="space-y-3">
              {todayTasks && todayTasks.length > 0 ? (
                todayTasks.slice(0, 5).map((task) => (
                  <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{task.lead_detail?.company_name}</p>
                      <p className="text-xs text-gray-500">
                        {task.task_type} - {format(new Date(task.scheduled_at), 'h:mm a')}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500">No tasks scheduled for today</p>
              )}
            </div>
            <Link
              to="/tasks"
              className="mt-4 inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
            >
              View all tasks →
            </Link>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">At Risk Leads</h3>
            <div className="space-y-3">
              {atRiskLeads && atRiskLeads.length > 0 ? (
                atRiskLeads.slice(0, 5).map((lead) => (
                  <Link
                    key={lead.id}
                    to={`/leads/${lead.id}`}
                    className="flex items-center justify-between p-3 bg-yellow-50 rounded hover:bg-yellow-100"
                  >
                    <div>
                      <p className="text-sm font-medium text-gray-900">{lead.company_name}</p>
                      <p className="text-xs text-gray-500">{lead.city} - {lead.status}</p>
                    </div>
                    <AlertCircle className="h-5 w-5 text-yellow-600" />
                  </Link>
                ))
              ) : (
                <p className="text-sm text-gray-500">No at-risk leads</p>
              )}
            </div>
            <Link
              to="/leads"
              className="mt-4 inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
            >
              View all leads →
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
