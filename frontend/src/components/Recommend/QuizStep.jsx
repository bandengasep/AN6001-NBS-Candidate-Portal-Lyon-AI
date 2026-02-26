/**
 * Branching quiz flow for programme recommendations.
 *
 * Step 1: Work experience → determines track
 * Step 2: Track-specific question → narrows programmes
 */

const EXPERIENCE_OPTIONS = [
  { label: '0-2 years (or fresh graduate)', value: 'junior', track: 'masters' },
  { label: '3-5 years', value: 'mid', track: 'both' },
  { label: '6+ years', value: 'senior', track: 'mba' },
];

const MBA_OPTIONS = [
  {
    label: 'Full-time intensive career switch',
    value: 'full-time-career-switch',
    programmes: ['Nanyang MBA'],
  },
  {
    label: 'Full-time with elite global network',
    value: 'full-time-elite',
    programmes: ['Nanyang Fellows MBA'],
  },
  {
    label: 'Part-time while working',
    value: 'part-time',
    programmes: ['Nanyang Professional MBA', 'Nanyang Executive MBA'],
  },
  {
    label: 'Senior leadership, part-time',
    value: 'senior-leadership',
    programmes: ['Nanyang Executive MBA'],
  },
];

const MASTERS_OPTIONS = [
  {
    label: 'Data, analytics, or AI',
    value: 'data-analytics',
    programmes: ['MSc Business Analytics', 'MSc Financial Engineering'],
  },
  {
    label: 'Finance or investments',
    value: 'finance',
    programmes: ['MSc Finance', 'MSc Financial Engineering', 'MSc Actuarial and Risk Analytics'],
  },
  {
    label: 'Accounting or audit',
    value: 'accounting',
    programmes: ['MSc Accountancy'],
  },
  {
    label: 'Marketing or branding',
    value: 'marketing',
    programmes: ['MSc Marketing Science'],
  },
  {
    label: 'General management or broad business foundation',
    value: 'general-management',
    programmes: ['Master in Management', 'MSc Marketing Science'],
  },
];

/**
 * Get the appropriate Step 2 options based on the user's track.
 */
function getStep2Options(track) {
  if (track === 'mba') return { question: 'What type of MBA programme are you looking for?', options: MBA_OPTIONS };
  if (track === 'masters') return { question: 'Which area interests you most?', options: MASTERS_OPTIONS };
  // 'both' — show all options
  return {
    question: 'Which direction interests you more?',
    options: [
      { label: 'MBA — leadership, strategy, career transformation', value: 'track-mba', track: 'mba' },
      { label: 'Specialized Masters — deep expertise in a specific field', value: 'track-masters', track: 'masters' },
    ],
  };
}

/**
 * Resolve the final matched programme names from the quiz answers.
 */
export function resolveMatches(answers) {
  const { experience, trackChoice, mbaChoice, mastersChoice } = answers;
  const exp = EXPERIENCE_OPTIONS.find((o) => o.value === experience);
  if (!exp) return [];

  let track = exp.track;
  if (track === 'both' && trackChoice) {
    const choice = getStep2Options('both').options.find((o) => o.value === trackChoice);
    track = choice?.track || 'masters';
  }

  if (track === 'mba') {
    const choice = MBA_OPTIONS.find((o) => o.value === mbaChoice);
    return choice?.programmes || [];
  }

  const choice = MASTERS_OPTIONS.find((o) => o.value === mastersChoice);
  return choice?.programmes || [];
}

/**
 * Branching quiz component.
 * @param {Object} props
 * @param {Object} props.answers - Current answers: { experience, trackChoice, mbaChoice, mastersChoice }
 * @param {Function} props.onAnswer - Called with (key, value)
 * @param {Function} props.onBack - Go back
 * @param {Function} props.onNext - Go forward / submit
 * @param {number} props.step - Current step (1, 2, or 3 for track-both sub-step)
 */
