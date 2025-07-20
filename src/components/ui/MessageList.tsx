'use client'

import React, { useEffect, useRef } from 'react'
import { Message } from './Message'
import { Message as MessageType } from '../../types/chat'

interface MessageListProps {
  messages: MessageType[]
  isLoading?: boolean
  streamingMessageId?: string | null
}

export function MessageList({ messages, isLoading, streamingMessageId }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div 
      ref={containerRef}
      className="flex-1 overflow-y-auto overflow-x-hidden p-4 space-y-4 scroll-smooth"
      style={{ 
        maxHeight: 'calc(100vh - 200px)',
        userSelect: 'text',
        WebkitUserSelect: 'text'
      }}
    >
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full min-h-[400px]">
          <div className="text-center text-gray-500 select-text">
            <div className="text-lg font-medium mb-2">Welcome to Deep Research Assistant</div>
            <p>Start a conversation by typing your question below.</p>
            <p className="text-sm mt-2">You can paste files, images, or text for analysis.</p>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <Message key={message.id} message={message} />
          ))}
          
          {isLoading && (
            <div className="flex gap-3 p-4 rounded-lg bg-white border border-gray-200 select-text">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-sm text-gray-900">AI Research Assistant</span>
                  <span className="text-xs text-gray-500">Analyzing...</span>
                </div>
                <div className="text-gray-600">
                  Conducting deep research analysis...
                </div>
              </div>
            </div>
          )}
        </>
      )}
      
      <div ref={messagesEndRef} className="h-4" />
    </div>
  )
} 