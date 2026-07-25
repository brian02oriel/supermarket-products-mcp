# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

The intent is to build an MCP (Model Context Protocol) server exposing supermarket product data/tools by querying 
from a MongoDB collections.
Treat any architectural decisions as greenfield — there is no existing structure to conform to yet.

## Environment

- Python >= 3.12 (pinned via `.python-version`)
- Dependency management via `uv` (`pyproject.toml` + `uv.lock`)

## Commands

- Install dependencies: `uv sync`
- Run the entry point: `uv run main.py`
- Add a dependency: `uv add <package>`
