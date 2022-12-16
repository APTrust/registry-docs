# Cross-Site Request Forgery

The [CSRF middleware](https://github.com/APTrust/registry/blob/master/middleware/csrf.go){target=_blank} is the last to run. It does the following:

1. Checks to see whether the request method is unsafe. Any method other than GET, HEAD, OPTIONS and TRACE is considered unsafe because it could add, delete, or alter data.
2. If the method is unsafe, it checks to ensure that the request includes matching CSRF tokens in the cookie headers and in the submitted form. If either token is missing, or if the tokens don't match, the server stops processing the request and returns an error.
3. This middleware will also reject unsafe requests coming from other domains.

For a concise description on how CSRF attacks work and how anti-forgery tokens can prevent them, see [Microsoft's CSRF write-up](https://learn.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks){target=_blank}.
