import { Routes, Route } from 'react-router-dom';
import SplashPage from './pages/SplashPage';
import RecommendPage from './pages/RecommendPage';
import ChatPage from './pages/ChatPage';
import ProgrammesPage from './pages/ProgrammesPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<SplashPage />} />
      <Route path="/recommend" element={<RecommendPage />} />
      <Route path="/chat" element={<ChatPage />} />
      <Route path="/programmes" element={<ProgrammesPage />} />
    </Routes>
  );
}

export default App;
