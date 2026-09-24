import { Text, View } from "@tarojs/components";

import "./index.scss";

const mockUser = {
  nickname: "小镇做题家",
  joinedDays: 12,
  totalAnswered: 128,
  accuracy: 0.76,
};

export default function Profile() {
  return (
    <View className="page profile">
      <View className="avatar">
        <Text className="avatar__text">题</Text>
      </View>
      <Text className="nickname">{mockUser.nickname}</Text>
      <Text className="joined">已加入 {mockUser.joinedDays} 天</Text>

      <View className="metrics">
        <View className="metric">
          <Text className="metric__num">{mockUser.totalAnswered}</Text>
          <Text className="metric__label">累计答题</Text>
        </View>
        <View className="metric">
          <Text className="metric__num">
            {Math.round(mockUser.accuracy * 100)}%
          </Text>
          <Text className="metric__label">正确率</Text>
        </View>
      </View>
    </View>
  );
}
