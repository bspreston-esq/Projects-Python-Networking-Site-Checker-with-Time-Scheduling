# Site Checker with Time Scheduling

**Category:** Networking

## Problem

An application that attempts to connect to a website or server every so many minutes or a given time and check if it is up. If it is down, it will notify you by email or by posting a notice on screen.

## Solution

Performs an HTTP GET with a configurable timeout and reports up/down, status code and latency; `--interval` (minutes) and `--count` schedule repeated checks and print a timestamped notice on screen. The demo starts a local server and also checks a closed port to exercise both outcomes.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py https://example.com
python3 main.py https://example.com --interval 5 --count 12
python3 main.py --demo
```

## Example

```text
up   status=200 5.4 ms (ok)
down status=None 0.1 ms (<urlopen error [Errno 111] Connection refused>)
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
