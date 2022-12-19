# Redis

Preservation Services workers use Redis to store interim processing data during ingest. Registry displays a summary of Redis data for WorkItems currently in progress. Only APTrust admins can see this data. The summary includes information about when each worker started and stopped working on an ingest, how many attempts each worker made, and what (if any) errors occurred.

The summary also includes essential metadata about the item being ingested, including info from its tag files, the number of payload files in the bag, and the total size, in bytes, of the bag.

These last bits of information may be particularly useful when diagnosing slow ingests. While a moderate-sized bag may typically ingest quickly, a moderate-sized bag containing tens of thousands of small files will take much longer to ingest.

## Deleting Redis Data

Generally, there is no need to delete Redis data. There are only two cases where an APTrust admin would want to delete Redis data:

1. When cancelling an ingest. You'll rarely do this. The system knows to cancel pending ingests when newer versions of the same bag arrive in a depositor's receiving bucket.
2. When requeuing an ingest item all the way back to the pre-fetch stage. Deleting the Redis data will remove older error messages that might prevent ingest workers from processing the bag.
