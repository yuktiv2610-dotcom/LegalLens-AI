import React, { useEffect, useState, useRef } from 'react';
import { useAppStore } from '../store/appStore';
import { getTasks, Task } from '../api/client';

// Intersection Observer Hook for Scroll Reveals
const useScrollReveal = (dependencies: any[]) => {
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('active');
          }
        });
      },
      { threshold: 0.1 }
    );

    // Small delay to ensure DOM is updated before observing
    setTimeout(() => {
      const elements = document.querySelectorAll('.reveal');
      elements.forEach((el) => observer.observe(el));
    }, 100);

    return () => observer.disconnect();
  }, dependencies);
};

const AshokChakra: React.FC = () => (
  <svg width="80" height="80" viewBox="0 0 200 200" className="animate-spin opacity-80" style={{ animationDuration: '25s' }}>
    <circle cx="100" cy="100" r="90" fill="none" stroke="#1A1612" strokeWidth="2" />
    <circle cx="100" cy="100" r="80" fill="none" stroke="#1A1612" strokeWidth="1" />
    <circle cx="100" cy="100" r="12" fill="#1A1612" />
    {Array.from({ length: 24 }).map((_, i) => {
      const angle = (i * 15) * (Math.PI / 180);
      const x2 = 100 + 78 * Math.cos(angle);
      const y2 = 100 + 78 * Math.sin(angle);
      return <line key={i} x1="100" y1="100" x2={x2} y2={y2} stroke="#1A1612" strokeWidth="1" />;
    })}
  </svg>
);

const HomeScreen: React.FC = () => {
  const { setCurrentPage, setCurrentTask } = useAppStore();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  // Pass tasks array so observer re-runs when cases finish loading
  useScrollReveal([tasks]);

  useEffect(() => {
    getTasks()
      .then(t => setTasks(t))
      .catch(e => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  const handleStartCase = (task: Task) => {
    setCurrentTask(task);
    setCurrentPage('analyzer');
  };

  return (
    <div className="flex flex-col w-full bg-warm-50">
      {/* Hero Section */}
      <section className="min-h-[80vh] flex flex-col justify-center items-center text-center px-6 relative reveal">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.03] pointer-events-none w-full h-full flex justify-center items-center overflow-hidden">
           <span className="font-serif text-[40vw] leading-none select-none">§</span>
        </div>
        
        <div className="mb-12 reveal delay-100">
          <AshokChakra />
        </div>
        
        <h1 className="font-serif text-5xl md:text-8xl text-ink mb-6 tracking-tight reveal delay-200">
          LEGAL INTELLIGENCE
        </h1>
        
        <p className="font-mono text-sm md:text-base text-ink-soft mb-12 max-w-2xl mx-auto uppercase tracking-[0.2em] reveal delay-300">
          OpenEnv Reasoning Environment v2.0
        </p>
        
        <div className="flex flex-wrap justify-center gap-6 relative z-10 reveal delay-300">
          <button className="pixel-btn" onClick={() => setCurrentPage('law_library')}>
            Law Database
          </button>
          <button className="pixel-btn" onClick={() => setCurrentPage('agent_lab')}>
            Agent Lab
          </button>
        </div>
      </section>

      {/* Case Files Section */}
      <section className="py-24 px-6 md:px-12 lg:px-24 bg-warm-100">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-6 mb-16 reveal">
            <h2 className="font-serif text-3xl md:text-4xl text-ink italic">Select Case File</h2>
            <div className="flex-1 h-[1px] bg-ink-soft/30" />
          </div>

          {loading ? (
            <div className="text-center py-24 font-mono text-ink-soft animate-pulse">
              Retrieving Archives...
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">
              {tasks.map((task, index) => (
                <div 
                  key={task.id} 
                  className={`chic-card cursor-pointer group reveal delay-${(index % 2 + 1) * 100}`}
                  onClick={() => handleStartCase(task)}
                >
                  <div className="flex justify-between items-start mb-8">
                    <div className="pixel-badge text-accent-rust border-accent-rust group-hover:bg-accent-rust group-hover:text-warm-50 transition-colors">
                      Level {task.difficulty}
                    </div>
                    <span className="font-mono text-xs text-ink-soft uppercase tracking-widest">
                      {task.domain.replace('_', ' ')}
                    </span>
                  </div>
                  
                  <h3 className="font-serif text-2xl md:text-3xl text-ink mb-4 group-hover:text-accent-rust transition-colors">
                    {task.name}
                  </h3>
                  
                  <p className="font-serif text-lg text-ink-soft mb-12 leading-relaxed">
                    {task.description}
                  </p>
                  
                  <div className="flex flex-wrap items-center justify-between mt-auto pt-6 border-t border-ink-soft/20">
                    <div className="flex flex-wrap gap-2">
                      {task.tags.map(tag => (
                        <span key={tag} className="font-mono text-[10px] text-ink-soft bg-warm-200 px-2 py-1 uppercase tracking-wider">
                          {tag}
                        </span>
                      ))}
                    </div>
                    <div className="font-pixel text-[8px] text-ink group-hover:translate-x-2 transition-transform">
                      START {'>'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 text-center bg-warm-50 reveal">
        <p className="font-serif italic text-ink-soft">
          LegalLens is an AI-assisted informational tool. It does not provide professional legal advice.
        </p>
      </footer>
    </div>
  );
};

export default HomeScreen;
