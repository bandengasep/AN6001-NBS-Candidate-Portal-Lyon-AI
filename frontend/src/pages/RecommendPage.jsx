import { useState } from 'react';
import { TopBar } from '../components/Layout/TopBar';
import { PortalHeader } from '../components/Layout/PortalHeader';
import { Footer } from '../components/Layout/Footer';
import { CVUpload } from '../components/Recommend/CVUpload';
import { QuizStep, QUIZ_STEPS } from '../components/Recommend/QuizStep';
import { Results } from '../components/Recommend/Results';
import { SpiderChart } from '../components/Charts/SpiderChart';
import { getRecommendations } from '../services/api';

// Map parsed CV fields to initial quiz answers
function cvToAnswers(cv) {
  const answers = {};

  // Quantitative
  if (cv.quantitative_background === 'Strong') answers.quantitative = 5;
  else if (cv.quantitative_background === 'Moderate') answers.quantitative = 3;
  else if (cv.quantitative_background === 'Limited') answers.quantitative = 1;

  // Experience
  const yrs = cv.years_experience ?? 0;
  if (yrs >= 10) answers.experience = 5;
  else if (yrs >= 6) answers.experience = 4;
  else if (yrs >= 3) answers.experience = 3;
  else if (yrs >= 1) answers.experience = 2;
  else answers.experience = 1;

  // Leadership
  if (cv.leadership_experience === 'Senior/Executive') answers.leadership = 5;
  else if (cv.leadership_experience === 'Mid-level/Manager') answers.leadership = 4;
  else answers.leadership = 1;

  return answers;
}

export default function RecommendPage() {
  // step: 0=CV upload, 1-7=quiz, 8=results
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [cvData, setCvData] = useState(null);
  const [matchResult, setMatchResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleCVParsed(parsed) {
    setCvData(parsed);
    setAnswers(cvToAnswers(parsed));
    setStep(1);
  }

  function handleSkipCV() {
    setStep(1);
  }

  function handleAnswer(axis, value) {
    setAnswers((prev) => ({ ...prev, [axis]: value }));
  }

  function handleQuizBack() {
    if (step === 1) {
      setStep(0);
    } else {
      setStep(step - 1);
    }
  }

  async function handleQuizNext() {
    if (step < QUIZ_STEPS.length) {
      setStep(step + 1);
    } else {
      // Submit for matching
      setIsLoading(true);
      setError(null);
      try {
        const payload = {
          ...answers,
          cv_text: cvData?.raw_text || null,
        };
        const result = await getRecommendations(payload);
        setMatchResult(result);
        setStep(QUIZ_STEPS.length + 1);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to get recommendations. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }
  }

  function handleRetake() {
    setStep(0);
    setAnswers({});
    setCvData(null);
    setMatchResult(null);
    setError(null);
  }

  const isResultsStep = step === QUIZ_STEPS.length + 1;
  const isQuizStep = step >= 1 && step <= QUIZ_STEPS.length;

  return (
    <div className="min-h-screen bg-[#F5F5F5] flex flex-col">
      <TopBar />
      <PortalHeader />

      <main className="flex-1 max-w-[1200px] mx-auto px-8 py-10 w-full">
        <div className={`grid gap-10 ${isResultsStep ? '' : 'lg:grid-cols-[1fr_380px]'}`}>
          {/* Left column: wizard steps */}
          <div className="bg-white rounded-lg border border-ntu-border p-8">
            {step === 0 && (
              <CVUpload onParsed={handleCVParsed} onSkip={handleSkipCV} />
            )}

            {isQuizStep && (
              <QuizStep
                stepIndex={step - 1}
                answers={answers}
                onAnswer={handleAnswer}
                onBack={handleQuizBack}
                onNext={handleQuizNext}
              />
            )}

            {isLoading && (
              <div className="text-center py-16">
                <div className="w-10 h-10 border-2 border-ntu-red border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                <p className="text-sm text-ntu-muted">Finding your best matches...</p>
              </div>
            )}

            {error && (
              <div className="text-center py-8">
                <p className="text-sm text-red-600 mb-4">{error}</p>
                <button onClick={handleQuizNext} className="text-sm text-ntu-red underline">Try again</button>
              </div>
            )}

            {isResultsStep && matchResult && (
              <Results
                userScores={matchResult.user_scores}
                matches={matchResult.matches}
                onRetake={handleRetake}
              />
            )}
          </div>

          {/* Right column: live spider chart (hidden on results page) */}
          {!isResultsStep && (
            <div className="hidden lg:block">
              <div className="bg-white rounded-lg border border-ntu-border p-6 sticky top-24">
                <h3 className="text-sm font-semibold text-ntu-dark mb-4">Your Profile</h3>
                <SpiderChart userScores={answers} />
                <p className="text-xs text-ntu-muted text-center mt-3">
                  {Object.keys(answers).length === 0
                    ? 'Answer quiz questions to build your profile'
                    : `${Object.keys(answers).length} of 7 axes filled`}
                </p>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
