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
        fullContent += chunk
        setChatState(prev => ({
          ...prev,
          messages: prev.messages.map(msg => 
            msg.id === assistantMessageId 
              ? { ...msg, content: fullContent }
              : msg
          )
        }))
      }

      // Mark as completed
      setChatState(prev => ({
        ...prev,
        messages: prev.messages.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, status: 'completed' }
            : msg
        ),
        streamingMessageId: null
      }))

    } catch (error) {
      console.error('❌ Error in chat:', error)
      
      // Update assistant message to show error
      setChatState(prev => ({
        ...prev,
        messages: prev.messages.map(msg => 
          msg.id === prev.streamingMessageId 
            ? { 
                ...msg, 
                content: '❌ I encountered an error while processing your request. Please ensure the API is properly configured and try again.',
                status: 'error'
              }
            : msg
        ),
        isLoading: false,
        streamingMessageId: null
      }))
    }
  }

  if (!user) {
    return null
  }

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">Research Chat</h1>
            <p className="text-sm text-gray-500">Ask me anything and I'll research it for you</p>
          </div>
          <div className="flex items-center space-x-3">
            <div className="text-sm text-gray-500">
              Connected as {user.email}
            </div>
          </div>
        </div>
      </div>

      {/* Chat Content */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="flex-1 overflow-hidden">
          <MessageList 
            messages={chatState.messages} 
            isLoading={chatState.isLoading}
            streamingMessageId={chatState.streamingMessageId}
          />
        </div>
        
        {/* Input Area */}
        <div className="border-t border-gray-200 bg-white">
          <div className="p-4">
            <ChatInput 
              onSendMessage={handleSendMessage}
              disabled={chatState.isLoading || !!chatState.streamingMessageId}
              placeholder="Ask a research question..."
            />
          </div>
        </div>
      </div>
    </div>
  )
} 