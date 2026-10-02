import React, { useState, useEffect } from 'react';
import { getLaws, LawRef } from '../api/client';

const LawLibrary: React.FC = () => {
  const [laws, setLaws] = useState<LawRef[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [domain, setDomain] = useState('');

  useEffect(() => {
    const fetchLaws = async () => {
      setLoading(true);
      try {
        const res = await getLaws(domain || undefined, query || undefined);
        setLaws(res.laws);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    
    // Simple debounce
    const t = setTimeout(fetchLaws, 300);
    return () => clearTimeout(t);
  }, [query, domain]);

  return (
    <div className="max-w-6xl mx-auto flex flex-col gap-6 h-[calc(100vh-100px)]">
      <div className="chic-card py-4 flex justify-between items-center flex-wrap gap-4">
        <h1 className="font-pixel text-xl text-cyan">LAW LIBRARY</h1>
        <div className="flex gap-4 w-full md:w-auto">
          <select 
            className="bg-warm-100 text-cyan border border-cyan p-2 font-mono text-sm outline-none"
            value={domain}
            onChange={e => setDomain(e.target.value)}
          >
            <option value="">ALL DOMAINS</option>
            <option value="cyber_law">CYBER LAW</option>
            <option value="criminal_law">CRIMINAL LAW</option>
            <option value="consumer_law">CONSUMER LAW</option>
            <option value="property_law">PROPERTY LAW</option>
          </select>
          <input 
            type="text" 
            placeholder="SEARCH KNOWLEDGE BASE..." 
            className="bg-warm-100 text-cyan border border-cyan p-2 font-mono text-sm outline-none flex-grow min-w-[200px]"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="flex-grow overflow-y-auto space-y-4 pr-2">
        {loading ? (
          <div className="text-center font-mono py-12 text-cyan-dim animate-pulse">QUERYING DATABASE...</div>
        ) : laws.length === 0 ? (
          <div className="text-center font-mono py-12 text-amber">NO RESULTS FOUND</div>
        ) : (
          laws.map(law => (
            <div key={law.id} className="chic-card flex flex-col gap-2">
              <div className="flex justify-between items-start border-b border-ink-soft/20 pb-2">
                <div>
                  <h3 className="font-pixel text-sm text-gold">{law.name}</h3>
                  <div className="font-mono text-xs text-cyan-dim mt-1">{law.reference}</div>
                </div>
                <div className="pixel-badge text-cyan border-cyan uppercase">{law.domain.replace('_', ' ')}</div>
              </div>
              <p className="font-mono text-sm text-ink-soft mt-2">{law.description}</p>
              <div className="font-mono text-xs text-purple-pixel mt-2">
                RELEVANCE: <span className="text-ink-soft">{law.relevance}</span>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {law.keywords.map(kw => (
                  <span key={kw} className="font-mono text-[10px] bg-cyan/10 text-cyan-dim px-2 py-1">#{kw}</span>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LawLibrary;
