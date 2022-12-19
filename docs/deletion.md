# File and Object Deletion

File and object deletion follow the same multi-step process:

1. An institutional user or institution admin clicks the **Delete** button on an object or file detail page. This creates a deletion request in the Registry database.
2. Registry sends an email to administrators at the institution, telling them that a deletion request awaits their review. The email includes a link and a token to review the request.
3. The institutional admin either approves or denies the request. If denied, processing stops there. If approved, we move on to step 4.
4. Registry creates a WorkItem for the deletion request and adds the WorkItem ID to NSQ's `delete_item` topic.

From there, the worker will double-check to ensure the deletion request was approved, and will then delete the files from long-term perservation, change their state from `A` (active) to `D` (deleted), and create the required Deletion PREMIS events.

Registry's back-end includes safegaurds to prevent non-institutional admins from approving deletions. APTrust admins can view deletion requests but cannot approve them, even accidentally. Institutional users cannot approve deletion requests, nor can admins from institutions that don't own the files/objects to be deleted.
