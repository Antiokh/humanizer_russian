#!/usr/bin/env python3
"""Compatibility entry point for the audited Ilyakhov integration.

The previous validator encoded the old 36-pattern / 24-recommendation registry
as if its soft-lint choices were the runtime contract. That registry remains
historical provenance, but runtime integration is now governed by the 102-rule
source study and integration matrix.
"""

from __future__ import annotations

from validate_ilyakhov_integration import main


if __name__ == "__main__":
    main()
