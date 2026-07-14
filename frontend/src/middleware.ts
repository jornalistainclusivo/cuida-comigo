import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("cc_access_token")?.value;
  const { pathname } = request.nextUrl;

  // Protected routes — require authentication
  const isProtectedRoute =
    pathname === "/dashboard" ||
    pathname.startsWith("/medicamentos") ||
    pathname.startsWith("/agenda") ||
    pathname.startsWith("/arquivo") ||
    pathname.startsWith("/perfil") ||
    pathname.startsWith("/notificacoes") ||
    pathname === "/onboarding";

  // Auth routes — redirect to dashboard if already logged in
  const isAuthRoute = pathname === "/login";

  if (isProtectedRoute && !token) {
    const loginUrl = new URL("/login", request.url);
    return NextResponse.redirect(loginUrl);
  }

  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}


// Config to specify matching paths
export const config = {
  matcher: [
    "/dashboard",
    "/medicamentos/:path*",
    "/agenda/:path*",
    "/arquivo/:path*",
    "/perfil/:path*",
    "/notificacoes/:path*",
    "/onboarding",
    "/login",
  ],
};
