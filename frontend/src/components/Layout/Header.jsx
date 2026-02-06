import { GraduationCap, ExternalLink } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-nbs-red text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and title */}
          <div className="flex items-center space-x-3">
            <div className="bg-white rounded-lg p-2">
              <GraduationCap className="h-6 w-6 text-nbs-red" />
            </div>
            <div>
              <h1 className="text-xl font-bold">NBS Degree Advisor</h1>
              <p className="text-xs text-red-200">Nanyang Business School</p>
            </div>
          </div>

          {/* Navigation links */}
          <nav className="hidden md:flex items-center space-x-6">
            <a
              href="https://www.ntu.edu.sg/business/admissions/graduate-studies"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-1 text-sm hover:text-red-200 transition-colors"
            >
              <span>Programmes</span>
              <ExternalLink className="h-3 w-3" />
            </a>
            <a
              href="https://www.ntu.edu.sg/business/admissions"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-1 text-sm hover:text-red-200 transition-colors"
            >
              <span>Admissions</span>
              <ExternalLink className="h-3 w-3" />
            </a>
            <a
              href="https://www.ntu.edu.sg/business"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-1 text-sm hover:text-red-200 transition-colors"
            >
              <span>NBS Website</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;
