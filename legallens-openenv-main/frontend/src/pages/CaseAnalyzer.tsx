import React, { useEffect, useState, useRef } from 'react';
import { useAppStore } from '../store/appStore';
import { resetCase, stepCase, Observation, EpisodeResult } from '../api/client';
import EvidenceBoard from '../components/EvidenceBoard';
import AICore from '../components/AICore';

const TIMELINE_STEPS = [
  'DOMAIN', 'ISSUES', 'LAW', 'EVIDENCE', 'JURISDICTION', 'ACTION', 'FINALIZE'
];

const CaseAnalyzer: React.FC = () => {
  const { currentTask, sessionId, setSessionId, observation, setObservation, setCurrentPage, setEpisodeResult } = useAppStore();
  const [loading, setLoading] = useState(false);
  const [aiState, setAiState] = useState<'IDLE' | 'READING' | 'THINKING' | 'SEARCHING' | 'EVALUATING' | 'RESPONDING'>('IDLE');
  
  // Initialize case on mount
  useEffect(() => {
    if (currentTask && !sessionId) {
      initCase();
    }
  }, [currentTask]);

  const initCase = async () => {
    if (!currentTask) return;
    setLoading(true);
    setAiState('READING');
    try {
      const res = await resetCase(currentTask.id);
      setSessionId(res.session_id);
      setObservation(res.observation);
      setAiState('IDLE');
    } catch (e) {
      console.error(e);
      setAiState('IDLE');
    } finally {
      setLoading(false);
    }
  };

  const executeAction = async (action: any) => {
    if (!sessionId || loading) return;
    setLoading(true);
    setAiState('THINKING');
    try {
      // Simulate slightly longer processing for visual effect
      await new Promise(r => setTimeout(r, 600));
      
      const res = await stepCase(sessionId, action);
      setObservation(res.observation);
      
      if (res.done && res.episode_result) {
        setEpisodeResult(res.episode_result);
        setCurrentPage('score');
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
      setAiState('IDLE');
    }
  };

  if (!currentTask || !observation) {
    return <div className="text-center font-mono py-12">LOADING CASE DATA...</div>;
  }

  // Determine current timeline progress
  let progressIndex = 0;
  if (observation.legal_domain) progressIndex = 1;
  if (observation.identified_issues.length > 0) progressIndex = 2;
  if (observation.identified_laws.length > 0) progressIndex = 3;
  if (observation.evidence.length > 0) progressIndex = 4;
  if (observation.jurisdiction) progressIndex = 5;
  if (observation.recommended_actions.length > 0) progressIndex = 6;
  if (observation.done) progressIndex = 7;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pb-12">
      {/* Left Column: Timeline & AI Core */}
      <div className="lg:col-span-3 flex flex-col gap-6">
        <AICore state={aiState} stepCount={observation.step_count} maxSteps={observation.step_count + observation.steps_remaining} reward={observation.cumulative_reward} />
        
        <div className="chic-card flex-grow">
          <div className="chic-card-header">{">>"} INVESTIGATION</div>
          <div className="pl-2 pt-2">
            {TIMELINE_STEPS.map((step, idx) => {
              const status = idx < progressIndex ? 'done' : (idx === progressIndex ? 'active' : 'pending');
              return (
                <div key={step} className="timeline-step">
                  <div className={`timeline-dot ${status}`}>
                    {status === 'done' ? '✓' : ''}
                  </div>
                  <span className={`font-mono text-sm ml-6 ${status === 'active' ? 'text-cyan' : (status === 'done' ? 'text-green-pixel' : 'text-ink-soft')}`}>
                    {step}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Middle Column: Case Details & Manual Actions (for demo/testing) */}
      <div className="lg:col-span-5 flex flex-col gap-6">
        <div className="chic-card">
          <div className="flex justify-between items-center mb-4 border-b border-ink-soft/20 pb-2">
            <h2 className="font-pixel text-xs text-gold">CASE FILE #{observation.case_id.split('-')[2]}</h2>
            <div className="pixel-badge text-cyan border-cyan">ACTIVE</div>
          </div>
          
          <div className="font-mono text-sm whitespace-pre-wrap text-ink-soft bg-warm-100 p-4 border border-ink-soft/20 max-h-[400px] overflow-y-auto">
            {observation.facts}
          </div>
        </div>

        {/* Action History / Terminal */}
        <div className="pixel-terminal flex-grow min-h-[250px] flex flex-col">
          <div className="pixel-terminal-title">{">"} SYSTEM LOGS</div>
          <div className="flex-grow overflow-y-auto font-mono text-xs space-y-2">
            <div className="text-cyan-dim">Session initialized. {currentTask.name} loaded.</div>
            {observation.last_action && (
              <div className="text-gold">{">"} ACTION: {observation.last_action}</div>
            )}
            {observation.last_action_result && (
              <div className={observation.last_error ? "text-red-pixel" : "text-green-pixel"}>
                {observation.last_action_result}
              </div>
            )}
            {observation.last_reward !== 0 && (
              <div className="text-purple-pixel">Reward updated: {observation.last_reward > 0 ? '+' : ''}{observation.last_reward.toFixed(2)}</div>
            )}
            <div className="blink-cursor mt-2">{">"} </div>
          </div>
        </div>
      </div>

      {/* Right Column: Knowledge & Evidence */}
      <div className="lg:col-span-4 flex flex-col gap-6">
        <div className="chic-card">
          <div className="chic-card-header">{">>"} KNOWN FACTS</div>
          <div className="font-mono text-xs space-y-3">
            <div>
              <span className="text-cyan-dim">DOMAIN:</span>{' '}
              <span className="text-gold">{observation.legal_domain || 'UNKNOWN'}</span>
            </div>
            <div>
              <span className="text-cyan-dim">JURISDICTION:</span>{' '}
              <span className="text-gold">{observation.jurisdiction || 'UNKNOWN'}</span>
            </div>
            <div>
              <span className="text-cyan-dim">ISSUES:</span>
              <ul className="list-disc pl-4 text-ink-soft mt-1">
                {observation.identified_issues.map((i, idx) => <li key={idx}>{i}</li>)}
                {observation.identified_issues.length === 0 && <li>None identified</li>}
              </ul>
            </div>
            <div>
              <span className="text-cyan-dim">LAWS:</span>
              <ul className="list-disc pl-4 text-ink-soft mt-1">
                {observation.identified_laws.map((l, idx) => (
                  <li key={idx} className={l.verified ? 'text-green-pixel' : 'text-amber'}>
                    {l.reference} {!l.verified && '(Unverified)'}
                  </li>
                ))}
                {observation.identified_laws.length === 0 && <li>None identified</li>}
              </ul>
            </div>
            {observation.missing_information.length > 0 && (
              <div>
                <span className="text-red-pixel">MISSING INFO:</span>
                <ul className="list-disc pl-4 text-ink-soft mt-1">
                  {observation.missing_information.map((m, idx) => <li key={idx}>{m}</li>)}
                </ul>
              </div>
            )}
          </div>
        </div>

        <EvidenceBoard evidence={observation.evidence} onAnalyze={(id) => executeAction({ action_type: 'ANALYZE_EVIDENCE', evidence_id: id })} />
        
        {/* Manual control panel (for user to act as agent) */}
        <div className="chic-card mt-auto">
          <div className="chic-card-header text-amber">{">>"} MANUAL OVERRIDE</div>
          <div className="grid grid-cols-2 gap-2 mt-2">
            <button className="pixel-btn text-[8px] p-2 border-cyan text-cyan hover:bg-cyan/10"
              onClick={() => executeAction({ action_type: 'CLASSIFY_DOMAIN', domain: currentTask.domain })}>
              SET DOMAIN
            </button>
            <button className="pixel-btn text-[8px] p-2 border-cyan text-cyan hover:bg-cyan/10"
              onClick={() => executeAction({ action_type: 'REQUEST_EVIDENCE', evidence_type: 'DOCUMENT' })}>
              REQ EVIDENCE
            </button>
            <button className="pixel-btn text-[8px] p-2 border-purple text-purple hover:bg-purple/10 col-span-2"
              onClick={() => executeAction({ action_type: 'FINALIZE_ANALYSIS', final_analysis: 'Manual finalizing for demo.', confidence: 0.8 })}>
              FINALIZE ANALYSIS
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CaseAnalyzer;
