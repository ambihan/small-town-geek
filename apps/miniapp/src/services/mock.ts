import type {
  DailySummary,
  KnowledgeStat,
  MistakeItem,
  Question,
} from "./types";

export const mockDailySummary: DailySummary = {
  totalQuestions: 10,
  finishedToday: 3,
  streakDays: 5,
};

export const mockQuestions: Question[] = [
  {
    id: "q1",
    content: "以下哪个是 Python 中不可变（immutable）类型？",
    options: [
      { key: "A", content: "list" },
      { key: "B", content: "dict" },
      { key: "C", content: "tuple" },
      { key: "D", content: "set" },
    ],
    answer: "C",
    explanation: "tuple 是不可变类型，创建后不能修改其元素。",
    knowledgePoint: "Data Types / Tuple",
  },
  {
    id: "q2",
    content: "表达式 `len('小镇做题家')` 的结果是？",
    options: [
      { key: "A", content: "4" },
      { key: "B", content: "5" },
      { key: "C", content: "6" },
      { key: "D", content: "报错" },
    ],
    answer: "B",
    explanation: "字符串长度按字符计，共 5 个中文字符。",
    knowledgePoint: "Data Types / String",
  },
];

export const mockMistakes: MistakeItem[] = [
  {
    id: "m1",
    questionContent: "Python 中 `is` 与 `==` 的区别？",
    knowledgePoint: "Object / Identity",
    wrongCount: 2,
  },
  {
    id: "m2",
    questionContent: "列表推导式与生成器表达式的差异？",
    knowledgePoint: "Function / Comprehension",
    wrongCount: 1,
  },
];

export const mockKnowledgeStats: KnowledgeStat[] = [
  { id: "k1", name: "Data Types", masteryScore: 0.82 },
  { id: "k2", name: "Function", masteryScore: 0.64 },
  { id: "k3", name: "OOP", masteryScore: 0.41 },
  { id: "k4", name: "Async", masteryScore: 0.2 },
];
