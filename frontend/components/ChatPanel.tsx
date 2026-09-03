'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';

interface Message {
  sender: 'user' | 'assistant';
  text: string;
  tools?: string[];
}

export const ChatPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputQuery, setInputQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: 'assistant',
      text: 'Hello! I am your Meridian Commercial Assistant. Ask me about SKU sales velocity drops, customer RFM cohorts, or request a campaign draft!',
    },
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputQuery.trim() || loading) return;

    const userMsg = inputQuery.trim();
    setInputQuery('');
    setMessages((prev) => [...prev, { sender: 'user', text: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: data.reply || 'Analysis complete.',
          tools: data.tool_calls_executed || [],
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: 'Assistant is temporarily unavailable, please try again.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-primary text-surface p-4 rounded-full shadow-2xl flex items-center space-x-2 border border-accent/40 hover:opacity-95 transition cursor-pointer"
        >
          <span className="text-xl">💬</span>
          <span className="font-display font-bold text-sm">Meridian Assistant</span>
        </button>
      ) : (
        <div className="bg-surface border border-border rounded-2xl w-96 md:w-[420px] shadow-2xl flex flex-col h-[520px]">
          {/* Drawer Header */}
          <div className="p-4 border-b border-border flex items-center justify-between bg-bg rounded-t-2xl">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-secondary text-surface flex items-center justify-center font-bold text-sm">
                M
              </div>
              <div>
                <div className="font-display font-bold text-sm text-primary">Meridian AI Assistant</div>
                <div className="text-[10px] font-mono text-muted">Function-Calling Tool Execution</div>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-muted hover:text-primary font-bold text-lg p-1 cursor-pointer"
            >
              ✕
            </button>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 p-4 overflow-y-auto space-y-4 text-xs font-sans">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[85%] p-3 rounded-xl leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-secondary text-surface font-medium'
                      : 'bg-bg text-primary border border-border'
                  }`}
                >
                  {msg.text}
                </div>

                {msg.tools && msg.tools.length > 0 && (
                  <div className="mt-1 flex items-center space-x-1">
                    <span className="text-[10px] text-muted font-mono">Tools Called:</span>
                    {msg.tools.map((t) => (
                      <Badge key={t} variant="accent">
                        {t}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="text-xs text-muted font-mono animate-pulse">
                Executing tool functions against Meridian analytics engine...
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSend} className="p-3 border-t border-border bg-surface rounded-b-2xl flex items-center space-x-2">
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder="Ask about sales drops, SKU trends, or campaign drafts..."
              className="flex-1 bg-bg border border-border rounded-xl px-3 py-2 text-xs font-sans focus:outline-none text-primary"
            />
            <Button variant="primary" size="sm" type="submit" disabled={loading}>
              Send
            </Button>
          </form>
        </div>
      )}
    </div>
  );
};
