import React, { useState } from 'react';
import { useAppStore } from '../store/appStore';

const ScoreScreen: React.FC = () => {
  const { episodeResult, setCurrentPage, reset } = useAppStore();
  const [showGraph, setShowGraph] = useState(false);

  if (!episodeResult) {
    setCurrentPage('home');
    return null;
  }

  const { final_score, grader_breakdown, feedback, total_steps, total_reward, final_analysis } = episodeResult;
  const scorePercent = Math.round(final_score * 100);
  
  let grade = 'F';
  let color = 'text-red-pixel';
  if (scorePercent >= 90) { grade = 'S'; color = 'text-gold'; }
  else if (scorePercent >= 80) { grade = 'A'; color = 'text-green-pixel'; }
  else if (scorePercent >= 70) { grade = 'B'; color = 'text-cyan'; }
  else if (scorePercent >= 60) { grade = 'C'; color = 'text-amber'; }

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6 pb-12">
      <div className="chic-card text-center py-8">
        <h1 className="font-pixel text-2xl text-cyan mb-2">CASE COMPLETE</h1>
        <p className="font-mono text-cyan-dim">EPISODE #{episodeResult.episode_id.split('-')[0]}</p>
        
        <div className="my-8">
          <div className={`font-pixel text-6xl ${color} mb-4 animate-pulse-slow`}>{grade}</div>
          <div className="font-pixel text-xl text-ink">SCORE: {scorePercent}%</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="chic-card">
          <div className="chic-card-header text-gold">{'>>'} EVALUATION BREAKDOWN</div>
          <div className="space-y-4 mt-4">
            {Object.entries(grader_breakdown).map(([key, val]) => (
              <div key={key} className="score-bar">
                <span className="score-label uppercase">{key}</span>
                <div className="score-track">
                  <div className="score-fill bg-cyan" style={{ width: `${val * 100}%` }} />
                </div>
                <span className="score-value">{Math.round(val * 100)}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="chic-card flex flex-col">
          <div className="chic-card-header text-purple-pixel">{'>>'} FINAL ANALYSIS</div>
          <div className="font-mono text-sm text-ink-soft bg-warm-100 p-4 border border-ink-soft/20 flex-grow whitespace-pre-wrap overflow-y-auto">
            {final_analysis || "No final analysis provided."}
          </div>
        </div>
      </div>

      <div className="chic-card">
        <div className="chic-card-header text-green-pixel">{'>>'} METRICS & FEEDBACK</div>
        <div className="font-mono text-sm text-ink-soft grid grid-cols-2 gap-4">
          <div>
            <span className="text-cyan-dim">STEPS TAKEN:</span> {total_steps}<br/>
            <span className="text-cyan-dim">ENV REWARD:</span> {total_reward.toFixed(2)}
          </div>
          <div>
            <span className="text-cyan-dim">GRADER NOTES:</span><br/>
            <span className="text-amber">{feedback}</span>
          </div>
        </div>
      </div>

      <div className="flex justify-center gap-6 mt-4">
        <button 
          className="pixel-btn pixel-btn-cyan"
          onClick={() => {
            reset();
            setCurrentPage('home');
          }}
        >
          [ NEW CASE ]
        </button>
      </div>
    </div>
  );
};

export default ScoreScreen;
