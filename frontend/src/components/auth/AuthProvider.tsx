'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { getCurrentUser, signIn, signUp, signOut, supabase, User, AuthState } from '@/lib/auth'

interface AuthContextType extends AuthState {
  signIn: (email: string, password: string) => Promise<{ user: User | null, error?: string }>
  signUp: (email: string, password: string) => Promise<{ user: User | null, error?: string }>
  signOut: () => Promise<{ error?: string }>
  clearError: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    loading: true,
    error: undefined
  })

  // Initialize auth state
  useEffect(() => {
    async function getInitialSession() {
      try {
        const user = await getCurrentUser()
        setAuthState({
          user,
          loading: false,
          error: undefined
        })
      } catch (error) {
        console.error('Error getting initial session:', error)
        setAuthState({
          user: null,
          loading: false,
          error: 'Failed to initialize authentication'
        })
      }
    }

    getInitialSession()

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        if (event === 'SIGNED_IN' && session) {
          setAuthState({
            user: {
              id: session.user.id,
              email: session.user.email,
              access_token: session.access_token
            },
            loading: false,
            error: undefined
          })
        } else if (event === 'SIGNED_OUT') {
          setAuthState({
            user: null,
            loading: false,
            error: undefined
          })
        }
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const handleSignIn = async (email: string, password: string) => {
    setAuthState(prev => ({ ...prev, loading: true, error: undefined }))
    
    const result = await signIn(email, password)
    
    if (result.error) {
      setAuthState(prev => ({ 
        ...prev, 
        loading: false, 
        error: result.error 
      }))
    } else {
      setAuthState({
        user: result.user,
        loading: false,
        error: undefined
      })
    }
    
    return result
  }

  const handleSignUp = async (email: string, password: string) => {
    setAuthState(prev => ({ ...prev, loading: true, error: undefined }))
    
    const result = await signUp(email, password)
    
    if (result.error) {
      setAuthState(prev => ({ 
        ...prev, 
        loading: false, 
        error: result.error 
      }))
    } else {
      setAuthState({
        user: result.user,
        loading: false,
        error: undefined
      })
    }
    
    return result
  }

  const handleSignOut = async () => {
    setAuthState(prev => ({ ...prev, loading: true }))
    
    const result = await signOut()
    
    setAuthState({
      user: null,
      loading: false,
      error: result.error
    })
    
    return result
  }

  const clearError = () => {
    setAuthState(prev => ({ ...prev, error: undefined }))
  }

  const value: AuthContextType = {
    ...authState,
    signIn: handleSignIn,
    signUp: handleSignUp,
    signOut: handleSignOut,
    clearError
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
} 