'use client'

import { useState } from 'react'
import { useAuth } from '../auth/AuthProvider'
import { MessageList } from './MessageList'
import { ChatInput } from './ChatInput'
import { LangGraphAPI, LangGraphMessage } from '../../lib/api'
import { Message, ChatState } from '../../types/chat'

export function ChatContainer() {
  const { user, signOut } = useAuth()
  
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    streamingMessageId: null
  })

  const langGraphAPI = new LangGraphAPI()

  const handleSendMessage = async (content: string, files?: File[]) => {
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
        streamingMessageId: assistantMessageId
      }))

      console.log('🚀 Sending message to LangGraph API:', content)
      
      // If files are attached, include them in the message
      let messageContent = content
      if (files && files.length > 0) {
        console.log('📎 Files attached:', files.map(f => f.name))
        // For now, we'll just mention the files in the message
        // In a full implementation, you'd want to process/analyze the files
        const fileInfo = files.map(f => `[File: ${f.name} (${f.type}, ${(f.size/1024).toFixed(1)}KB)]`).join('\n')
        messageContent = `${content}\n\nAttached files:\n${fileInfo}`
      }

      // Send message to API
      const response = await langGraphAPI.sendMessage(
        messageContent, 
        conversationHistory, 
        user?.access_token
      )

      console.log('✅ Got response from API, starting stream...')

      let accumulatedContent = ''
      
      // Stream the response
      for await (const chunk of langGraphAPI.streamResponse(response)) {
        accumulatedContent += chunk
        
        setChatState(prev => ({
          ...prev,
          messages: prev.messages.map(msg => 
            msg.id === assistantMessageId 
              ? { ...msg, content: accumulatedContent }
              : msg
          )
        }))
      }

      // Mark as completed
      setChatState(prev => ({
        ...prev,
        isLoading: false,
        streamingMessageId: null,
        messages: prev.messages.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, status: 'completed' }
            : msg
        )
      }))

    } catch (error) {
      console.error('❌ Error in chat:', error)
      
      // Show error message
      setChatState(prev => ({
        ...prev,
        isLoading: false,
        streamingMessageId: null,
        messages: prev.messages.map(msg => 
          msg.id === assistantMessageId 
            ? { 
                ...msg, 
                content: 'Sorry, I encountered an error while processing your request. Please try again.',
                status: 'error'
              }
            : msg
        )
      }))
    }
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Please sign in</h2>
          <p className="text-gray-600">You need to be signed in to use the research assistant.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="flex-shrink-0 bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Deep Research Assistant</h1>
            <p className="text-sm text-gray-600">AI-powered research and analysis</p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              Welcome, {user.email}
            </span>
            <button
              onClick={signOut}
              className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
            >
              Sign out
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      <MessageList 
        messages={chatState.messages}
        isLoading={chatState.isLoading}
        streamingMessageId={chatState.streamingMessageId}
      />

      {/* Input */}
      <div className="flex-shrink-0">
        <ChatInput 
          onSendMessage={handleSendMessage}
          disabled={chatState.isLoading}
          placeholder="Ask me anything... Upload files, paste images, or type your research question."
        />
      </div>
    </div>
  )
} 