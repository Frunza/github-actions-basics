# GitHub Actions basics

## Goal

Learn how to write basic `GitHub Actions` for one of our applications.

## Prerequisites

A Linux or MacOS machine for local development. If you are running Windows, you first need to set up the *Windows Subsystem for Linux (WSL)* environment.

You need `docker cli` on your machine for testing purposes, and/or on the machines that run your pipeline.
You can check this by running the following command:
```sh
docker --version
```

## What we have

In our scenario, let's imagine that we have a small `python` application and some unit tests for it. Of course we use very good practices and have everything running in `Docker` containers.

Let's start with a `python` file that has a function:
```python
#!/usr/bin/env python3

from typing import Dict, List, Any

def formatLinks(links: List[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for link in links:
        if not isinstance(link, dict):
            continue
        label = str(link.get("label", "")).strip()
        url = str(link.get("url", "")).strip()
        if label and url:
            parts.append(f"[{label}]({url})")
    return " ".join(parts)
```
, located at *app/generate.py*.

Our unit tests look like:
```python
# unit-tests/test_generate.py
import unittest

import sys
sys.path.append('app')
from app.generate import formatLinks

class TestGenerate(unittest.TestCase):

    def test_formatLinks_emptyList(self):
        """Should return empty string when links list is empty"""
        result = formatLinks([])
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
```

To run everything in a `Docker` container we have the following *Dockerfile*:
```dockerfile
# Dockerfile
FROM python:3.13-alpine

COPY . /app
WORKDIR /app
```

Our *docker-compose* file is running the unit tests and looks like:
```yaml
# docker-compose.yml
services:
  main:
    image: pythonunittests
    working_dir: /app
    entrypoint: ["sh", "-c"]
    command: ["python3 -m unittest discover -s ./unit-tests -p 'test_*.py'"]
```

We run everything from a script named *test.sh*:
```sh
#!/bin/sh
set -e

docker build -t pythonunittests .
docker compose run --rm main
```

This means that on our local machine we can just run:
```sh
sh test.sh
```
to trigger the unit tests.

## What we want

Since we have a setup that runs in a `Docker` container, we now want to add `GitHub Actions`.

## Implementation

Since our setup only involves calling the *test.sh* script, we need to use a machine with `docker cli` available to run our pipeline. The only thing to do is to create a `GitHub` *workflow* like:
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run tests
        run: sh test.sh
```
at *.github/workflows/ci.yml*. If we use *ubuntu-latest* as the base image for our machine, we get `docker cli` out of the box. In the first step of the workflow we just check out our repository, and afterwards run the script, exactly as we run it locally.

## Final thoughts

If you follow this pattern, you have the advantage of keeping your `GitHub` *workflow* minimal, and you can run the same code locally as long as you have `docker cli` installed and all necessary required environment variables, if any. Another advantage is that you can very easily migrate this to any other *CI/CD* tool like `GitLab` or others.
