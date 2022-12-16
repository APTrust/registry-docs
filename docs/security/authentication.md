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
