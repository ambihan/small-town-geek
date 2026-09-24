import { useEffect, useState } from "react";
import { Text, View } from "@tarojs/components";

import { fetchKnowledgeStats } from "@/services/quiz";
import type { KnowledgeStat } from "@/services/types";

import "./index.scss";

export default function Learning() {
  const [stats, setStats] = useState<KnowledgeStat[]>([]);

  useEffect(() => {
    fetchKnowledgeStats().then(setStats);
  }, []);

  return (
    <View className="page learning">
      <Text className="title">知识点掌握度</Text>
      {stats.map((item) => (
        <View key={item.id} className="row">
          <View className="row__head">
            <Text className="row__name">{item.name}</Text>
            <Text className="row__percent">
              {Math.round(item.masteryScore * 100)}%
            </Text>
          </View>
          <View className="bar">
            <View
              className="bar__fill"
              style={{ width: `${Math.round(item.masteryScore * 100)}%` }}
            />
          </View>
        </View>
      ))}
    </View>
  );
}
