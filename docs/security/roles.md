# Roles and Privileges

Registry uses role-based privileges.

Registry permissions are role-based with the following general rules:

* Institutional Users can access resources belonging to their own institution, but cannot perform destructive actions and manipulate other user accounts.
* Institutional Admins can do everything Institutional Users can do, plus approve deletion requests and manipulate other user accounts at their own institution.
* The System Administrator account has all privileges at all institutions, plus some additional privileges such as creating, editing, and deactivating institutions, managing NSQ services, re-queueing WorkItems, and other administrative tasks.

The table below describes who can do what.

<!-- To edit the table below, edit RegsitryFeatures.ods, then save it as a csv file and set the delimiter character to | (pipe) -->


| Feature | Web <br/> UI | Member <br/> API | Admin <br/> API | Roles Allowed | Ownership Restrictions | Description and Notes |
| -- | -- | -- | -- | -- | -- | -- |
Alert – List|✓|||All|User’s own alerts|View alerts pertaining to your account.
Alert – Mark Read|✓|||All|User’s own alerts|Mark alerts as read.
Alert – Mark Unread|✓|||All|User’s own alerts|Mark alerts as unread.
Alert – Show|✓|||All|User’s own alerts|Show the text of an alert.
Checksum – Create|||✓|System account|None|Create a new checksum for a Generic File.
Checksum – List||✓|✓|All|User’s own institution|List checksums for Generic Files.
Checksum – Show||✓|✓|All|User’s own institution|Show details of a checksum.
Dashboard – Show|✓|||All|User’s own institution|Show the dashboard, with an overview of deposits and recent work items.
Deletion – Approve|✓|||Inst. Admin only|User’s own institution|Approve a file or object deletion request submitted by another user at your institution.
Deletion – List|✓|||Inst. Admin only|User’s own institution|Display a list of deletion requests for your institution.
Deletion – Reject|✓|||Inst. Admin only|User’s own institution|Reject a file/object deletion request.
Deletion – Review|✓|||Inst. Admin only|User’s own institution|Review a file/object deletion request with the option to approve or reject it.
Deletion – Show|✓||✓|All|User’s own institution|Display a file/object deletion request without the object to approve or reject it.
Generic File – Create|||✓|System account||Create a single Generic Files. This happens only when recording a successful ingest.
Generic File – Create Batch|||✓|System account||Create a batch of Generic Files. This happens only when recording a successful ingest.
Generic File – Delete|||✓|Inst. Admin only|User’s own institution|Delete a Generic File. This happens only after deletion request has been approved.
Generic File – Edit|||✓|System account||Edit a Generic File. This happens only when re-ingesting an existing file.
Generic File – List|✓|✓|✓|All|User’s own institution|List Generic Files belonging to your institution.
Generic File – Request Delete|✓|||Inst. Admin only|User’s own institution|Request deletion of one of your institution’s files. (Deletion must be approved by an institutional admin.)
Generic File – Request Restore|✓|||All|User’s own institution|Request restoration of one of your institution’s files.
Generic File – Show|✓|✓|✓|All|User’s own institution|Display details of a Generic File belonging to your institution.
Institution – Create|✓|||APTrust admin||Create a new institution.
Institution – Delete|✓|||APTrust admin||Soft-deletes an institution by marking it as inactive.
Institution – Edit|✓|||APTrust admin||Edit an existing institution.
Institution – List|✓||✓|APTrust admin, System account||List all institutions.
Institution – Show|✓||✓|APTrust admin, System account||Show details of an institution.
Institution – Undelete|✓|||APTrust admin, System account||Reactivate a “deleted” institution.
Intellectual Object – Create|||✓|System account||Create an Intellectual Object. This happens only when recording a successful ingest.
Intellectual Object – Delete|||✓|System account||Only after approval by institutional admin
Intellectual Object – Edit|||✓|System account||Edit an Intellectual Object. This happens only when re-ingesting an existing object.
Intellectual Object – List|✓|✓|✓|All|User’s own institution|List Intellectual Objects belonging to your institution.
Intellectual Object – List Events|✓|||All|User’s own institution|List Premis events associated with an Intellectual Object.
Intellectual Object – List Files|✓|||All|User’s own institution|List Generic Files associated with an Intellectual Object.
Intellectual Object – Request Delete|✓|||Inst. Admin only||Request deletion of an Intellectual Object. (Deletion must approved by an institutional admin.)
Intellectual Object – Request Restore|✓|||All|User’s own institution|Request restoration of one of your institution’s Intellectual Objects.
Intellectual Object – Show|✓|✓|✓|All|User’s own institution|Show details of an Intellectual Object.
NSQ – Admin|✓|||APTrust admin||Show NSQ admin panel.
Premis Event – Create|||✓|System account||Create a Premis event. This happens on ingest, fixity check, deletion.
Premis Event – List|✓|✓|✓|All|User’s own institution|List Premis events belonging to your institution.
Premis Event – Show|✓|✓|✓|All|User’s own institution|Show details of a Premis event.
Storage Record – Create|||✓|System account||Create a storage record describing where a file is stored. This happens only when recording a successful ingest.
Storage Record – List|||✓|System account||Show a list of storage records. Non-system users can see Storage Records as part of file detail in web UI.
Storage Record – Show|||✓|System account||Display details of a storage record. Non-admin users can see Storage Records as part of file detail in web UI.
User – Confirm Phone|✓|||All|User’s own account|Confirm your phone number for two-factor authentication by entering the code we sent you.
User – Create|✓|||Inst. Admin, APTrust admin|User’s own institution|Create a new user.
User – Delete|✓|||Inst. Admin, APTrust admin|User’s own institution|Soft-deletes a user by marking them as inactive.
User – Edit|✓|||Inst. Admin, APTrust admin|User’s own institution|Users can edit their own details, but not others, unless they’re an admin.
User – Forgot Password|✓|||All|User’s own account|Sends an email to you with a link to help you log in.
User – Generate API Key|✓|||All|User’s own account|Generates an API key so you can access the member API.
User – Generate Backup Codes|✓|||All|User’s own account|Generates backup codes that two-factor auth users can use to login when they don’t have access to their phone.
User – List|✓|||Inst. Admin, APTrust admin|User’s own institution|Displays a list of users at your institution.
User – Login Second Factor|✓|||All|User’s own account|Allows users to enter backup or SMS codes for second factor of login.
User – My Account|✓|||All|User’s own account|Display the details of your account.
User – Reset Password|✓|||All|User’s own account|Reset your password.
User – Set Up 2-Factor Auth|✓|||All|User’s own account|Begin the two-factor authentication setup process by choosing Authy or SMS.
User – Show|✓|||Inst. Admin, APTrust admin|User’s own institution|Display the details of another user’s account.
User – Sign In|✓|||All|User’s own account|Sign in to the web UI.
User – Sign Out|✓|||All|User’s own account|Sign out of the web UI.
User – Undelete|✓|||Inst. Admin, APTrust admin|User’s own institution|Reactivate a “deleted” user.
WorkItem – Create|||✓|System account||Create a new WorkItem.
WorkItem – Delete Redis Data|✓|||APTrust admin||Delete the Redis data associated with a WorkItem. Do this only when requeuing an item back to the first stage of ingest, and only when you really want to throw out all the metadata and start over.
WorkItem – Edit|✓||✓|APTrust admin, System account||Edit an existing work item.
WorkItem – List|✓|✓|✓|All|User’s own institution|List work items for your institution.
WorkItem – Requeue|✓|||APTrust admin||Requeue a work item so workers will retry it.
WorkItem – Show|✓|✓|✓|All|User’s own institution|Show the details of an individual work item.
