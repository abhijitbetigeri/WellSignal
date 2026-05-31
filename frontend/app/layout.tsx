import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "WellSignal — GTM Intelligence for Wellness",
  description: "Real-time market intelligence for wellness operators and corporate HR teams",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-[#0a0a0f] text-white">{children}</body>
    </html>
  );
}
