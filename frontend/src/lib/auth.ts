import { createClient } from '@supabase/supabase-js'

// Configuration from environment variables
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export interface User {
  id: string
  email?: string
  access_token?: string
}

export interface AuthState {
  user: User | null
  loading: boolean
  error?: string
}

// Get current user session
export async function getCurrentUser(): Promise<User | null> {
  try {
    const { data: { session }, error } = await supabase.auth.getSession()
    
    if (error) {
      console.error('Error getting session:', error)
      return null
    }
    
    if (!session?.user) {
      return null
    }
    
    return {
      id: session.user.id,
      email: session.user.email,
      access_token: session.access_token
    }
  } catch (error) {
    console.error('Error in getCurrentUser:', error)
    return null
  }
}

// Sign in with email and password
export async function signIn(email: string, password: string): Promise<{ user: User | null, error?: string }> {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })
    
    if (error) {
      return { user: null, error: error.message }
    }
    
    if (!data.session?.user) {
      return { user: null, error: 'No user returned from sign in' }
    }
    
    return {
      user: {
        id: data.session.user.id,
        email: data.session.user.email,
        access_token: data.session.access_token
      }
    }
  } catch (error) {
    return { 
      user: null, 
      error: error instanceof Error ? error.message : 'Unknown error occurred'
    }
  }
}

// Sign up with email and password
export async function signUp(email: string, password: string): Promise<{ user: User | null, error?: string }> {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password
    })
    
    if (error) {
      return { user: null, error: error.message }
    }
    
    if (!data.session?.user) {
      return { user: null, error: 'Please check your email to confirm your account' }
    }
    
    return {
      user: {
        id: data.session.user.id,
        email: data.session.user.email,
        access_token: data.session.access_token
      }
    }
  } catch (error) {
    return { 
      user: null, 
      error: error instanceof Error ? error.message : 'Unknown error occurred'
    }
  }
}

// Sign out
export async function signOut(): Promise<{ error?: string }> {
  try {
    const { error } = await supabase.auth.signOut()
    
    if (error) {
      return { error: error.message }
    }
    
    return {}
  } catch (error) {
    return { 
      error: error instanceof Error ? error.message : 'Unknown error occurred'
    }
  }
}

// Get access token for API calls
export async function getAccessToken(): Promise<string | null> {
  try {
    const { data: { session } } = await supabase.auth.getSession()
    return session?.access_token || null
  } catch (error) {
    console.error('Error getting access token:', error)
    return null
  }
} 