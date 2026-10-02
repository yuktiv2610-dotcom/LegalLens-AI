import React, { useState, useEffect, useRef } from 'react';
import { getTasks, runAgent, Task, AgentRunResult } from '../api/client';

const AgentLab: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<string>('cyber_fraud');
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState<AgentRunResult | null>(null);
  const terminalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getTasks().then(setTasks).catch(console.error);
  }, []);

  const handleRun = async () => {
    setIsRunning(true);
    setResult(null);
    try {
      const res = await runAgent(selectedTask, 15);
      setResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsRunning(false);
    }
  };

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [result, isRunning]);

  return (
    <div className="max-w-5xl mx-auto flex flex-col gap-6 h-[calc(100vh-100px)]">
      <div className="flex justify-between items-center chic-card py-4">
        <h1 className="font-pixel text-xl text-gold">AGENT LAB</h1>
        <div className="flex gap-4 items-center">
          <select 
            className="bg-warm-100 text-cyan border border-cyan p-2 font-mono text-sm outline-none"
            value={selectedTask}
            onChange={e => setSelectedTask(e.target.value)}
            disabled={isRunning}
          >
            {tasks.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
          </select>
          <button 
            className="pixel-btn pixel-btn-green"
            onClick={handleRun}
            disabled={isRunning}
          >
            {isRunning ? '[ RUNNING... ]' : '[ RUN AGENT ]'}
          </button>
        </div>
      </div>

      <div className="flex-grow pixel-terminal flex flex-col">
        <div className="pixel-terminal-title">{">"} LIVE EXECUTION LOG</div>
        <div ref={terminalRef} className="flex-grow overflow-y-auto font-mono text-xs space-y-2 pb-4">
          {!isRunning && !result && (
            <div className="text-cyan-dim">Select a task and click RUN AGENT to start execution.</div>
          )}
          {isRunning && !result && (
            <div className="text-amber animate-pulse">Initializing baseline heuristic agent...</div>
          )}
          {result && (
            <>
              <div className="text-cyan">{'=' .repeat(50)}</div>
              <div className="text-cyan">STARTING EPISODE: {result.task_id}</div>
              <div className="text-cyan">{'=' .repeat(50)}</div>
              
              {result.steps.map((s, i) => (
                <div key={i} className="my-2 p-2 bg-warm-100 border-l-2 border-cyan/30">
                  <div className="text-purple-pixel font-bold">[STEP {s.step}] ACTION: {s.action}</div>
                  <div className={s.error ? 'text-red-pixel' : 'text-green-pixel'}>
                    {">"} {s.error || s.result}
                  </div>
                  <div className="text-amber">{">"} Reward: {s.reward.toFixed(2)}</div>
                </div>
              ))}
              
              <div className="text-cyan mt-4">{'=' .repeat(50)}</div>
              <div className="text-gold font-bold">EPISODE COMPLETE</div>
              <div className="text-ink">TOTAL REWARD: {result.total_reward.toFixed(4)}</div>
              <div className="text-ink">FINAL SCORE: {(result.final_score * 100).toFixed(0)}%</div>
              <div className="text-cyan mt-2">GRADER FEEDBACK:</div>
              <div className="text-amber">{result.feedback}</div>
            </>
          )}
          {isRunning && <div className="blink-cursor">{">"} </div>}
        </div>
      </div>
    </div>
  );
};

export default AgentLab;
