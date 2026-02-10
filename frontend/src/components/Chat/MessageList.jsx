import { MessageBubble } from './MessageBubble';
import { HandoffCard } from './HandoffCard';
import { LoadingDots } from './LoadingDots';

export function MessageList({ messages, isLoading, messagesEndRef, conversationId }) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-1">
      {messages.map((message, index) => {
        // Check if this is a consecutive message from the same role
        const prevMessage = messages[index - 1];
        const isConsecutive = prevMessage && prevMessage.role === message.role;

        // Render hand-off card for handoff messages
        if (message.role === 'handoff') {
          return (
            <div key={message.id} className="mt-3">
              <HandoffCard conversationId={conversationId} />
            </div>
          );
        }

        return (
          <div key={message.id} className={isConsecutive ? 'mt-0.5' : 'mt-3'}>
            <MessageBubble
              message={message}
              hideAvatar={isConsecutive}
            />
          </div>
        );
      })}

      {isLoading && (
        <div className="flex justify-start mt-3 mb-4">
          <div className="flex max-w-[85%] lg:max-w-[75%]">
            <div className="flex-shrink-0 mr-3">
              <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                <div className="animate-pulse">
                  <div className="w-4 h-4 bg-gray-300 rounded-full"></div>
                </div>
              </div>
            </div>
            <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
              <LoadingDots />
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}

export default MessageList;
