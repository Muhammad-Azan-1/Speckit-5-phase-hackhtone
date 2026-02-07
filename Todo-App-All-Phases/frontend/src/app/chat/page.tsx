"use client";

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { useTaskMutations } from '@/hooks/use-tasks';
import { useConversations, useMessages } from '@/hooks/use-chat';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Bot, Send, User as UserIcon, MoreVertical, Trash2, Pencil, Loader2 } from 'lucide-react';

import { Message, Conversation } from '@/types/chat';

export default function ChatPage() {
  const { conversations, mutate: mutateConversations } = useConversations();
  const [selectedConversation, setSelectedConversation] = useState<number | null>(null);
  const [inputMessage, setInputMessage] = useState('');

  // Use SWR for messages
  // Use SWR for messages
  const { messages, isLoading: isMessagesLoading, mutate: mutateMessages } = useMessages(selectedConversation);

  // Local state for optimistic updates only (if needed) or just use SWR data
  // We'll sync SWR data to local state if we want to keep the existing structure, 
  // OR strictly use SWR data. 
  // Given the existing code heavily uses `messages` state (e.g. for optimistic updates),
  // let's try to align `messages` with `swrMessages` but allow local optimistic appends.

  // Actually, mixing them is tricky. Let's rely on SWR for the source of truth,
  // and handle optimistic updates via mutate.

  // For this refactor, let's keep it simple: 
  // SWR handles fetching. We won't maintain a separate `messages` state for FETCHED data,
  // but we might need a way to show optimistic messages.

  // Let's keep `messages` state compliant with the existing render logic?
  // No, checking the verifying steps, "Every time I visit... load every time".
  // The fix is SWR.

  const [isLoading, setIsLoading] = useState(false); // Can likely remove in favor of isMessagesLoading
  const [isSending, setIsSending] = useState(false);
  const [editingConversation, setEditingConversation] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const { user, isAuthenticated } = useAuth();
  const { refreshAll, createTask, updateTask, deleteTask, updateTaskCompletion } = useTaskMutations();
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Sync SWR messages with local state if we want to preserve the optimistic logic structure easily
  // Or better, just use swrMessages directly in render? 
  // The existing `sendMessage` pushes to `messages` state.
  // If we switch to correct SWR usage, `sendMessage` should `mutate` the cache.

  // Let's use `messages` for rendering, and update it when SWR data arrives.
  // This is a "sync" pattern. 


  useEffect(() => {
    setIsLoading(isMessagesLoading);
  }, [isMessagesLoading]);

  // Scroll to bottom whenever messages change or user is typing

  // Scroll to bottom whenever messages change or user is typing
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isSending]);

  // Remove manual fetch effects
  // useEffect(() => { if (isAuthenticated && user) fetchConversations(); }, ...);
  // useEffect(() => { if (selectedConversation) fetchMessages(...); }, ...);


  const createConversation = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/conversations`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (response.ok) {
        const newConversation = await response.json();
        // Optimistic update
        mutateConversations([newConversation, ...conversations], false);
        setSelectedConversation(newConversation.id);

        // Clear messages for new convo
        // Note: swrMessages is tied to selectedConversation. Changing selectedConversation changes the key.
        // So we don't need to clear messages manually for the NEW key, it triggers a fetch (or empty cache).
        // But we should reset our local 'messages' state which we sync.
        // But we should reset our local 'messages' state which we sync.
        mutateMessages([], false);

        // Final revalidate
        mutateConversations();
      } else {
        console.error('Failed to create conversation');
      }
    } catch (error) {
      console.error('Error creating conversation:', error);
    }
  };

  const deleteConversation = async (conversationId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/conversations/${conversationId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        mutateConversations(conversations.filter((c: any) => c.id !== conversationId), false);
        if (selectedConversation === conversationId) {
          setSelectedConversation(null);
          mutateMessages([], false);
        }
        mutateConversations();
      } else {
        console.error('Failed to delete conversation');
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const renameConversation = async (conversationId: number) => {
    if (!editTitle.trim()) {
      setEditingConversation(null);
      return;
    }
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/conversations/${conversationId}`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ summary: editTitle }),
      });

      if (response.ok) {
        mutateConversations(conversations.map((c: any) => c.id === conversationId ? { ...c, summary: editTitle } : c), false);
        mutateConversations();
      }
    } catch (error) {
      console.error('Error renaming conversation:', error);
    } finally {
      setEditingConversation(null);
      setEditTitle('');
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isSending) return;

    setIsSending(true);

    // Optimistically add user message to UI
    const tempUserMessage: Message = {
      id: Date.now(),
      conversation_id: selectedConversation || 0,
      user_id: user?.id || '',
      role: 'user',
      content: inputMessage,
      summary: null,
      created_at: new Date().toISOString()
    };

    // Update local state directly for instant feedback (since we sync 'messages' from SWR but also want instant UI)
    // We update 'messages' state directly, and when SWR revalidates, it will update 'swrMessages' which updates 'messages'.
    // setMessages(prev => [...prev, tempUserMessage]);

    // Also mutate SWR cache optimistically
    // Also mutate SWR cache optimistically
    if (messages) {
      mutateMessages([...messages, tempUserMessage], false);
    }

    const messageToSend = inputMessage;
    setInputMessage('');

    try {
      // Use the AI chat endpoint for processing
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageToSend,
          conversation_id: selectedConversation
        }),
      });

      if (response.ok) {
        const data = await response.json();

        // If no conversation was selected, set the new one
        if (!selectedConversation && data.conversation_id) {
          setSelectedConversation(data.conversation_id);
          mutateConversations(); // Fetch new convo list
        }

        // Add AI response to messages
        const aiMessage: Message = {
          id: Date.now() + 1,
          conversation_id: data.conversation_id,
          user_id: user?.id || '',
          role: 'assistant',
          content: data.response,
          summary: null,
          created_at: new Date().toISOString()
        };

        // setMessages(prev => [...prev, aiMessage]);

        // Mutate SWR
        if (messages) {
          mutateMessages([...messages, tempUserMessage, aiMessage], false);
        } else {
          mutateMessages([tempUserMessage, aiMessage], false);
        }
        // Invalidate to get real IDs etc
        mutateMessages();

        // Check for tool calls and refresh data if needed
        if (data.tool_calls && data.tool_calls.length > 0) {
          const hasTaskUpdates = data.tool_calls.some((tool: any) =>
            ['add_task', 'update_task', 'complete_task', 'delete_task', 'add_category', 'delete_category'].includes(tool.name)
          );

          if (hasTaskUpdates) {
            if (hasTaskUpdates) {
              data.tool_calls.forEach((tool: any) => {
                console.log("Processing tool update:", tool.name, tool.output);

                if (tool.name === 'add_task' && tool.output && !tool.output.error) {
                  createTask(tool.output);
                } else if (tool.name === 'update_task' && tool.output && !tool.output.error) {
                  updateTask(tool.output);
                } else if (tool.name === 'complete_task' && tool.output && !tool.output.error) {
                  // The output has the new 'completed' status
                  updateTaskCompletion(tool.output.id, tool.output.completed);
                } else if (tool.name === 'delete_task' && tool.output && !tool.output.error) {
                  deleteTask(tool.output.task_id);
                }
              });

              // Still refresh everything to be safe, but UI should already be updated
              refreshAll();
            }
          }
        }
      } else {
        console.error('Failed to send message');
        if (messages) mutateMessages(messages.filter(m => m.id !== tempUserMessage.id), false);
        setInputMessage(messageToSend);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      if (messages) mutateMessages(messages.filter(m => m.id !== tempUserMessage.id), false);
      setInputMessage(messageToSend);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex h-full bg-background overflow-hidden">
      {/* Sidebar for conversations */}
      <div className="w-64 border-r flex flex-col overflow-hidden">
        <div className="p-4 border-b">
          <Button onClick={createConversation} className="w-full">
            New Chat
          </Button>
        </div>
        <ScrollArea className="flex-1 p-2">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              className={`group p-3 rounded-md mb-2 cursor-pointer hover:bg-accent flex items-center justify-between ${selectedConversation === conv.id ? 'bg-primary/10' : ''
                }`}
              onClick={() => setSelectedConversation(conv.id)}
            >
              <div className="flex-1 min-w-0">
                {editingConversation === conv.id ? (
                  <Input
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') renameConversation(conv.id);
                      if (e.key === 'Escape') setEditingConversation(null);
                    }}
                    onBlur={() => renameConversation(conv.id)}
                    onClick={(e) => e.stopPropagation()}
                    autoFocus
                    className="h-6 text-sm"
                  />
                ) : (
                  <>
                    <div className="font-medium truncate">
                      {conv.summary || `Chat ${conv.id}`}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {new Date(conv.created_at).toLocaleDateString()}
                    </div>
                  </>
                )}
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 opacity-0 group-hover:opacity-100"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditTitle(conv.summary || `Chat ${conv.id}`);
                      setEditingConversation(conv.id);
                    }}
                  >
                    <Pencil className="cursor-pointer h-4 w-4 mr-2" />
                    Rename
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    className="text-destructive"
                    onClick={(e) => deleteConversation(conv.id, e)}
                  >
                    <Trash2 className="cursor-pointer h-4 w-4 mr-2" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          ))}
        </ScrollArea>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {!selectedConversation ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8">
            <Bot className="h-16 w-16 text-muted-foreground mb-4" />
            <h2 className="text-2xl font-bold mb-2">Welcome to the AI Chat</h2>
            <p className="text-muted-foreground mb-6 text-center">
              Select an existing conversation or start a new one to begin chatting with the AI assistant.
            </p>
            <Button onClick={createConversation}>Start New Chat</Button>
          </div>
        ) : (
          <>
            {/* Messages area - takes available space and scrolls internally */}
            <div className="flex-1 overflow-hidden flex flex-col min-h-0">
              <div className="border-b p-4 shrink-0">
                <h1 className="text-xl font-bold">AI Chat Assistant</h1>
                <p className="text-sm text-muted-foreground">Ask anything and get intelligent responses</p>
              </div>

              <div className="flex-1 overflow-hidden p-4">
                <Card className="h-full border-0 shadow-none flex flex-col bg-transparent">
                  <CardContent className="p-0 flex-1 min-h-0">
                    <ScrollArea ref={scrollAreaRef} className="h-full pr-4">
                      {isLoading && messages.length === 0 ? (
                        <div className="flex items-center justify-center h-full">
                          <Loader2 className="h-6 w-6 animate-spin mr-2" />
                          <p>Loading messages...</p>
                        </div>
                      ) : messages.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-full text-center p-8">
                          <Bot className="h-12 w-12 text-muted-foreground mb-4" />
                          <h3 className="text-lg font-medium mb-2">Start a conversation</h3>
                          <p className="text-muted-foreground max-w-md">
                            Ask me anything! I can help with information, ideas, or just chat about your day.
                          </p>
                        </div>
                      ) : (
                        <div className="space-y-6 pb-4">
                          {messages.map((msg) => (
                            <div
                              key={msg.id}
                              className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end flex-row-reverse' : ''
                                }`}
                            >
                              {msg.role !== 'user' && (
                                <Avatar className="border">
                                  <AvatarFallback className="bg-primary/10">
                                    <Bot className="h-4 w-4 text-primary" />
                                  </AvatarFallback>
                                </Avatar>
                              )}
                              <div
                                className={`max-w-[70%] rounded-lg px-4 py-3 ${msg.role === 'user'
                                  ? 'bg-primary text-primary-foreground rounded-br-none'
                                  : 'bg-secondary rounded-bl-none'
                                  }`}
                              >
                                <div className="whitespace-pre-wrap">{msg.content}</div>
                                <div className="text-xs opacity-70 mt-2 flex justify-between">
                                  <span>
                                    {msg.role === 'user' ? 'You' : 'AI Assistant'}
                                  </span>
                                  <span>
                                    {new Date(msg.created_at).toLocaleTimeString([], {
                                      hour: '2-digit',
                                      minute: '2-digit',
                                    })}
                                  </span>
                                </div>
                              </div>
                              {msg.role === 'user' && (
                                <Avatar className="border">
                                  <AvatarFallback className="bg-secondary">
                                    <UserIcon className="h-4 w-4" />
                                  </AvatarFallback>
                                </Avatar>
                              )}
                            </div>
                          ))}
                          {/* Typing indicator when waiting for AI response */}
                          {isSending && (
                            <div className="flex items-start gap-3">
                              <Avatar className="border">
                                <AvatarFallback className="bg-primary/10">
                                  <Bot className="h-4 w-4 text-primary" />
                                </AvatarFallback>
                              </Avatar>
                              <div className="bg-secondary rounded-lg rounded-bl-none px-4 py-3">
                                <div className="flex items-center gap-1">
                                  <Loader2 className="h-4 w-4 animate-spin" />
                                  <span className="text-sm text-muted-foreground">AI is thinking...</span>
                                </div>
                              </div>
                            </div>
                          )}

                          <div ref={messagesEndRef} />
                        </div>
                      )}
                    </ScrollArea>
                  </CardContent>
                </Card>
              </div>
            </div>



            {/* Input area */}
            <div className="border-t p-4 pb-6 shrink-0 bg-background">
              <div className="flex gap-2">
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your message..."
                  disabled={isLoading}
                />
                <Button
                  onClick={sendMessage}
                  disabled={isSending || !inputMessage.trim()}
                >
                  {isSending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
              </div>
              <p className="text-xs text-muted-foreground text-center mt-2">
                AI-powered task assistant. Ask me to add, list, complete, delete, or update your tasks!
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}