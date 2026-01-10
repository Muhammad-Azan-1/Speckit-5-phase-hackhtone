'use client'

import Header from './header'
import { Sidebar } from './sidebar'
import { Toaster } from '@/components/ui/sonner'

import { useAuth } from '@/hooks/use-auth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { Loader2 } from 'lucide-react'

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const { user, loading } = useAuth()
    const router = useRouter()

    useEffect(() => {
        if (!loading && !user) {
            router.push('/login')
        }
    }, [user, loading, router])

    if (loading && !user) {
        return (
            <div className="flex h-screen items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-gray-500" />
            </div>
        )
    }

    if (!user) {
        return null // Will redirect via useEffect
    }

    return (
        <>
            <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
                {/* Desktop Sidebar */}
                <aside className="hidden lg:flex w-64 flex-col border-r bg-white dark:bg-gray-950">
                    <Sidebar className="px-4" />
                </aside>

                {/* Main Content */}
                <div className="flex flex-1 flex-col overflow-hidden">
                    <Header />
                    <main className="flex-1 overflow-y-auto p-6">
                        {children}
                    </main>
                </div>
            </div>
            <Toaster position="top-right" richColors />
        </>
    )
}
