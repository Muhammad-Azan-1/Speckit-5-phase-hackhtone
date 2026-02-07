export interface Message {
    id: number;
    conversation_id: number;
    user_id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    summary: string | null;
    created_at: string;
}

export interface Conversation {
    id: number;
    user_id: string;
    summary: string | null;
    created_at: string;
    updated_at: string;
}
