/**
 * InputBar Component
 *
 * Message input area with send button
 */
import { useState, KeyboardEvent } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

interface InputBarProps {
  onSend: (message: string) => void;
  isSending: boolean;
  placeholder?: string;
  disabled?: boolean;
}

export const InputBar = ({
  onSend,
  isSending,
  placeholder = 'Ask me anything...',
  disabled = false,
}: InputBarProps) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim() || isSending || disabled) return;

    onSend(input.trim());
    setInput('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Send on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-border bg-card p-4">
      <div className="flex gap-3 items-end">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isSending || disabled}
          className="flex-1 min-h-[60px] max-h-[200px] resize-none rounded-2xl border-2 focus-visible:border-primary"
          rows={2}
        />
        <Button
          onClick={handleSend}
          disabled={!input.trim() || isSending || disabled}
          className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 rounded-2xl font-bold hover:shadow-xl transition-all h-[60px]"
        >
          {isSending ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Send className="h-5 w-5" />
          )}
        </Button>
      </div>

      <p className="text-xs text-muted-foreground mt-2">
        Press <kbd className="px-1.5 py-0.5 bg-secondary rounded text-xs">Enter</kbd> to send,{' '}
        <kbd className="px-1.5 py-0.5 bg-secondary rounded text-xs">Shift+Enter</kbd> for new
        line
      </p>
    </div>
  );
};

export default InputBar;
