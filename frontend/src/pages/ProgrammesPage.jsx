import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { TopBar } from '../components/Layout/TopBar';
import { PortalHeader } from '../components/Layout/PortalHeader';
import { Footer } from '../components/Layout/Footer';
import { getPrograms } from '../services/api';

const FILTER_TABS = ['All', 'MBA', 'MSc', 'PhD', 'Executive'];

function getBannerColor(degreeType) {
  if (!degreeType) return 'bg-ntu-dark';
  const dt = degreeType.toLowerCase();
  if (dt.includes('mba') || dt.includes('executive')) return 'bg-ntu-red';
  if (dt.includes('msc') || dt.includes('master')) return 'bg-ntu-blue';
  return 'bg-ntu-dark';
}

function getTypeColor(degreeType) {
  if (!degreeType) return 'text-ntu-dark';
  const dt = degreeType.toLowerCase();
  if (dt.includes('mba') || dt.includes('executive')) return 'text-ntu-red';
  if (dt.includes('msc') || dt.includes('master')) return 'text-ntu-blue';
  return 'text-ntu-dark';
}

function matchesFilter(degreeType, filter) {
  if (filter === 'All') return true;
  if (!degreeType) return false;
  const dt = degreeType.toLowerCase();
  const f = filter.toLowerCase();
  return dt.includes(f);
}

export default function ProgrammesPage() {
  const [programs, setPrograms] = useState([]);
  const [activeFilter, setActiveFilter] = useState('All');

  useEffect(() => {
    getPrograms()
      .then((data) => setPrograms(Array.isArray(data) ? data : []))
      .catch(() => setPrograms([]));
  }, []);

  const filtered = programs.filter((p) => matchesFilter(p.degree_type, activeFilter));

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <TopBar />
      <PortalHeader />

      <main className="flex-1">
        <section className="max-w-[1200px] mx-auto px-8 py-12">
          <div className="mb-8 pb-4 border-b-2 border-ntu-red">
            <h1 className="text-2xl font-bold text-ntu-dark leading-tight">
              Graduate Programmes
              <span className="block text-sm font-normal text-ntu-muted mt-1">Explore our world-class business education offerings</span>
            </h1>
          </div>

          {/* Filter Tabs */}
          <div className="flex gap-2 mb-7 flex-wrap">
            {FILTER_TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveFilter(tab)}
                className={`px-4 py-1.5 rounded text-sm font-semibold border transition-all cursor-pointer ${
                  activeFilter === tab
                    ? 'bg-ntu-red text-white border-ntu-red'
                    : 'bg-white text-ntu-body border-ntu-border hover:border-ntu-red hover:text-ntu-red'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Programme Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filtered.map((prog) => (
              <div key={prog.id || prog.name} className="bg-white border border-ntu-border rounded-md overflow-hidden hover:shadow-lg hover:-translate-y-0.5 transition-all">
                <div className={`h-1.5 w-full ${getBannerColor(prog.degree_type)}`} />
                <div className="p-5">
                  <div className={`text-[0.7rem] font-semibold uppercase tracking-wider mb-1 ${getTypeColor(prog.degree_type)}`}>
                    {prog.degree_type}
                  </div>
                  <div className="text-[1.05rem] font-semibold text-ntu-dark leading-snug mb-3">{prog.name}</div>
                  <div className="flex gap-4 text-xs text-ntu-muted mb-4">
                    {prog.duration && (
                      <span className="flex items-center gap-1">
                        <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                        {prog.duration}
                      </span>
                    )}
                  </div>
                  <div className="flex gap-3">
                    {prog.url && (
                      <a href={prog.url} target="_blank" rel="noopener noreferrer"
                         className="text-xs text-ntu-blue hover:underline">Visit NBS Page</a>
                    )}
                    <Link to={`/chat?programme=${encodeURIComponent(prog.name)}`}
                          className="text-xs text-ntu-red hover:underline">Ask Lyon</Link>
                  </div>
                </div>
              </div>
            ))}
            {filtered.length === 0 && (
              <div className="col-span-3 text-center py-12 text-ntu-muted">
                {programs.length === 0 ? <p>Loading programmes...</p> : <p>No programmes match this filter.</p>}
              </div>
            )}
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
