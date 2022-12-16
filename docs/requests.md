# Request Lifecycle

Processing for virtually all Registry requests follows the same pattern, flowing through the these steps, in order:

1. Authentication middleware ensures the user is logged in.
2. Authorization middleware ensures the user is allowed to access the resources they are requesting.
3. CSRF middlware ensures bad actors can't hijack valid user sessions to perform unsavory actions.
4. The request handler mapped to the current URL is invoked. (URLs are mapped to handlers in [app/application.go](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank}.)
    a. The request handler creates a [web request](https://github.com/APTrust/registry/blob/master/web/webui/request.go){target=_blank} or [API request](https://github.com/APTrust/registry/blob/master/web/api/request.go){target=_blank} object to perform common basic operations. More on this below.
    b. The request handler performs its custom logic.
    c. The request handler constructs and returns a response.

## The Web Request Object

The [web request object](https://github.com/APTrust/registry/blob/master/web/webui/request.go){target=_blank} performs the following common operations for virtually all requests:

1. Populates common template data so the response template can display it. (E.g. the current user, the csrf token for HTML forms, a flash message, and more.)
2. Determines whether the requested page should be displayed as a stand-alone page or a modal element. In the first case, the server will return a full HTML document with head and body elements. In the second it returns an HTML snippet, which is usually a single div. This code exists because in early iterations of the UI design, some elements changed from modal display to standalone pages and back again. Many pages still support both rendering methods.
3. Clears out old flash cookies.

If the request is for an index (list) page, the request object parses the filters from the query string, constructs the where clause for the query, loads results, and sets up a pager object that will let the user move through the result set.

Note that each data model in the application's [pgmodels directory](https://github.com/APTrust/registry/tree/master/pgmodels){target=_blank} includes a list of allowed filters. The web Request object parses the filter params and knows how to build a where clause from these. The where clause is SQL-safe, and the Request object will ignore any params that are not explicitly whitelisted.

## The API Request Object

The [API request object](https://github.com/APTrust/registry/blob/master/web/api/request.go){target=_blank} performs the same set of common tasks as the web request object, though it's tailored to assist in generating JSON output instead of HTML.

Because the API allows creating and updating sensitive records, such as WorkItems, IntellectualObjects, and GenericFiles, the API request object's `AssertValidIDs` function does some additional sanity checking to prevent malformed and malicious API requests from touching records belonging to the wrong institutions.

## The ResourceAuthorization Model

You'll notice that both the web and API request objects load the ResourceAuthorization model from the current request context. This model was constructed by the [authorization middleware](security/authorization.md) during its aurhorization check.

This model contains some essential information for processing requests related to a single resource, including the resource type, ID, and identifier, as well as the ID of the institution that owns the resource. Request handlers use these IDs to load or update the requested resource.
