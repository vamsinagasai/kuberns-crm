import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import { ArrowLeft } from 'lucide-react'
import toast from 'react-hot-toast'

export default function VisitForm() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const leadId = searchParams.get('lead')

  const [formData, setFormData] = useState({
    lead: leadId || '',
    scheduled_at: new Date().toISOString().slice(0, 16),
    meeting_permitted: true,
    meeting_declined: false,
    meeting_rescheduled: false,
    person_spoken_to: '',
    person_role: '',
    frameworks_discussed: [],
    interest_level: '',
    partnership_interest: 'not_discussed',
    deployment_pain_points: '',
    next_steps_agreed: '',
    decline_reason: '',
    reschedule_reason: '',
  })

  const { data: leads } = useQuery({
    queryKey: ['leads'],
    queryFn: async () => {
      const res = await api.get('/leads/leads/')
      return res.data.results || res.data
    },
  })

  const visitMutation = useMutation({
    mutationFn: async (data) => {
      const taskData = {
        task_data: {
          lead: parseInt(data.lead),
          scheduled_at: data.scheduled_at,
          task_type: 'visit',
        },
        ...data,
      }
      const res = await api.post('/tasks/visits/', taskData)
      return res.data
    },
    onSuccess: () => {
      toast.success('Visit logged successfully!')
      navigate('/tasks')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to log visit')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!formData.lead) {
      toast.error('Please select a lead')
      return
    }

    if (formData.meeting_permitted && !formData.person_spoken_to) {
      toast.error('Person spoken to is required when meeting is permitted')
      return
    }

    if (formData.meeting_declined && !formData.decline_reason) {
      toast.error('Decline reason is required')
      return
    }

    visitMutation.mutate(formData)
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
      <button
        onClick={() => navigate('/tasks')}
        className="mb-4 inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Tasks
      </button>

      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-5 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-gray-900">Log Visit</h1>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-5 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Lead *
            </label>
            <select
              name="lead"
              value={formData.lead}
              onChange={handleChange}
              required
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select a lead</option>
              {leads?.map(lead => (
                <option key={lead.id} value={lead.id}>
                  {lead.company_name} - {lead.first_name} {lead.last_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Visit Date & Time *
            </label>
            <input
              type="datetime-local"
              name="scheduled_at"
              value={formData.scheduled_at}
              onChange={handleChange}
              required
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                name="meeting_permitted"
                checked={formData.meeting_permitted}
                onChange={(e) => {
                  setFormData(prev => ({
                    ...prev,
                    meeting_permitted: e.target.checked,
                    meeting_declined: !e.target.checked && prev.meeting_declined,
                    meeting_rescheduled: !e.target.checked && prev.meeting_rescheduled,
                  }))
                }}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label className="ml-2 block text-sm text-gray-900">
                Meeting Permitted
              </label>
            </div>

            {formData.meeting_permitted && (
              <div className="ml-6 space-y-4 border-l-2 border-blue-200 pl-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Person Spoken To *
                  </label>
                  <input
                    type="text"
                    name="person_spoken_to"
                    value={formData.person_spoken_to}
                    onChange={handleChange}
                    required
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Their Role
                  </label>
                  <input
                    type="text"
                    name="person_role"
                    value={formData.person_role}
                    onChange={handleChange}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Interest Level
                  </label>
                  <select
                    name="interest_level"
                    value={formData.interest_level}
                    onChange={handleChange}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Select interest level</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Deployment Pain Points
                  </label>
                  <textarea
                    name="deployment_pain_points"
                    value={formData.deployment_pain_points}
                    onChange={handleChange}
                    rows={3}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Next Steps Agreed
                  </label>
                  <textarea
                    name="next_steps_agreed"
                    value={formData.next_steps_agreed}
                    onChange={handleChange}
                    rows={3}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            )}

            <div className="flex items-center">
              <input
                type="checkbox"
                name="meeting_declined"
                checked={formData.meeting_declined}
                onChange={(e) => {
                  setFormData(prev => ({
                    ...prev,
                    meeting_declined: e.target.checked,
                    meeting_permitted: !e.target.checked && prev.meeting_permitted,
                    meeting_rescheduled: !e.target.checked && prev.meeting_rescheduled,
                  }))
                }}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label className="ml-2 block text-sm text-gray-900">
                Meeting Declined
              </label>
            </div>

            {formData.meeting_declined && (
              <div className="ml-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Reason for Declining *
                </label>
                <textarea
                  name="decline_reason"
                  value={formData.decline_reason}
                  onChange={handleChange}
                  required
                  rows={3}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            )}
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate('/tasks')}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={visitMutation.isPending}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
            >
              {visitMutation.isPending ? 'Saving...' : 'Log Visit'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
