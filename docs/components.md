# Code Components

The Registry app is built primarily on the [Gin web framework](https://github.com/gin-gonic/gin){target=_blank} and the [go-pg](https://github.com/go-pg/pg){target=_blank} ORM for Postgres.

Additional packages (listed in go.mod) include:

* aws-sdk-go for SES and SNS services (but not for S3 or Glacier)
* go-authy for authy push notifications used in two-factor login
* govalidator for data validation
* httpexpect for testing web and API requests
* nsq for talking to NSQ services
* redis for talking to Redis/Elasticache
* testify for unit and integration tests
* viper for reading config settings
* zerolog for logging

The headings below give a high-level overview of key files and components, describing where to find them, what they do, and how they fit into the system.

This page attempts to give an overview only. Components are described in more detail on dedicated pages.

## The Application File

The [application file](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank} includes essential setup and configuration steps to run the Registry app. This includes:

* Defining routes for the web UI, member API and admin API.
* Defining template helpers, which are functions that can be executed within HTML templates.
* Running code to load all HTML templates at application start.
* Initializing midleware.

The application file defined a single public function called Run() which runs the Registry service. This function is called in [registry.go](https://github.com/APTrust/registry/blob/master/registry.go){_target=blank} to start the server. It's also called in the test suite to run a background server to handle test queries.

## Template Helpers

The [templates.go](https://github.com/APTrust/registry/tree/master/helpers/templates.go){target=_blank} file defines a number of helper functions that can be called from within the application's HTML templates. The functions' names will tell you what they do. Each function also includes a docstring.

Note that these functions must be registered to work inside of templates. The registration happens in the `initTeplates()` function in [app/application.go](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank}

## Constants

[constant.go](https://github.com/APTrust/registry/blob/master/constants/constants.go){target=_blank} defines a number of constants used througout the app. This is to avoid having the app littered with mistyped strings or strings whose cases don't match. The constants' names are descriptive enough to tell you what they mean.

[permissions.go](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank} defines permissions and which roles they are assigned to. See the [Authorization](security/authorization) page for details on how permissions are applied.

## The Configuration Object

The [Configuration Object](https://github.com/APTrust/registry/blob/master/common/config.go) loads config variables from a .env file and from environment variables, which can be pumped into Docker containers from Amazon's Parameter Store.

In development and test environments, most config settings are stored in .dev.env or .test.env. To load the right config, specify one of the following on the command line:

```
APT_ENV=dev ./registry serve
```

or

```
APT_ENV=test ./registry serve
```

Config settings are loaded first from the .env file, then from the environment, with environment values overwriting .env file values via viper's `AutomaticEnv()` call.

The environment is loaded and made globally available by the [Context() function](https://github.com/APTrust/registry/blob/master/common/context.go), which returns a singleton instance of APTContext, described below.

## The Context Object

The [Context() function](https://github.com/APTrust/registry/blob/master/common/context.go) returns a singleton instance of APTContext, which makes the following items available to all parts of the Registry application:

* A `Configuration` object containing all config settings.
* A `DB` object which provides a connection pool to the Postgres database.
* A `Log` object for logging.
* An `AuthyClient` for two-factor auth push notifications.
* A `RedisClient` for talking to Redis.
* An `NSQClient` for talking to NSQ.
* An `SESClient` for sending emails to users. These are usually password-reset emails, or emails asking someone to review a deletion request.
* An `SNSClient` for sending login codes to two-factor auth users via text message.

## Security Middleware

Sucurity middleware is registered in the [application file](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank}. The source is in the [middleware directory](https://github.com/APTrust/registry/tree/master/middleware){target=_blank}.

Each piece of middleware touches every request *before* the registered request handler. The components have the following responsibilities:

| Compenent | Responsibility |
| --------- | -------------- |
|[authenticate.go](https://github.com/APTrust/registry/blob/master/middleware/authenticate.go){target=_blank}| Ensures the current user is authenticated before accessing endpoints that require authentication. |
|[authorize.go](https://github.com/APTrust/registry/blob/master/middleware/authorize.go){target=_blank}| Ensures the user is authorized to perform the current request. This component depends on the [authorization_map.go](https://github.com/APTrust/registry/blob/master/middleware/authorization_map.go){target=_blank} and [resource_authorization.go](https://github.com/APTrust/registry/blob/master/middleware/resource_authorization.go){target=_blank} files in the middleware directory, as well as the [permissions.go](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank} file in the constants directory. |
|[csrf.go](https://github.com/APTrust/registry/blob/master/middleware/csrf.go){target=_blank}| This ensures that CSRF tokens are present and valid for all POST and PUT requests. |

See the [Security Overview](security) for info on how security checks fit into the request lifecycle.

## The Request Object

The Request object handles boilerplate processing common to all requests, such as parsing common query data, loading common tempdate data value, showing or hiding submenus, setting up a pager for list responses, and loading requested objects or lists of objects.

There are two versions of the request object: one for [web requests](https://github.com/APTrust/registry/blob/master/web/webui/request.go){target=_blank} and one for [API requests](https://github.com/APTrust/registry/blob/master/web/api/request.go){target=_blank}.

You'll notice in that in both the Web UI and the REST APIs, most handlers begin with a call to `req := NewRequest(c)` to handle the boilerplate setup. (The `c` param is the `*gin.Context` object, which contains the HTTP request and lots of other metadata.)

## The Pager

The [pager object](https://github.com/APTrust/registry/blob/master/common/pager.go){target=_blank} contains information about lists, including how many total results a list query yielded and links to the next and previous pages of results. This object works for both Web (HTML) and API (JSON) requests.

Because this object is automatically set up by the Request object, you generally don't have to touch it or think about it.

## Custom Forms

The [forms directory](https://github.com/APTrust/registry/tree/master/forms){target=_blank} defines custom forms for each type of object a user or admin may edit through the web UI. It also contains filter forms for all of the Web UI's list pages.

The form objects define what goes into each form. Forms layout and rendering is defined in the [views directory](https://github.com/APTrust/registry/blob/master/views){target=_blank}. For example, the form for editing user details is in the
[user form template](https://github.com/APTrust/registry/blob/master/views/users/form.html){target=_blank}. while the for for filtering a list of users in in the [user filters form](https://github.com/APTrust/registry/blob/master/views/users/_filters.html){target=_blank}.

## Views

Views are HTML templates used to render web pages. All of the Registry's views are in the [views directory](https://github.com/APTrust/registry/blob/master/views){target=_blank}. The [application file](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank} loads all of them at startup.

## Models

The application models are defind in the [pgmodels directory](https://github.com/APTrust/registry/tree/master/pgmodels){target=_blank}. These models map to database tables and views through the [go-pg](https://github.com/go-pg/pg){target=_blank} ORM.

## Web and API Handlers

All of the handlers for the Web UI are defined in the [web/webui directory](https://github.com/APTrust/registry/tree/master/web/webui){target=_blank}.

Handlers for the member API, which is a read-only subset of the admin API, are in the
[web/api/common](https://github.com/APTrust/registry/tree/master/web/api/common){target=_blank} directory.

Handlers for the admin API are in the [web/api/admin](https://github.com/APTrust/registry/tree/master/web/api/admin){target=_blank} directory.

These handlers are mapped to URLs in the [application file](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank}.

## UI Components Page

The [UI components page](https://repo.aptrust.org/ui_components){target=_blank} displays available UI components and the HTML required to render them. Refer to this page when creating new features.
