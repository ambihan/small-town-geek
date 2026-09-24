export default defineAppConfig({
  pages: [
    "pages/index/index",
    "pages/quiz/index",
    "pages/mistakes/index",
    "pages/learning/index",
    "pages/profile/index",
  ],
  window: {
    backgroundTextStyle: "light",
    navigationBarBackgroundColor: "#ffffff",
    navigationBarTitleText: "小镇做题家",
    navigationBarTextStyle: "black",
  },
  tabBar: {
    color: "#8a8a8a",
    selectedColor: "#f97316",
    backgroundColor: "#ffffff",
    borderStyle: "black",
    // 说明：V0.1 暂不放置 tabBar 图标（避免引入二进制资源），
    // 微信端将以纯文字展示。后续可在 src/assets 下补充 iconPath。
    list: [
      { pagePath: "pages/index/index", text: "首页" },
      { pagePath: "pages/quiz/index", text: "刷题" },
      { pagePath: "pages/mistakes/index", text: "错题" },
      { pagePath: "pages/learning/index", text: "学习" },
      { pagePath: "pages/profile/index", text: "我的" },
    ],
  },
});
