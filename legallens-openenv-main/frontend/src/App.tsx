import { useEffect } from 'react';
import { useAppStore } from './store/appStore';
import { checkHealth } from './api/client';
import BootSequence from './components/BootSequence';
import HomeScreen from './pages/HomeScreen';
import CaseAnalyzer from './pages/CaseAnalyzer';
import AgentLab from './pages/AgentLab';
import LawLibrary from './pages/LawLibrary';
import ScoreScreen from './pages/ScoreScreen';

function App() {
  const { bootComplete, currentPage, setBackendOnline } = useAppStore();

  useEffect(() => {
    // Check backend health
    checkHealth()
      .then(() => setBackendOnline(true))
      .catch(() => setBackendOnline(false));
  }, [setBackendOnline]);

  if (!bootComplete) {
    return <BootSequence />;
  }

  return (
    <div className="min-h-screen w-full bg-warm-50 text-ink flex flex-col relative overflow-hidden font-serif">
      
      {/* Chic Header */}
      <header className="w-full relative z-50 border-b border-ink-soft/20 bg-warm-50/80 backdrop-blur-md px-6 py-5 flex justify-between items-center">
        <div 
          className="cursor-pointer group flex items-center gap-4"
          onClick={() => useAppStore.getState().setCurrentPage('home')}
        >
          <span className="text-2xl font-bold group-hover:text-accent-rust transition-colors">§</span> 
          <span className="font-mono text-sm tracking-widest uppercase group-hover:text-accent-rust transition-colors mt-1">LEGALLENS 2.0</span>
        </div>
        <div className="flex gap-4 items-center">
          <div className="font-mono text-xs uppercase tracking-widest text-ink flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${useAppStore.getState().backendOnline ? 'bg-accent-sage' : 'bg-accent-rust'}`} />
            SYS_ONLINE
          </div>
        </div>
      </header>

      {/* Main Content (Full Bleed) */}
      <main className="w-full flex-grow relative z-10">
        {currentPage === 'home' && <HomeScreen />}
        {currentPage === 'analyzer' && <CaseAnalyzer />}
        {currentPage === 'agent_lab' && <AgentLab />}
        {currentPage === 'law_library' && <LawLibrary />}
        {currentPage === 'score' && <ScoreScreen />}
      </main>
    </div>
  );
}

export default App;
