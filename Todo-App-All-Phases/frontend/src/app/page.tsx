'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { useState, useEffect } from 'react';
import { ArrowRight, CheckCircle2, Sparkles, Bot } from 'lucide-react';
import { LandingHeader } from '@/components/layout/landing-header';

export default function Home() {
  const [text, setText] = useState('');
  const fullText = "Organize your work, amplify your productivity.";

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setText(fullText.slice(0, index));
      index++;
      if (index > fullText.length) clearInterval(interval);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-gray-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-800 flex flex-col items-center justify-center">
      <LandingHeader />
      <main className="max-w-4xl w-[100%] text-center space-y-6 md:space-y-8 animate-in fade-in zoom-in duration-500 pt-32 px-4 pb-12">
        {/* Animated Badge */}
        <div className="inline-flex items-center rounded-full border px-6 py-3 text-sm font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-primary text-primary-foreground hover:bg-primary/80 mb-4 cursor-pointer">
          Welcome to Todo App 🎉
        </div>

        {/* Hero Text */}
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-gray-900 dark:text-white min-h-[80px] md:min-h-[144px]">
          {text}
          <span className="animate-pulse">|</span>
        </h1>

        <p className="max-w-2xl mx-auto text-xl text-gray-600 dark:text-gray-300">
          The task management app designed for speed, simplicity, and getting things done.
          Manage projects, track tasks, and collaborate effortlessly.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8">
          <Link href="/login">
            <Button size="lg" className="h-12 px-8 text-lg bg-gray-900 text-white hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-100 shadow-lg hover:shadow-xl transition-all duration-300">
              Get Started <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
          <Link href="/about">
            <Button variant="outline" size="lg" className="h-12 px-8 text-lg border-gray-300 hover:bg-gray-100 dark:border-gray-700 dark:hover:bg-gray-800 transition-all duration-300">
              Learn More
            </Button>
          </Link>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 text-left">
          <div className="p-6 bg-white dark:bg-gray-900/50 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm hover:shadow-md transition-shadow">
            <CheckCircle2 className="h-10 w-10 text-green-500 mb-4" />
            <h3 className="text-lg font-bold mb-2">Smart Organization</h3>
            <p className="text-gray-600 dark:text-gray-400">Categorize tasks, set priorities, and filter with ease to focus on what matters.</p>
          </div>
          <div className="p-6 bg-white dark:bg-gray-900/50 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm hover:shadow-md transition-shadow">
            <div className="h-10 w-10 text-blue-500 mb-4 flex items-center justify-center text-2xl">🚀</div>
            <h3 className="text-lg font-bold mb-2">Boost Productivity</h3>
            <p className="text-gray-600 dark:text-gray-400">Streamlined workflow with quick actions, drag-and-drop, and keyboard shortcuts.</p>
          </div>
          <div className="p-6 bg-white dark:bg-gray-900/50 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm hover:shadow-md transition-shadow">
            <div className="h-10 w-10 text-purple-500 mb-4 flex items-center justify-center text-2xl">🔒</div>
            <h3 className="text-lg font-bold mb-2">Secure & Private</h3>
            <p className="text-gray-600 dark:text-gray-400">Your data is encrypted and secure. We value your privacy above all else.</p>
          </div>
        </div>

        {/* AI Assistant Section */}
        <div className="mt-24 w-full bg-gradient-to-r from-gray-900 to-gray-800 dark:from-gray-800 dark:to-gray-900 rounded-2xl p-8 md:p-12 text-white relative overflow-hidden group">
          <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-blue-500 rounded-full blur-3xl opacity-20 group-hover:opacity-30 transition-opacity"></div>
          <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-40 h-40 bg-purple-500 rounded-full blur-3xl opacity-20 group-hover:opacity-30 transition-opacity"></div>

          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="text-left space-y-4 max-w-xl">
              <div className="inline-flex items-center rounded-full bg-blue-500/10 border border-blue-500/20 px-3 py-1 text-sm text-blue-300 backdrop-blur-sm">
                <Sparkles className="h-4 w-4 mr-2 text-blue-400" />
                Coming Soon
              </div>
              <h2 className="text-3xl md:text-4xl font-bold">Meet Your AI Productivity Assistant</h2>
              <p className="text-gray-300 text-lg">
                Manage everything with just a chat. Ask our AI to create tasks, set reminders, and organize your day—like having a personal secretary.
              </p>
            </div>

            <div className="relative">
              <div className="w-24 h-24 bg-white/10 rounded-2xl flex items-center justify-center backdrop-blur-md border border-white/20 shadow-xl">
                <Bot className="h-12 w-12 text-white" />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
