"use client";

const COLORS = [
  "from-violet-600/20 to-purple-600/10 border-violet-500/30",
  "from-emerald-600/20 to-teal-600/10 border-emerald-500/30",
  "from-amber-600/20 to-orange-600/10 border-amber-500/30",
];

export default function BundleCard({ bundle, index, mode }: { bundle: any; index: number; mode: string }) {
  const price = bundle.suggested_price || bundle.price_per_employee_monthly;
  const priceStr = typeof price === "number" ? `$${price}/employee/mo` : price;

  return (
    <div className={`bg-gradient-to-br ${COLORS[index % 3]} border rounded-2xl p-6 animate-slide-up`}
         style={{ animationDelay: `${index * 100}ms` }}>

      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-1">
            Bundle {index + 1}
          </div>
          <h3 className="text-lg font-bold text-white leading-tight">{bundle.bundle_name}</h3>
        </div>
        {priceStr && (
          <div className="text-right shrink-0">
            <div className="text-xs text-white/50 mb-0.5">Price</div>
            <div className="text-sm font-bold text-white bg-white/10 px-3 py-1 rounded-lg">{priceStr}</div>
          </div>
        )}
      </div>

      {/* Services */}
      {bundle.services?.length > 0 && (
        <div className="mb-4">
          <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-2">Includes</div>
          <div className="flex flex-wrap gap-1.5">
            {bundle.services.map((s: string, i: number) => (
              <span key={i} className="text-xs bg-white/10 text-white/80 px-2.5 py-1 rounded-full">{s}</span>
            ))}
          </div>
        </div>
      )}

      {/* Target */}
      {bundle.target_segment && (
        <div className="mb-3">
          <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-1">Target</div>
          <p className="text-sm text-white/70">{bundle.target_segment}</p>
        </div>
      )}

      {/* Market gap */}
      {bundle.competitor_gap && (
        <div className="mb-3 bg-white/5 rounded-xl p-3">
          <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-1">🎯 Market Gap</div>
          <p className="text-sm text-white/80 leading-relaxed">{bundle.competitor_gap}</p>
        </div>
      )}

      {/* Mode-specific extras */}
      {mode === "operator" && bundle.outreach_angle && (
        <div className="bg-white/5 rounded-xl p-3">
          <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-1">💬 Pitch Angle</div>
          <p className="text-sm text-white/80 italic">"{bundle.outreach_angle}"</p>
        </div>
      )}
      {mode === "corporate" && bundle.projected_roi && (
        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3 mt-2">
          <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1">💰 Projected ROI</div>
          <p className="text-sm text-emerald-300">{bundle.projected_roi}</p>
        </div>
      )}
    </div>
  );
}
