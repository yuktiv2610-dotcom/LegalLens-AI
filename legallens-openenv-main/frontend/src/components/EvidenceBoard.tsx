import React from 'react';
import { EvidenceItem } from '../api/client';

interface Props {
  evidence: EvidenceItem[];
  onAnalyze?: (id: string) => void;
}

const EvidenceBoard: React.FC<Props> = ({ evidence, onAnalyze }) => {
  return (
    <div className="chic-card flex-grow flex flex-col">
      <div className="chic-card-header">{'>>'} EVIDENCE BOARD</div>
      
      {evidence.length === 0 ? (
        <div className="flex-grow flex items-center justify-center font-mono text-xs text-cyan-dim/50 border-2 border-dashed border-cyan/10 m-2">
          NO EVIDENCE COLLECTED
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 p-2 overflow-y-auto max-h-[300px]">
          {evidence.map(item => (
            <div key={item.id} className={`evidence-card ${item.collected ? 'collected' : ''}`}>
              <div className="flex justify-between items-start mb-2">
                <span className="font-pixel text-[6px] text-purple-pixel uppercase">{item.evidence_type}</span>
                <span className={`font-pixel text-[6px] ${item.collected ? 'text-green-pixel' : 'text-amber'}`}>
                  {item.status}
                </span>
              </div>
              <p className="font-mono text-[10px] text-gray-300 mb-3 truncate" title={item.description}>
                {item.description}
              </p>
              {!item.collected && onAnalyze && (
                <button 
                  className="pixel-btn text-[6px] p-1 border-cyan text-cyan hover:bg-cyan/10 w-full"
                  onClick={() => onAnalyze(item.id)}
                >
                  [ ANALYZE ]
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EvidenceBoard;
