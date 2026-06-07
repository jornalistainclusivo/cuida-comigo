/**
 * Service Worker — Orquestração do Cuidado (PWA)
 *
 * Strategy:
 *   - Cache-First:  Medication protocols (critical offline data)
 *   - Network-First: Tasks (frequently updated, needs freshness)
 *   - Stale-While-Revalidate: Static assets (CSS, JS, fonts)
 */

const CACHE_NAME = "cuidado-v1";
const STATIC_ASSETS = ["/", "/manifest.json"];

// ── Install: pre-cache static shell ───────────────────────────────

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// ── Activate: clean old caches ────────────────────────────────────

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// ── Fetch: route-based caching strategy ───────────────────────────

self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== "GET") return;

  // Strategy 1: Cache-First for medication protocols (critical offline)
  if (url.pathname.includes("/protocols")) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Strategy 2: Network-First for tasks (need freshness)
  if (url.pathname.includes("/tasks")) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Strategy 3: Stale-While-Revalidate for static assets
  if (
    request.destination === "style" ||
    request.destination === "script" ||
    request.destination === "font" ||
    request.destination === "image"
  ) {
    event.respondWith(staleWhileRevalidate(request));
    return;
  }

  // Default: Network-First
  event.respondWith(networkFirst(request));
});

// ── Caching Strategies ────────────────────────────────────────────

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response(
      JSON.stringify({ detail: "Offline — dados em cache indisponíveis." }),
      {
        status: 503,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;

    return new Response(
      JSON.stringify({ detail: "Offline — sem dados em cache." }),
      {
        status: 503,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(request);

  const fetchPromise = fetch(request)
    .then((response) => {
      if (response.ok) {
        cache.put(request, response.clone());
      }
      return response;
    })
    .catch(() => cached);

  return cached || fetchPromise;
}
