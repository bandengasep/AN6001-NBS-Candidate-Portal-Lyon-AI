import { Link, useNavigate } from 'react-router-dom';

/**
 * Results view showing matched programmes with text rationale.
 * @param {Object} props
 * @param {Array} props.matches - Matched programmes from API
 * @param {Function} props.onRetake - Restart the quiz
 */
export function Results({ matches, onRetake }) {
  const navigate = useNavigate();

  function handleAskLyon(match) {
    navigate(`/chat?programme=${encodeURIComponent(match.name)}`);
  }

  return (
    <div>
      <h2 className="text-xl font-bold text-ntu-dark mb-2">Your Programme Recommendations</h2>
      <p className="text-sm text-ntu-muted mb-8">
        Based on your answers, here are the NBS programmes that best fit your profile.
      </p>

      {/* Matches */}
      {matches.length > 0 ? (
        <div className="space-y-5">
          {matches.map((match, i) => (
            <div key={match.program_id} className="border border-ntu-border rounded-lg overflow-hidden">
              <div className="p-6">
                <div className="mb-3">
                  <span className="text-xs font-semibold text-ntu-red uppercase tracking-wider">
                    Recommended {matches.length > 1 ? `#${i + 1}` : ''}
                  </span>
                  <h3 className="text-lg font-bold text-ntu-dark mt-1">{match.name}</h3>
                  <span className="text-xs text-ntu-muted">{match.degree_type}</span>
                </div>

                {match.rationale && (
                  <p className="text-sm text-ntu-body leading-relaxed mb-4">
                    {match.rationale}
                  </p>
                )}

                <div className="flex gap-3 pt-2">
                  {match.url && (
                    <a href={match.url} target="_blank" rel="noopener noreferrer"
                       className="px-4 py-2 text-xs border border-ntu-blue text-ntu-blue rounded hover:bg-ntu-blue/[0.04] transition-colors">
                      Visit NBS Page
                    </a>
                  )}
                  <button onClick={() => handleAskLyon(match)}
                          className="px-4 py-2 text-xs bg-ntu-red text-white rounded hover:bg-ntu-red-hover transition-colors">
                    Ask Lyon About This
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-ntu-muted">
          <p>No matches found. Try adjusting your answers.</p>
        </div>
      )}

      <div className="mt-8 flex gap-4">
        <button onClick={onRetake}
                className="px-5 py-2.5 text-sm border border-ntu-border text-ntu-body rounded hover:border-ntu-red hover:text-ntu-red transition-colors">
          Retake Quiz
        </button>
        <Link to="/programmes"
              className="px-5 py-2.5 text-sm text-ntu-red font-medium hover:underline">
          Browse All Programmes
        </Link>
      </div>
    </div>
  );
}
