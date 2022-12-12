# Testing

To run the Registry's unit tests, simply run `./registry test` from the project's top-level directory.

Note that `/registry` is a bash script. When run with the `test` argument, it does the following:

1. Starts a local instance of Registry.
2. Starts a local instance of NSQ.
3. Starts a local instance of Redis.
4. Runs unit tests.
5. Runs basic integration tests with NSQ and Redis.

The Redis and NSQ binaries are stored in the project's bin directory, under `bin/linux` and `bin/osx`.

!!! Note

    The Registry test suite assumes you have a Registry database
    running inside a local Postgres instance. If you don't see the
    [Registry README](https://github.com/APTrust/registry/blob/master/README.md){target=_blank}
    for info on how to set one up.

## Thorough Testing

Registry's unit and integration tests will tell you whether the system's basic functions are operating as expected, and they will generally catch regressions caused by new or updated code.

These tests, however, do not really tell you how Registry will behave in the context of a fully-functioning APTrust environment. Registry's ability to interact correctly with Preservation Services is the most important thing to ensure, and for that, you'll need to run Preserv's integration and end-to-end test suites.

For more on that, see the [Preserv testing guide](https://aptrust.github.io/preserv-docs/testing/){target=_blank}.

!!! important

    If you make any changes to Registry that may affect its interaction with Preserv, run the Preserv integration and end-to-end tests before committing your new code to the master branch.
