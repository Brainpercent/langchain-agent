import { ApiResponse } from '@/types/chat'
import { getAccessToken } from './auth'

// Configuration
const LANGGRAPH_API_URL = process.env.NEXT_PUBLIC_LANGGRAPH_API_URL || 'http://localhost:2024'
const ASSISTANT_ID = process.env.NEXT_PUBLIC_ASSISTANT_ID || 'Deep Researcher'

export interface LangGraphMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface LangGraphRequest {
  input: {
    messages: LangGraphMessage[]
  }
  config?: {
    configurable?: {
      model_name?: string
      thread_id?: string
    }
  }
  stream?: boolean
}

export interface LangGraphStreamResponse {
  event: string
  data: any
}

export class LangGraphAPI {
  private baseUrl: string
  private assistantId: string

  constructor() {
    this.baseUrl = LANGGRAPH_API_URL
    this.assistantId = ASSISTANT_ID
  }

  async sendMessage(userMessage: string, conversationHistory: LangGraphMessage[] = []): Promise<Response> {
    // Get access token for authentication
    const accessToken = await getAccessToken()
    
    if (!accessToken) {
      throw new Error('Authentication required. Please log in to continue.')
    }

    const messages = [
      ...conversationHistory,
      { role: 'user' as const, content: userMessage }
    ]

    // Generate a unique thread ID for this conversation
    const threadId = `thread_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    // LangGraph standard format - create thread first, then run
    const createThreadPayload = {
      metadata: {},
      config: {
        configurable: {
          model_name: 'gpt-4o'
        }
      }
    }

    // Create thread first
    try {
      console.log('Creating thread...')
      const createThreadResponse = await fetch(`${this.baseUrl}/threads`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify(createThreadPayload)
      })

      if (!createThreadResponse.ok) {
        const errorText = await createThreadResponse.text()
        console.log('Failed to create thread:', errorText)
        throw new Error(`Failed to create thread: ${createThreadResponse.status} ${createThreadResponse.statusText}`)
      }

      const threadData = await createThreadResponse.json()
      console.log('Thread created:', threadData)
      const actualThreadId = threadData.thread_id

      // Now create a run with the messages
      const runPayload = {
        assistant_id: this.assistantId,
        input: {
          messages: messages
        },
        config: {
          configurable: {
            model_name: 'gpt-4o'
          }
        },
        stream_mode: "values",
        stream: true
      }

      console.log('Creating run with payload:', JSON.stringify(runPayload, null, 2))
      
      const runResponse = await fetch(`${this.baseUrl}/threads/${actualThreadId}/runs/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify(runPayload)
      })

      console.log(`Run response status: ${runResponse.status}`)
      
      if (runResponse.ok) {
        console.log('Success with LangGraph thread/run API')
        return runResponse
      } else {
        const errorText = await runResponse.text()
        console.log('Run failed:', errorText)
        throw new Error(`Run failed: ${runResponse.status} ${runResponse.statusText}`)
      }

    } catch (error) {
      console.log('Thread/run approach failed, trying direct assistant invoke:', error)
      
      // Fallback to direct assistant invocation
      const payload: LangGraphRequest = {
        input: {
          messages
        },
        config: {
          configurable: {
            model_name: 'gpt-4o',
            thread_id: threadId
          }
        },
        stream: true
      }

      // Try different possible endpoint formats with corrected payload
      const possibleEndpoints = [
        `${this.baseUrl}/assistants/${this.assistantId}/invoke`,
        `${this.baseUrl}/threads/invoke`, 
        `${this.baseUrl}/invoke`,
        `${this.baseUrl}/runs/stream`
      ]

      let lastError: Error | null = null

      for (const endpoint of possibleEndpoints) {
        try {
          console.log(`Trying endpoint: ${endpoint}`)
          console.log('Payload:', JSON.stringify(payload, null, 2))
          
          const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'text/event-stream',
              'Authorization': `Bearer ${accessToken}`,
            },
            body: JSON.stringify(payload)
          })

          console.log(`Response status: ${response.status}`)
          
          if (response.ok) {
            console.log(`Success with endpoint: ${endpoint}`)
            return response
          } else {
            const errorText = await response.text()
            console.log(`Failed with endpoint: ${endpoint}, status: ${response.status}, error: ${errorText}`)
            
            if (response.status === 422) {
              // Try simplified payload for 422 errors
              const simplifiedPayload = {
                messages: messages.map(msg => ({
                  role: msg.role,
                  content: msg.content
                })),
                stream: true
              }
              
              console.log(`Trying simplified payload for ${endpoint}:`, JSON.stringify(simplifiedPayload, null, 2))
              
              const retryResponse = await fetch(endpoint, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'text/event-stream',
                  'Authorization': `Bearer ${accessToken}`,
                },
                body: JSON.stringify(simplifiedPayload)
              })
              
              if (retryResponse.ok) {
                console.log(`Success with simplified payload for endpoint: ${endpoint}`)
                return retryResponse
              }
            }
            
            if (response.status !== 404) {
              // If it's not a 404, this might be the right endpoint with a different error
              throw new Error(`API request failed: ${response.status} ${response.statusText}`)
            }
          }
        } catch (error) {
          console.log(`Error with endpoint: ${endpoint}`, error)
          lastError = error as Error
          continue
        }
      }

      // If all endpoints failed, throw the last error
      throw new Error(`All API endpoints failed. Last error: ${lastError?.message || 'Unknown error'}`)
    }
  }

  async *streamResponse(response: Response): AsyncGenerator<string, void, unknown> {
    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('Response body is not readable')
    }

    try {
      let buffer = ''
      let currentEvent = ''
      let lastCompleteResponse = ''
      
      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break
        
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        
        // Keep the last incomplete line in buffer
        buffer = lines.pop() || ''
        
        for (const line of lines) {
          if (line.trim() === '') continue
          
          console.log('🔍 Raw SSE line:', line)
          
          if (line.startsWith('event: ')) {
            currentEvent = line.slice(7).trim()
            console.log('📋 Current event type:', currentEvent)
          } else if (line.startsWith('data: ')) {
            const data = line.slice(6).trim()
            
            if (data === '[DONE]') {
              console.log('✅ Stream finished with [DONE]')
              return
            }
            
            try {
              const parsed = JSON.parse(data)
              console.log('🔍 Parsed SSE data:', parsed)
              console.log('🔍 Current event:', currentEvent)
              
              // Handle different event types from LangGraph
              if (currentEvent === 'values') {
                console.log('📦 Values event detected')
                if (parsed.messages && Array.isArray(parsed.messages)) {
                  const messages = parsed.messages
                  console.log('📦 Found messages array with length:', messages.length)
                  
                  // Find the last assistant message
                  for (let i = messages.length - 1; i >= 0; i--) {
                    const message = messages[i]
                    if (message && (message.type === 'ai' || message.role === 'assistant') && message.content) {
                      const content = message.content.trim()
                      
                      // Only yield if this is a significantly different response
                      if (content && content.length > 10) { // Only process substantial responses
                        if (content !== lastCompleteResponse) {
                          console.log('✅ New complete assistant response:', content)
                          lastCompleteResponse = content
                          // Yield a special marker to indicate this should replace previous content
                          yield `__REPLACE__${content}`
                        } else {
                          console.log('🔄 Same response, skipping')
                        }
                      }
                      break // Only process the last assistant message
                    }
                  }
                }
              } else if (currentEvent === 'metadata') {
                console.log('📦 Metadata event (skipping)')
                // Skip metadata events
                continue
              }
              // Remove other event handlers since we only want the final values
            } catch (e) {
              console.warn('⚠️ Failed to parse SSE data:', data, e)
            }
          } else {
            console.log('❓ Non-data SSE line:', line)
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  }

  private extractAnyContent(data: any): string | null {
    // Recursively try to find any content field
    if (typeof data === 'string') {
      return data
    }
    
    if (Array.isArray(data)) {
      for (const item of data) {
        const content = this.extractAnyContent(item)
        if (content) return content
      }
    }
    
    if (typeof data === 'object' && data !== null) {
      // Check common content fields
      if (data.content && typeof data.content === 'string') {
        return data.content
      }
      if (data.text && typeof data.text === 'string') {
        return data.text
      }
      if (data.message && typeof data.message === 'string') {
        return data.message
      }
      
      // Recursively check all properties
      for (const key in data) {
        const content = this.extractAnyContent(data[key])
        if (content) return content
      }
    }
    
    return null
  }
}

// Export a singleton instance
export const langGraphAPI = new LangGraphAPI() 