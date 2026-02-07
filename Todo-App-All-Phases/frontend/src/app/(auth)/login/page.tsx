'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { AuthCard } from '@/components/auth/auth-card';
import { LoginForm } from '@/components/forms/login-form';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';

export default function LoginPage() {
  const router = useRouter();

  const handleSuccess = () => {
    // Optionally redirect to a different page after successful login
    toast.success('Logged in successfully!');
    router.push('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 py-12 px-4 sm:px-6 lg:px-8">
      <AuthCard
        title="Welcome Back"
        description="Enter your email and password to access your account"
      >
        <LoginForm onSuccess={handleSuccess} />

        <div className="mt-6 text-center text-sm text-gray-600 dark:text-gray-300">
          Don't have an account?{' '}
          <Link href="/register" className="font-semibold text-gray-800 hover:text-gray-600 transition-colors relative group dark:text-gray-300 dark:hover:text-gray-200">
            Sign up
            <span className="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-gray-800 transition-all duration-300 group-hover:w-full dark:bg-gray-300"></span>
          </Link>
        </div>
      </AuthCard>
      <Toaster position="top-right" />
    </div>
  );
}