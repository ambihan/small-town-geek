import { BookOpen, Users, Lightbulb } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const stats = [
  { label: "题目", value: 0, icon: BookOpen },
  { label: "用户", value: 0, icon: Users },
  { label: "知识点", value: 0, icon: Lightbulb },
] as const;

export default function Home() {
  return (
    <main className="container py-12">
      <header className="mb-10">
        <h1 className="text-3xl font-bold tracking-tight">小镇做题家</h1>
        <p className="mt-1 text-muted-foreground">Admin Dashboard</p>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {stats.map(({ label, value, icon: Icon }) => (
          <Card key={label}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle>{label}</CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{value}</div>
            </CardContent>
          </Card>
        ))}
      </section>
    </main>
  );
}
