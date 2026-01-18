import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import { ArrowLeft, Edit, Phone, Mail, MapPin } from 'lucide-react'
import { format } from 'date-fns'

export default function LeadDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: lead, isLoading } = useQuery({
    queryKey: ['lead', id],
    queryFn: async () => {
      const res = await api.get(`/leads/leads/${id}/`)
      return res.data
    },
  })

  const { data: tasks } = useQuery({
    queryKey: ['tasks', 'lead', id],
    queryFn: async () => {
      const res = await api.get(`/tasks/tasks/?lead=${id}`)
      return res.data.results || res.data
    },
  })

  const getStatusColor = (status) => {
    const colors = {
      open: 'bg-blue-100 text-blue-800',
      sales_nurture: 'bg-yellow-100 text-yellow-800',
      won: 'bg-green-100 text-green-800',
      lost: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  if (isLoading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!lead) {
    return <div className="text-center py-12">Lead not found</div>
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      <div className="mb-4 flex items-center justify-between">
        <button
          onClick={() => navigate('/leads')}
          className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Leads
        </button>
        <button
          onClick={() => navigate(`/leads/${id}/edit`)}
          className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          <Edit className="h-4 w-4 mr-2" />
          Edit Lead
        </button>
      </div>

      <div className="bg-white shadow rounded-lg mb-6">
        <div className="px-6 py-5 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{lead.company_name}</h1>
              <p className="mt-1 text-sm text-gray-500">
                {lead.first_name} {lead.last_name}
              </p>
            </div>
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(lead.status)}`}>
              {lead.status.replace('_', ' ').toUpperCase()}
            </span>
          </div>
        </div>

        <div className="px-6 py-5 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-3">Contact Information</h3>
            <div className="space-y-2">
              <div className="flex items-center text-sm">
                <Phone className="h-4 w-4 mr-2 text-gray-400" />
                <span>{lead.phone}</span>
              </div>
              {lead.email && (
                <div className="flex items-center text-sm">
                  <Mail className="h-4 w-4 mr-2 text-gray-400" />
                  <span>{lead.email}</span>
                </div>
              )}
              <div className="flex items-center text-sm">
                <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                <span>{lead.city}{lead.state && `, ${lead.state}`}</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-3">Business Details</h3>
            <div className="space-y-2 text-sm">
              {lead.industry && <p><span className="font-medium">Industry:</span> {lead.industry}</p>}
              {lead.company_size && <p><span className="font-medium">Size:</span> {lead.company_size}</p>}
              {lead.infrastructure && <p><span className="font-medium">Infrastructure:</span> {lead.infrastructure}</p>}
              {lead.client_type && <p><span className="font-medium">Client Type:</span> {lead.client_type}</p>}
              {lead.intent && <p><span className="font-medium">Intent:</span> {lead.intent}</p>}
            </div>
          </div>

          {lead.frameworks_used && lead.frameworks_used.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-2">Frameworks</h3>
              <div className="flex flex-wrap gap-2">
                {lead.frameworks_used.map((fw, idx) => (
                  <span key={idx} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {fw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {lead.research_notes && (
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-2">Research Notes</h3>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{lead.research_notes}</p>
            </div>
          )}
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-5 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-medium text-gray-900">Tasks & Activities</h2>
            <button
              onClick={() => navigate(`/visits/new?lead=${lead.id}`)}
              className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Log Visit
            </button>
          </div>
        </div>
        <div className="px-6 py-5">
          {tasks && tasks.length > 0 ? (
            <div className="space-y-4">
              {tasks.map((task) => (
                <div key={task.id} className="border-l-4 border-blue-500 pl-4 py-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {task.task_type.replace('_', ' ').toUpperCase()}
                      </p>
                      <p className="text-xs text-gray-500">
                        {format(new Date(task.scheduled_at), 'MMM d, yyyy h:mm a')}
                      </p>
                      {task.outcome_notes && (
                        <p className="text-sm text-gray-700 mt-1">{task.outcome_notes}</p>
                      )}
                    </div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      task.status === 'completed' ? 'bg-green-100 text-green-800' :
                      task.status === 'missed' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {task.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No tasks yet</p>
          )}
        </div>
      </div>
    </div>
  )
}
