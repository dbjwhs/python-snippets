#!/bin/bash

# Script to run pytest on all Python projects
# Created by Claude

# Color definitions
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Starting directory
START_DIR="../"

# Initialize counters
total_projects=0
successful_projects=0
failed_projects=0

# Array to store results
declare -a results

echo -e "${YELLOW}Starting test run across all Python projects...${NC}"
echo "=================================================="

# Find all directories that could be Python projects and save to temp file to avoid subshell issues
project_files=$(find "$START_DIR" -type f -name "pyproject.toml" -o -name "setup.py")

# Process each project
for project_file in $project_files; do
    project_dir=$(dirname "$project_file")

    # Check if pytest is available for this project
    if [ -d "$project_dir/tests" ] || grep -q "pytest" "$project_file" 2>/dev/null; then
        total_projects=$((total_projects + 1))
        project_name=$(basename "$project_dir")

        echo -e "\n${YELLOW}Testing project: ${project_name}${NC}"
        echo "Directory: $project_dir"

        # Save current directory
        current_dir=$(pwd)

        # Navigate to project directory
        cd "$project_dir" || continue

        # Check for venv/virtualenv
        venv_activated=false
        if [ -d "venv" ]; then
            echo "Activating venv..."
            source venv/bin/activate
            venv_activated=true
        elif [ -d ".venv" ]; then
            echo "Activating .venv..."
            source .venv/bin/activate
            venv_activated=true
        fi

        # Run pytest
        echo "Running pytest..."
        if python -m pytest; then
            echo -e "${GREEN}✓ Tests passed for $project_name${NC}"
            results+=("${GREEN}✓ $project_name${NC}")
            successful_projects=$((successful_projects + 1))
        else
            echo -e "${RED}✗ Tests failed for $project_name${NC}"
            results+=("${RED}✗ $project_name${NC}")
            failed_projects=$((failed_projects + 1))
        fi

        # Deactivate venv if it was activated
        if [ "$venv_activated" = true ]; then
            echo "Deactivating venv..."
            deactivate
        fi

        # Return to original directory
        cd "$current_dir" || exit
    fi
done

# Print summary
echo -e "\n\n${YELLOW}Test Run Summary${NC}"
echo "=================================================="
for result in "${results[@]}"; do
    echo -e "$result"
done

echo -e "\n${YELLOW}Results:${NC}"
echo -e "${GREEN}Successful: $successful_projects${NC}"
echo -e "${RED}Failed: $failed_projects${NC}"
echo -e "Total projects tested: $total_projects"
echo "=================================================="

if [ "$failed_projects" -eq 0 ] && [ "$total_projects" -gt 0 ]; then
    echo -e "${GREEN}All tests passed successfully!${NC}"
    exit 0
else
    if [ "$total_projects" -eq 0 ]; then
        echo -e "${YELLOW}No Python projects with tests were found.${NC}"
        exit 0
    else
        echo -e "${RED}Some tests failed. Please review the failures.${NC}"
        exit 1
    fi
fi
