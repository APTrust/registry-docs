# Authentication

Registry supports two types of authentication: a sign-in based scheme for users accessing the Web UI and a token-based scheme for API consumers accessing the member or admin API.

## Web UI

While the `UserSignInShow()` and `UserSignIn()` methods of the  [Users Controller](https://github.com/APTrust/registry/blob/master/web/webui/users_controller.go){target=_blank} handle the sign-in process, the [Authentication middleware](https://github.com/APTrust/registry/blob/master/middleware/authenticate.go){target=_blank} checks the session cookie on subsequent requests.

The session cookie contains an encrypted User ID, which the authentication middleware uses to look up the user record. It then stores the User object in the Gin context for later access.

The authentication middleware ensures the following:

1. That the request includes a valid user session cookie with a valid user if the request tries to access a protected resource. See below for a list of resources that do not require authentication.
2. That the user will be forced to complete the password change process before accessing any other resources, if the user happens to be in the middle of the password change process.
3. That the user will be forced to complete the second step of two-factor authentication before accessing any other resources, if they have logged in with their email and password and have not yet completed the second step of two-factor auth.

### Endpoints Exempt from Authorization

The [middleware/authentication.go](https://github.com/APTrust/registry/blob/master/middleware/authenticate.go){target=_blank} includes a function called `ExemptFromAuth()` to check whether the current request is exempt from authentication. Currently, the following endpoints are exempt:

| Endpoint | Explanation |
| -------- | ----------- |
| /users/sign_in | Users obviously won't be logged in when they go to the sign-in page. They have to be able to see it to log in. |
| /users/sign_out | This page tells the user they've signed out. |
| /users/forgot_password | This page is for users who have forgotten their password and received a password-reset email. The page includes a text input for them to enter the password reset token we sent them. |
| /users/complete_password_reset/ | After entering their reset token, users choose a new password on this page. The app includes security measures to prevent people accessing this page without having previously entered the reset token. |
| /ui-components | This page displays a gallery of UI components, for developer reference. It's static and contains no sensitive information. |
| /static/* | This is the prefix for all static resources, including scripts, stylesheets, icons and fonts. |
| /favicon/* | This returns the site's favicon. |
| /error | This page displayes errors, including errors telling you you need to log in. |

## API

If the Authentication middleware detects that the user has requested an API endpoint rather than a web endpoint, the `GetUserFromAPIHeaders()` function extracts the header values for `X-Pharos-API-User` and `X-Pharos-API-Key` and loads the user based on their API key.

## Default Headers

The Authentication middleware also sets some default headers for every request. We want to set these here because we want to those headers even when authenticaion fails and the auth middleware responds directly to the user.

We set the following headers in `SetDefaultHeaders()`:

| Name | Value | Description |
| ---- | ----- | ----------- |
| Cache-Control | no-cache | Tells browsers and proxies not to cache responses. This is set only for dynamic content, not for static content like scripts, stylesheets and images. |
| Pragma | no-store | Same as Cache-Control above, but for really old browsers. |
| Strict-Transport-Security | max-age=31536000 | Forces clients to use HTTPS instead of HTTP. |
| X-XSS-Protection | 1 | Instructs browsers to stop loading or sanitize the page if they detect a cross-site scripting attack. |
| X-Content-Type-Options | "nosniff" | Blocks content sniffing that could transform non-executable MIME types into executable MIME types. |
| Content-Security-Policy | "default-src 'self'; font-src 'self' fonts.gstatic.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com; script-src 'self' 'unsafe-inline'" | Prevents some cross-site scripting and data injection attacks. The policy spelled out in the value of this header says the browser should trust scripts, fonts, and stylesheets from our own domain. It should also accept fonts from Google's font serving domain, fonts.gstatic.com and CSS from fonts.googlapis.com. The `unsafe-inline` statements mean the browser should trust inline JavaScript from our domain and inline CSS from fonts.googleapis.com. Confirming browsers will reject fonts, scripts, and stylesheets from other sources. |
