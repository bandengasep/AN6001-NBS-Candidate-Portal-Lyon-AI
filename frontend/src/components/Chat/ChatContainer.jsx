import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';

export function ChatContainer({
  messages,
  isLoading,
  error,
  messagesEndRef,
  onSendMessage,
  onClearChat,
}) {
  return (
    <div className="flex flex-col h-full bg-white">
      {/* Error banner */}
      {error && (
        <div className="bg-red-50 border-b border-red-200 px-4 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Messages area */}
      <MessageList
        messages={messages}
        isLoading={isLoading}
        messagesEndRef={messagesEndRef}
      />

      {/* Input area */}
      <ChatInput
        onSend={onSendMessage}
        onClear={onClearChat}
        isLoading={isLoading}
      />
    </div>
  );
}

export default ChatContainer;
