#!/bin/bash
# Script to destroy Azure infrastructure for Soligit

set -e

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
TERRAFORM_DIR="$PROJECT_ROOT/infrastructure/azure"

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Main
print_warning "This will DESTROY all Azure resources for Soligit!"
print_warning "This action cannot be undone."
echo ""
read -p "Are you absolutely sure? Type 'destroy' to confirm: " confirm

if [ "$confirm" != "destroy" ]; then
    print_error "Destruction cancelled."
    exit 0
fi

cd "$TERRAFORM_DIR"
terraform destroy

echo "All resources have been destroyed."
