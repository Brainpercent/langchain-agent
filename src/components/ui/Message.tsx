import { formatTimestamp, cn } from '../../lib/utils'
import { Message as MessageType } from '../../types/chat'
import ReactMarkdown from 'react-markdown'
import { UserIcon, ComputerDesktopIcon, ClipboardIcon, CheckIcon } from '@heroicons/react/24/solid'
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
      // Fallback for older browsers
      const textArea = document.createElement('textarea')
      textArea.value = message.content
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand('copy')
      document.body.removeChild(textArea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }
  
  return (
    <div className={cn(
      'flex gap-4 p-6 rounded-xl transition-all duration-200 hover:shadow-sm group',
      'select-text cursor-text',
      isUser ? 'bg-blue-50 ml-12' : 'bg-white border border-gray-100 shadow-sm'
    )}
    style={{ userSelect: 'text', WebkitUserSelect: 'text' }}
    >
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
              {formatTimestamp(message.timestamp)}
            </span>
            {message.status === 'streaming' && (
              <span className="text-xs text-blue-600 font-medium">
                Analyzing...
              </span>
            )}
          </div>
          
          {/* Copy Button - Only show for assistant messages and on hover */}
          {!isUser && (
            <button
              onClick={handleCopy}
              className={cn(
                'opacity-0 group-hover:opacity-100 transition-opacity duration-200',
                'p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700',
                'flex items-center gap-1 text-xs font-medium cursor-pointer'
              )}
              title="Copy message"
            >
              {copied ? (
                <>
                  <CheckIcon className="w-4 h-4 text-green-600" />
                  <span className="text-green-600">Copied!</span>
                </>
              ) : (
                <>
                  <ClipboardIcon className="w-4 h-4" />
                  <span>Copy</span>
                </>
              )}
            </button>
          )}
        </div>

        {/* Message Content */}
        <div className={cn(
          'prose prose-sm max-w-none',
          'prose-headings:text-gray-900 prose-headings:font-semibold',
          'prose-p:text-gray-700 prose-p:leading-relaxed',
          'prose-ul:text-gray-700 prose-ol:text-gray-700',
          'prose-li:text-gray-700',
          'prose-strong:text-gray-900 prose-strong:font-semibold',
          'prose-code:text-blue-600 prose-code:bg-blue-50 prose-code:px-1 prose-code:py-0.5 prose-code:rounded',
          'prose-pre:bg-gray-900 prose-pre:text-gray-100',
          'prose-blockquote:border-l-blue-500 prose-blockquote:bg-blue-50 prose-blockquote:text-gray-700',
          'select-text cursor-text'
        )}
        style={{ userSelect: 'text', WebkitUserSelect: 'text' }}
        >
          {isUser ? (
            <div className="whitespace-pre-wrap break-words select-text">
              {message.content}
            </div>
          ) : (
            <div className="select-text">
              <ReactMarkdown
                components={{
                  // Custom components for better styling
                  h1: ({ children }) => <h1 className="text-xl font-bold mb-4 text-gray-900 select-text">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-lg font-semibold mb-3 text-gray-900 select-text">{children}</h2>,
                  h3: ({ children }) => <h3 className="text-base font-semibold mb-2 text-gray-900 select-text">{children}</h3>,
                  p: ({ children }) => <p className="mb-3 text-gray-700 leading-relaxed select-text">{children}</p>,
                  ul: ({ children }) => <ul className="mb-3 pl-4 space-y-1 select-text">{children}</ul>,
                  ol: ({ children }) => <ol className="mb-3 pl-4 space-y-1 select-text">{children}</ol>,
                  li: ({ children }) => <li className="text-gray-700 select-text">{children}</li>,
                  code: ({ children, className }) => {
                    const isInline = !className
                    return isInline ? (
                      <code className="bg-blue-50 text-blue-600 px-1 py-0.5 rounded text-sm font-mono select-text">
                        {children}
                      </code>
                    ) : (
                      <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto select-text">
                        <code className="select-text">{children}</code>
                      </pre>
                    )
                  },
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-blue-500 bg-blue-50 pl-4 py-2 my-4 select-text">
                      {children}
                    </blockquote>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}
        </div>

        {/* Message Status */}
        {message.status === 'error' && (
          <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center gap-2 text-red-700 text-sm">
              <span className="font-medium">Error:</span>
              <span>Failed to process message</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 