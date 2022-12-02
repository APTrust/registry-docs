# Registry Documentation

This project contains documentation for APTrust's Registry. It does not try to duplicate the REST API documentation at https://aptrust.github.io/registry/. Instead, it covers technical details required to debug, maintain, and extend the code.

This is a source repository. The public-facing documentation lives at https://aptrust.github.io/registry-docs/.

## Local Editing

If you want to edit this documentation locally, you'll need Python 3.x and pip. To set it all up, just run
`pip install -r requirements.txt`. Then you can start the server with `mkdocs serve`.

If you get a message saying mkdocs is not installed, try running the server with this command: `python3 -m mkdocs serve`

## Deploying to GitHub pages

```
mkdocs gh-deploy
```

or

```
python3 -m mkdocs gh-deploy
```
