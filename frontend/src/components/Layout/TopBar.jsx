export function TopBar() {
  return (
    <div className="bg-ntu-dark py-1.5 px-8 flex justify-end gap-6 text-xs">
      <a href="https://www.ntu.edu.sg" target="_blank" rel="noopener noreferrer"
         className="text-white/70 hover:text-white transition-colors">NTU Home</a>
      <a href="https://www.ntu.edu.sg/business" target="_blank" rel="noopener noreferrer"
         className="text-white/70 hover:text-white transition-colors">NBS Website</a>
      <a href="https://www.ntu.edu.sg/business/admissions" target="_blank" rel="noopener noreferrer"
         className="text-white/70 hover:text-white transition-colors">Admissions</a>
    </div>
  );
}
