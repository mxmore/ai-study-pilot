export async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...init
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export interface Question {
  id: string;
  prompt: string;
  question_type: string;
  options?: { label: string; value: string }[];
  solution?: string;
  difficulty?: number;
  knowledge_codes: string[];
}

export async function getQuestions(): Promise<Question[]> {
  return fetchJSON<Question[]>('/api/questions');
}
