import { TopBar } from '../components/Layout/TopBar';
import { PortalHeader } from '../components/Layout/PortalHeader';
import { Sidebar } from '../components/Layout/Sidebar';
import { ChatContainer } from '../components/Chat/ChatContainer';
import { useChat } from '../hooks/useChat';
import { useSearchParams } from 'react-router-dom';
import { useEffect, useRef } from 'react';

/**
 * Build a context-rich first message when user comes from the recommendation wizard.
 * This gives Lyon all the background it needs to give relevant advice.
 */
function buildRecommendMessage(programme, context) {
  if (!context) {
    return `Tell me more about the ${programme} programme`;
  }

  let msg = `I just completed the programme recommendation quiz and was matched to ${programme} with a ${context.matchScore}% match score.`;

  if (context.cvSummary) {
    const cv = context.cvSummary;
    const parts = [];
    if (cv.industry) parts.push(`I work in ${cv.industry}`);
    if (cv.yearsExperience) parts.push(`with ${cv.yearsExperience} years of experience`);
    if (cv.educationLevel) parts.push(`and hold a ${cv.educationLevel} degree`);
    if (parts.length > 0) {
      msg += ` Here's my background: ${parts.join(', ')}.`;
    }
    if (cv.skills && cv.skills.length > 0) {
      msg += ` My key skills include: ${cv.skills.join(', ')}.`;
    }
    if (cv.quantitativeBackground) {
      msg += ` My quantitative background is ${cv.quantitativeBackground.toLowerCase()}.`;
    }
    if (cv.leadershipExperience) {
      msg += ` Leadership level: ${cv.leadershipExperience.toLowerCase()}.`;
    }
  }

  msg += ` Does this programme fit my profile well? What should I know about it?`;

  return msg;
}

export default function ChatPage() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get('programme');
  const hasSentInitial = useRef(false);
  const {
    messages, isLoading, error, messagesEndRef, sendMessage, clearChat,
  } = useChat();

  // If navigated from recommendation with a programme, auto-send a context-rich message
  useEffect(() => {
    if (programme && messages.length <= 1 && !hasSentInitial.current) {
      hasSentInitial.current = true;

      // Check for recommendation context in sessionStorage
      let context = null;
      try {
        const stored = sessionStorage.getItem('recommendContext');
        if (stored) {
          context = JSON.parse(stored);
          sessionStorage.removeItem('recommendContext'); // One-time use
        }
      } catch (e) {
        // Ignore parse errors
      }

      sendMessage(buildRecommendMessage(programme, context));
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
