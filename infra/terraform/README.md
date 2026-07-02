# Foundry package demo (Terraform + AVM + CI/CD)

This folder packages the infrastructure side of the talk:

- **AVM module** for Resource Group (`avm-res-resources-resourcegroup`)
- **AVM module** for AI Services account (`avm-res-cognitiveservices-account`)
- **AzAPI resource** for Foundry project (`Microsoft.CognitiveServices/accounts/projects@2025-06-01`)
- Optional account/project **RBAC** and optional model deployments
- GitHub Actions workflow at `.github/workflows/terraform-foundry-cicd.yml`

## What it deploys

1. Resource group  
2. AI Services (Foundry) account (`kind = AIServices`, project management enabled)  
3. Foundry project child resource under that account  
4. Optional role assignments and optional OpenAI deployments

## Local usage

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -auto-approve -var-file=terraform.tfvars
```

Then copy the output snippet into your app `.env`:

```bash
terraform output -raw env_snippet
```

## CI/CD workflow

Workflow: `.github/workflows/terraform-foundry-cicd.yml`

- **PR / push**: `fmt` + `validate`; `plan` runs when Azure OIDC secrets are configured.
- **Manual deploy**: run **workflow_dispatch** with `apply=true`.

### Required GitHub secrets (OIDC)

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

These are for an Entra app/service principal configured with GitHub OIDC federation.

### Optional backend secrets (remote state)

If provided, the workflow initializes an AzureRM backend instead of local state:

- `TFSTATE_RESOURCE_GROUP`
- `TFSTATE_STORAGE_ACCOUNT`
- `TFSTATE_CONTAINER`
- `TFSTATE_KEY`

If omitted, the workflow uses local backend (`-backend=false`) for demo friendliness.

## Notes

- The app repo itself is backend-agnostic; this package just provisions Foundry resources.
- For private networking scenarios, extend `network_acls`/private endpoints and use deployment approvals in GitHub environments.
