import { useEffect, useState } from "react";
import Taro from "@tarojs/taro";
import { Button, Text, View } from "@tarojs/components";

import { fetchDailySummary } from "@/services/quiz";
import type { DailySummary } from "@/services/types";

import "./index.scss";

export default function Index() {
  const [summary, setSummary] = useState<DailySummary | null>(null);

  useEffect(() => {
    fetchDailySummary().then(setSummary);
  }, []);

  const goQuiz = () => {
    Taro.switchTab({ url: "/pages/quiz/index" });
  };

  return (
    <View className="page home">
      <View className="hero">
        <Text className="hero__title">小镇做题家</Text>
        <Text className="hero__subtitle">今天也要认真刷 10 道题</Text>
      </View>

      <View className="stat-row">
        <View className="stat">
          <Text className="stat__num">{summary?.finishedToday ?? 0}</Text>
          <Text className="stat__label">今日已完成</Text>
        </View>
        <View className="stat">
          <Text className="stat__num">{summary?.totalQuestions ?? 0}</Text>
          <Text className="stat__label">今日目标</Text>
        </View>
        <View className="stat">
          <Text className="stat__num">{summary?.streakDays ?? 0}</Text>
          <Text className="stat__label">连续天数</Text>
        </View>
      </View>

      <Button className="primary-btn" onClick={goQuiz}>
        开始刷题
      </Button>
    </View>
  );
}
