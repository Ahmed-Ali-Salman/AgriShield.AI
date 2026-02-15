import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Auth middleware — redirects unauthenticated users to /login.
 *
 * Note: JWT is stored in localStorage (client-side), so this middleware
 * checks for an `auth_token` cookie that the login page sets.
 * For a more robust approach, use HTTP-only cookies for the JWT.
 */
export function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl;

    // Public routes that don't require authentication
    const publicPaths = ['/login', '/register'];
    if (publicPaths.some((p) => pathname.startsWith(p))) {
        return NextResponse.next();
    }

    // Check for auth token cookie
    const token = request.cookies.get('auth_token')?.value;
    if (!token && pathname.startsWith('/dashboard')) {
        return NextResponse.redirect(new URL('/login', request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/dashboard/:path*'],
};
