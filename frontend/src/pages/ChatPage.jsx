import { TopBar } from '../components/Layout/TopBar';
import { PortalHeader } from '../components/Layout/PortalHeader';
import { Sidebar } from '../components/Layout/Sidebar';
import { ChatContainer } from '../components/Chat/ChatContainer';
import { useChat } from '../hooks/useChat';
import { useSearchParams } from 'react-router-dom';
import { useEffect } from 'react';

export default function ChatPage() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get('programme');
  const {
    messages, isLoading, error, messagesEndRef, sendMessage, clearChat,
  } = useChat();

  // If navigated from recommendation with a programme, auto-send a message
  useEffect(() => {
    if (programme && messages.length <= 1) {
      sendMessage(`Tell me more about the ${programme} programme`);
    }
  }, [programme]);

  return (
    <div className="h-screen flex flex-col bg-white">
      <TopBar />
      <PortalHeader />
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
