/**
 * Serves public/ from Workers Static Assets (binding ASSETS), adding the fleet's
 * security headers and no-cache on HTML. Every request runs through here
 * (run_worker_first in wrangler.toml). Asset reads are not KV operations.
 *
 * CSP allows: MapLibre (cdnjs), deck.gl (unpkg), Google Fonts, Mapbox styles/tiles/sprites/
 * glyphs (api.mapbox.com, *.tiles.mapbox.com), OpenFreeMap keyless tiles, and Umami if set.
 */

const CSP = [
  "default-src 'self'",
  // static.cloudflareinsights.com: the zone's Cloudflare Web Analytics beacon, auto-injected at the edge.
  "script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com unpkg.com analytics.devlab502.net static.cloudflareinsights.com",
  "style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com",
  "font-src fonts.gstatic.com",
  "img-src 'self' data: blob: api.mapbox.com *.tiles.mapbox.com tiles.openfreemap.org",
  "connect-src 'self' api.mapbox.com *.tiles.mapbox.com events.mapbox.com tiles.openfreemap.org analytics.devlab502.net cloudflareinsights.com static.cloudflareinsights.com",
  "worker-src blob:",
  "child-src blob:",
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "object-src 'none'",
].join('; ');

function addSecurityHeaders(headers) {
  headers.set('X-Content-Type-Options', 'nosniff');
  headers.set('X-Frame-Options', 'DENY');
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  headers.set('Content-Security-Policy', CSP);
}

function injectAnalytics(response, env) {
  const ct = response.headers.get('content-type') || '';
  if (ct.includes('text/html') && env.UMAMI_SITE_ID) {
    return new HTMLRewriter()
      .on('head', {
        element(el) {
          el.append(`<script defer src="https://analytics.devlab502.net/script.js" data-website-id="${env.UMAMI_SITE_ID}"></script>`, { html: true });
        },
      })
      .transform(response);
  }
  return response;
}

function isHtml(path, response) {
  return (
    !path.includes('.') ||
    path.endsWith('.html') ||
    (response.headers.get('content-type') || '').includes('text/html')
  );
}

export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    const asset = await env.ASSETS.fetch(request);
    const headers = new Headers(asset.headers);
    addSecurityHeaders(headers);
    if (isHtml(path, asset)) headers.set('Cache-Control', 'no-cache');
    else if (path.startsWith('/data/')) headers.set('Cache-Control', 'public, max-age=86400');
    const response = new Response(asset.body, {
      status: asset.status,
      statusText: asset.statusText,
      headers,
    });
    return injectAnalytics(response, env);
  },
};
