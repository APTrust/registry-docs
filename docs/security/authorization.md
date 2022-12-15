# Authorization

Authorization middleware runs after authentication middleware. By the time it touches the request, the authentication middlware has added the User object to the current request.

The [authorization middlware](https://github.com/APTrust/registry/blob/master/middleware/authorize.go){target=_blank} uses that User object to do the following:

1. Check the URL/request path to see what type of resource the user is requesting. If the resource maps to a specific database record (a work item, generic file, intellectual object, etc.), it looks up the record to see which institution it belongs to.
2. Check the [authrorization map](https://github.com/APTrust/registry/blob/master/middleware/authorization_map.go){target=_blank} to see if the user is allowed to access that particular resource belonging to that particular institution.
3. Constructs a [ResourceAuthorization object](https://github.com/APTrust/registry/blob/master/middleware/resource_authorization.go){target=_blank} with the following information:
    * Handler - The name of the HTTP handler function that will handle the user's request.
    * ResourceID - The unique id of the resource (work item, file, obect, etc.) the user requested. This will be zero if the user is requesting a list of items.
    * ResourceIdentifier - The string identifier of the requested resource. This applies to institutions, intellectual objects and generic files.
    * ResourceInstId - The ID of the institution to which the resource belongs.
    * ResourceType - The type of resource (IntellectualObject, WorkItem, GenericFile, etc.).
    * Permission - The permission required to access the requested resource. These are defined in [constants/permissions](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank}.
    * Checked - True or false, indicating whether the authorization middleware checked that the user has permission to access the requested resource.
    * Approved - True or false, indicating whether the user has permission to access the requested resource.
    * Error - Describes any error that occurred during the authorization check.

The authorization middleware will not let a request proceed unless the ResourceAuthorization object's `Checked` and `Approved` attrbutes are both true.

## Things to Note

1. If, when adding a new endpoint, you to forget to define a permission for it, you will never be able to reach that endpoint, because without a defined permission, `ResourceAuthorization.Checked` will be false.
2. Requests for list endpoints, such as the WorkItems list and the IntellectualObject list, cannot include a ResourceID or a ResourceInstID, because the requests don't target a single resource. Unless the requesting user is an APTrust admin, database queries issued by these requests will **always** include an Institution ID filter, with the ID set to the user's own institution ID. For example, when a user from virginia.edu requests a list of WorkItems, objects, or files, the system will force a where clause into their queries stating `where institution_id = [user's institution id]`. This occurs in the `LoadResourceList()` function of the Web UI's [Request object](https://github.com/APTrust/registry/blob/master/web/webui/request.go){target=_blank} and in the `LoadResourceList()` function of the API's [Request object](https://github.com/APTrust/registry/blob/master/web/api/request.go){target=_blank}.

## Permission Definitions

All of Registry's permission are defined in [constants/permissions.go](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank}. The `initPermissions()` function in that file assigns permissions to roles like so:

```go

	// Institutional User Role
	instUser[ChecksumRead] = true
	instUser[DashboardShow] = true
    // ... additional permissions omitted for brevity...


	// Institutional Admin Role
	instAdmin[FileDelete] = true
	instAdmin[FileRead] = true
    // ... additional permissions omitted for brevity...


    // Sys Admin Role
	sysAdmin[ChecksumCreate] = true
	sysAdmin[ChecksumDelete] = false // no one can do this
	sysAdmin[ChecksumRead] = true
    // ... additional permissions omitted for brevity...

```

Registry permissions are role-based with the following general rules:

* Institutional Users can access resources belonging to their own institution, but cannot perform destructive actions and manipulate other user accounts.
* Institutional Admins can do everything Institutional Users can do, plus approve deletion requests and manipulate other user accounts at their own institution.
* The System Administrator account has all privileges at all institutions, plus some additional privileges such as creating, editing, and deactivating institutions, managing NSQ services, re-queueing WorkItems, and other administrative tasks.


!!! important

    No role has any permission unless it is explicitly granted in [constants/permissions.go](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank}, and some permissions are explicitly denied to all users because they violate business rules.

    For example, no user can delete checksums or delete or alter PREMIS events. The endpoints to perform these actions don't even exist, and the underlying data models will throw errors if anyone even tries to perform these actions.


## Permission Mapping

While permissions are defined and assigned to roles in [constants/permissions.go](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank}, they are mapped to request handlers in [middleware/authorization_map.go](https://github.com/APTrust/registry/blob/master/middleware/authorization_map.go){target=_blank}. The authorization map tells the app which permission is required to access each request handler.

!!! important

    If you don't map a permission to your new request handler, no one will be able to reach it, ever, because the authorization check will fail.

## Permission Checking

The [middleware/authorization.go](https://github.com/APTrust/registry/blob/master/middleware/authorize.go){target=_blank} middleware figures out which request handler responds to the current URL. It reads the authorization map to see which permission is required to access that handler, then determines whether the current user is allowed to call that handler. It also does further checks, as described above, to see if the user can access whatever resources that handler touches.

## List of Authorization-Related Files

| File | Description |
| ---- | ----------- |
| [constants/permissions.go](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank} | Defines all of the system permissions and assigns them to roles at application start. |
| [middleware/authorization_map.go](https://github.com/APTrust/registry/blob/master/middleware/authorization_map.go){target=_blank} | Maps permissions to web and API request handlers. |
| [middleware/authorize.go](https://github.com/APTrust/registry/blob/master/middleware/authorize.go){target=_blank} | Authorizes requests and decides whether or not to pass the request on to the handler. |
| [middleware/resource_authorization.go](https://github.com/APTrust/registry/blob/master/middleware/resource_authorization.go){target=_blank} | Includes logic to compare user permissions to the authorization map, and to do fine-grained resource-level checks. (I.e. Ensures objects user is requesting actually belong to that user's institution.) |
| [web/webui/request.go](https://github.com/APTrust/registry/blob/master/web/webui/request.go){target=_blank} | Enforces filters in list requests to ensure users access only resources belonging to their own institution.
| [web/api/request/go](https://github.com/APTrust/registry/blob/master/web/api/request.go){target=_blank} | Enforces filters in API list requests to ensure users access only resources belonging to their own institution.
