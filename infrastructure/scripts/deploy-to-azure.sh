#!/bin/bash
# Deployment script for Soligit backend on Azure VM

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
TERRAFORM_DIR="$PROJECT_ROOT/infrastructure/azure"

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if Terraform is installed
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform is not installed. Please install it first."
        exit 1
    fi
    
    # Check if logged in to Azure
    if ! az account show &> /dev/null; then
        print_error "Not logged in to Azure. Please run 'az login' first."
        exit 1
    fi
    
    print_info "All prerequisites met!"
}

init_terraform() {
    print_info "Initializing Terraform..."
    cd "$TERRAFORM_DIR"
    terraform init
}

plan_infrastructure() {
    print_info "Planning infrastructure changes..."
    cd "$TERRAFORM_DIR"
    terraform plan -out=tfplan
}

apply_infrastructure() {
    print_info "Applying infrastructure changes..."
    cd "$TERRAFORM_DIR"
    terraform apply tfplan
    rm -f tfplan
}

get_vm_ip() {
    cd "$TERRAFORM_DIR"
    terraform output -raw vm_public_ip
}

configure_backend() {
    local VM_IP=$1
    local SSH_USER=$(cd "$TERRAFORM_DIR" && terraform output -raw admin_username 2>/dev/null || echo "azureuser")
    
    print_info "Configuring backend on VM..."
    print_warning "Please update the .env file on the VM with your API keys"
    print_info "SSH to VM: ssh $SSH_USER@$VM_IP"
    print_info "Edit .env: sudo nano /opt/soligit/backend/.env"
    print_info "Restart: sudo systemctl restart supervisor"
}

# Main script
main() {
    print_info "Starting Azure deployment for Soligit backend..."
    
    check_prerequisites
    init_terraform
    plan_infrastructure
    
    read -p "Do you want to apply these changes? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        print_warning "Deployment cancelled."
        exit 0
    fi
    
    apply_infrastructure
    
    VM_IP=$(get_vm_ip)
    
    print_info "Deployment completed successfully!"
    print_info "VM Public IP: $VM_IP"
    print_info "Backend URL: http://$VM_IP:8000"
    print_info "API Docs: http://$VM_IP:8000/docs"
    
    configure_backend "$VM_IP"
}

# Run main function
main "$@"
