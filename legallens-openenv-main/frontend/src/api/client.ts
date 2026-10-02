// LegalLens 2.0 - API client
import axios from 'axios';

const BASE = '';  // Uses vite proxy in dev, same origin in prod

export const api = axios.create({ baseURL: BASE });

export interface Task {
  id: string;
  name: string;
  description: string;
  domain: string;
  difficulty: number;
  max_steps: number;
  tags: string[];
  facts?: string;
  hints?: string[];
}

export interface LawRef {
  id: string;
  name: string;
  reference: string;
  domain: string;
  description: string;
  relevance: string;
  jurisdiction: string;
  keywords: string[];
  verified: boolean;
}

export interface EvidenceItem {
  id: string;
  name: string;
  evidence_type: string;
  status: string;
  description: string;
  collected: boolean;
}

export interface Observation {
  case_id: string;
  task_id: string;
  facts: string;
  legal_domain?: string;
  jurisdiction?: string;
  court_or_forum?: string;
  identified_issues: string[];
  identified_laws: LawRef[];
  evidence: EvidenceItem[];
  recommended_actions: string[];
  missing_information: string[];
  last_action?: string;
  last_action_result?: string;
  last_reward: number;
  last_error?: string;
  step_count: number;
  steps_remaining: number;
  cumulative_reward: number;
  done: boolean;
  confidence: number;
  available_actions: string[];
  suggested_next_action?: string;
}

export interface StepResult {
  observation: Observation;
  reward: number;
  done: boolean;
  info: Record<string, unknown>;
  error?: string;
  episode_result?: EpisodeResult;
}

export interface EpisodeResult {
  task_id: string;
  task_name: string;
  case_id: string;
  episode_id: string;
  success: boolean;
  total_steps: number;
  total_reward: number;
  final_score: number;
  rewards_per_step: number[];
  grader_breakdown: Record<string, number>;
  errors: string[];
  feedback: string;
  final_analysis?: string;
}

export interface AgentStep {
  step: number;
  action: string;
  reward: number;
  done: boolean;
  result?: string;
  error?: string;
}

export interface AgentRunResult {
  task_id: string;
  steps: AgentStep[];
  rewards: number[];
  total_reward: number;
  final_score: number;
  success: boolean;
  total_steps: number;
  grader_breakdown: Record<string, number>;
  feedback: string;
  final_analysis?: string;
}

// API Methods
export const getTasks = () => api.get<{ tasks: Task[] }>('/api/tasks').then(r => r.data.tasks);
export const getTask = (id: string) => api.get<Task>(`/api/tasks/${id}`).then(r => r.data);
export const getLaws = (domain?: string, query?: string) =>
  api.get<{ laws: LawRef[]; count: number }>('/api/laws', { params: { domain, query } }).then(r => r.data);

export const resetCase = (task_id: string, session_id?: string) =>
  api.post<{ session_id: string; observation: Observation }>('/api/case/reset', { task_id, session_id }).then(r => r.data);

export const stepCase = (session_id: string, action: Record<string, unknown>) =>
  api.post<StepResult>('/api/case/step', { session_id, action }).then(r => r.data);

export const getState = (session_id: string) =>
  api.get('/api/case/state', { params: { session_id } }).then(r => r.data);

export const getResult = (session_id: string) =>
  api.get<EpisodeResult>('/api/case/result', { params: { session_id } }).then(r => r.data);

export const runAgent = (task_id: string, max_steps = 15) =>
  api.post<AgentRunResult>('/api/agent/run', { task_id, max_steps }).then(r => r.data);

export const saveMemory = (session_id: string) =>
  api.post('/api/memory/save', null, { params: { session_id } }).then(r => r.data);

export const getMemory = () =>
  api.get<{ cases: unknown[]; count: number }>('/api/memory').then(r => r.data);

export const createWhatIf = (session_id: string, modified_fact: string) =>
  api.post('/api/case/whatif', { session_id, modified_fact }).then(r => r.data);

export const checkHealth = () =>
  api.get<{ status: string; version: string }>('/health').then(r => r.data);
