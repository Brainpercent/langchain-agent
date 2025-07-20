'use client'

import React, { useState, KeyboardEvent, useRef, DragEvent, ClipboardEvent } from 'react'
import { PaperAirplaneIcon, PaperClipIcon, PhotoIcon, XMarkIcon } from '@heroicons/react/24/solid'
import { cn } from '../../lib/utils'

interface ChatInputProps {
  onSendMessage: (message: string, files?: File[]) => void
  disabled?: boolean
  placeholder?: string
}

interface UploadedFile {
  file: File
  preview?: string
  id: string
}

export function ChatInput({ 
  onSendMessage, 
  disabled = false,
  placeholder = "Ask me anything... You can also paste or upload files for analysis." 
}: ChatInputProps) {
  const [input, setInput] = useState('')
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = () => {
    const trimmedInput = input.trim()
    if ((trimmedInput || uploadedFiles.length > 0) && !disabled) {
      const files = uploadedFiles.map(uf => uf.file)
      let messageContent = trimmedInput
      
      // Add file info to message if files are attached
      if (uploadedFiles.length > 0) {
        const fileList = uploadedFiles.map(uf => `📎 ${uf.file.name} (${(uf.file.size / 1024).toFixed(1)}KB)`).join('\n')
        messageContent = trimmedInput + (trimmedInput ? '\n\n' : '') + fileList
      }
      
      onSendMessage(messageContent, files)
      setInput('')
      setUploadedFiles([])
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleFileSelect = (files: FileList | null) => {
    if (!files) return
    
    const newFiles: UploadedFile[] = []
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      const id = Math.random().toString(36).substr(2, 9)
      
      const uploadedFile: UploadedFile = { file, id }
      
      // Create preview for images
      if (file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          uploadedFile.preview = e.target?.result as string
          setUploadedFiles(prev => prev.map(f => f.id === id ? uploadedFile : f))
        }
        reader.readAsDataURL(file)
      }
      
      newFiles.push(uploadedFile)
    }
    
    setUploadedFiles(prev => [...prev, ...newFiles])
  }

  const handlePaste = (e: ClipboardEvent<HTMLTextAreaElement>) => {
    const items = e.clipboardData?.items
    if (!items) return

    for (let i = 0; i < items.length; i++) {
      const item = items[i]
      
      if (item.type.indexOf('image') !== -1) {
        e.preventDefault()
        const file = item.getAsFile()
        if (file) {
          const fileList = { length: 1, item: () => file, 0: file } as unknown as FileList
          handleFileSelect(fileList)
        }
      }
    }
  }

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
    handleFileSelect(e.dataTransfer.files)
  }

  const removeFile = (id: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== id))
  }

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 128) + 'px'
    }
  }

  return (
    <div className="border-t border-gray-200 bg-white">
      {/* File Previews */}
      {uploadedFiles.length > 0 && (
        <div className="p-4 pb-0">
          <div className="flex flex-wrap gap-2">
            {uploadedFiles.map((uploadedFile) => (
              <div
                key={uploadedFile.id}
                className="relative bg-gray-50 border border-gray-200 rounded-lg p-3 pr-8 max-w-xs"
              >
                <button
                  onClick={() => removeFile(uploadedFile.id)}
                  className="absolute top-1 right-1 w-5 h-5 bg-gray-400 hover:bg-red-500 text-white rounded-full flex items-center justify-center text-xs"
                >
                  <XMarkIcon className="w-3 h-3" />
                </button>
                
                {uploadedFile.preview ? (
                  <div className="flex items-center gap-2">
                    <img 
                      src={uploadedFile.preview} 
                      alt="Preview" 
                      className="w-10 h-10 object-cover rounded"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {uploadedFile.file.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {(uploadedFile.file.size / 1024).toFixed(1)}KB
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <div className="w-10 h-10 bg-gray-200 rounded flex items-center justify-center">
                      <PaperClipIcon className="w-5 h-5 text-gray-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {uploadedFile.file.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {(uploadedFile.file.size / 1024).toFixed(1)}KB
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div 
        className={cn(
          "p-4 transition-colors duration-200",
          isDragging && "bg-blue-50 border-t-2 border-blue-500"
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isDragging && (
          <div className="absolute inset-0 bg-blue-50 bg-opacity-90 flex items-center justify-center z-10 border-2 border-dashed border-blue-500 rounded-lg m-2">
            <div className="text-center">
              <PhotoIcon className="w-12 h-12 text-blue-500 mx-auto mb-2" />
              <p className="text-blue-700 font-medium">Drop files here to analyze</p>
            </div>
          </div>
        )}

        <div className="flex gap-3 items-end">
          <div className="flex-1">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => {
                setInput(e.target.value)
                adjustTextareaHeight()
              }}
              onKeyDown={handleKeyDown}
              onPaste={handlePaste}
              placeholder={placeholder}
              disabled={disabled}
              rows={1}
              className={cn(
                'w-full resize-none rounded-lg border border-gray-300 px-3 py-2',
                'focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder-gray-500 text-gray-900',
                'disabled:bg-gray-100 disabled:cursor-not-allowed',
                'min-h-[44px] max-h-32 transition-all duration-200'
              )}
              style={{ 
                height: 'auto',
                minHeight: '44px'
              }}
            />
          </div>

          {/* File Upload Button */}
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled}
            className={cn(
              'flex-shrink-0 w-11 h-11 rounded-lg flex items-center justify-center',
              'bg-gray-100 hover:bg-gray-200 disabled:bg-gray-100',
              'transition-colors duration-200',
              'disabled:cursor-not-allowed text-gray-600'
            )}
            title="Upload file"
          >
            <PaperClipIcon className="w-5 h-5" />
          </button>
          
          {/* Send Button */}
          <button
            onClick={handleSubmit}
            disabled={disabled || (!input.trim() && uploadedFiles.length === 0)}
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
        
        <div className="mt-2 text-xs text-gray-500 flex justify-between">
          <span>Press Enter to send, Shift + Enter for new line</span>
          <span>Drag & drop or paste files to analyze</span>
        </div>

        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          className="hidden"
          onChange={(e) => handleFileSelect(e.target.files)}
          accept="image/*,.pdf,.doc,.docx,.txt,.csv,.json,.md"
        />
      </div>
    </div>
  )
} 