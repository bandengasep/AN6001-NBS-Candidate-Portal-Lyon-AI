import { Header } from '../components/Layout/Header';
import { Sidebar } from '../components/Layout/Sidebar';
import { ChatContainer } from '../components/Chat/ChatContainer';
import { useChat } from '../hooks/useChat';

export default function ChatPage() {
  const {
    messages,
    isLoading,
    error,
    messagesEndRef,
    sendMessage,
    clearChat,
  } = useChat();

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar onQuestionClick={sendMessage} />
        <main className="flex-1 flex flex-col">
          <ChatContainer
            messages={messages}
            isLoading={isLoading}
            error={error}
            messagesEndRef={messagesEndRef}
            onSendMessage={sendMessage}
            onClearChat={clearChat}
          />
        </main>
      </div>
    </div>
  );
}
