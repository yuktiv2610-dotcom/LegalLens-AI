import React, { useState, useEffect } from 'react';
import { useAppStore } from '../store/appStore';

const BOOT_LOGS = [
  "INITIALIZING LEGAL ENGINE...",
  "LOADING CASE DATABASE...",
  "INITIALIZING AI CORE...",
  "VERIFYING LEGAL PRECEDENTS...",
  "SYSTEM STATUS: ONLINE",
  "> READY FOR CASE"
];

const BootSequence: React.FC = () => {
  const { setBootComplete } = useAppStore();
  const [logs, setLogs] = useState<string[]>([]);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let currentLog = 0;
    
    const interval = setInterval(() => {
      if (currentLog < BOOT_LOGS.length) {
        setLogs(prev => [...prev, BOOT_LOGS[currentLog]]);
        setProgress(Math.min(100, (currentLog + 1) * 20));
        currentLog++;
      } else {
        clearInterval(interval);
        setTimeout(() => setBootComplete(true), 1000);
      }
    }, 400);

    return () => clearInterval(interval);
  }, [setBootComplete]);

  return (
    <div className="min-h-screen bg-warm-50 flex flex-col items-center justify-center p-4 noise-overlay">
      <div className="w-full max-w-2xl pixel-terminal bg-white">
        <div className="font-pixel text-ink text-center mb-8">
          ==================================<br/>
                  LEGALENS OS v2.0          <br/>
          ==================================
        </div>
        
        <div className="mb-8 space-y-4 font-mono text-ink-soft">
          {logs.map((log, i) => (
            <div key={i} className="typewriter">{">"} {log}</div>
          ))}
          {logs.length < BOOT_LOGS.length && (
            <div className="blink-cursor">{">"} </div>
          )}
        </div>

        <div className="w-full max-w-md mx-auto">
          <div className="pixel-progress-track mb-4">
            <div 
              className="pixel-progress-fill" 
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <div className="text-center mt-12">
          <button 
            className="pixel-btn text-xs"
            onClick={() => setBootComplete(true)}
          >
            [ SKIP SEQUENCE ]
          </button>
        </div>
      </div>
    </div>
  );
};

export default BootSequence;
