import { useState, useEffect } from 'react';
import { getPrograms } from '../../services/api';
import { ProgramCard } from './ProgramCard';
import { Loader2 } from 'lucide-react';

export function ProgramList({ onAskAboutProgram }) {
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchPrograms() {
      try {
        const data = await getPrograms();
        setPrograms(data);
      } catch (err) {
        console.error('Error fetching programs:', err);
        setError('Failed to load programmes');
      } finally {
        setLoading(false);
      }
    }

    fetchPrograms();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
        <span className="ml-2 text-gray-500">Loading programmes...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-8 text-gray-500">
        {error}
      </div>
    );
  }

  if (programs.length === 0) {
    return (
      <div className="text-center p-8 text-gray-500">
        No programmes available
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {programs.map((program) => (
        <ProgramCard
          key={program.id || program.name}
          program={program}
          onClick={(name) => onAskAboutProgram(`Tell me about the ${name} programme at NBS`)}
        />
      ))}
    </div>
  );
}

export default ProgramList;
