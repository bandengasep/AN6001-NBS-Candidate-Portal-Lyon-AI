import { Link } from 'react-router-dom';
import { SpiderChart } from '../Charts/SpiderChart';

/**
 * Results view showing user profile spider chart and top 3 programme matches.
 * @param {Object} props
 * @param {Object} props.userScores - User's quiz answers as scores
 * @param {Array} props.matches - Top 3 matched programmes from API
 * @param {Function} props.onRetake - Restart the quiz
 */
export function Results({ userScores, matches, onRetake }) {
  return (
    <div>
      <h2 className="text-xl font-bold text-ntu-dark mb-2">Your Programme Recommendations</h2>
      <p className="text-sm text-ntu-muted mb-8">
        Based on your profile, here are the NBS programmes that best match your background and goals.
      </p>

      {/* User profile chart */}
      <div className="bg-white border border-ntu-border rounded-lg p-6 mb-8">
        <h3 className="text-sm font-semibold text-ntu-dark mb-4">Your Profile</h3>
        <div className="max-w-[400px] mx-auto">
          <SpiderChart userScores={userScores} />
        </div>
      </div>

      {/* Matches */}
      {matches.length > 0 ? (
        <div className="space-y-6">
          {matches.map((match, i) => (
            <div key={match.program_id} className="bg-white border border-ntu-border rounded-lg overflow-hidden">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <span className="text-xs font-semibold text-ntu-muted uppercase tracking-wider">
                      #{i + 1} Match
                    </span>
                    <h3 className="text-lg font-bold text-ntu-dark">{match.name}</h3>
                    <span className="text-xs text-ntu-muted">{match.degree_type}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-ntu-red">{Math.round(match.similarity * 100)}%</div>
                    <div className="text-xs text-ntu-muted">match</div>
                  </div>
                </div>

                {/* Overlay chart */}
                <div className="max-w-[350px] mx-auto mb-4">
                  <SpiderChart
                    userScores={userScores}
                    programmeOverlays={[{ name: match.name, scores: match.profile_scores }]}
                  />
                </div>

                <div className="flex gap-3 pt-2">
                  {match.url && (
                    <a href={match.url} target="_blank" rel="noopener noreferrer"
                       className="px-4 py-2 text-xs border border-ntu-blue text-ntu-blue rounded hover:bg-ntu-blue/[0.04] transition-colors">
                      Visit NBS Page
                    </a>
                  )}
                  <Link to={`/chat?programme=${encodeURIComponent(match.name)}`}
                        className="px-4 py-2 text-xs bg-ntu-red text-white rounded hover:bg-ntu-red-hover transition-colors">
                    Ask Lyon About This
                  </Link>
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
