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
    this.baseUrl = process.env.NEXT_PUBLIC_LANGGRAPH_API_URL || 'http://localhost:2024'
    this.assistantId = process.env.NEXT_PUBLIC_ASSISTANT_ID || 'default'
  }

  async sendMessage(userMessage: string, conversationHistory: LangGraphMessage[] = []): Promise<Response> {
    const messages = [
      ...conversationHistory,
      { role: 'user' as const, content: userMessage }
    ]

    const threadId = `thread_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`

    const requestBody = {
      input: {
        messages: messages
      },
      config: {
        configurable: {
          thread_id: threadId
        }
      },
      stream: true
    }

    console.log('🚀 Sending request to LangGraph API...')
    console.log('URL:', `${this.baseUrl}/runs/stream`)
    console.log('Request body:', JSON.stringify(requestBody, null, 2))

    try {
      const response = await fetch(`${this.baseUrl}/runs/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify(requestBody)
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('❌ API request failed:', response.status, errorText)
        throw new Error(`API request failed: ${response.status} ${response.statusText}`)
      }

      console.log('✅ API request successful, response ready for streaming')
      return response
    } catch (error) {
      console.error('❌ Network error:', error)
      throw error
    }
  }

  async *streamResponse(response: Response): AsyncGenerator<string, void, unknown> {
    if (!response.body) {
      throw new Error('No response body available for streaming')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let lastContent = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        
        if (done) {
          console.log('🏁 Stream completed')
          break
        }

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          const trimmedLine = line.trim()
          
          if (trimmedLine === '') continue
          if (trimmedLine === 'event: end') {
            console.log('📝 Received end event')
            return
          }
          if (!trimmedLine.startsWith('data: ')) continue

          try {
            const dataStr = trimmedLine.substring(6)
            if (dataStr === '[DONE]') {
              console.log('📝 Received [DONE] marker')
              return
            }

            const data = JSON.parse(dataStr)
            console.log('📦 Parsed SSE data:', data)

            if (data.event === 'on_chain_end' && data.name === 'LangGraph') {
              const outputData = data.data?.output
              if (outputData?.messages && Array.isArray(outputData.messages)) {
                const lastMessage = outputData.messages[outputData.messages.length - 1]
                if (lastMessage?.content && typeof lastMessage.content === 'string') {
                  const newContent = lastMessage.content

                  if (newContent !== lastContent) {
                    if (lastContent && newContent.startsWith(lastContent)) {
                      const incrementalContent = newContent.substring(lastContent.length)
                      if (incrementalContent) {
                        console.log('📄 Yielding incremental content:', incrementalContent)
                        yield incrementalContent
                      }
                    } else {
                      console.log('🔄 Content replaced, yielding replacement marker')
                      yield `__REPLACE__${newContent}`
                    }
                    lastContent = newContent
                  }
                }
              }
            }
          } catch (parseError) {
            console.warn('⚠️ Failed to parse SSE data:', parseError, 'Raw line:', trimmedLine)
            continue
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  }
}

export const langGraphAPI = new LangGraphAPI() 