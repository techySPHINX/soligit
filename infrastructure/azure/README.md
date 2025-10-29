# Azure Infrastructure for Soligit Backend

This directory contains Terraform configuration files to deploy the Soligit backend on Azure Virtual Machine.

## Prerequisites

1. **Azure Account**: You need an active Azure subscription
2. **Azure CLI**: Install from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
3. **Terraform**: Install from https://www.terraform.io/downloads

## Setup Instructions

### 1. Install Azure CLI and Login

```bash
# Install Azure CLI (Windows)
winget install Microsoft.AzureCLI

# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### 2. Install Terraform

```bash
# Windows (using Chocolatey)
choco install terraform

# Or download from https://www.terraform.io/downloads
```

### 3. Configure Variables

```bash
# Copy the example file
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values
notepad terraform.tfvars
```

Update the following in `terraform.tfvars`:
- `admin_password`: Set a strong password
- `location`: Choose your preferred Azure region (e.g., "eastus", "westus2", "westeurope")
- Other variables as needed

### 4. Deploy Infrastructure

```bash
# Navigate to infrastructure directory
cd infrastructure/azure

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

Type `yes` when prompted to confirm.

### 5. Get Connection Details

After deployment, Terraform will output:
- `vm_public_ip`: Public IP address of your VM
- `ssh_command`: SSH command to connect to the VM
- `backend_url`: URL to access your backend API

```bash
# View outputs
terraform output
```

### 6. Configure Environment Variables

SSH into the VM and update the `.env` file:

```bash
# SSH to the VM
ssh azureuser@<VM_PUBLIC_IP>

# Edit the .env file
sudo nano /opt/soligit/backend/.env
```

Update with your actual API keys:
- `GEMINI_API_KEY`
- `WEAVIATE_API_KEY`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `AAI_TOKEN`

Then restart the backend:

```bash
sudo systemctl restart supervisor
```

### 7. Verify Deployment

```bash
# Check if backend is running
curl http://<VM_PUBLIC_IP>:8000

# Or visit in browser
http://<VM_PUBLIC_IP>:8000/docs
```

## Management Commands

### Redeploy Application

```bash
# SSH to VM
ssh azureuser@<VM_PUBLIC_IP>

# Run deployment script
sudo /opt/soligit/deploy.sh
```

### Check Application Logs

```bash
# Backend logs
sudo tail -f /var/log/soligit-backend.out.log
sudo tail -f /var/log/soligit-backend.err.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
# Restart backend
sudo supervisorctl restart soligit-backend

# Restart nginx
sudo systemctl restart nginx
```

## Infrastructure Management

### Update Infrastructure

```bash
# Make changes to .tf files
# Then apply changes
terraform apply
```

### Destroy Infrastructure

```bash
# WARNING: This will delete all resources
terraform destroy
```

Type `yes` when prompted.

## Cost Estimation

Using `Standard_B2s` VM:
- VM: ~$30-40/month
- Storage: ~$5-10/month
- Bandwidth: Variable based on usage
- **Total: ~$35-50/month**

## Security Best Practices

1. **Change Default Password**: Use a strong, unique password
2. **Update .env File**: Never commit real API keys to git
3. **Enable HTTPS**: Configure SSL certificate (Let's Encrypt recommended)
4. **Update Regularly**: Keep system and packages updated
5. **Monitor Logs**: Regularly check logs for suspicious activity
6. **Backup Data**: Set up regular backups for important data

## Troubleshooting

### Cannot SSH to VM
- Check NSG rules allow port 22
- Verify public IP is correct
- Check VM is running

### Backend Not Responding
```bash
# Check if backend is running
sudo supervisorctl status soligit-backend

# Restart if needed
sudo supervisorctl restart soligit-backend
```

### Out of Memory
- Upgrade VM size to `Standard_B2ms` or larger
- Monitor memory usage with `htop`

## Architecture

```
Internet
   |
   v
Azure Public IP
   |
   v
Network Security Group (Firewall)
   |
   v
Virtual Network
   |
   v
VM with Ubuntu 22.04
   |
   +-- Nginx (Reverse Proxy) :80
   |
   +-- FastAPI Backend :8000
   |
   +-- Python Virtual Environment
   |
   +-- Application Code (/opt/soligit)
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/techySPHINX/soligit/issues
- Azure Support: https://azure.microsoft.com/support/
