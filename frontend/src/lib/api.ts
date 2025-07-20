// API Response types
export interface LangGraphMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface StreamChunk {
  type: 'chunk' | 'complete'
  content: string
}

export class LangGraphAPI {
  private baseUrl: string
  private assistantId: string

  constructor() {
    // Use same origin for API calls to avoid CORS issues
    // Check if window is available (client-side) to avoid SSR issues
    if (typeof window !== 'undefined') {
      this.baseUrl = process.env.NODE_ENV === 'production' 
        ? window.location.origin 
        : 'http://localhost:3000'
    } else {
      // Server-side fallback
      this.baseUrl = process.env.NEXT_PUBLIC_VERCEL_URL 
        ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}`
        : 'http://localhost:3000'
    }
    this.assistantId = process.env.NEXT_PUBLIC_ASSISTANT_ID || 'deep_researcher'
  }

  async sendMessage(userMessage: string, conversationHistory: LangGraphMessage[] = [], accessToken?: string): Promise<Response> {
    console.log('🚀 Sending request to Vercel API...')
    console.log('Base URL:', this.baseUrl)
    console.log('Message:', userMessage)
    console.log('Using authorization:', accessToken ? 'Yes (token provided)' : 'No (missing token)')

    try {
      // Prepare headers
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      }

      // Add authorization header if token is provided
      if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`
      }

      // Prepare request body for Vercel API
      const requestBody = {
        message: userMessage,
        platform: 'web',
        user_id: 'web_user',
        channel_id: 'web_chat',
        history: conversationHistory
      }

      console.log('Request body:', JSON.stringify(requestBody, null, 2))

      const response = await fetch(`${this.baseUrl}/api/v1/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody)
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('❌ API request failed:', response.status, errorText)
        
        // Try to provide helpful error messages
        if (response.status === 403) {
          throw new Error('Access forbidden. Please make sure you are logged in and your session is valid.')
        } else if (response.status === 401) {
          throw new Error('Authentication failed. Please log in again.')
        } else if (response.status === 404) {
          throw new Error('API endpoint not found. Please check your deployment configuration.')
        } else {
          throw new Error(`API request failed: ${response.status} ${response.statusText}`)
        }
      }

      console.log('✅ API request successful')
      return response
    } catch (error) {
      console.error('❌ Network error:', error)
      throw error
    }
  }

  async *streamResponse(response: Response): AsyncGenerator<string, void, unknown> {
    if (!response.body) {
      throw new Error('No response body available')
    }

    try {
      // Parse the JSON response from Vercel API
      const data = await response.json()
      
      if (data.status === 'error') {
        throw new Error(data.error || 'Unknown error from API')
      }

      // Simulate streaming by yielding the response gradually
      const content = data.response || ''
      console.log('📄 Received content from API:', content.length, 'characters')
      
      // Split content into chunks and stream them
      const words = content.split(' ')
      let currentContent = ''
      
      for (let i = 0; i < words.length; i++) {
        currentContent += (i > 0 ? ' ' : '') + words[i]
        
        // Yield chunks of approximately 5-10 words for smooth streaming effect
        if (i % 7 === 0 || i === words.length - 1) {
          const chunk = i === 0 ? currentContent : ' ' + words.slice(Math.max(0, i - 6), i + 1).join(' ')
          yield chunk
          
          // Small delay to simulate streaming
          await new Promise(resolve => setTimeout(resolve, 50))
        }
      }
      
      console.log('🏁 Streaming completed')
    } catch (error) {
      console.error('❌ Error processing response:', error)
      throw error
    }
  }
}

export const langGraphAPI = new LangGraphAPI() 