import type { Metadata, Viewport } from "next";
import Link from "next/link";
import { SkipLink } from "@/components/SkipLink";
import "./globals.css";

export const metadata: Metadata = {
  title: "Orquestração do Cuidado",
  description:
    "Plataforma de gestão compartilhada para descentralizar a carga cognitiva e operacional de cuidadores informais.",
  manifest: "/manifest.json",
  applicationName: "Orquestração do Cuidado",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Cuidado",
  },
};

export const viewport: Viewport = {
  themeColor: "#0D4F4F",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <link rel="apple-touch-icon" href="/icons/icon-192.png" />
        {/* Service Worker registration */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                  navigator.serviceWorker.register('/sw.js')
                    .catch(() => { /* SW registration failed — non-blocking */ });
                });
              }
            `,
          }}
        />
      </head>
      <body>
        <SkipLink />

        <header>
          <nav aria-label="Navegação principal">
            <Link href="/" aria-current="page">
              <strong>Cuidado</strong>
            </Link>
          </nav>
        </header>

        <main id="main-content" tabIndex={-1}>
          {children}
        </main>

        <footer>
          <p>
            <small>
              © {new Date().getFullYear()} Orquestração do Cuidado — JINC Apps
            </small>
          </p>
        </footer>
      </body>
    </html>
  );
}
