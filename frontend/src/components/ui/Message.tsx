import { formatTimestamp, cn } from '../../lib/utils'
import { Message as MessageType } from '../ui/ChatContainer'
import ReactMarkdown from 'react-markdown'
import { UserIcon, ComputerDesktopIcon, ClipboardIcon } from '@heroicons/react/24/solid'
import { useState } from 'react'

interface MessageProps {
  message: MessageType
}

export function Message({ message }: MessageProps) {
  const isUser = message.role === 'user'
  const isStreaming = message.status === 'streaming'
  const [copied, setCopied] = useState(false)
  
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy text:', err)
    }
  }
  
  return (
    <div className={cn(
      'flex gap-4 p-6 rounded-xl transition-all duration-200 hover:shadow-sm',
      isUser ? 'bg-blue-50 ml-12' : 'bg-white border border-gray-100 shadow-sm'
    )}>
      {/* Avatar */}
      <div className={cn(
        'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-sm',
        isUser ? 'bg-blue-600' : 'bg-gray-700'
      )}>
        {isUser ? (
          <UserIcon className="w-5 h-5 text-white" />
        ) : isStreaming ? (
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
        ) : (
          <ComputerDesktopIcon className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3">
            <span className="font-semibold text-sm text-gray-900">
              {isUser ? 'You' : 'AI Research Assistant'}
            </span>
            <span className="text-xs text-gray-500">
              {isStreaming ? 'Researching...' : formatTimestamp(message.timestamp)}
            </span>
            {message.status && (
              <div className={cn(
                'w-2 h-2 rounded-full',
                message.status === 'sending' && 'bg-yellow-400',
                message.status === 'completed' && 'bg-green-400',
                message.status === 'error' && 'bg-red-400',
                message.status === 'streaming' && 'bg-blue-400 animate-pulse'
              )} />
            )}
          </div>
          
          {/* Copy Button */}
          {!isStreaming && message.content && (
            <button
              onClick={handleCopy}
              className="opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-gray-100"
              title="Copy message"
            >
              <ClipboardIcon className={cn(
                "w-4 h-4",
                copied ? "text-green-600" : "text-gray-400"
              )} />
            </button>
          )}
        </div>
        
        <div className="text-gray-800 leading-relaxed">
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none prose-blue">
              <ReactMarkdown
                components={{
                  // Custom link rendering with proper styling
                  a: ({ href, children }) => (
                    <a 
                      href={href} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 underline font-medium"
                    >
                      {children}
                    </a>
                  ),
                  // Better code block styling
                  code: ({ className, children }) => {
                    const isInline = !className
                    return isInline ? (
                      <code className="bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded text-sm font-mono">
                        {children}
                      </code>
                    ) : (
                      <code className="block bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono">
                        {children}
                      </code>
                    )
                  },
                  // Better paragraph spacing
                  p: ({ children }) => (
                    <p className="mb-4 last:mb-0 leading-relaxed">{children}</p>
                  ),
                  // Better list styling
                  ul: ({ children }) => (
                    <ul className="mb-4 pl-6 space-y-1">{children}</ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="mb-4 pl-6 space-y-1">{children}</ol>
                  ),
                  li: ({ children }) => (
                    <li className="leading-relaxed">{children}</li>
                  ),
                  // Better heading styling
                  h1: ({ children }) => (
                    <h1 className="text-xl font-bold mb-3 text-gray-900">{children}</h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="text-lg font-semibold mb-2 text-gray-900">{children}</h2>
                  ),
                  h3: ({ children }) => (
                    <h3 className="text-base font-semibold mb-2 text-gray-900">{children}</h3>
                  ),
                  // Better blockquote styling
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-700 my-4">
                      {children}
                    </blockquote>
                  ),
                }}
              >
                {message.content || (isStreaming ? 'Researching your question...' : '')}
              </ReactMarkdown>
              {isStreaming && message.content && (
                <span className="inline-block w-2 h-5 bg-blue-600 animate-pulse ml-1" />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 