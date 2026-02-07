import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { loginSchema, type LoginFormData } from '@/lib/validations';
import { signIn } from '@/lib/auth-client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { toast } from 'sonner';
import { Eye, EyeOff } from 'lucide-react';

interface LoginFormProps {
  onSuccess?: () => void;
}

export function LoginForm({ onSuccess }: LoginFormProps) {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const isLoading = form.formState.isSubmitting;

  const onSubmit = async (data: LoginFormData) => {
    console.log(process.env.NEXT_PUBLIC_BETTER_AUTH_URL)
    try {
      // Call Better Auth login API
      const response = await signIn.email({
        email: data.email,
        password: data.password,
      });

      if (response.error) {
        // Check if error is due to unverified email
        if (response.error.status === 403 && response.error.message?.toLowerCase().includes('verify')) {
          toast.error('Email not verified', {
            description: 'Please verify your email address before logging in.',
          });
          router.push(`/verify-email?email=${encodeURIComponent(data.email)}`);
          return;
        }

        throw new Error(response.error.message || 'Login failed');
      }

      // Fetch JWT token for FastAPI requests (separate from session token)
      const { authClient } = await import('@/lib/auth-client');
      const tokenResponse = await authClient.token();

      if (tokenResponse.data?.token) {
        localStorage.setItem('auth-token', tokenResponse.data.token);
      }

      // Show success message
      toast.success('Login Successful!', {
        description: 'You have been logged in successfully!',
      });

      // Call success callback if provided
      if (onSuccess) {
        onSuccess();
      } else {
        // Redirect to dashboard or home page
        router.push('/');
      }
    } catch (error: any) {
      console.error('Login error:', error);

      // Show error message
      toast.error('Login Failed', {
        description: error.message || 'Invalid email or password',
      });
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem className="mb-4">
              <FormLabel className="text-gray-700 dark:text-gray-300">Email Address</FormLabel>
              <FormControl>
                <Input
                  className="h-10 rounded-lg dark:bg-gray-800 dark:text-white"
                  placeholder="Enter your email"
                  type="email"
                  {...field}
                  disabled={isLoading}
                />
              </FormControl>
              <FormMessage className="text-xs mt-1" />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem className="mb-6">
              <FormLabel className="text-gray-700 dark:text-gray-300">Password</FormLabel>
              <FormControl>
                <div className="relative">
                  <Input
                    className="h-10 rounded-lg dark:bg-gray-800 dark:text-white pr-10"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter your password"
                    {...field}
                    disabled={isLoading}
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="absolute right-0 top-0 h-10 w-10 px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                    disabled={isLoading}
                  >
                    {showPassword ? (
                      <Eye className="h-4 w-4 text-gray-500" />
                    ) : (
                      <EyeOff className="h-4 w-4 text-gray-500" />
                    )}
                    <span className="sr-only">
                      {showPassword ? 'Hide password' : 'Show password'}
                    </span>
                  </Button>
                </div>
              </FormControl>
              <FormMessage className="text-xs mt-1" />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          className="w-full h-10 rounded-lg text-base font-semibold transition-all duration-300 bg-gray-900 text-white hover:bg-gray-700 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200"
          disabled={isLoading}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing In...
            </span>
          ) : (
            'Sign In'
          )}
        </Button>
      </form>
    </Form>
  );
}