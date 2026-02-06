import { MessageBubble } from './MessageBubble';
import { LoadingDots } from './LoadingDots';

export function MessageList({ messages, isLoading, messagesEndRef }) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-2">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {isLoading && (
        <div className="flex justify-start mb-4">
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
