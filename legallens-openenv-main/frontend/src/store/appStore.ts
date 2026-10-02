import { create } from 'zustand';
import type { Observation, EpisodeResult, Task, AgentRunResult } from '../api/client';

interface AppState {
  // Session
  sessionId: string | null;
  currentTask: Task | null;
  observation: Observation | null;
  episodeResult: EpisodeResult | null;
  agentResult: AgentRunResult | null;

  // UI
  currentPage: string;
  bootComplete: boolean;
  isLoading: boolean;
  backendOnline: boolean;

  // Actions
  setSessionId: (id: string | null) => void;
  setCurrentTask: (task: Task | null) => void;
  setObservation: (obs: Observation | null) => void;
  setEpisodeResult: (result: EpisodeResult | null) => void;
  setAgentResult: (result: AgentRunResult | null) => void;
  setCurrentPage: (page: string) => void;
  setBootComplete: (v: boolean) => void;
  setLoading: (v: boolean) => void;
  setBackendOnline: (v: boolean) => void;
  reset: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  sessionId: null,
  currentTask: null,
  observation: null,
  episodeResult: null,
  agentResult: null,
  currentPage: 'home',
  bootComplete: false,
  isLoading: false,
  backendOnline: false,

  setSessionId: (id) => set({ sessionId: id }),
  setCurrentTask: (task) => set({ currentTask: task }),
  setObservation: (obs) => set({ observation: obs }),
  setEpisodeResult: (result) => set({ episodeResult: result }),
  setAgentResult: (result) => set({ agentResult: result }),
  setCurrentPage: (page) => set({ currentPage: page }),
  setBootComplete: (v) => set({ bootComplete: v }),
  setLoading: (v) => set({ isLoading: v }),
  setBackendOnline: (v) => set({ backendOnline: v }),
  reset: () => set({
    sessionId: null,
    observation: null,
    episodeResult: null,
    currentTask: null,
  }),
}));
