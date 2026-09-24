export interface QuestionOption {
  key: string;
  content: string;
}

export interface Question {
  id: string;
  content: string;
  options: QuestionOption[];
  answer: string;
  explanation: string;
  knowledgePoint: string;
}

export interface MistakeItem {
  id: string;
  questionContent: string;
  knowledgePoint: string;
  wrongCount: number;
}

export interface KnowledgeStat {
  id: string;
  name: string;
  masteryScore: number;
}

export interface DailySummary {
  totalQuestions: number;
  finishedToday: number;
  streakDays: number;
}
