const QUIZ_STEPS = [
  {
    axis: 'quantitative',
    question: 'How would you describe your quantitative and analytical skills?',
    options: [
      { label: 'Limited - I prefer qualitative work', value: 1 },
      { label: 'Moderate - I can work with data when needed', value: 3 },
      { label: 'Strong - I enjoy statistics, modelling, and data analysis', value: 4 },
      { label: 'Expert - I have a STEM background or work with data daily', value: 5 },
    ],
  },
  {
    axis: 'experience',
    question: 'How many years of professional work experience do you have?',
    options: [
      { label: 'Fresh graduate or less than 1 year', value: 1 },
      { label: '1-3 years', value: 2 },
      { label: '3-6 years', value: 3 },
      { label: '6-10 years', value: 4 },
      { label: 'More than 10 years', value: 5 },
    ],
  },
  {
    axis: 'leadership',
    question: 'What best describes your leadership or management experience?',
    options: [
      { label: 'No formal leadership roles yet', value: 1 },
      { label: 'Team lead or project lead experience', value: 3 },
      { label: 'Manager overseeing a team or department', value: 4 },
      { label: 'Senior executive or director level', value: 5 },
    ],
  },
  {
    axis: 'tech_analytics',
    question: 'How interested are you in technology, data science, or AI?',
    options: [
      { label: 'Not really my thing', value: 1 },
      { label: 'Somewhat interested', value: 2 },
      { label: 'Very interested - I want to use it in my career', value: 4 },
      { label: 'It is my career - I work in tech/analytics', value: 5 },
    ],
  },
  {
    axis: 'business_domain',
    question: 'Which business area interests you most?',
    options: [
      { label: 'General management and strategy', value: 1 },
      { label: 'Marketing, branding, or consumer insights', value: 2 },
      { label: 'Finance, accounting, or investment', value: 3 },
      { label: 'Data analytics, technology, or operations', value: 4 },
      { label: 'Research or academia', value: 5 },
    ],
  },
  {
    axis: 'career_ambition',
    question: 'What is your primary goal for pursuing a graduate degree?',
    options: [
      { label: 'Explore my options and learn new skills', value: 1 },
      { label: 'Advance in my current field', value: 2 },
      { label: 'Switch to a new career or industry', value: 3 },
      { label: 'Move into senior leadership', value: 4 },
      { label: 'Pursue academic research or a PhD', value: 5 },
    ],
  },
  {
    axis: 'study_flexibility',
    question: 'What is your preferred study mode?',
    options: [
      { label: 'Full-time intensive (12 months or less)', value: 1 },
      { label: 'Full-time standard pace', value: 2 },
      { label: 'Either full-time or part-time', value: 3 },
      { label: 'Part-time - I want to keep working', value: 4 },
    ],
  },
];

/**
 * Single quiz question with radio options.
 * @param {Object} props
 * @param {number} props.stepIndex - 0-based question index
 * @param {Object} props.answers - Current answers object
 * @param {Function} props.onAnswer - Called with (axis, value)
 * @param {Function} props.onBack - Go to previous step
 * @param {Function} props.onNext - Go to next step
 */
export function QuizStep({ stepIndex, answers, onAnswer, onBack, onNext }) {
  const step = QUIZ_STEPS[stepIndex];
  const selected = answers[step.axis];
  const totalSteps = QUIZ_STEPS.length;

  return (
    <div>
      {/* Progress bar */}
      <div className="mb-6">
        <div className="flex justify-between text-xs text-ntu-muted mb-2">
          <span>Question {stepIndex + 1} of {totalSteps}</span>
          <span>{Math.round(((stepIndex + 1) / totalSteps) * 100)}%</span>
        </div>
        <div className="w-full h-1.5 bg-ntu-border rounded-full">
          <div
            className="h-full bg-ntu-red rounded-full transition-all duration-300"
            style={{ width: `${((stepIndex + 1) / totalSteps) * 100}%` }}
          />
        </div>
      </div>

      <h2 className="text-lg font-bold text-ntu-dark mb-5">{step.question}</h2>

      <div className="space-y-2.5 mb-8">
        {step.options.map((opt) => (
          <label
            key={opt.value}
            className={`block border rounded-lg p-4 cursor-pointer transition-all ${
              selected === opt.value
                ? 'border-ntu-red bg-ntu-red/[0.04]'
                : 'border-ntu-border hover:border-ntu-red/40'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                selected === opt.value ? 'border-ntu-red' : 'border-ntu-border'
              }`}>
                {selected === opt.value && (
                  <div className="w-2 h-2 rounded-full bg-ntu-red" />
                )}
              </div>
              <input
                type="radio"
                name={step.axis}
                value={opt.value}
                checked={selected === opt.value}
                onChange={() => onAnswer(step.axis, opt.value)}
                className="sr-only"
              />
              <span className="text-sm text-ntu-body">{opt.label}</span>
            </div>
          </label>
        ))}
      </div>

      <div className="flex justify-between">
        <button
          onClick={onBack}
          className="px-5 py-2 text-sm text-ntu-body border border-ntu-border rounded hover:border-ntu-red hover:text-ntu-red transition-colors"
        >
          Back
        </button>
        <button
          onClick={onNext}
          disabled={selected === undefined}
          className={`px-6 py-2 text-sm font-semibold rounded transition-colors ${
            selected !== undefined
              ? 'bg-ntu-red text-white hover:bg-ntu-red-hover'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
        >
          {stepIndex === totalSteps - 1 ? 'See Results' : 'Next'}
        </button>
      </div>
    </div>
  );
}

export { QUIZ_STEPS };
