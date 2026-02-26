import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { TopBar } from '../components/Layout/TopBar';
import { PortalHeader } from '../components/Layout/PortalHeader';
import { Footer } from '../components/Layout/Footer';
import { getPrograms } from '../services/api';

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

export default function SplashPage() {
  const [programs, setPrograms] = useState([]);

  useEffect(() => {
    getPrograms()
      .then((data) => setPrograms(Array.isArray(data) ? data.slice(0, 6) : []))
      .catch(() => setPrograms([]));
  }, []);

  return (
    <div className="min-h-screen bg-white">
      <TopBar />
      <PortalHeader />

      {/* Hero Section */}
      <section className="relative overflow-hidden" style={{ background: 'linear-gradient(135deg, #1a1a2e 0%, #2D2D2D 50%, #3a1520 100%)' }}>
        {/* Overlays */}
        <div className="absolute inset-0 pointer-events-none" style={{
          background: 'radial-gradient(ellipse at 80% 50%, rgba(224,25,50,0.15) 0%, transparent 50%), radial-gradient(ellipse at 20% 80%, rgba(0,113,188,0.08) 0%, transparent 40%)'
        }} />

        <div className="max-w-[1200px] mx-auto px-8 py-20 relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center min-h-[520px]">
          {/* Left: text */}
          <div>
            <h1 className="text-4xl lg:text-5xl font-bold text-white leading-tight mb-5 tracking-tight">
              Find the Right NBS<br />Graduate Degree <span className="text-ntu-gold">for You</span>
            </h1>
            <p className="text-white/65 text-lg leading-relaxed max-w-[480px] mb-8">
              Whether you're exploring options or ready to apply, we'll help you
              navigate NBS graduate programmes with AI-powered recommendations
              and personalised advice from Lyon, NTU's degree advisor.
            </p>
            <div className="flex gap-4 flex-wrap">
              <Link to="/recommend" className="inline-flex items-center gap-2 px-6 py-3 bg-ntu-red text-white rounded font-semibold text-sm hover:bg-ntu-red-hover transition-colors">
                <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
                </svg>
                Get Programme Recommendations
              </Link>
              <Link to="/chat" className="inline-flex items-center gap-2 px-6 py-3 border-2 border-white/40 text-white rounded font-semibold text-sm hover:border-white hover:bg-white/[0.08] transition-colors">
                <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                </svg>
                Chat with Lyon
              </Link>
            </div>
          </div>

          {/* Right: pathway cards */}
          <div className="flex flex-col gap-4">
            <Link to="/recommend" className="block relative bg-white/[0.06] backdrop-blur border border-ntu-red bg-[rgba(224,25,50,0.08)] rounded-lg p-6 hover:bg-[rgba(224,25,50,0.12)] transition-all hover:-translate-y-0.5">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-9 h-9 rounded-md bg-ntu-red flex items-center justify-center">
                  <svg className="w-[18px] h-[18px] text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/><path d="M9 15h6"/><path d="M9 11h6"/>
                  </svg>
                </div>
                <div>
                  <div className="text-[0.7rem] font-semibold uppercase tracking-wider text-white/60">Not sure yet?</div>
                  <div className="text-white font-semibold text-lg">Upload CV + Take Quiz</div>
                </div>
              </div>
              <div className="text-white/50 text-sm leading-relaxed">Get matched to NBS programmes based on your background, skills, and career goals.</div>
            </Link>

            <Link to="/chat" className="block relative bg-white/[0.06] backdrop-blur border border-white/10 rounded-lg p-6 hover:bg-white/10 hover:border-white/20 transition-all hover:-translate-y-0.5">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-9 h-9 rounded-md bg-white/10 flex items-center justify-center">
                  <svg className="w-[18px] h-[18px] text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                  </svg>
                </div>
                <div>
                  <div className="text-[0.7rem] font-semibold uppercase tracking-wider text-white/45">Already decided?</div>
                  <div className="text-white font-semibold text-lg">Ask Lyon Directly</div>
                </div>
              </div>
              <div className="text-white/50 text-sm leading-relaxed">Chat with NTU's AI degree advisor about specific programmes, admissions requirements, and campus life.</div>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <div className="bg-[#F5F5F5] border-b border-ntu-border">
        <div className="max-w-[1200px] mx-auto px-8 py-7 grid grid-cols-2 md:grid-cols-4 gap-8">
          {[
            { number: '11', label: 'Graduate Programmes' },
            { number: '#1', label: 'MBA in Singapore, #12 Globally (FT)' },
            { number: '100+', label: 'Nationalities Represented' },
            { number: 'AACSB & EQUIS', label: 'Internationally Accredited' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl font-bold text-ntu-red leading-none mb-1">{stat.number}</div>
              <div className="text-xs text-ntu-muted">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Programmes Section */}
      <section className="max-w-[1200px] mx-auto px-8 py-16">
        <div className="flex justify-between items-end mb-8 pb-4 border-b-2 border-ntu-red">
          <div>
            <h2 className="text-2xl font-bold text-ntu-dark leading-tight">
              Graduate Programmes
              <span className="block text-sm font-normal text-ntu-muted mt-1">Explore our world-class business education offerings</span>
            </h2>
          </div>
          <Link to="/programmes" className="text-ntu-red text-sm font-semibold flex items-center gap-1 hover:gap-2 transition-all whitespace-nowrap">
            View all programmes
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {programs.map((prog) => (
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
          {programs.length === 0 && (
            <div className="col-span-3 text-center py-12 text-ntu-muted">
              <p>Loading programmes...</p>
            </div>
          )}
        </div>
      </section>

      {/* Lyon Teaser Section */}
      <section className="bg-[#F5F5F5] py-16 px-8">
        <div className="max-w-[1200px] mx-auto grid grid-cols-1 lg:grid-cols-2 gap-14 items-center">
          <div>
            <span className="inline-block text-[0.72rem] font-semibold uppercase tracking-wider text-ntu-red bg-ntu-red/[0.08] px-2.5 py-1 rounded mb-4">
              AI-Powered Advisor
            </span>
            <h2 className="text-2xl font-bold text-ntu-dark mb-1">Meet Lyon, Your NBS Degree Advisor</h2>
            <p className="text-ntu-body text-[0.95rem] leading-relaxed mb-6">
              NTU's lion mascot knows NBS inside out. Ask about programme details,
              admission requirements, career outcomes, or get help comparing
              programmes. Available 24/7.
            </p>
            <ul className="space-y-2 mb-8">
              {[
                'Search across all 11 NBS graduate programmes',
                'Compare programmes side by side',
                'Get answers on admissions, fees, and deadlines',
                "Warm, professional advice from NTU's lion mascot",
              ].map((feature) => (
                <li key={feature} className="flex items-start gap-2.5 text-sm text-ntu-body">
                  <svg className="w-[18px] h-[18px] text-ntu-red flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 6L9 17l-5-5"/></svg>
                  {feature}
                </li>
              ))}
            </ul>
            <Link to="/chat" className="inline-flex items-center gap-2 px-6 py-3 bg-ntu-red text-white rounded font-semibold text-sm hover:bg-ntu-red-hover transition-colors">
              <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
              </svg>
              Start Chatting with Lyon
            </Link>
          </div>

          {/* Chat Preview */}
          <div className="bg-white border border-ntu-border rounded-lg shadow-md overflow-hidden">
            <div className="bg-ntu-dark p-4 flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full bg-ntu-red flex items-center justify-center text-white font-bold text-sm">L</div>
              <div className="flex-1">
                <div className="text-white text-sm font-semibold">Lyon</div>
                <div className="text-white/50 text-xs">NBS Degree Advisor</div>
              </div>
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            </div>
            <div className="p-5 flex flex-col gap-3 min-h-[260px]">
              <div className="self-start max-w-[82%] bg-[#F5F5F5] text-ntu-body rounded-md rounded-bl-sm px-4 py-2.5 text-sm leading-relaxed">
                Hi there! Welcome to NBS. I'm Lyon, NTU's resident lion. What programme are you interested in?
              </div>
              <div className="self-end max-w-[82%] bg-ntu-red text-white rounded-md rounded-br-sm px-4 py-2.5 text-sm leading-relaxed">
                What's the difference between MBA and EMBA?
              </div>
              <div className="self-start max-w-[82%] bg-[#F5F5F5] text-ntu-body rounded-md rounded-bl-sm px-4 py-2.5 text-sm leading-relaxed">
                Great question! The Nanyang MBA is a 12-month full-time programme, ideal for a career switch. The Executive MBA is an 18-month part-time programme designed for senior leaders who want to keep working. Want me to compare them side by side?
              </div>
            </div>
            <div className="px-5 py-3 border-t border-ntu-border flex items-center gap-3">
              <input type="text" placeholder="Ask Lyon anything..." disabled className="flex-1 border border-ntu-border rounded px-3 py-2 text-sm text-ntu-body outline-none" />
              <button disabled className="w-9 h-9 rounded bg-ntu-red flex items-center justify-center">
                <svg className="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>
              </button>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
