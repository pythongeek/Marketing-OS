import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";

export const metadata: Metadata = {
  title: "AgenticMarketingPro Admin",
  description: "Visual admin backend for the AgenticMarketingPro operating system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-background text-text min-h-screen">
        <div className="flex">
          <AuthProvider>{children}</AuthProvider>
        </div>
      </body>
    </html>
  );
}
