# The APTrust Registry

The APTrust Registry is a web application and REST API providing information about what we've stored in our preservation repository.

The web application lets depositors find, restore, and delete intellectual objects and generic files. It also shows the status of work items (i.e. ingests, restoration and deletion requests), and provides basic user management functions to local institutional admins.

The member API provides read-only access to objects, files, work items and related records to APTrust depositors.

The admin API provides read-write access to Preserv service workers that process ingests, restorations, fixity checks and deletions. Preserv is the Registry's most active client. Fixity checks typically issue 10,000+ requests per hour. A slow ingest day may result in only a few hundred API requests, while a very busy day may result in a million or so requests.

## External Components & Services

The Registry is written in Go, using the Gin web framework. The application runs inside Docker containers in Amazon's ECS/Fargate service. It tends to be light on memory and heavy on CPU when under load. ECS will add Registry containers when CPU usages passes a certain threshold and scale them back as load decreases.

It stores persistent data in a Postgres database running on Amazon's RDS, using [go-pg](https://github.com/go-pg/pg){target=_blank} as an object-relational mapper.

While the Registry handles incoming requests from web browsers, member API consumers around the country, and from Preserv, it also establishes outbound connections to the following services:

| Service | Description |
| ------- | ----------- |
| Postgres | The main, long-term data store containing info about all objects and files stored in preservation buckets, plus their associated checksums, storage records and Premis events. The Postgres DB also contains user and institutional account records and info about work items. |
| Authy | Used to send push notifications for multifactor authentication. |
| NSQ | This queue service pushes work items to the Preserv workers that carry out the actual work. Registry sends Deletion and Restoration requests to NSQ in response to user actions in the Web UI. |
| Redis | Registry reads JSON data from Redis describing the state of long-running ingest processes. Registry can also delete Redis data on demand when requeuing Work Items. Redis data is available to APTrust admins only. |
| Amazon SES | Registry sends alerts and password-reset messages via email through Amazon's Simple Email Service. |
| Amazon SNS | Registry sends one-time passwords in text messages through Amazon's SNS service. This is for multifactor authentication. |
