# The Registry Database

Registry uses a Postgres database, which runs in RDS in our live environments. You'll find connection settings in the .env files, such as [.env.test](https://github.com/APTrust/registry/blob/master/.env.test){target=_blank} for non-live environments, and in AWS Parameter Store for live environments.

The database was converted from the old Pharos DB. An overview of the migrations is available in [this README](https://github.com/APTrust/registry/tree/master/db/pharos){target=_blank}.

You can generate the current schema by loading the [initial launch schema](https://github.com/APTrust/registry/blob/master/db/initial_launch_schema.sql){target=_blank} and then running the [migrations](https://github.com/APTrust/registry/tree/master/db/migrations){target=_blank} on top of that. This is what happens when you run the registry test suite with the `./registry test` command.

Under the hood, the test suite calls a set of functions in [db/testutil.go](https://github.com/APTrust/registry/blob/master/db/testutil.go){target=_blank} to do the following:

* drop all objects in the database
* load the initial launch schema
* run all migrations in the db/migrations folder
* load fixtures for testing

## Migrations

We are currently not using any migration manager. We write migrations as pure idempotent SQL and run them manually from the staging/demo/production bastion server.

We'll look into better migration management solutions in the future. It's essential, however, to write idempotent migrations so that re-running a migration will not corrupt or damage the database.

!!! Note

    The migration files are well commented. Look there if you're interested in details of what's going on and why things were written the way they were.


### Migration Patterns

Migration files are SQL files in the [db/migrations](https://github.com/APTrust/registry/tree/master/db/migrations){target=_blank} directory.

They are named in the order they should be run. For example,
001_deposit_stats.sql runs before 002_work_item_restorations.sql.

Each migration begins by setting a `started_at` timestamp in the `schema_migrations` table and ends by setting a `finished_at` timestamp.

## Views

The database uses views for most of Registry's detail and list pages. The old Pharos application used Rails and ActiveRecord to define relations, and typically issued many queries to assemble the data that the new DB assembles in views. Views allow Registry to issue single queries where Rails issued multiple queries.

## Materialized Views

The database includes a number of materialized views to hold statistics that are expensive to calculate. The include counts and sums from large tables. The views are populated hourly by three SQL functions in [db/migrations/001_deposit_stats.sql](https://github.com/APTrust/registry/blob/master/db/migrations/001_deposit_stats.sql){target=_blank}.

These functions are intelligent enough to avoid unnecessary work. They are called by Registry itself every hour or so.

When Registry starts, it creates a single [Context object](https://github.com/APTrust/registry/blob/master/common/context.go){target=_blank} whose initializer calls `initCronJobs()`. That runs the update functions in  [common/cron.go](https://github.com/APTrust/registry/blob/master/common/cron.go){target=_blank} every hour or so.
