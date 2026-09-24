import {
  mockDailySummary,
  mockKnowledgeStats,
  mockMistakes,
  mockQuestions,
} from "./mock";
import type {
  DailySummary,
  KnowledgeStat,
  MistakeItem,
  Question,
} from "./types";

/**
 * 业务 API 统一放在 services 层。V0.1 先返回 mock data，
 * 后续 Milestone 在此接入 FastAPI（禁止在页面里直接调用 Taro.request）。
 */

export async function fetchDailySummary(): Promise<DailySummary> {
  return Promise.resolve(mockDailySummary);
}

export async function fetchDailyQuestions(): Promise<Question[]> {
  return Promise.resolve(mockQuestions);
}

export async function fetchMistakes(): Promise<MistakeItem[]> {
  return Promise.resolve(mockMistakes);
}

export async function fetchKnowledgeStats(): Promise<KnowledgeStat[]> {
  return Promise.resolve(mockKnowledgeStats);
}
