"use client";

const URGENCY_COLORS: Record<string, string> = {
  high:   "bg-red-500/20 text-red-300 border-red-500/40",
  medium: "bg-yellow-500/20 text-yellow-300 border-yellow-500/40",
  low:    "bg-green-500/20 text-green-300 border-green-500/40",
};

const SOURCE_COLORS: Record<string, string> = {
  classpass:  "bg-purple-500/20 text-purple-300",
  eventbrite: "bg-orange-500/20 text-orange-300",
  luma:       "bg-pink-500/20 text-pink-300",
  reddit:     "bg-red-500/20 text-red-300",
  linkedin:   "bg-blue-500/20 text-blue-300",
  serp:       "bg-cyan-500/20 text-cyan-300",
};

const TYPE_ICONS: Record<string, string> = {
  demand_spike:    "📈",
  competitor_move: "🎯",
  corporate_buyer: "🏢",
  review_trend:    "⭐",
  general:         "📡",
};

export default function SignalCard({ signal }: { signal: any }) {
  const d = signal.data || {};
  const label = d.name || d.title || d.job_title || d.query || "Signal";
  const sub = d.location || d.date || d.start_at?.slice(0, 10) || d.company_name || "";

  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4 hover:border-white/20 transition-all animate-slide-up">
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2 flex-wrap">
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SOURCE_COLORS[signal.source] || "bg-gray-500/20 text-gray-300"}`}>
            {signal.source}
          </span>
          {signal.wellness_category && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300">
              {signal.wellness_category}
            </span>
          )}
        </div>
        {signal.urgency && (
          <span className={`text-xs px-2 py-0.5 rounded-full border font-semibold ${URGENCY_COLORS[signal.urgency] || ""}`}>
            {signal.urgency}
          </span>
        )}
      </div>

      <div className="flex items-start gap-2">
        <span className="text-lg">{TYPE_ICONS[signal.signal_type] || "📡"}</span>
        <div>
          <p className="text-sm font-medium text-white leading-snug line-clamp-2">{label}</p>
          {sub && <p className="text-xs text-white/50 mt-0.5">{sub}</p>}
          {signal.summary && (
            <p className="text-xs text-white/60 mt-1 leading-relaxed line-clamp-2">{signal.summary}</p>
          )}
        </div>
      </div>
    </div>
  );
}
