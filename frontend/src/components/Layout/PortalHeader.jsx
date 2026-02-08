import { Link } from 'react-router-dom';

export function PortalHeader() {
  return (
    <header className="bg-white border-b border-ntu-border sticky top-0 z-50 shadow-sm">
      <div className="max-w-[1200px] mx-auto px-8 py-3 flex justify-between items-center">
        <Link to="/" className="flex items-center gap-3 no-underline">
          <div className="w-10 h-10 bg-ntu-red rounded flex items-center justify-center">
            <span className="text-white font-bold text-sm">NBS</span>
          </div>
          <div className="h-7 w-px bg-ntu-border" />
          <div>
            <div className="text-ntu-dark font-semibold text-[1.05rem] leading-tight">Candidate Portal</div>
            <div className="text-ntu-muted text-[0.72rem]">Nanyang Business School</div>
          </div>
        </Link>
        <nav className="hidden md:flex items-center gap-8">
          <Link to="/programmes" className="text-ntu-body text-sm hover:text-ntu-red transition-colors">Programmes</Link>
          <Link to="/chat" className="text-ntu-body text-sm hover:text-ntu-red transition-colors">Ask Lyon</Link>
          <Link to="/recommend" className="bg-ntu-red text-white px-5 py-2 rounded text-sm font-semibold hover:bg-ntu-red-hover transition-colors">Get Started</Link>
        </nav>
      </div>
    </header>
  );
}
