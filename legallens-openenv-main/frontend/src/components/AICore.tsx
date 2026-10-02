import React from 'react';

interface AICoreProps {
  state: 'IDLE' | 'READING' | 'THINKING' | 'SEARCHING' | 'EVALUATING' | 'RESPONDING';
  stepCount: number;
  maxSteps: number;
  reward: number;
}

const AICore: React.FC<AICoreProps> = ({ state, stepCount, maxSteps, reward }) => {
  const getCoreColor = () => {
    switch (state) {
      case 'IDLE': return 'border-cyan shadow-pixel-cyan text-cyan';
      case 'READING': return 'border-cyan shadow-pixel-cyan text-cyan animate-pulse';
      case 'THINKING': return 'border-purple shadow-pixel-purple text-purple animate-pulse-slow';
      case 'SEARCHING': return 'border-amber shadow-pixel-amber text-amber animate-spin-slow';
      case 'EVALUATING': return 'border-gold shadow-pixel-gold text-gold animate-pulse';
      case 'RESPONDING': return 'border-green shadow-pixel-green text-green';
      default: return 'border-cyan text-cyan';
    }
  };

  const getAsciiFace = () => {
    switch (state) {
      case 'IDLE': return '( ^_^ )';
      case 'READING': return '( o_o )';
      case 'THINKING': return '( -_- )';
      case 'SEARCHING': return '( >_< )';
      case 'EVALUATING': return '( $_$ )';
      case 'RESPONDING': return '( ^O^ )';
      default: return '( ^_^ )';
    }
  };

  return (
    <div className="chic-card flex flex-col items-center">
      <div className="w-full flex justify-between mb-4">
        <span className="font-pixel text-[6px] text-cyan-dim">AI CORE v2.0</span>
        <span className="font-pixel text-[6px] text-cyan-dim">STEP {stepCount}/{maxSteps}</span>
      </div>
      
      <div className={`w-24 h-24 rounded-full border-4 flex items-center justify-center bg-white mb-4 transition-all duration-300 ${getCoreColor()}`}>
        <div className="font-mono text-xl font-bold">{getAsciiFace()}</div>
      </div>
      
      <div className="font-pixel text-[8px] text-center mb-4 tracking-wider h-4">
        {state === 'IDLE' && '> WAITING FOR INPUT'}
        {state === 'READING' && '> PARSING FACTS...'}
        {state === 'THINKING' && '> GENERATING PLAN...'}
        {state === 'SEARCHING' && '> QUERYING DATABASE...'}
        {state === 'EVALUATING' && '> ASSESSING REWARD...'}
        {state === 'RESPONDING' && '> EXECUTING ACTION...'}
      </div>
      
      <div className="w-full">
        <div className="score-bar">
          <span className="score-label text-[6px]">REWARD</span>
          <div className="score-track h-2">
            <div className="score-fill" style={{ width: `${Math.max(0, Math.min(100, (reward / 1.0) * 100))}%` }} />
          </div>
          <span className="score-value text-[6px]">{reward.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
};

export default AICore;
