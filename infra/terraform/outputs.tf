output "resource_group_name" {
  description = "Deployed resource group name."
  value       = module.resource_group.name
}

output "ai_services_account_name" {
  description = "AI Services account name."
  value       = module.ai_services.name
}

output "ai_services_account_id" {
  description = "AI Services account resource ID."
  value       = module.ai_services.resource_id
}

output "ai_services_endpoint" {
  description = "AI Services account endpoint."
  value       = module.ai_services.endpoint
}

output "foundry_project_name" {
  description = "Foundry project name."
  value       = azapi_resource.foundry_project.name
}

output "foundry_project_id" {
  description = "Foundry project resource ID."
  value       = azapi_resource.foundry_project.id
}

output "foundry_project_endpoint" {
  description = "Project endpoint used by the Python demo (`FOUNDRY_PROJECT_ENDPOINT`)."
  value       = "https://${module.ai_services.name}.services.ai.azure.com/api/projects/${azapi_resource.foundry_project.name}"
}

output "portal_links" {
  description = "Portal URLs for the account and project."
  value = {
    account = "https://portal.azure.com/#@/resource${module.ai_services.resource_id}"
    project = "https://portal.azure.com/#@/resource${azapi_resource.foundry_project.id}"
  }
}

output "env_snippet" {
  description = "Paste these values into `.env` to run the app against Foundry."
  value       = <<-EOT
MODEL_BACKEND=foundry
FOUNDRY_PROJECT_ENDPOINT=https://${module.ai_services.name}.services.ai.azure.com/api/projects/${azapi_resource.foundry_project.name}
FOUNDRY_MODEL=${var.foundry_model_name}
EOT
}
