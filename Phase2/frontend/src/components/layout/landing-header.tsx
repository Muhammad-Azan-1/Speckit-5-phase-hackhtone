'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
    Sheet,
    SheetContent,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { useSession, signOut } from '@/lib/auth-client';
import { cn } from '@/lib/utils';
import { LayoutDashboard, LogOut, Menu } from 'lucide-react';
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/components/ui/alert-dialog';

export function LandingHeader() {
    const { data: session } = useSession();
    const router = useRouter();
    const [scrolled, setScrolled] = useState(false);
    const [showLogoutDialog, setShowLogoutDialog] = useState(false);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            const isScrolled = window.scrollY > 20;
            setScrolled(isScrolled);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const handleLogout = async () => {
        await signOut();
        router.refresh();
        setIsOpen(false);
    };

    return (
        <header
            className={cn(
                "fixed top-0 left-0 right-0 z-50 transition-all duration-300 mx-auto px-6 py-4 flex items-center justify-between",
                scrolled
                    ? "bg-white/70 dark:bg-black/70 backdrop-blur-md shadow-sm border-b border-gray-200/50 dark:border-gray-800/50 max-w-full"
                    : "bg-transparent max-w-5xl mt-4 rounded-full"
            )}
        >
            <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 flex items-center justify-center text-white dark:text-gray-900 font-bold text-lg">
                    T
                </div>
                <span className="font-bold text-xl text-gray-900 dark:text-white tracking-tight">
                    TodoApp
                </span>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden sm:flex items-center gap-4">
                {session ? (
                    <>
                        <Button
                            variant="ghost"
                            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                            onClick={() => setShowLogoutDialog(true)}
                        >
                            <LogOut className="mr-2 h-4 w-4" />
                            Log out
                        </Button>
                        <Link href="/dashboard">
                            <Button className="font-semibold bg-gray-900 text-white hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200 shadow-lg hover:shadow-xl transition-all duration-300">
                                <LayoutDashboard className="mr-2 h-4 w-4" />
                                Dashboard
                            </Button>
                        </Link>
                    </>
                ) : (
                    <>
                        <Link href="/login">
                            <Button variant="ghost" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white font-medium">
                                Log in
                            </Button>
                        </Link>
                        <Link href="/register">
                            <Button className="font-semibold bg-gray-900 text-white hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200 shadow-md hover:shadow-lg transition-all duration-300">
                                Sign up
                            </Button>
                        </Link>
                    </>
                )}
            </nav>

            {/* Mobile Menu */}
            <div className="sm:hidden">
                <Sheet open={isOpen} onOpenChange={setIsOpen}>
                    <SheetTrigger asChild>
                        <Button variant="ghost" size="icon">
                            <Menu className="h-6 w-6" />
                        </Button>
                    </SheetTrigger>
                    <SheetContent>
                        <SheetHeader>
                            <SheetTitle>Menu</SheetTitle>
                        </SheetHeader>
                        <div className="flex flex-col gap-4 mt-8">
                            {session ? (
                                <>
                                    <Link href="/dashboard" onClick={() => setIsOpen(false)}>
                                        <Button className="w-full font-semibold bg-gray-900 text-white hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200">
                                            <LayoutDashboard className="mr-2 h-4 w-4" />
                                            Dashboard
                                        </Button>
                                    </Link>
                                    <Button
                                        variant="outline"
                                        className="w-full"
                                        onClick={() => {
                                            setIsOpen(false);
                                            setShowLogoutDialog(true);
                                        }}
                                    >
                                        <LogOut className="mr-2 h-4 w-4" />
                                        Log out
                                    </Button>
                                </>
                            ) : (
                                <>
                                    <Link href="/login" onClick={() => setIsOpen(false)}>
                                        <Button variant="outline" className="w-full">
                                            Log in
                                        </Button>
                                    </Link>
                                    <Link href="/register" onClick={() => setIsOpen(false)}>
                                        <Button className="w-full font-semibold bg-gray-900 text-white hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200">
                                            Sign up
                                        </Button>
                                    </Link>
                                </>
                            )}
                        </div>
                    </SheetContent>
                </Sheet>
            </div>

            <AlertDialog open={showLogoutDialog} onOpenChange={setShowLogoutDialog}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you sure you want to log out?</AlertDialogTitle>
                        <AlertDialogDescription>
                            You will need to sign in again to access your tasks and settings.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction onClick={handleLogout}>
                            Log out
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </header>
    );
}
