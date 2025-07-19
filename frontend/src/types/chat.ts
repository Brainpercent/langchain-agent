export interface Message {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
  status?: 'pending' | 'completed' | 'error' | 'streaming'
}

export interface ChatState {
  messages: Message[]
  isLoading: boolean
  error?: string
  streamingMessageId?: string
}

export interface ApiResponse {
  content: string
  status: 'success' | 'error'
  error?: string
} 