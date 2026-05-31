"use client";

const COLORS: Record<string, string> = {
  classpass:  "#8b5cf6",
  eventbrite: "#f97316",
  luma:       "#ec4899",
  reddit:     "#ef4444",
  linkedin:   "#3b82f6",
  serp:       "#06b6d4",
};

export default function SourceBreakdown({ signals }: { signals: any[] }) {
  const counts: Record<string, number> = {};
  const urgency: Record<string, number> = { high: 0, medium: 0, low: 0 };
  const categories: Record<string, number> = {};

  for (const s of signals) {
    counts[s.source] = (counts[s.source] || 0) + 1;
    if (s.urgency) urgency[s.urgency] = (urgency[s.urgency] || 0) + 1;
    if (s.wellness_category) categories[s.wellness_category] = (categories[s.wellness_category] || 0) + 1;
  }

  const total = signals.length;
  const topCategories = Object.entries(categories).sort((a, b) => b[1] - a[1]).slice(0, 5);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* Source breakdown */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-5">
        <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">By Source</div>
        <div className="space-y-2">
          {Object.entries(counts).map(([src, cnt]) => (
            <div key={src}>
              <div className="flex justify-between text-sm mb-1">
                <span className="capitalize text-white/70">{src}</span>
                <span className="text-white font-medium">{cnt}</span>
              </div>
              <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div className="h-full rounded-full transition-all"
                     style={{ width: `${(cnt / total) * 100}%`, background: COLORS[src] || "#6b7280" }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Urgency */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-5">
        <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">By Urgency</div>
        <div className="flex flex-col gap-3">
          {[["high", "#ef4444"], ["medium", "#eab308"], ["low", "#22c55e"]].map(([u, color]) => (
            <div key={u} className="flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: color }} />
              <div className="flex-1">
                <div className="flex justify-between text-sm mb-1">
                  <span className="capitalize text-white/70">{u}</span>
                  <span className="text-white font-medium">{urgency[u] || 0}</span>
                </div>
                <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${((urgency[u] || 0) / total) * 100}%`, background: color }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top categories */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-5">
        <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">Top Categories</div>
        <div className="space-y-2">
          {topCategories.map(([cat, cnt]) => (
            <div key={cat} className="flex items-center justify-between">
              <span className="text-sm capitalize text-white/70">{cat}</span>
              <div className="flex items-center gap-2">
                <div className="w-16 h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-400 rounded-full"
                       style={{ width: `${(cnt / (topCategories[0][1])) * 100}%` }} />
                </div>
                <span className="text-sm text-white font-medium w-6 text-right">{cnt}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
