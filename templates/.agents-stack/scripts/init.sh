#!/bin/bash
# agents-stack init script
# Run after copying template into your project

set -e

echo "==> agents-stack init"
echo ""

# Check git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Initializing git repository..."
    git init
fi

# Check for required files
if [ ! -f "CONSTITUTION.md" ]; then
    echo "ERROR: CONSTITUTION.md not found. Are you in the project root?"
    exit 1
fi

# Prompt for project name
read -p "Project name: " project_name
if [ -z "$project_name" ]; then
    project_name=$(basename "$(pwd)")
fi

# Initialize tracked-work.json
cat > .agents-stack/tracked-work.json << EOF
{
  "active": null,
  "parked": [],
  "backlog": []
}
EOF

echo ""
echo "==> Done. agents-stack is ready."
echo ""
echo "Next steps:"
echo "  1. Fill in CONSTITUTION.md with your tech stack and rules"
echo "  2. Edit .agents-stack/reference/architecture.md with your project architecture"
echo "  3. Create your first workstream (orchestrator will guide you)"
echo ""
echo "See ROADMAP.md and AGENTS.md for workflow details."
