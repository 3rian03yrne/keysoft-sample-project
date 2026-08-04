# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

See @README.md for project overview and @pyproject.toml for project config.

# Logging
- Use the `logging` logger, never `print()`.

# Code Style
- All Modules should include docstrings
- All functions should include multiline docstrings
- Public functions have **type hints**.
- On failure, **raise** a domain error or return a structured `{"ok": False, "error": ...}` —
  never a silent empty result.

# Testing 
- Use pytest for testing
- Include new test for any new functionality