export function QuizStep({ answers, onAnswer, onBack, onNext, step }) {
  // Step 1: Work experience
  if (step === 1) {
    return (
      <QuizQuestion
        stepLabel="Step 1 of 2"
        progress={50}
        question="How many years of work experience do you have?"
        options={EXPERIENCE_OPTIONS}
        selectedValue={answers.experience}
        onSelect={(value) => onAnswer('experience', value)}
        onBack={onBack}
        onNext={onNext}
        canProceed={!!answers.experience}
        nextLabel="Next"
      />
    );
  }

  // Determine track from experience
  const exp = EXPERIENCE_OPTIONS.find((o) => o.value === answers.experience);
  const track = exp?.track || 'masters';

  // Step 2a: If track is 'both', ask which direction first
  if (step === 2 && track === 'both' && !answers.trackChoice) {
    const { question, options } = getStep2Options('both');
    return (
      <QuizQuestion
        stepLabel="Step 2a of 2"
        progress={66}
        question={question}
        options={options}
        selectedValue={answers.trackChoice}
        onSelect={(value) => onAnswer('trackChoice', value)}
        onBack={onBack}
        onNext={onNext}
        canProceed={!!answers.trackChoice}
        nextLabel="Next"
      />
    );
  }

  // Resolve effective track
  let effectiveTrack = track;
  if (track === 'both' && answers.trackChoice) {
    const choice = getStep2Options('both').options.find((o) => o.value === answers.trackChoice);
    effectiveTrack = choice?.track || 'masters';
  }

  // Step 2 (or 2b): Track-specific question
  if (effectiveTrack === 'mba') {
    return (
      <QuizQuestion
        stepLabel="Step 2 of 2"
        progress={100}
        question="What type of MBA programme are you looking for?"
        options={MBA_OPTIONS}
        selectedValue={answers.mbaChoice}
        onSelect={(value) => onAnswer('mbaChoice', value)}
        onBack={onBack}
        onNext={onNext}
        canProceed={!!answers.mbaChoice}
        nextLabel="See Results"
      />
    );
  }

  return (
    <QuizQuestion
      stepLabel="Step 2 of 2"
      progress={100}
      question="Which area interests you most?"
      options={MASTERS_OPTIONS}
      selectedValue={answers.mastersChoice}
      onSelect={(value) => onAnswer('mastersChoice', value)}
      onBack={onBack}
      onNext={onNext}
      canProceed={!!answers.mastersChoice}
      nextLabel="See Results"
    />
  );
}

/**
 * Reusable question UI with radio options.
 */
function QuizQuestion({ stepLabel, progress, question, options, selectedValue, onSelect, onBack, onNext, canProceed, nextLabel }) {
  return (
    <div>
      {/* Progress bar */}
      <div className="mb-6">
        <div className="flex justify-between text-xs text-ntu-muted mb-2">
          <span>{stepLabel}</span>
          <span>{progress}%</span>
        </div>
        <div className="w-full h-1.5 bg-ntu-border rounded-full">
          <div
            className="h-full bg-ntu-red rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <h2 className="text-lg font-bold text-ntu-dark mb-5">{question}</h2>

      <div className="space-y-2.5 mb-8">
        {options.map((opt) => (
          <label
            key={opt.value}
            className={`block border rounded-lg p-4 cursor-pointer transition-all ${
              selectedValue === opt.value
                ? 'border-ntu-red bg-ntu-red/[0.04]'
                : 'border-ntu-border hover:border-ntu-red/40'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                selectedValue === opt.value ? 'border-ntu-red' : 'border-ntu-border'
              }`}>
                {selectedValue === opt.value && (
                  <div className="w-2 h-2 rounded-full bg-ntu-red" />
                )}
              </div>
              <input
                type="radio"
                name={question}
                value={opt.value}
                checked={selectedValue === opt.value}
                onChange={() => onSelect(opt.value)}
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
          disabled={!canProceed}
          className={`px-6 py-2 text-sm font-semibold rounded transition-colors ${
            canProceed
              ? 'bg-ntu-red text-white hover:bg-ntu-red-hover'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
        >
          {nextLabel}
        </button>
      </div>
    </div>
  );
}

export default QuizStep;
