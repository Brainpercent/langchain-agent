'use client'

import React, { useState, KeyboardEvent } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/solid'
import { cn } from '../../lib/utils'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
  placeholder?: string
}

export function ChatInput({ 
  onSendMessage, 
  disabled = false,
  placeholder = "Ask me anything about your research..." 
}: ChatInputProps) {
  const [input, setInput] = useState('')

  const handleSubmit = () => {
    const trimmedInput = input.trim()
    if (trimmedInput && !disabled) {
      onSendMessage(trimmedInput)
      setInput('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="flex gap-3 items-end">
        <div className="flex-1">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className={cn(
              'w-full resize-none rounded-lg border border-gray-300 px-3 py-2',
              'focus:ring-2 focus:ring-blue-500 focus:border-transparent',
              'placeholder-gray-500 text-gray-900',
              'disabled:bg-gray-100 disabled:cursor-not-allowed',
              'min-h-[44px] max-h-32'
            )}
            style={{ 
              height: 'auto',
              minHeight: '44px'
            }}
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement
              target.style.height = 'auto'
              target.style.height = Math.min(target.scrollHeight, 128) + 'px'
            }}
          />
        </div>
        
        <button
          onClick={handleSubmit}
          disabled={disabled || !input.trim()}
          className={cn(
            'flex-shrink-0 w-11 h-11 rounded-lg flex items-center justify-center',
            'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300',
            'transition-colors duration-200',
            'disabled:cursor-not-allowed'
          )}
        >
          <PaperAirplaneIcon className="w-5 h-5 text-white" />
        </button>
      </div>
      
      <div className="mt-2 text-xs text-gray-500">
        Press Enter to send, Shift + Enter for new line
      </div>
    </div>
  )
} 