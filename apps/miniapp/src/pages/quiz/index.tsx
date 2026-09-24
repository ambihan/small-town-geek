import { useEffect, useState } from "react";
import { Text, View } from "@tarojs/components";

import { fetchDailyQuestions } from "@/services/quiz";
import type { Question } from "@/services/types";

import "./index.scss";

export default function Quiz() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    fetchDailyQuestions().then(setQuestions);
  }, []);

  const question = questions[current];
  const answered = selected !== null;

  const onSelect = (key: string) => {
    if (answered) return;
    setSelected(key);
  };

  const next = () => {
    setSelected(null);
    setCurrent((c) => (c + 1) % Math.max(questions.length, 1));
  };

  if (!question) {
    return (
      <View className="page">
        <Text className="empty">正在加载题目…</Text>
      </View>
    );
  }

  return (
    <View className="page quiz">
      <Text className="quiz__progress">
        第 {current + 1} / {questions.length} 题
      </Text>
      <Text className="quiz__content">{question.content}</Text>

      <View className="options">
        {question.options.map((opt) => {
          const isAnswer = opt.key === question.answer;
          const isPicked = opt.key === selected;
          let cls = "option";
          if (answered && isAnswer) cls += " option--correct";
          else if (answered && isPicked) cls += " option--wrong";
          return (
            <View
              key={opt.key}
              className={cls}
              onClick={() => onSelect(opt.key)}
            >
              <Text className="option__key">{opt.key}</Text>
              <Text className="option__text">{opt.content}</Text>
            </View>
          );
        })}
      </View>

      {answered && (
        <View className="explain">
          <Text className="explain__title">
            {selected === question.answer ? "回答正确 🎉" : "回答错误"}
          </Text>
          <Text className="explain__text">{question.explanation}</Text>
          <View className="next-btn" onClick={next}>
            <Text className="next-btn__text">下一题</Text>
          </View>
        </View>
      )}
    </View>
  );
}
