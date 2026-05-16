import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Worker {
  worker_id: string;
  name: string;
  age: number;
  primary_skill: string;
  transferable_skills: string;
  education: string;
  physicality: string;
  current_zone: string;
  zone_function: string;
  shift: string;
  shift_hours: string;
  load_status: string;
  load_percentage: number;
  available: string;
}

export interface ZoneStats {
  zone: string;
  total_workers: number;
  available_workers: number;
  unavailable_workers: number;
  load_distribution: {
    low: number;
    medium: number;
    high: number;
  };
  average_load_percentage: number;
  shifts?: {
    morning: number;
    afternoon: number;
  };
}

export interface SearchResult {
  status: string;
  query?: string;
  excluded_zone?: string;
  count?: number;
  workers?: any[];
  message?: string;
}

export interface RecommendationResponse {
  status: string;
  recommendations: string;
  input: string;
}

export const workersApi = {
  // Get all workers
  getAll: () => api.get<Worker[]>('/api/workers'),
  
  // Get worker by ID
  getById: (id: string) => api.get<Worker>(`/api/workers/${id}`),
  
  // Get zone statistics
  getZoneStats: (zone: string) => api.get<ZoneStats>(`/api/zones/${zone}`),
  
  // Get all zones statistics
  getAllZonesStats: () => api.get<Record<string, any>>('/api/zones'),
  
  // Search workers
  search: (query: string, excludeZone?: string) => 
    api.post<SearchResult>('/api/search', { 
      query, 
      exclude_zone: excludeZone 
    }),
  
  // Get AI recommendations
  getRecommendations: (managerInput: string) => 
    api.post<RecommendationResponse>('/api/recommendations', { 
      manager_input: managerInput 
    }),
  
  // Health check
  healthCheck: () => api.get('/'),
};

// Made with Bob
