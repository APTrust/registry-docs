# Security Overview

Registry's security system has three main components. Click on any link to learn more.

1. [Authentication](authentication.md) handles user logins, two-factor auth functions, and request-level identity verification.
2. [Authorization](authorization.md) handles endpoint and resource-level permission checks.
3. [CSRF](csrf.md) handles tokens to prevent cross-site request forgery (CSRF).

Aside from user login, all of these security features are implemented in middleware to ensure that security checks run before any request is handled. If any request hits an endpoint without first getting explicit approval from security middleware, the application will return an error and the request handler will not be called.

This pattern, inspired by the Rais devise gem, puts the onus on the developer to ensure security checks occur for each request. If the developer forgets to explicit add a security for a new request handler, no one will ever be able to reach that handler.
