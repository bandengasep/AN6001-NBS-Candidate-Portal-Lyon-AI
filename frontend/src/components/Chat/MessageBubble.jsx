import { User, Bot, AlertCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export function MessageBubble({ message }) {
  const { role, content, sources, timestamp } = message;

  const isUser = role === 'user';
  const isError = role === 'error';

  const formatTime = (ts) => {
    return new Date(ts).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      className={`flex message-enter ${
        isUser ? 'justify-end' : 'justify-start'
      } mb-4`}
    >
      <div
        className={`flex max-w-[85%] lg:max-w-[75%] ${
          isUser ? 'flex-row-reverse' : 'flex-row'
        }`}
      >
        {/* Avatar */}
        <div
          className={`flex-shrink-0 ${
            isUser ? 'ml-3' : 'mr-3'
          }`}
        >
          <div
            className={`w-8 h-8 rounded-full flex items-center justify-center ${
              isUser
                ? 'bg-nbs-red text-white'
                : isError
                ? 'bg-red-100 text-red-600'
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            {isUser ? (
              <User className="h-4 w-4" />
            ) : isError ? (
              <AlertCircle className="h-4 w-4" />
            ) : (
              <Bot className="h-4 w-4" />
            )}
          </div>
        </div>

        {/* Message content */}
        <div className="flex flex-col">
          <div
            className={`rounded-2xl px-4 py-3 ${
              isUser
                ? 'bg-nbs-red text-white rounded-br-md'
                : isError
                ? 'bg-red-50 text-red-800 border border-red-200 rounded-bl-md'
                : 'bg-gray-100 text-gray-800 rounded-bl-md'
            }`}
          >
            {isUser ? (
              <p className="text-sm whitespace-pre-wrap">{content}</p>
            ) : (
              <div className="text-sm markdown-content">
                <ReactMarkdown>{content}</ReactMarkdown>
              </div>
            )}
          </div>

          {/* Timestamp and sources */}
          <div
            className={`flex items-center mt-1 space-x-2 ${
              isUser ? 'justify-end' : 'justify-start'
            }`}
          >
            <span className="text-xs text-gray-400">
              {formatTime(timestamp)}
            </span>

            {sources && sources.length > 0 && (
              <span className="text-xs text-gray-400">
                | {sources.length} source{sources.length > 1 ? 's' : ''} used
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
