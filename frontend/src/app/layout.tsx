import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AgriShield AI — Cyber-Resilient Food Supply Intelligence',
  description: 'Securing the digital backbone of food security with AI-powered risk scoring, anomaly detection, and real-time alerts.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang='en'>
      <body>{children}</body>
    </html>
  );
}
