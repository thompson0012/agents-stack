# Optional Skills Guide

This `AGENTS.md` extends `../AGENTS.md`. Root constitutional rules cannot be overridden.

## Local Scope

This directory contains the template's optional top-level skill packages. Inventory only the immediate child directories here; ignore filesystem noise such as `.DS_Store`.

## Rules

- Packages in this directory are not part of shipped default truth unless a downstream repo both includes and enables them.
- Shipped inventories must not claim these optional packages by default.
- When an optional package is promoted into the default shipped surface, update every affected inventory in the same change.

## Current Top-Level Directories

- `coding-and-data/`
- `cx-ticket-triage/`
- `data-exploration/`
- `feature-spec/`
- `media/`
- `using-documents/`
- `using-finance/`
- `using-legal/`
- `using-marketing/`
- `using-research/`
- `using-sales/`
- `visualization/`
- `website-building/`
