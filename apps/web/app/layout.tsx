import type { Metadata, Viewport } from "next";
import "./globals.css";
import { PwaRegister } from "./pwa";

export const metadata: Metadata = {
  title: "PRAJNA — Agentic Search",
  description: "Evidence-first universal agentic search by Prajwal Devaraj",
  applicationName: "PRAJNA",
  manifest: "/manifest.webmanifest",
};

export const viewport: Viewport = {
  themeColor: "#090b10",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body><PwaRegister />{children}</body>
    </html>
  );
}
