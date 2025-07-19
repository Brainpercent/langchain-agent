'use client'

import React, { useState, useRef, useEffect } from 'react'
import { ChatInput } from './ChatInput'
import { MessageList } from './MessageList'
import { Message, ChatState } from '../../types/chat'
import { langGraphAPI, LangGraphMessage } from '../../lib/api'
import { useAuth } from '../auth/AuthProvider'
import { LoginForm } from '../auth/LoginForm'
import { ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline'

export function ChatContainer() {
  const { user, loading: authLoading, signOut } = useAuth()
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isLoading: false,
  })

  // Show loading spinner while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Show login form if user is not authenticated
  if (!user) {
    return <LoginForm />
  }

  const handleSendMessage = async (content: string) => {
    // Create user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content,
      role: 'user',
      timestamp: new Date(),
      status: 'completed'
    }

    // Add user message to state
    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true
    }))

    try {
      // Convert chat history to LangGraph format
      const conversationHistory: LangGraphMessage[] = chatState.messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }))

      // Create assistant message for streaming
      const assistantMessageId = `assistant-${Date.now()}`
      const assistantMessage: Message = {
        id: assistantMessageId,
        content: '',
        role: 'assistant',
        timestamp: new Date(),
        status: 'streaming'
      }

      // Add assistant message to state
      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        isLoading: false,
        streamingMessageId: assistantMessageId
      }))

      // Send message to LangGraph API
      console.log('🚀 Sending message to LangGraph API:', content)
      const response = await langGraphAPI.sendMessage(content, conversationHistory)
      console.log('✅ Got response from API, starting stream...')
      
      // Stream the response
      let fullContent = ''
      for await (const chunk of langGraphAPI.streamResponse(response)) {
        console.log('📦 Received chunk:', chunk)
        
        // Check if this is a replacement marker
        if (chunk.startsWith('__REPLACE__')) {
          // Replace the entire content with the new response
          fullContent = chunk.substring(11) // Remove __REPLACE__ prefix
          console.log('🔄 Replacing content with:', fullContent)
        } else {
          // Regular incremental content
          fullContent += chunk
        }
        
        console.log('📝 Full content so far:', fullContent)
        
        setChatState(prev => ({
          ...prev,
          messages: prev.messages.map(msg => 
            msg.id === assistantMessageId 
              ? { ...msg, content: fullContent, status: 'streaming' }
              : msg
          )
        }))
      }

      console.log('🏁 Stream completed. Final content:', fullContent)

      // Mark as completed
      setChatState(prev => ({
        ...prev,
        messages: prev.messages.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, status: 'completed' }
            : msg
        ),
        streamingMessageId: undefined
      }))

    } catch (error) {
      console.error('❌ Error in chat:', error)
      
      setChatState(prev => ({
        ...prev,
        isLoading: false,
        streamingMessageId: undefined,
        error: error instanceof Error ? error.message : 'Failed to send message. Please try again.'
      }))

      // If there's a streaming message, mark it as error
      if (chatState.streamingMessageId) {
        setChatState(prev => ({
          ...prev,
          messages: prev.messages.map(msg => 
            msg.id === chatState.streamingMessageId 
              ? { ...msg, status: 'error', content: 'Failed to get response' }
              : msg
          )
        }))
      }
    }
  }

  const clearError = () => {
    setChatState(prev => ({ ...prev, error: undefined }))
  }

  const handleSignOut = async () => {
    await signOut()
    // Clear chat state when signing out
    setChatState({
      messages: [],
      isLoading: false,
    })
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">
            AI Research Assistant
          </h1>
          <p className="text-sm text-gray-600">
            Welcome back, {user.email}
          </p>
        </div>
        <button
          onClick={handleSignOut}
          className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
        >
          <ArrowRightOnRectangleIcon className="w-4 h-4" />
          Sign Out
        </button>
      </div>

      {/* Messages */}
      <MessageList 
        messages={chatState.messages} 
        isLoading={chatState.isLoading}
      />

      {/* Error Display */}
      {chatState.error && (
        <div className="bg-red-50 border-t border-red-200 px-6 py-3 flex justify-between items-center">
          <p className="text-sm text-red-600">{chatState.error}</p>
          <button 
            onClick={clearError}
            className="text-red-600 hover:text-red-800 text-sm font-medium"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Input */}
      <ChatInput 
        onSendMessage={handleSendMessage}
        disabled={chatState.isLoading || !!chatState.streamingMessageId}
      />
    </div>
  )
} 