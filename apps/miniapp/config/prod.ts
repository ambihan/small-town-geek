import type { UserConfigExport } from "@tarojs/cli";

export default {
  mini: {},
  h5: {
    /**
     * 生产环境如需分析包体积，可开启：
     * webpackChain (chain) { chain.plugin('analyzer').use(BundleAnalyzerPlugin, []) }
     */
  },
} satisfies UserConfigExport;
