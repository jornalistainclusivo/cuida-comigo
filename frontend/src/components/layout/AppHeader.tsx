"use client";

import { usePathname } from "next/navigation";
import { Navigation } from "@/components/Navigation";

interface AppHeaderProps {
  isLoggedIn?: boolean;
}

export function AppHeader({ isLoggedIn = false }: AppHeaderProps) {
  const pathname = usePathname();

  // Hide the internal app header on the public Landing Page
  if (pathname === "/") return null;

  return <Navigation isLoggedIn={isLoggedIn} />;
}
