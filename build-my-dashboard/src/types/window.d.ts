// Type declarations for backend integration
declare global {
  interface Window {
    healthData: {
      current: any;
      loading: boolean;
      error: string | null;
      userId: string;
      refreshInterval: number | null;
    };
    healthAPI: {
      fetchData: (userId?: string, numRecords?: number) => Promise<any>;
      startAutoRefresh: (intervalMs?: number) => void;
      stopAutoRefresh: () => void;
      getCurrentData: () => any;
      getBaseURL: () => string;
    };
  }
}

export {};
