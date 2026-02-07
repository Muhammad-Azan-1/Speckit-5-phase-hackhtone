'use client'

import Header from '@/components/layout/header'
import { Sidebar } from '@/components/layout/sidebar'
import { useAuth } from '@/hooks/use-auth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { Loader2 } from 'lucide-react'

export default function ChatLayout({
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
        return null
    }

    return (
        <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
            {/* Desktop Sidebar */}
            <aside className="hidden lg:flex w-64 flex-col border-r bg-white dark:bg-gray-950">
                <Sidebar className="px-4" />
            </aside>

            {/* Main Content */}
            <div className="flex flex-1 flex-col overflow-hidden">
                <Header />
                {/* Removed padding (p-6) and overflow-y-auto to let page handle it */}
                <main className="flex-1 overflow-hidden">
                    {children}
                </main>
            </div>
        </div>
    )
}