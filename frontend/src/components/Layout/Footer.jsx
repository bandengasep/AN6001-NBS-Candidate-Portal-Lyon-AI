export function Footer() {
  return (
    <footer className="bg-ntu-dark text-white/60 text-sm">
      <div className="max-w-[1200px] mx-auto px-8 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <div className="text-white font-semibold mb-2">Nanyang Business School</div>
          <div className="text-white/40 text-xs leading-relaxed">
            Nanyang Technological University, Singapore<br />
            50 Nanyang Avenue, Singapore 639798<br /><br />
            AN6001 AI and Big Data Group Project
          </div>
        </div>
        <div>
          <h4 className="text-white/40 text-xs font-semibold uppercase tracking-wider mb-3">Quick Links</h4>
          <a href="https://www.ntu.edu.sg/business" target="_blank" rel="noopener noreferrer"
             className="block text-white/65 text-sm py-1 hover:text-white transition-colors">NBS Website</a>
          <a href="https://www.ntu.edu.sg/business/admissions" target="_blank" rel="noopener noreferrer"
             className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Admissions</a>
          <a href="https://www.ntu.edu.sg/business/admissions/graduate-studies" target="_blank" rel="noopener noreferrer"
             className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Graduate Studies</a>
        </div>
        <div>
          <h4 className="text-white/40 text-xs font-semibold uppercase tracking-wider mb-3">Resources</h4>
          <a href="/recommend" className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Programme Finder</a>
          <a href="/chat" className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Chat with Lyon</a>
          <a href="/programmes" className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Browse Programmes</a>
        </div>
      </div>
      <div className="max-w-[1200px] mx-auto px-8 py-4 border-t border-white/10 flex justify-between text-xs text-white/35">
        <span>&copy; 2026 Nanyang Technological University. All rights reserved.</span>
        <span>Powered by AI</span>
      </div>
    </footer>
  );
}
