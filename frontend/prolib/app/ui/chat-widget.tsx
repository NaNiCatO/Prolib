"use client"
import React, { useEffect, useRef, useState } from 'react';
import { MessageSquare, X, Send, GripVertical } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

interface Message {
    content: string;
    isUser: boolean;
    timestamp: Date;
}

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState<Message[]>([
        {
            content: 'Hello, How can I assist you?',
            isUser: false,
            timestamp: new Date(),
        },
    ]);

    // Size state with defaults
    const [size, setSize] = useState({ width: 320, height: 400 });
    const [isResizing, setIsResizing] = useState(false);

    // Refs
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const chatRef = useRef<HTMLDivElement>(null);
    const resizeStartPos = useRef({ x: 0, y: 0 });
    const initialSize = useRef({ width: 0, height: 0 });

    // Size constraints
    const MIN_WIDTH = 280;
    const MAX_WIDTH = 500;
    const MIN_HEIGHT = 300;
    const MAX_HEIGHT = 600;

    // Auto-scroll to bottom when messages change
    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    // Handle resize events
    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => {
            if (!isResizing) return;

            // For top-left resizing, dragging left/up increases size
            const deltaX = resizeStartPos.current.x - e.clientX;
            const deltaY = resizeStartPos.current.y - e.clientY;

            const newWidth = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, initialSize.current.width + deltaX));
            const newHeight = Math.min(MAX_HEIGHT, Math.max(MIN_HEIGHT, initialSize.current.height + deltaY));

            setSize({ width: newWidth, height: newHeight });
        };

        const handleMouseUp = () => {
            setIsResizing(false);
        };

        if (isResizing) {
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
        }

        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, [isResizing]);

    const startResize = (e: React.MouseEvent) => {
        e.preventDefault();
        setIsResizing(true);
        resizeStartPos.current = { x: e.clientX, y: e.clientY };

        if (chatRef.current) {
            initialSize.current = {
                width: chatRef.current.offsetWidth,
                height: chatRef.current.offsetHeight
            };
        }
    };

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const handleSendMessage = (e: React.FormEvent) => {
        e.preventDefault();

        if (!message.trim()) return;

        // Add user message
        const newMessages = [
            ...messages,
            {
                content: message,
                isUser: true,
                timestamp: new Date(),
            },
        ];

        setMessages(newMessages);
        setMessage('');

        // Simulate bot response (in a real app, you'd call your Prolog backend here)
        

        setTimeout(() => {
            setMessages(prevMessages => [
                ...prevMessages,
                {
                    content: "I'm processing your request. How can I help with your book search?",
                    isUser: false,
                    timestamp: new Date(),
                },
            ]);
        }, 500);
    };

    return (
        <div className="fixed bottom-4 right-4 z-50">
            {isOpen ? (
                <Card
                    ref={chatRef}
                    className="shadow-lg relative"
                    style={{
                        width: `${size.width}px`,
                        height: `${size.height}px`
                    }}
                >
                    {/* Resize handle in top-left corner */}
                    <div
                        className="absolute left-0 top-0 cursor-nwse-resize w-6 h-6 flex items-center justify-center z-10"
                        onMouseDown={startResize}
                    >
                        <GripVertical className="h-4 w-4 text-gray-400" />
                    </div>

                    <CardHeader className="p-4 border-b bg-primary/10 gap-0">
                        <div className="flex justify-between items-center">
                            <CardTitle className="text-base font-medium">AI Chat Helper</CardTitle>
                            <Button variant="ghost" size="icon" onClick={toggleChat} className="h-8 w-8">
                                <X className="h-4 w-4" />
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent className="p-0 flex flex-col" style={{ height: `calc(100% - 65px)` }}>
                        <div className="grow overflow-y-auto overflow-x-hidden p-4 space-y-4">
                            {messages.map((msg, index) => (
                                <div
                                    key={index}
                                    className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div
                                        className={`max-w-xs p-3 rounded-lg ${msg.isUser
                                            ? 'bg-primary text-primary-foreground ml-12'
                                            : 'bg-muted mr-12'
                                            } break-words overflow-hidden`}
                                    >
                                        {msg.content}
                                    </div>
                                </div>
                            ))}
                            {/* Invisible element at the bottom for scrolling reference */}
                            <div ref={messagesEndRef} />
                        </div>
                        <form onSubmit={handleSendMessage} className="border-t p-2 flex gap-2 mt-auto">
                            <Input
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                placeholder="Type your message here.."
                                className="flex-1"
                            />
                            <Button type="submit" size="icon" variant="ghost">
                                <Send className="h-4 w-4" />
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            ) : (
                <Button
                    onClick={toggleChat}
                    className="rounded-full h-12 w-12 shadow-lg flex items-center justify-center"
                >
                    <MessageSquare className="h-6 w-6" />
                </Button>
            )}
        </div>
    );
};