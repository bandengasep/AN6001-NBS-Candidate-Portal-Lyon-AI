import { useState } from 'react';
import { TopBar } from '../components/Layout/TopBar';
import { PortalHeader } from '../components/Layout/PortalHeader';
import { Footer } from '../components/Layout/Footer';
import { CVUpload } from '../components/Recommend/CVUpload';
import { QuizStep, resolveMatches } from '../components/Recommend/QuizStep';
import { Results } from '../components/Recommend/Results';
import { getRecommendations } from '../services/api';

/**
 * Map parsed CV experience to quiz experience value.
 */
function cvToExperience(cv) {
  const yrs = cv.years_experience ?? 0;
  if (yrs >= 6) return 'senior';
  if (yrs >= 3) return 'mid';
  return 'junior';
}

export default function RecommendPage() {
  // phase: 'cv' | 'quiz' | 'loading' | 'results' | 'error'
  const [phase, setPhase] = useState('cv');
  const [answers, setAnswers] = useState({});
  const [cvData, setCvData] = useState(null);
  const [matchResult, setMatchResult] = useState(null);
  const [error, setError] = useState(null);
  // Quiz step: 1 = experience, 2 = track/interest, 3 = sub-track for 'both'
  const [quizStep, setQuizStep] = useState(1);

  function handleCVParsed(parsed) {
    setCvData(parsed);
    setAnswers({ experience: cvToExperience(parsed) });
    setQuizStep(1);
    setPhase('quiz');
  }

  function handleSkipCV() {
    setQuizStep(1);
    setPhase('quiz');
  }

  function handleAnswer(key, value) {
    setAnswers((prev) => ({ ...prev, [key]: value }));
  }

  function handleQuizBack() {
    if (quizStep === 1) {
      setPhase('cv');
    } else {
      // Clear the answer for the current step when going back
      if (quizStep === 2) {
        setAnswers((prev) => {
          const next = { ...prev };
          delete next.trackChoice;
          delete next.mbaChoice;
          delete next.mastersChoice;
          return next;
        });
      }
      setQuizStep(quizStep - 1);
    }
  }

  async function handleQuizNext() {
    // Determine if we need another step
    const exp = answers.experience;
    const track = exp === 'senior' ? 'mba' : exp === 'junior' ? 'masters' : 'both';

    if (quizStep === 1) {
      setQuizStep(2);
      return;
    }

    // Step 2: check if 'both' track needs a sub-step
    if (quizStep === 2 && track === 'both' && !answers.trackChoice) {
      // They just answered the track choice, move to step 3 (actual question)
      // This is handled by the QuizStep component internally
      // If trackChoice is selected, QuizStep shows the next question
      // But we need to re-render so just stay at step 2
      return;
    }

    // Check if we have a final answer
    const matched = resolveMatches(answers);
    if (matched.length > 0 || answers.mbaChoice || answers.mastersChoice) {
      // Submit for matching
      setPhase('loading');
      setError(null);
      try {
        const payload = {
          experience: answers.experience,
          track_choice: answers.trackChoice || null,
          mba_choice: answers.mbaChoice || null,
          masters_choice: answers.mastersChoice || null,
        };
        const result = await getRecommendations(payload);
        setMatchResult(result);
        setPhase('results');
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to get recommendations. Please try again.');
        setPhase('error');
      }
    }
  }

  function handleRetake() {
    setPhase('cv');
    setAnswers({});
    setCvData(null);
    setMatchResult(null);
    setError(null);
    setQuizStep(1);
  }

  return (
    <div className="min-h-screen bg-[#F5F5F5] flex flex-col">
      <TopBar />
      <PortalHeader />

      <main className="flex-1 max-w-[1200px] mx-auto px-8 py-10 w-full">
        <div className={`max-w-[680px] mx-auto`}>
          <div className="bg-white rounded-lg border border-ntu-border p-8">
            {phase === 'cv' && (
              <CVUpload onParsed={handleCVParsed} onSkip={handleSkipCV} />
            )}

            {phase === 'quiz' && (
              <QuizStep
                step={quizStep}
                answers={answers}
                onAnswer={handleAnswer}
                onBack={handleQuizBack}
                onNext={handleQuizNext}
              />
            )}

            {phase === 'loading' && (
              <div className="text-center py-16">
                <div className="w-10 h-10 border-2 border-ntu-red border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                <p className="text-sm text-ntu-muted">Finding your best matches...</p>
              </div>
            )}

            {phase === 'error' && (
              <div className="text-center py-8">
                <p className="text-sm text-red-600 mb-4">{error}</p>
                <button onClick={() => { setPhase('quiz'); }} className="text-sm text-ntu-red underline">Try again</button>
              </div>
            )}

            {phase === 'results' && matchResult && (
              <Results
                matches={matchResult.matches}
                onRetake={handleRetake}
              />
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
