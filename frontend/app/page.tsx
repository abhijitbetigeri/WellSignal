"use client";
import { useState } from "react";
import SignalCard from "@/components/SignalCard";
import BundleCard from "@/components/BundleCard";
import OutreachCard from "@/components/OutreachCard";
import SourceBreakdown from "@/components/SourceBreakdown";

type Mode = "operator" | "corporate";

const TABS = ["signals", "analysis", "bundles", "outreach"] as const;
type Tab = typeof TABS[number];

export default function Dashboard() {
  const [mode, setMode] = useState<Mode>("operator");
  const [tab, setTab] = useState<Tab>("signals");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  // Operator form
  const [location, setLocation] = useState("san-francisco");
  const [category, setCategory] = useState("yoga");

  // Corporate form
  const [company, setCompany] = useState("Stripe");
  const [industry, setIndustry] = useState("technology");
  const [employees, setEmployees] = useState("200");
  const [corpLocation, setCorpLocation] = useState("San Francisco");

  const run = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    setTab("signals");

    const payload =
      mode === "operator"
        ? { mode, location, category }
        : { mode, company_name: company, industry, employee_count: parseInt(employees), location: corpLocation };

    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
      setTab("signals");
    } catch (e: any) {
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const signals = result?.signals || [];
  const analysis = result?.competitor_analysis || {};
  const bundles = result?.bundles || [];
  const outreach = result?.outreach_drafts || [];

  const tabCount: Record<Tab, number> = {
    signals: signals.length,
    analysis: Object.keys(analysis).filter(k => k !== "error").length,
    bundles: bundles.length,
    outreach: outreach.length,
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      {/* Header */}
      <header className="border-b border-white/10 bg-white/[0.02] backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-emerald-500 flex items-center justify-center text-sm font-bold">W</div>
            <div>
              <div className="font-bold text-lg leading-none">WellSignal</div>
              <div className="text-xs text-white/40">GTM Intelligence · Bright Data + Claude</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-white/50">Live data</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        {/* Mode toggle + form */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
          {/* Mode switcher */}
          <div className="flex gap-2 mb-6">
            {(["operator", "corporate"] as Mode[]).map((m) => (
              <button key={m} onClick={() => { setMode(m); setResult(null); }}
                className={`px-5 py-2 rounded-xl text-sm font-semibold transition-all ${
                  mode === m
                    ? "bg-gradient-to-r from-violet-600 to-emerald-600 text-white shadow-lg"
                    : "bg-white/10 text-white/60 hover:text-white hover:bg-white/15"
                }`}>
                {m === "operator" ? "🧘 Wellness Operator" : "🏢 Corporate HR"}
              </button>
            ))}
          </div>

          {/* Forms */}
          {mode === "operator" ? (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="text-xs text-white/50 uppercase tracking-wider block mb-2">Location</label>
                <input value={location} onChange={e => setLocation(e.target.value)}
                  placeholder="san-francisco"
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-sm text-white placeholder-white/30 focus:outline-none focus:border-violet-400 transition-colors" />
              </div>
              <div>
                <label className="text-xs text-white/50 uppercase tracking-wider block mb-2">Wellness Category</label>
                <select value={category} onChange={e => setCategory(e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-violet-400 transition-colors">
                  {["yoga", "meditation", "breathwork", "pilates", "dance", "coaching", "retreat", "fitness"].map(c => (
                    <option key={c} value={c} className="bg-[#1a1a2e]">{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-end">
                <button onClick={run} disabled={loading}
                  className="w-full py-3 rounded-xl bg-gradient-to-r from-violet-600 to-emerald-600 hover:from-violet-500 hover:to-emerald-500 text-white font-semibold text-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg">
                  {loading ? "⏳ Analyzing..." : "🔍 Analyze Market"}
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { label: "Company Name", value: company, set: setCompany, placeholder: "Stripe" },
                { label: "Industry", value: industry, set: setIndustry, placeholder: "technology" },
                { label: "Employees", value: employees, set: setEmployees, placeholder: "200" },
                { label: "Location", value: corpLocation, set: setCorpLocation, placeholder: "San Francisco" },
              ].map(({ label, value, set, placeholder }) => (
                <div key={label}>
                  <label className="text-xs text-white/50 uppercase tracking-wider block mb-2">{label}</label>
                  <input value={value} onChange={e => set(e.target.value)} placeholder={placeholder}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-sm text-white placeholder-white/30 focus:outline-none focus:border-emerald-400 transition-colors" />
                </div>
              ))}
              <div className="sm:col-span-2 lg:col-span-4">
                <button onClick={run} disabled={loading}
                  className="w-full py-3 rounded-xl bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white font-semibold text-sm transition-all disabled:opacity-50 shadow-lg">
                  {loading ? "⏳ Building Wellness Plan..." : "🏢 Generate Wellness Recommendations"}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-300 text-sm">
            ❌ {error}
          </div>
        )}

        {/* Loading skeleton */}
        {loading && (
          <div className="space-y-4 animate-pulse">
            <div className="grid grid-cols-3 gap-4">
              {[1,2,3].map(i => <div key={i} className="skeleton h-24 rounded-2xl" />)}
            </div>
            <div className="grid grid-cols-2 gap-4">
              {[1,2].map(i => <div key={i} className="skeleton h-48 rounded-2xl" />)}
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="space-y-6">
            {/* Summary stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { label: "Signals Scraped", value: signals.length, icon: "📡", color: "from-violet-600/20" },
                { label: "Market Gaps", value: analysis.market_gaps?.length || 0, icon: "🎯", color: "from-amber-600/20" },
                { label: "Bundles Ready", value: bundles.length, icon: "📦", color: "from-emerald-600/20" },
                { label: "Outreach Drafts", value: outreach.length, icon: "✉️", color: "from-blue-600/20" },
              ].map(({ label, value, icon, color }) => (
                <div key={label} className={`bg-gradient-to-br ${color} to-transparent border border-white/10 rounded-2xl p-4 text-center`}>
                  <div className="text-3xl mb-1">{icon}</div>
                  <div className="text-2xl font-bold text-white">{value}</div>
                  <div className="text-xs text-white/50 mt-0.5">{label}</div>
                </div>
              ))}
            </div>

            {/* Tabs */}
            <div className="flex gap-1 bg-white/5 border border-white/10 rounded-xl p-1 w-fit">
              {TABS.map(t => (
                <button key={t} onClick={() => setTab(t)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all capitalize flex items-center gap-2 ${
                    tab === t ? "bg-white/15 text-white" : "text-white/50 hover:text-white"
                  }`}>
                  {t}
                  {tabCount[t] > 0 && (
                    <span className={`text-xs px-1.5 py-0.5 rounded-full ${tab === t ? "bg-white/20" : "bg-white/10"}`}>
                      {tabCount[t]}
                    </span>
                  )}
                </button>
              ))}
            </div>

            {/* Tab: Signals */}
            {tab === "signals" && (
              <div className="space-y-6">
                <SourceBreakdown signals={signals} />
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {signals.map((s: any, i: number) => <SignalCard key={i} signal={s} />)}
                </div>
              </div>
            )}

            {/* Tab: Analysis */}
            {tab === "analysis" && (
              <div className="space-y-4">
                {analysis.error ? (
                  <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-300 text-sm">{analysis.error}</div>
                ) : (
                  <>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Market gaps */}
                      <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                        <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">🎯 Market Gaps ({analysis.market_gaps?.length})</div>
                        <ul className="space-y-2">
                          {analysis.market_gaps?.map((g: string, i: number) => (
                            <li key={i} className="flex items-start gap-2 text-sm text-white/80">
                              <span className="text-amber-400 mt-0.5 shrink-0">◆</span>{g}
                            </li>
                          ))}
                        </ul>
                      </div>
                      {/* Rising categories */}
                      <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                        <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">📈 Rising Categories</div>
                        <ul className="space-y-2">
                          {analysis.rising_categories?.map((c: string, i: number) => (
                            <li key={i} className="flex items-start gap-2 text-sm text-white/80">
                              <span className="text-emerald-400 mt-0.5 shrink-0">▲</span>{c}
                            </li>
                          ))}
                        </ul>
                      </div>
                      {/* Recommendations */}
                      <div className="md:col-span-2 bg-white/5 border border-white/10 rounded-2xl p-6">
                        <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">💡 Recommendations</div>
                        <ul className="space-y-3">
                          {analysis.recommendations?.map((r: string, i: number) => (
                            <li key={i} className="flex items-start gap-3 text-sm text-white/80">
                              <span className="bg-violet-500/20 text-violet-300 text-xs px-2 py-0.5 rounded-full shrink-0 mt-0.5">{i+1}</span>{r}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    {/* Summary */}
                    {analysis.summary && (
                      <div className="bg-gradient-to-br from-violet-600/10 to-emerald-600/10 border border-white/10 rounded-2xl p-6">
                        <div className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-2">Executive Summary</div>
                        <p className="text-white/80 leading-relaxed">{analysis.summary}</p>
                      </div>
                    )}
                  </>
                )}
              </div>
            )}

            {/* Tab: Bundles */}
            {tab === "bundles" && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                {bundles.length === 0
                  ? <p className="text-white/40 text-sm col-span-3">No bundles generated yet.</p>
                  : bundles.map((b: any, i: number) => <BundleCard key={i} bundle={b} index={i} mode={mode} />)}
              </div>
            )}

            {/* Tab: Outreach */}
            {tab === "outreach" && (
              <div className="space-y-4">
                {outreach.length === 0
                  ? <div className="bg-white/5 border border-white/10 rounded-2xl p-8 text-center text-white/40 text-sm">
                      Outreach drafts are generated in Corporate HR mode only.
                    </div>
                  : outreach.map((e: any, i: number) => <OutreachCard key={i} email={e} index={i} />)}
              </div>
            )}

            {/* ROI summary (corporate only) */}
            {mode === "corporate" && result.roi_summary && (
              <div className="bg-gradient-to-br from-emerald-600/15 to-teal-600/10 border border-emerald-500/30 rounded-2xl p-6">
                <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-2">💰 ROI Summary</div>
                <p className="text-white/80 leading-relaxed">{result.roi_summary}</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
