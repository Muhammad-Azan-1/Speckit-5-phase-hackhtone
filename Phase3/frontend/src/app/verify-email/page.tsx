'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { authClient } from '@/lib/auth-client';
import { toast } from 'sonner';
import { Toaster } from '@/components/ui/sonner';
import { Mail, CheckCircle, RefreshCw } from 'lucide-react';

const COOLDOWN_SECONDS = 30;
const COOLDOWN_STORAGE_KEY = 'verify-email-cooldown-end';

function VerifyEmailContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const email = searchParams.get('email') || '';

    const [cooldown, setCooldown] = useState(0);
    const [isResending, setIsResending] = useState(false);

    // Initialize cooldown from localStorage on mount
    useEffect(() => {
        const storedEndTime = localStorage.getItem(COOLDOWN_STORAGE_KEY);
        if (storedEndTime) {
            const endTime = parseInt(storedEndTime, 10);
            const remaining = Math.ceil((endTime - Date.now()) / 1000);
            if (remaining > 0) {
                setCooldown(remaining);
            } else {
                localStorage.removeItem(COOLDOWN_STORAGE_KEY);
            }
        }
    }, []);

    // Countdown timer
    useEffect(() => {
        if (cooldown <= 0) return;

        const timer = setInterval(() => {
            setCooldown((prev) => {
                if (prev <= 1) {
                    localStorage.removeItem(COOLDOWN_STORAGE_KEY);
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);

        return () => clearInterval(timer);
    }, [cooldown]);

    const handleResendEmail = async () => {
        if (!email || cooldown > 0) return;

        setIsResending(true);

        try {
            await authClient.sendVerificationEmail({
                email,
                callbackURL: '/login',
            });

            // Set cooldown
            const endTime = Date.now() + COOLDOWN_SECONDS * 1000;
            localStorage.setItem(COOLDOWN_STORAGE_KEY, endTime.toString());
            setCooldown(COOLDOWN_SECONDS);

            toast.success('Verification email sent!', {
                description: 'Check your inbox for the verification link.',
            });
        } catch (error: any) {
            console.error('Failed to resend email:', error);
            toast.error('Failed to send email', {
                description: error.message || 'Please try again later.',
            });
        } finally {
            setIsResending(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl">
                {/* Icon */}
                <div className="flex justify-center">
                    <div className="w-20 h-20 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
                        <Mail className="w-10 h-10 text-gray-600 dark:text-gray-300" />
                    </div>
                </div>

                {/* Title */}
                <div className="text-center">
                    <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                        Check your email
                    </h1>
                    <p className="mt-2 text-gray-600 dark:text-gray-400">
                        We&apos;ve sent a verification link to
                    </p>
                    {email && (
                        <p className="mt-1 font-semibold text-gray-900 dark:text-white">
                            {email}
                        </p>
                    )}
                </div>

                {/* Instructions */}
                <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 space-y-2">
                    <div className="flex items-start gap-3">
                        <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                            Click the link in the email to verify your account
                        </p>
                    </div>
                    <div className="flex items-start gap-3">
                        <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                            After verification, you&apos;ll be redirected to login
                        </p>
                    </div>
                </div>

                {/* Resend Button */}
                <div className="space-y-4">
                    <Button
                        onClick={handleResendEmail}
                        disabled={cooldown > 0 || isResending || !email}
                        className="w-full h-12 rounded-lg text-base font-semibold"
                        variant={cooldown > 0 ? "outline" : "default"}
                    >
                        {isResending ? (
                            <span className="flex items-center gap-2">
                                <RefreshCw className="w-4 h-4 animate-spin" />
                                Sending...
                            </span>
                        ) : cooldown > 0 ? (
                            `Resend in ${cooldown}s`
                        ) : (
                            <span className="flex items-center gap-2">
                                <RefreshCw className="w-4 h-4" />
                                Resend verification email
                            </span>
                        )}
                    </Button>

                    <div className="text-center">
                        <Link
                            href="/login"
                            className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
                        >
                            Already verified?{' '}
                            <span className="font-semibold underline">Sign in</span>
                        </Link>
                    </div>
                </div>
            </div>
            <Toaster position="top-right" />
        </div>
    );
}

export default function VerifyEmailPage() {
    return (
        <Suspense fallback={<div className="min-h-screen flex items-center justify-center">Loading...</div>}>
            <VerifyEmailContent />
        </Suspense>
    );
}
