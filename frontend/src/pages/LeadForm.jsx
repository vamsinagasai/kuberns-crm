import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import { ArrowLeft } from 'lucide-react'
import toast from 'react-hot-toast'

export default function LeadForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = !!id

  const { data: lead } = useQuery({
    queryKey: ['lead', id],
    queryFn: async () => {
      const res = await api.get(`/leads/leads/${id}/`)
      return res.data
    },
    enabled: isEdit,
  })

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    company_name: '',
    company_size: '',
    industry: '',
    city: '',
    state: '',
    phone: '',
    email: '',
    status: 'open',
    intent: '',
    infrastructure: '',
    client_type: '',
    cloud_spending: '',
    decision_maker: false,
    role: '',
    frameworks_used: [],
    research_notes: '',
    closing_strategy: '',
    partnership_interest: 'not_discussed',
  })

  // Populate form if editing
  useEffect(() => {
    if (lead) {
      setFormData({
        first_name: lead.first_name || '',
        last_name: lead.last_name || '',
        company_name: lead.company_name || '',
        company_size: lead.company_size || '',
        industry: lead.industry || '',
        city: lead.city || '',
        state: lead.state || '',
        phone: lead.phone || '',
        email: lead.email || '',
        status: lead.status || 'open',
        intent: lead.intent || '',
        infrastructure: lead.infrastructure || '',
        client_type: lead.client_type || '',
        cloud_spending: lead.cloud_spending || '',
        decision_maker: lead.decision_maker || false,
        role: lead.role || '',
        frameworks_used: lead.frameworks_used || [],
        research_notes: lead.research_notes || '',
        closing_strategy: lead.closing_strategy || '',
        partnership_interest: lead.partnership_interest || 'not_discussed',
      })
    }
  }, [lead])

  const leadMutation = useMutation({
    mutationFn: async (data) => {
      if (isEdit) {
        const res = await api.put(`/leads/leads/${id}/`, data)
        return res.data
      } else {
        const res = await api.post('/leads/leads/', data)
        return res.data
      }
    },
    onSuccess: () => {
      toast.success(isEdit ? 'Lead updated successfully!' : 'Lead created successfully!')
      navigate('/leads')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to save lead')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!formData.first_name || !formData.last_name || !formData.company_name || !formData.phone || !formData.city) {
      toast.error('Please fill in all required fields')
      return
    }

    leadMutation.mutate(formData)
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
        onClick={() => navigate('/leads')}
        className="mb-4 inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Leads
      </button>

      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-5 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-gray-900">
            {isEdit ? 'Edit Lead' : 'Create New Lead'}
          </h1>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-5 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                First Name *
              </label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Last Name *
              </label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company Name *
              </label>
              <input
                type="text"
                name="company_name"
                value={formData.company_name}
                onChange={handleChange}
                required
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phone *
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                City *
              </label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                required
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                State
              </label>
              <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Industry
              </label>
              <input
                type="text"
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="open">Open</option>
                <option value="sales_nurture">Sales Nurture</option>
                <option value="won">Won</option>
                <option value="lost">Lost</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Intent
              </label>
              <select
                name="intent"
                value={formData.intent}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select intent</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Research Notes
            </label>
            <textarea
              name="research_notes"
              value={formData.research_notes}
              onChange={handleChange}
              rows={4}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate('/leads')}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={leadMutation.isPending}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
            >
              {leadMutation.isPending ? 'Saving...' : isEdit ? 'Update Lead' : 'Create Lead'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
