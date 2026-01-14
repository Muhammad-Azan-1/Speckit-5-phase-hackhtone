'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { LayoutDashboard, CheckSquare, Settings, Menu, Home, MessageCircle } from 'lucide-react'

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
    mobile?: boolean
    onClose?: () => void
}

export function Sidebar({ className, mobile, onClose }: SidebarProps) {
    const pathname = usePathname()

    const routes = [
        {
            label: 'Dashboard',
            icon: LayoutDashboard,
            href: '/dashboard',
            active: pathname === '/' || pathname === '/dashboard',
        },
        {
            label: 'Todos',
            icon: CheckSquare,
            href: '/todos',
            active: pathname === '/todos',
        },
        {
            label: 'Chat',
            icon: MessageCircle,
            href: '/chat',
            active: pathname === '/chat',
        },
        {
            label: 'Settings',
            icon: Settings,
            href: '/settings',
            active: pathname === '/settings',
        },
    ]

    return (
        <div className={cn("pb-12 h-screen relative", className)}>
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight text-gray-900 dark:text-white">
                        Todo App
                    </h2>
                    <div className="space-y-1">
                        {routes.map((route) => (
                            <Button
                                key={route.href}
                                variant={route.active ? "secondary" : "ghost"}
                                className={cn(
                                    "w-full justify-start text-base",
                                    route.active && "bg-gray-100 dark:bg-gray-800"
                                )}
                                asChild
                                onClick={() => mobile && onClose?.()}
                            >
                                <Link href={route.href}>
                                    <route.icon className="mr-2 h-5 w-5" />
                                    {route.label}
                                </Link>
                            </Button>
                        ))}
                    </div>
                </div>
                <Separator className="my-4" />
            </div>

            {/* Go to Home Button - Pushed to bottom */}
            <div className="absolute bottom-4 left-0 w-full px-3">
                <Button
                    variant="outline"
                    className="w-full justify-start text-base border-gray-200 dark:border-gray-800 text-gray-700 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-800 transition-colors"
                    asChild
                    onClick={() => mobile && onClose?.()}
                >
                    <Link href="/">
                        <Home className="mr-2 h-5 w-5" />
                        Go to Home
                    </Link>
                </Button>
            </div>
        </div>
    )
}
