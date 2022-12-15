# Security Overview

Registry's security system has three main components. Click on any link to learn more.

1. [Authentication](authentication.md) handles user logins, two-factor auth functions, and request-level identity verification.
2. [Authorization](authorization.md) handles endpoint and resource-level permission checks.
3. [CSRF](csrf.md) handles tokens to prevent cross-site request forgery (CSRF).

Aside from user login, all of these security features are implemented in middleware to ensure that security checks run before any request is handled. If any request hits an endpoint without first getting explicit approval from security middleware, the application will return an error and the request handler will not be called.

This pattern, inspired by the Rails devise gem, puts the onus on the developer to ensure security checks occur for each request. If the developer forgets to explicit add a security for a new request handler, no one will ever be able to reach that handler.

## About Middleware

The [Gin web framework](https://github.com/gin-gonic/gin){target=_blank} allows us to define middleware that executes before (and after) a request reaches our application's request handlers.

The `initMiddleware()` function in [application.go](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank} defines four middlewares to be executed in order.

The first is a general logger. It always passes control to the next middlware, which is [Authentication](authentication.md). If the authentication middleware determines the current user can proceed with the request, it passes control to the next middleware, which is authorization.

If the authenticated middleware determines the user cannot proceed with the request (because the request requires authentication and the user is missing a valid session cookie), it sends an error response and the request ends there. It never even reaches the authorization step.

The [Authorization](authorization.md) middleware checks to see if the user is authorized to perform the requested action or to access the requested resource. If so, it passes the request on to the CSRF middleware. If not, request processing ends here, with the middleware returning an error response to the user.

If the user is attempting a PUT or POST request, the [CSRF middleware](csrf.md) ensures that the request includes valid CSRF tokens. If a token is missing from the cookie or the form, or if the tokens don't match, processing end here with the CSRF middleware returning an error response.

Middlewares push requests to the next step of processing by calling the `Next()` function. Note that middlewares can touch the response object in the Gin context after calling `Next()`, though Registry does not do this. Maintainers can add post-processing in future generations of Registry if necessary.
