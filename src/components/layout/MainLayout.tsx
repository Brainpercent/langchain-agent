import { useState } from 'react'
import { Sidebar } from './Sidebar'
import { ChatContainer } from '../ui/ChatContainer'
import { LoginForm } from '../auth/LoginForm'
import { useAuth } from '../auth/AuthProvider'

export function MainLayout() {
  const { user, loading } = useAuth()
  const [currentPage, setCurrentPage] = useState('chat')

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Show login form if user is not authenticated
  if (!user) {
    return <LoginForm />
  }

  const renderContent = () => {
    switch (currentPage) {
      case 'home':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Welcome to Deep Research Assistant
              </h1>
              <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-3">
                  🚀 Get Started
                </h2>
                <p className="text-gray-600 mb-4">
                  Your AI-powered research assistant is ready to help you explore any topic in depth.
                  Click on "Research Chat" to start a conversation.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-blue-900 mb-2">🔍 Deep Research</h3>
                    <p className="text-blue-700 text-sm">
                      Ask complex questions and get comprehensive, well-researched answers
                    </p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-green-900 mb-2">📊 Real-time Analysis</h3>
                    <p className="text-green-700 text-sm">
                      Watch as the AI searches, analyzes, and synthesizes information
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      
      case 'chat':
        return (
          <div className="flex-1 bg-gray-50">
            <ChatContainer />
          </div>
        )
      
      case 'experiments':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Experiments</h1>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">
                  Experiment dashboard coming soon. Here you'll be able to compare different
                  research approaches and save your favorite configurations.
                </p>
              </div>
            </div>
          </div>
        )
      
      case 'monitoring':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Monitoring</h1>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">
                  Usage analytics and performance monitoring will be available here.
                </p>
              </div>
            </div>
          </div>
        )
      
      case 'history':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Chat History</h1>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">
                  Your previous research conversations will be saved and accessible here.
                </p>
              </div>
            </div>
          </div>
        )

      case 'channels':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Channel Manager</h1>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 bg-indigo-500 rounded-lg flex items-center justify-center mr-3">
                      <span className="text-white font-bold">D</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Discord</h3>
                      <p className="text-sm text-gray-500">Not connected</p>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-4">
                    Connect your Discord server to enable AI research assistance in your channels.
                  </p>
                  <button className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors">
                    Connect Discord
                  </button>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center mr-3">
                      <span className="text-white font-bold">S</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Slack</h3>
                      <p className="text-sm text-gray-500">Not connected</p>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-4">
                    Add the AI research assistant to your Slack workspace.
                  </p>
                  <button className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors">
                    Connect Slack
                  </button>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-3">
                      <span className="text-white font-bold">T</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Telegram</h3>
                      <p className="text-sm text-gray-500">Not connected</p>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-4">
                    Deploy a Telegram bot for research assistance on the go.
                  </p>
                  <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                    Connect Telegram
                  </button>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 bg-emerald-500 rounded-lg flex items-center justify-center mr-3">
                      <span className="text-white font-bold">W</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">WhatsApp</h3>
                      <p className="text-sm text-gray-500">Not connected</p>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-4">
                    Connect WhatsApp Business API for research assistance via messaging.
                  </p>
                  <button className="w-full bg-emerald-600 text-white py-2 px-4 rounded-lg hover:bg-emerald-700 transition-colors">
                    Connect WhatsApp
                  </button>
                </div>
              </div>
            </div>
          </div>
        )

      case 'api-keys':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-6">API Keys</h1>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-800">Manage API Keys</h2>
                    <p className="text-gray-600">Create and manage API keys for external integrations.</p>
                  </div>
                  <button className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                    Generate New Key
                  </button>
                </div>
                
                <div className="border rounded-lg overflow-hidden">
                  <div className="bg-gray-50 px-6 py-3 border-b">
                    <div className="grid grid-cols-4 gap-4">
                      <div className="font-medium text-gray-700">Name</div>
                      <div className="font-medium text-gray-700">Key</div>
                      <div className="font-medium text-gray-700">Created</div>
                      <div className="font-medium text-gray-700">Actions</div>
                    </div>
                  </div>
                  <div className="px-6 py-8 text-center text-gray-500">
                    No API keys created yet. Click "Generate New Key" to get started.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )

      case 'webhooks':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Webhooks</h1>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-800">Webhook Management</h2>
                    <p className="text-gray-600">Configure incoming and outgoing webhooks for real-time integrations.</p>
                  </div>
                  <button className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                    Add Webhook
                  </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div className="border rounded-lg p-4">
                    <h3 className="font-semibold text-gray-800 mb-2">Incoming Webhooks</h3>
                    <p className="text-gray-600 text-sm mb-3">
                      Receive data from external services and trigger research workflows.
                    </p>
                    <div className="bg-gray-50 rounded p-2 text-xs font-mono text-gray-700">
                      POST /api/webhooks/incoming
                    </div>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h3 className="font-semibold text-gray-800 mb-2">Outgoing Webhooks</h3>
                    <p className="text-gray-600 text-sm mb-3">
                      Send research results and notifications to external services.
                    </p>
                    <div className="bg-gray-50 rounded p-2 text-xs font-mono text-gray-700">
                      Configure endpoints
                    </div>
                  </div>
                </div>

                <div className="border rounded-lg overflow-hidden">
                  <div className="bg-gray-50 px-6 py-3 border-b">
                    <div className="grid grid-cols-5 gap-4">
                      <div className="font-medium text-gray-700">Name</div>
                      <div className="font-medium text-gray-700">URL</div>
                      <div className="font-medium text-gray-700">Type</div>
                      <div className="font-medium text-gray-700">Status</div>
                      <div className="font-medium text-gray-700">Actions</div>
                    </div>
                  </div>
                  <div className="px-6 py-8 text-center text-gray-500">
                    No webhooks configured yet. Click "Add Webhook" to get started.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      
      case 'docs':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Documentation</h1>
              <div className="bg-white rounded-lg shadow p-6 space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">How to Use</h3>
                  <p className="text-gray-600 mb-3">
                    Simply type your research question in the chat interface and watch as the AI:
                  </p>
                  <ul className="list-disc list-inside text-gray-600 space-y-1">
                    <li>Searches multiple sources for relevant information</li>
                    <li>Analyzes and synthesizes the findings</li>
                    <li>Provides comprehensive, well-structured answers</li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">Example Questions</h3>
                  <ul className="list-disc list-inside text-gray-600 space-y-1">
                    <li>"What are the latest developments in quantum computing?"</li>
                    <li>"How does climate change affect global food security?"</li>
                    <li>"What are the ethical implications of AI in healthcare?"</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )
      
      case 'settings':
        return (
          <div className="flex-1 bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Settings</h1>
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600">
                  Customize your research assistant preferences and API configurations here.
                </p>
              </div>
            </div>
          </div>
        )
      
      default:
        return null
    }
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar currentPage={currentPage} onPageChange={setCurrentPage} />
      {renderContent()}
    </div>
  )
} 