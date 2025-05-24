// // hooks/useAuthStore.ts
// import { create } from 'zustand'

// type User = {
//   username: string
//   user_id: string
// }

// type AuthStore = {
//   user: User | null
//   session_id: string | null
//   setUser: (user: User) => void
//   setSessionId: (sessionId: string) => void
// }

// export const useAuthStore = create<AuthStore>((set) => ({
//   user: null,
//   session_id: null,
//   setUser: (user) => {
//     set({ user })
//     localStorage.setItem('user', JSON.stringify(user))
//   },
//   setSessionId: (sessionId) => set({ session_id: sessionId }),
// }))
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type User = {
  username: string
  user_id: string
}

type AuthState = {
  user: User | null
  login: (user: User) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      login: (user) => set({ user }),
      logout: () => set({ user: null }),
    }),
    {
      name: 'auth-store', // localStorage key
      partialize: (state) => ({ user: state.user }), // only persist the user
    }
  )
)
