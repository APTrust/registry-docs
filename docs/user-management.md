# User Management

Institutional admins can add, edit, and delete user accounts at their own institutions. APTrust admins can add, edit, and delete user accounts belonging to any institution. Institutional users can edit only their own account.

Note that user deletion is "soft deletion," in which the system simply marks the user's account inactive. Inactives cannot log in until an admin reactivates their account.

The system does not delete users because their account records must remain in order for audit records to make sense. WorkItems, for example, record info about who requested file and object restorations. Deletion records include info about who requested and who approved a deletion.

Admins can manage users by clicking the **User** link in the left nav bar. From there, the process should be intuitive.

Note that after adding a new user, you will need to request AWS keys from APTrust for that user; otherwise, they won't be able to access S3 buckets for ingest and restoration.
