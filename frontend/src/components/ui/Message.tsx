import { formatTimestamp, cn } from '../../lib/utils'
import { Message as MessageType } from '../../types/chat'
import ReactMarkdown from 'react-markdown'
import { UserIcon, ComputerDesktopIcon } from '@heroicons/react/24/solid'

interface MessageProps {
  message: MessageType
}

export function Message({ message }: MessageProps) {
  const isUser = message.role === 'user'
  const isStreaming = message.status === 'streaming'
  
  return (
    <div className={cn(
      'flex gap-3 p-4 rounded-lg',
      isUser ? 'bg-blue-50 ml-8' : 'bg-white border border-gray-200'
    )}>
      {/* Avatar */}
      <div className={cn(
        'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
        isUser ? 'bg-blue-600' : 'bg-gray-600'
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
        <div className="flex items-center gap-2 mb-1">
          <span className="font-medium text-sm text-gray-900">
            {isUser ? 'You' : 'AI Assistant'}
          </span>
          <span className="text-xs text-gray-500">
            {isStreaming ? 'Responding...' : formatTimestamp(message.timestamp)}
          </span>
          {message.status && (
            <div className={cn(
              'w-2 h-2 rounded-full',
              message.status === 'pending' && 'bg-yellow-400',
              message.status === 'completed' && 'bg-green-400',
              message.status === 'error' && 'bg-red-400',
              message.status === 'streaming' && 'bg-blue-400 animate-pulse'
            )} />
          )}
        </div>
        
        <div className="text-gray-800">
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>
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