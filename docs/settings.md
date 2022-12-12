# Settings

Registry loads settings into its [config object](https://github.com/APTrust/registry/blob/master/common/config.go){target=_blank} the first time the [common.Context()](https://github.com/APTrust/registry/blob/master/common/context.go){target=_blank} function is called.

Registry loads settings from the .env file whose name matched the `APT_ENV` environment variable. For example, if `APT_ENV=dev`, Registry will load settings from the `.env.dev` file in the top level directory of the Registry project. If `APT_ENV=test`, it will load `.env.test`.

After loading settings from the file, the config object loads them from the environment using Viper's `AutomaticEnv()` function. **Values loaded from the environment override values defined in the .env file.**

This is handy in Fargate/ECS because we can store sensitive settings, such as database credentials, in Amazon's Parameter Store. Before ECS starts the Registry's Docker container, it runs a sidecar process to load environment variables from Parameter Store. Those variables are then available in the environment when Registry starts, and the config object can read them.

!!! Danger

    Store sensitive credentials in your local environment for dev and test, or in parameter store for live environments. Otherwise, you risk accidentally leaking credentials, most likely in a GitHub commit.

    Sentive credentials include:

    * AWS_ACCESS_KEY_ID
    * AWS_SECRET_ACCESS_KEY
    * COOKIE_BLOCK_KEY
    * COOKIE_HASH_KEY
    * DB_HOST
    * DB_USER
    * DB_PASSWORD
    * REDIS_PASSWORD

## Setting Definitions

| Name | Description |
| ---- | ----------- |
| AWS_ACCESS_KEY_ID | AWS access key for connecting to SES and SNS services. |
| AWS_REGION | The AWS region to connect to for SES and SNS services. This should be the same region Registry runs in, which is `us-east-1a`. |
| AWS_SECRET_ACCESS_KEY | The AWS secret key for connecting to SES and SNS services. |
| COOKIE BLOCK_KEY | Used along with COOKIE_HASH_KEY to encrypt cookies stored in the user's browser. |
| COOKIE_DOMAIN | The name of the domain that can set and read cookies. For development and test, this should be `localhost`. For live environments, it should match the fully qualified domain name, e.g. `staging.aptrust.org`. |
| COOKIE_HASH_KEY | Used along with COOKIE_BLOCK_KEY to encrypt cookies stored in the user's browser. |
| DB_DRIVER | The name of the dabase driver. This should always be `postgres`. |
| DB_HOST | The name of the databse host. For dev and test, this should be `localhost`. For live environments, it should be the fully qualified domain name or internal private hostname of the RDS instance that hosts our postgres database. |
| DB_NAME | The name of the database. E.g. `apt_registry_test` or `pharos_demo`. |
| DB_PASSWORD | The password to connect to the postgres database. |
| DB_PORT | The postgres database port. Usually 5432. |
| DB_USER | The username to connect to the postgres database. |
| DB_USE_SSL | Should we use SSL when connecting to the database? For localhost connections, this is usually false. For RDS connections, it should be true. |
| EMAIL_ENABLED | Set this to true on all live systems and to false for dev and test systems. When set to false, Registry will print the contents of emails to STDOUT. This is helpful for testing "forgot password" emails and deletion confirmation emails. |
| EMAIL_FROM_ADDRESS | The from address to attach to all system-generated emails. Typically, this is `help@aptrust.org`. |
| ENABLE_TWO_FACTOR_AUTHY | Set this to true in live systems and false in dev and test systems. |
| ENABLE_TWO_FACTOR_SMS | Set this to true in live systems and false in dev and test systems. When set to false, Registry will print two-factor SMS codes to STDOUT so developers can complete the login process. |
| FLASH_COOKIE_NAME | The name of the cookie used to display transient notifications in the web UI. |
| HTTPS_COOKIES | Set this to true on live systems that use HTTPS connections, and to false for dev and test setups that run on localhost. |
| LOG_CALLER | When true, this logs additional information about the calling function in certain log messages. For live systems, this should be false, unless we're debugging difficult issues. |
| LOG_FILE | The path to the file where Registry should write its log statements. Setting this `STDOUT` causes Registry to log to STDOUT. On live systems, set this to `STDOUT` so the logs go into CloudWatch. |
| LOG_LEVEL | This describes how detailed the logs should be. For production systems, we generally want 1 (info). For dev and test systems, 0 (debug) will provide additional information. Allowed values are: -1: Trace, 0: Debug, 1: Info, 2: Warn, 3: Error, 4: Fatal, 5: Panic, 6: None, 7: Disabled |
| LOG_SQL | If true, Registry will log all SQL statements. We almost always want this set to false because it produces massive logs. Use this only to debug tricky SQL issues. |
| LOG_TO_CONSOLE | If true, Registry will log to the console as well as to the log file. On live systems (prod, demo, staging), this should be false because we log to STDOUT anyway. On dev and test systems, you can set this to true to watch the logs in your console as you interact with Registry. |
| NSQ_URL | The URL of the NSQ service. Note that NSQ usually runs three processes (nsqd, nsqlookupd, and nsqadmin) on three different ports. The one you want here is nsqd, which runs on port 4151. On a local dev machine, this will be http://localhost:4151 |
| OTP_EXPIRATION | The time before a two-factor OTP token expires. These tokens are sent via SMS. This setting uses Go's time notation, so `90s` is 90 seconds, `15m` is 15 minutes, `1h` is one hour.  |
| PREFS_COOKIE_NAME | The name of Registry's preferences cookie. This is not yet in use, but may be in future. |
| REDIS_DEFAULT_DB | The default Redis database we want to connect to. This is a numeric value between 0-15, and is almost always `0` (zero). |
| REDIS_PASSWORD | The password used to connect to the Redis database. |
| REDIS_URL | The URL of the Redis server to connect to. This should include a hostname and port, but not a protocol. E.g. `localhost:6379`. |
| SESSION_COOKIE_NAME | The name of the Registry's session cookie. |
| SESSION_MAX_AGE | The maximum time, in seconds, that the session cookie can live. This is usually set between 86400 (one day) and 604800 (seven days). Note that this setting actually applies to **all** cookies. |
