# Data Models

The data models that form the core of the Registry are located in the [pgmodels directory](https://github.com/APTrust/registry/tree/master/pgmodels){target=_blank}. These models map directly to database tables or database views.

Table-backed models support inserts and usually updates and deletions. (Some records, such as PREMIS events, cannot be updated or deleted.) Most models implementing deletion support soft-deletion only.

View-backed models are read-only. These are generally used to gather data for detail and list pages with a single query.

## The Base Model

The base models, BaseModel and TimestampModel, are defined in [pgmodels/pgmodel.go](https://github.com/APTrust/registry/blob/master/pgmodels/pgmodel.go){target=_blank}, which also defines base methods for insertion, updating, and transactions.

This file has two other important functions:

* `initFilters()` defines a whitelist of allowed filters for each model type.
* `InstIDFor()` returns the ID of the insitution that owns any given resource.

`InstIDFor()` is especially important for the security checks run by the [resource authorization middleware](https://github.com/APTrust/registry/blob/master/middleware/resource_authorization.go){target=_blank}, which checks permissions against roles and ensures institutional users and admins can access only those resources belonging to their own institutions.

## Allowed Filters

Each model defines a list of allowed filters that users can use to refine results in list queries. The filters are often defined on the view version of a model. For example, [pgmodels/work_item_view.go](https://github.com/APTrust/registry/blob/master/pgmodels/work_item_view.go){target=_blank} defines a number of filters for the WorkItem list.

These filters become the names of form controls in the related filter form. See, for example, the [WorkItemFilterForm](https://github.com/APTrust/registry/blob/master/forms/work_item_filter_form.go){target=_blank}.

That form will be rendered by the [work item filters view](https://github.com/APTrust/registry/blob/master/views/work_items/_filters.html){target=_blank}.

When a user submits a query to the WorkItem list page, the `GetFilterCollection()` function of the [web request object](https://github.com/APTrust/registry/blob/master/web/webui/request.go){target=_blank} parses the query string into a  [FilterCollection object](https://github.com/APTrust/registry/blob/master/pgmodels/filter_collection.go){target=_blank}, whose `ToQuery()` function converts it to a
[Query object](https://github.com/APTrust/registry/blob/master/pgmodels/query.go){target=_blank}.

The effect of all this is that we can add new query fields for any table or view simply by adding items to the allowed filters list. As long as the filter name follows a defined pattern, the Registry code will know what to do with it. This system also ensures that Registry won't accept unknown or dangerous filters, only those that are whitelisted.

The QueryOp map in [pgmodels/query.go](https://github.com/APTrust/registry/blob/master/pgmodels/query.go){target=_blank} defines how filter name suffixes map to SQL operators. For example, query string parameters `size=99` and `size__eq=99` both turn into the SQL condition `size = 99`. Similarly, `size__gt=99` turns into `size > 99`, while `size__gteq=99` turns into `size >= 99`.

The QueryOp map supports numeric operators as well as string and boolean equality, `ILIKE`, `IN`, `NOT IN`, `IS NULL` and `IS NOT NULL`.

## List of Models

Below is a list of models in the pgmodels directory, along with a brief description of each. For more information, click on a model name to view the souce.


| Model | Description |
| ----- | ----------- |
[Alert](https://github.com/APTrust/registry/blob/master/pgmodels/alert.go){target=_blank} | An alert sent to one or more users. E.g. password-reset email, deletion request review notice, etc. |
[AlertView](https://github.com/APTrust/registry/blob/master/pgmodels/alert_view.go){target=_blank} | Read-only model containing additional fields from records related to the alert. This is used for querying and display. |
[Checksum](https://github.com/APTrust/registry/blob/master/pgmodels/checksum.go){target=_blank} | A checksum record for an individual GenericFile. Checksums cannot be deleted or updated. |
[ChecksumView](https://github.com/APTrust/registry/blob/master/pgmodels/checksum_view.go){target=_blank} | Read-only model containing additional fields from records related to the checksum. This is used for querying and display. |
[Counts](https://github.com/APTrust/registry/blob/master/pgmodels/counts.go){target=_blank} | Includes several objects used to represent object, file, event, and work item counts. |
[DeletionRequest](https://github.com/APTrust/registry/blob/master/pgmodels/deletion_request.go){target=_blank} | Contains information about a request to delete a GenericFile or IntellectualObject. |
[DeletionRequestView](https://github.com/APTrust/registry/blob/master/pgmodels/deletion_request_view.go){target=_blank} | Read-only model containing additional fields from records related to the deletion request. This is used for querying and display. |
[DepositFormatStats](https://github.com/APTrust/registry/blob/master/pgmodels/deposit_format_stats.go){target=_blank} | Contains stats about an institution's deposits. Possibly obsolete. This may have been superseded by DepositStats. |
[DepositStats](https://github.com/APTrust/registry/blob/master/pgmodels/deposit_stats.go){target=_blank} | Contains repository-wide stats used in Registry's Reports page. |
[GenericFile](https://github.com/APTrust/registry/blob/master/pgmodels/generic_file.go){target=_blank} | Represents a single file in preservation storage. |
[GenericFileView](https://github.com/APTrust/registry/blob/master/pgmodels/generic_file_view.go){target=_blank} | Read-only model containing additional fields from records related to the file. This is used for querying and display. |
[Institution](https://github.com/APTrust/registry/blob/master/pgmodels/institution.go){target=_blank} | Describes an institution (aka depositor). |
[InstitutionView](https://github.com/APTrust/registry/blob/master/pgmodels/institution_view.go){target=_blank} | Read-only model containing additional fields from records related to the institution. This is used for querying and display. |
[IntellectualObject](https://github.com/APTrust/registry/blob/master/pgmodels/intellectual_object.go){target=_blank} | Represents an object in preservation storage. An IntellectualObject is a collection of GenericFiles, plus some metadata, such as Title, Access settings, etc. |
[IntellectualObjectView](https://github.com/APTrust/registry/blob/master/pgmodels/intellectual_object_view.go){target=_blank} | Read-only model containing additional fields from records related to the object. This is used for querying and display. |
[PremisEvent](https://github.com/APTrust/registry/blob/master/pgmodels/premis_event.go){target=_blank} | Describes an action that the system or one of its users has performed on an IntellectualObject or GenericFile. PREMIS events cannot be updated or deleted. |
[PremisEventView](https://github.com/APTrust/registry/blob/master/pgmodels/premis_event_view.go){target=_blank} | Read-only model containing additional fields from records related to the event. This is used for querying and display. |
[StorageRecord](https://github.com/APTrust/registry/blob/master/pgmodels/storage_record.go){target=_blank} | Describes where in preservation storage a file can be found. |
[User](https://github.com/APTrust/registry/blob/master/pgmodels/user.go){target=_blank} | A Registry User. |
[UserView](https://github.com/APTrust/registry/blob/master/pgmodels/user_view.go){target=_blank} | Read-only model containing additional fields from records related to the user. This is used for querying and display. |
[WorkItem](https://github.com/APTrust/registry/blob/master/pgmodels/work_item.go){target=_blank} | Describes a task that is, has been, or will be carried out by Preserv's ingest, restoration or deletion services. |
[WorkItemView](https://github.com/APTrust/registry/blob/master/pgmodels/work_item_view.go){target=_blank} | Read-only model containing additional fields from records related to the WorkItem. This is used for querying and display. |

## List of Non-Model Objects in pgmodels

The following files in the pgmodels folder are not models but are related to models and database access.

| File | Description |
| ----- | ----------- |
[factory.go](https://github.com/APTrust/registry/blob/master/pgmodels/factory.go){target=_blank} | Like Rails' FactoryGirl, this file contains functions to generate model instances for unit and integration tests. |
[filter_collection.go](https://github.com/APTrust/registry/blob/master/pgmodels/filter_collection.go){target=_blank} | Contains information about filters a user wants to apply when querying a list of records. |
[json_types.go](https://github.com/APTrust/registry/blob/master/pgmodels/json_types.go){target=_blank} | Contains specially-defined serialization models for some pgmodel types. These are for cases in which some front-end component requires a custom (usually lightweight) serialization of an object. |
[pgmodel.go](https://github.com/APTrust/registry/blob/master/pgmodels/pgmodel.go){target=_blank} | Contains base fields and functions inherited by other pgmolde.s |
[query.go](https://github.com/APTrust/registry/blob/master/pgmodels/query.go){target=_blank} | Contains information necessary to generate a database query, including where clause, sorting, offsets, and limits. This can be constructed from a FilterCollection object, which in turn is parsed from query string params. |
