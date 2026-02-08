import { Link } from 'react-router-dom';

export default function SplashPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-ntu-dark mb-4">NBS Candidate Portal</h1>
        <p className="text-ntu-body mb-8">Coming soon - full splash page</p>
        <div className="flex gap-4 justify-center">
          <Link to="/recommend" className="px-6 py-3 bg-ntu-red text-white rounded">Get Recommendations</Link>
          <Link to="/chat" className="px-6 py-3 border border-ntu-red text-ntu-red rounded">Chat with Lyon</Link>
        </div>
      </div>
    </div>
  );
}
