"use client";
import { useState } from "react";

export default function OutreachCard({ email, index }: { email: any; index: number }) {
  const [copied, setCopied] = useState(false);

  const copyEmail = () => {
    navigator.clipboard.writeText(`Subject: ${email.subject}\n\n${email.body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white/5 border border-white/10 rounded-2xl p-6 animate-slide-up"
         style={{ animationDelay: `${index * 100}ms` }}>
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="text-xs text-white/50 mb-1">To: {email.target_role} @ {email.target_company}</div>
          <div className="font-semibold text-white">📧 {email.subject}</div>
        </div>
        <button onClick={copyEmail}
          className="shrink-0 text-xs bg-white/10 hover:bg-white/20 text-white/70 hover:text-white px-3 py-1.5 rounded-lg transition-all">
          {copied ? "✅ Copied" : "Copy"}
        </button>
      </div>
      <p className="text-sm text-white/70 leading-relaxed whitespace-pre-line border-t border-white/10 pt-4">{email.body}</p>
      {email.signal_used && (
        <div className="mt-3 text-xs text-white/40 italic">Signal used: {email.signal_used}</div>
      )}
    </div>
  );
}
