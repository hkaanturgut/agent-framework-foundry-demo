resource "random_string" "account_suffix" {
  length  = 6
  upper   = false
  special = false
}

locals {
  normalized_prefix_raw = replace(lower(var.name_prefix), "/[^a-z0-9]/", "")
  normalized_prefix     = length(local.normalized_prefix_raw) > 0 ? substr(local.normalized_prefix_raw, 0, 10) : "build26"

  normalized_environment_raw = replace(lower(var.environment), "/[^a-z0-9]/", "")
  normalized_environment     = length(local.normalized_environment_raw) > 0 ? substr(local.normalized_environment_raw, 0, 6) : "dev"

  resource_group_name = coalesce(var.resource_group_name, "rg-${local.normalized_prefix}-${local.normalized_environment}")

  ai_services_account_name = substr(
    "${local.normalized_prefix}${local.normalized_environment}${random_string.account_suffix.result}",
    0,
    24
  )

  project_name_raw     = replace(lower(var.project_name), "/[^a-z0-9-]/", "-")
  project_name_trimmed = trim(local.project_name_raw, "-")
  foundry_project_name = length(local.project_name_trimmed) > 0 ? substr(local.project_name_trimmed, 0, 63) : "launch-desk"

  default_tags = {
    demo        = "build-2026-recap"
    workload    = "foundry-agent-framework"
    environment = var.environment
  }

  effective_tags = merge(local.default_tags, var.tags)

  effective_project_role_assignments = {
    for key, assignment in var.project_role_assignments : key => {
      principal_id                           = assignment.principal_id
      role_definition_name                   = try(assignment.role_definition_name, null)
      role_definition_id                     = try(assignment.role_definition_id, null)
      description                            = try(assignment.description, null)
      principal_type                         = try(assignment.principal_type, null)
      condition                              = try(assignment.condition, null)
      condition_version                      = try(assignment.condition_version, null)
      delegated_managed_identity_resource_id = try(assignment.delegated_managed_identity_resource_id, null)
      skip_service_principal_aad_check       = try(assignment.skip_service_principal_aad_check, false)
    }
  }
}

module "resource_group" {
  source  = "Azure/avm-res-resources-resourcegroup/azurerm"
  version = "0.4.0"

  name             = local.resource_group_name
  location         = var.location
  tags             = local.effective_tags
  enable_telemetry = var.enable_telemetry
}

module "ai_services" {
  source  = "Azure/avm-res-cognitiveservices-account/azurerm"
  version = "0.11.1"

  name                          = local.ai_services_account_name
  location                      = var.location
  parent_id                     = module.resource_group.resource_id
  kind                          = "AIServices"
  sku_name                      = var.ai_services_sku_name
  allow_project_management      = var.allow_project_management
  local_auth_enabled            = var.local_auth_enabled
  public_network_access_enabled = var.public_network_access_enabled
  custom_subdomain_name         = coalesce(var.custom_subdomain_name, local.ai_services_account_name)
  network_acls                  = var.network_acls
  role_assignments              = var.account_role_assignments
  cognitive_deployments         = var.cognitive_deployments
  managed_identities = {
    system_assigned = true
  }
  deployment_serialization_enabled = true
  dynamic_throttling_enabled       = true
  tags                             = local.effective_tags
  enable_telemetry                 = var.enable_telemetry
}

resource "azapi_resource" "foundry_project" {
  type      = "Microsoft.CognitiveServices/accounts/projects@2025-06-01"
  name      = local.foundry_project_name
  parent_id = module.ai_services.resource_id
  location  = var.location

  identity {
    type = "SystemAssigned"
  }

  body = {
    properties = {
      displayName = var.project_display_name
      description = var.project_description
    }
  }

  tags                      = local.effective_tags
  schema_validation_enabled = false
  response_export_values    = ["*"]
}

resource "azurerm_role_assignment" "project" {
  for_each = local.effective_project_role_assignments

  scope                                  = azapi_resource.foundry_project.id
  principal_id                           = each.value.principal_id
  role_definition_name                   = each.value.role_definition_id == null ? each.value.role_definition_name : null
  role_definition_id                     = each.value.role_definition_id
  description                            = each.value.description
  principal_type                         = each.value.principal_type
  condition                              = each.value.condition
  condition_version                      = each.value.condition_version
  delegated_managed_identity_resource_id = each.value.delegated_managed_identity_resource_id
  skip_service_principal_aad_check       = each.value.skip_service_principal_aad_check
}
