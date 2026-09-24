import { useEffect, useState } from "react";
import { Text, View } from "@tarojs/components";

import { fetchMistakes } from "@/services/quiz";
import type { MistakeItem } from "@/services/types";

import "./index.scss";

export default function Mistakes() {
  const [items, setItems] = useState<MistakeItem[]>([]);

  useEffect(() => {
    fetchMistakes().then(setItems);
  }, []);

  return (
    <View className="page mistakes">
      <Text className="title">我的错题</Text>
      {items.map((item) => (
        <View key={item.id} className="card">
          <Text className="card__content">{item.questionContent}</Text>
          <View className="card__meta">
            <Text className="tag">{item.knowledgePoint}</Text>
            <Text className="count">错 {item.wrongCount} 次</Text>
          </View>
        </View>
      ))}
    </View>
  );
}
