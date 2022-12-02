# Code Structure

The [Registry's GitHub repository](https://github.com/APTrust/registry){_target=blank} contains the follwing directories and files:

| Name | Description |
| ---- | ----------- |
| .github/workflows | Just what it says. Workflows including mirroring code to Gitlab. |
| .vscode | Contains a barbones launch.json file telling VS Code how the launch the Registry app. |
| alert_templates | Contains a set of text templates used to send email alerts to Registry users. |
| app | Contains the main application.go file that defines routes, template helpers, and initializes middleware. |
| bin | Contains NSQ and Redis binaries to run external services on Mac and Linux. These are required for testing. See [bin/README.md](https://github.com/APTrust/registry/tree/master/bin){target=_blank} for details. |
| cfn | Contains CloudFormation templates for deploying Registry to Fargate. The key files are [cfn-registry-cluster.tmpl](https://github.com/APTrust/registry/blob/master/cfn/cfn-registry-cluster.tmpl){target=_blank}, which is a template for the deployment file, and [cfn-registry-cluster.yml](https://github.com/APTrust/registry/blob/master/cfn/cfn-registry-cluster.yml){target=_blank}, which is the actual deployment file. |
| common | Contains code commonly used by other components throughout the Registry app. The most important of these are the [Configuration Object](/components/#the-configuration-object) and the [Context Object](/components/#the-context-object). |
| constants | Defines [constants.go](https://github.com/APTrust/registry/blob/master/constants/constants.go){target=_blank} used throughout the application and [permissions.go](https://github.com/APTrust/registry/blob/master/constants/permissions.go){target=_blank} defining which roles can do what. We don't put permissions in the database because we want them to be immutable. |
| db | Contains the database schema, migrations, fixitures, and some utility functions to load fixtures for testing. |
| docs | Contains wireframes used in the UI design process. |
| forms | Defines objects used to render, validate and parse form data. |
| helpers | Defines a number of helper functions used in text and HTML templates. |
| loader | Contains code for a standalone app to load database fixtures. |
| middleware | Contains code for user authentication and authorization, and resource setup used in virtually all web and API requests. |
| network | Contains code for clients that talk to external services, including Authy, NSQ, Redis, and Amazon's SES (Email) and SNS (Text/SMS). |
| pgmodels | Defines the data models for items stored in the Postgres database. |
| static | Contains statically served web resources, including scripts, stylesheets and images. |
| swagger | Contains the output of the Swagger documentation generator. This output is served on our [Swagger doc site](https://aptrust.github.io/registry/){taget=_blank} |
| views | Contains HTML templates for all pages in the Web UI. |
| web | Contains handlers for web requests. Read on... |
| web/api | Contains handlers for API requests. |
| web/api/admin | Contains handlers specific to the admin API, which is the read-write API used by Preserv to process ingests, deletions, restorations and fixity checks. |
| web/api/common | Contains handlers for the read-only member API. Some of these handlers are also used by the admin API. See the routing table in [app/application.go](https://github.com/APTrust/registry/blob/master/app/application.go){target=_blank} |
| web/testutil | Contains utilities for testing the web UI and REST APIs. |
| web/webui | Contains handlers for web UI requests. |
| .env files | Contain settings used in various environments (dev, test, etc.) |
| Dockerfile | Describes how to build Registry's Docker container. |
| Dockerfile.multi | ? |
| Makefile | Contains build commands to create the Docker container and update the CloudFormation deployment template. |
| member_api_v3.yml| Contains a description of the API used to generate Swagger docs. |
| registry | A shell script used to run and/or test the Registry. `./registry serve` runs an instance of the Registry on localhost:8080 (along with NSQ and Redis). `./registry test` runs the test suite. |
| registry.go | The file from which the Registry binary is compiled. Its `main()` method creates an instance of the app and runs it, listening on port 8080. |
