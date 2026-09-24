import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "小镇做题家 · Admin",
  description: "小镇做题家管理后台",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
