# Default Headers

The Authentication middleware, which is the first to touch each request, also sets some default headers. We want to set these headers as soon as possible in the response lifecycle because we want to those headers to be present even when authenticaion fails and the auth middleware responds directly to the user.

Most of these headers are security-related, so we document them here. The Authentication middleware's `SetDefaultHeaders()` function sets the following:

| Name | Value | Description |
| ---- | ----- | ----------- |
| Cache-Control | no-cache | Tells browsers and proxies not to cache responses. This is set only for dynamic content, not for static content like scripts, stylesheets and images. |
| Pragma | no-store | Same as Cache-Control above, but for really old browsers. |
| Strict-Transport-Security | max-age=31536000 | Forces clients to use HTTPS instead of HTTP. |
| X-XSS-Protection | 1 | Instructs browsers to stop loading or sanitize the page if they detect a cross-site scripting attack. |
| X-Content-Type-Options | "nosniff" | Blocks content sniffing that could transform non-executable MIME types into executable MIME types. |
| Content-Security-Policy | "default-src 'self'; font-src 'self' fonts.gstatic.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com; script-src 'self' 'unsafe-inline'" | Prevents some cross-site scripting and data injection attacks. The policy spelled out in the value of this header says the browser should trust scripts, fonts, and stylesheets from our own domain. It should also accept fonts from Google's font serving domain, fonts.gstatic.com and CSS from fonts.googlapis.com. The `unsafe-inline` statements mean the browser should trust inline JavaScript from our domain and inline CSS from fonts.googleapis.com. Confirming browsers will reject fonts, scripts, and stylesheets from other sources. |
