import { useState } from 'react'
import { useAuth } from '../auth/AuthProvider'
import {
  ChatBubbleLeftRightIcon,
  Cog6ToothIcon,
  DocumentTextIcon,
  HomeIcon,
  ChartBarIcon,
  BeakerIcon,
  ClockIcon,
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
  WifiIcon,
  LinkIcon,
  KeyIcon
} from '@heroicons/react/24/outline'

interface SidebarProps {
  currentPage: string
  onPageChange: (page: string) => void
}

export function Sidebar({ currentPage, onPageChange }: SidebarProps) {
  const { user, signOut } = useAuth()

  const menuItems = [
    { id: 'home', label: 'Home', icon: HomeIcon },
    { id: 'chat', label: 'Research Chat', icon: ChatBubbleLeftRightIcon },
    { id: 'experiments', label: 'Experiments', icon: BeakerIcon, count: 0 },
    { id: 'monitoring', label: 'Monitoring', icon: ChartBarIcon, count: 0 },
    { id: 'history', label: 'Chat History', icon: ClockIcon },
  ]

  const channelItems = [
    { id: 'channels', label: 'Channel Manager', icon: WifiIcon },
    { id: 'api-keys', label: 'API Keys', icon: KeyIcon },
    { id: 'webhooks', label: 'Webhooks', icon: LinkIcon },
  ]

  const settingsItems = [
    { id: 'docs', label: 'Documentation', icon: DocumentTextIcon },
    { id: 'settings', label: 'Settings', icon: Cog6ToothIcon },
  ]

  const renderMenuSection = (title: string, items: typeof menuItems) => (
    <div className="mb-6">
      <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 px-3">
        {title}
      </h3>
      <div className="space-y-1">
        {items.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.id
          
          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-left transition-colors ${
                isActive 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-5 h-5" />
                <span className="text-sm font-medium">{item.label}</span>
              </div>
              {item.count !== undefined && (
                <span className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded-full">
                  {item.count}
                </span>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )

  return (
    <div className="w-64 bg-gray-900 text-white h-screen flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">AI</span>
          </div>
          <span className="font-semibold text-lg">Deep Research</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 overflow-y-auto">
        {renderMenuSection("Main", menuItems)}
        {renderMenuSection("Integrations", channelItems)}
        {renderMenuSection("System", settingsItems)}
      </nav>

      {/* User Section */}
      <div className="p-4 border-t border-gray-700">
        {user && (
          <div className="space-y-2">
            <div className="flex items-center space-x-3 px-3 py-2">
              <UserCircleIcon className="w-8 h-8 text-gray-400" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {user.email}
                </p>
                <p className="text-xs text-gray-400">Research Assistant</p>
              </div>
            </div>
            <button
              onClick={signOut}
              className="w-full flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-800 hover:text-white rounded-lg transition-colors"
            >
              <ArrowRightOnRectangleIcon className="w-5 h-5" />
              <span className="text-sm font-medium">Sign Out</span>
            </button>
          </div>
        )}
      </div>
    </div>
  )
} 