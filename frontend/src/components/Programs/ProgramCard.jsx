import { Clock, ExternalLink, GraduationCap } from 'lucide-react';

export function ProgramCard({ program, onClick }) {
  const { name, degree_type, description, duration, url } = program;

  const degreeColors = {
    MBA: 'bg-red-100 text-red-800',
    EMBA: 'bg-purple-100 text-purple-800',
    Executive: 'bg-purple-100 text-purple-800',
    MSc: 'bg-blue-100 text-blue-800',
    Other: 'bg-gray-100 text-gray-800',
  };

  const colorClass = degreeColors[degree_type] || degreeColors.Other;

  return (
    <div className="bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow p-4">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          <GraduationCap className="h-5 w-5 text-gray-400" />
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${colorClass}`}>
            {degree_type}
          </span>
        </div>
        {url && (
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-nbs-red transition-colors"
            title="Visit programme page"
          >
            <ExternalLink className="h-4 w-4" />
          </a>
        )}
      </div>

      <h3 className="font-semibold text-gray-900 mb-2">{name}</h3>

      {description && (
        <p className="text-sm text-gray-600 mb-3 line-clamp-3">
          {description}
        </p>
      )}

      <div className="flex items-center justify-between">
        {duration && (
          <div className="flex items-center text-sm text-gray-500">
            <Clock className="h-4 w-4 mr-1" />
            {duration}
          </div>
        )}

        <button
          onClick={() => onClick(name)}
          className="text-sm text-nbs-red hover:text-nbs-red-dark font-medium"
        >
          Ask about this
        </button>
      </div>
    </div>
  );
}

export default ProgramCard;
