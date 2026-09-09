export type SearchMode = "quick" | "deep" | "compare" | "code" | "news";

export interface SearchSource {
  id: string;
  title: string;
  url: string;
  snippet: string;
  domain: string;
  score: number;
  published_at?: string | null;
}

export interface SearchResponse {
  session_id: string;
  query: string;
  mode: SearchMode;
  answer: string;
  sources: SearchSource[];
  evidence: { claim: string; source_ids: string[]; stance: string }[];
  trust: {
    band: string;
    score: number;
    source_count: number;
    domain_diversity: number;
    agreement_ratio: number;
    notes: string[];
  };
  trace: { name: string; status: string; detail: string }[];
}
