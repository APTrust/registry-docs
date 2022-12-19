# File and Object Restoration

Users can request object restoration by clicking the **Restore** button on the object detail page. They can request file restoration by clicking the **Restore** on the file detail page, or under the expanded file detail view on an object detail page.

For individual file restorations, the system will restore files from preservation storage to the depositor's restoration bucket. The file will be restored using its identifier as key.

That is, file `virginia.edu/photos/data/image1.jpg` will be restored to `aptrust.restore.virginia.edu/virginia.edu/photos/data/image1.jpg`.

Restored objects will be bagged and copied to the restoration bucket as a tar file. So, object `virginia.edu/photos` will be restored to `aptrust.restore.virginia.edu/photos.tar`. Because the files are being re-bagged, the they may appear in different order in the restored tar file than in the originally submitted tar file.

Larger files and bags generally take longer to restore than smaller ones.

# Glacier Restorations

Glacier Restorations work just like S3 and Wasabi restorations, except that items need to be moved from Glacier to S3 first, so they can be retrieved. That step can take up to five hours for items stored in regular Glacier archives, and up to twelve hours for items stored in Glacier Deep archives.
