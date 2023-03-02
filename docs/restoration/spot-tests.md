# Restoration Spot Tests

Restoration spot tests are initiated by APTrust, restoring one random bag to an institution. The points of the exercise are:

1. To ensure we restore bags correctly.
2. To ensure depositors can process restored bags internally, which often means:

    1. Making sense of the contents
    1. Being able to re-import the contents into their local institutional repository or digital asset management system.

Each institution can enable or disable spot tests through the Registry's edit institution page. To disable spot tests, set **Restoration spot test frequency** to zero. To enable it, set it to a positive, non-zero value, and spot tests will run every N days. Typical settings are 30, 60, or 90 days.

## Spot Test Mechanism

Spot tests run as a daily cron job inside the Registry, initialized in the `initRestorationSpotTests` function in `app/cron.go`. When run, Registry does the following:

1. Determines if it even needs to run. If a spot test is currently running, or has run in the past 24 hours (according to `ar_internal_metadata`), it does nothing.
1. Updates the `ar_internal_metadata` table in the Postgres DB to say it's running. This prevents other Registry processes from running the spot test at the same time.
1. Checks each institution to see if it's due for a spot test. If an institution wants to run spot tests every X days, and it's been more than X days since the last spot test, the system will run one now for that institution.
1. Finds a suitable object to be restored. We generally want to avoid restoring massive objects and object that have been recently restored. See the function `pgmodels.SmallestObjectNotRestoredInXDays` for info on how we choose a suitable candidate.
1. Creates a restoration WorkItem to restore the object.
1. Queues the WorkItem in NSQ, so a worker will pick it up.
1. Assigns the WorkItem ID to the institution's LastSpotRestoreWorkItemID, so we'll know when the depositor's last spot test occurred.

When the restoration completes, the method `WorkItem.AlertOnSuccessfulSpotTest()` sends a notice to the institution's users saying that the restoration is complete. It tells them where to find the restored object and suggests they try to run it through their internal restoration processes.
