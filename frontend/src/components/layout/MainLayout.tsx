import { useState } from 'react'
import { Sidebar } from './Sidebar'
import { ChatContainer } from '../ui/ChatContainer'

export function MainLayout() {
  const [currentPage, setCurrentPage] = useState('chat')

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