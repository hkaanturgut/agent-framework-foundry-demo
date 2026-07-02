variable "location" {
  description = "Azure location for the Foundry resources."
  type        = string
  default     = "canadacentral"
}

variable "name_prefix" {
  description = "Prefix used to build resource names."
  type        = string
  default     = "build26foundry"
}

variable "environment" {
  description = "Environment name used in naming/tagging."
  type        = string
  default     = "dev"
}

variable "resource_group_name" {
  description = "Optional override for resource group name."
  type        = string
  default     = null
}

variable "project_name" {
  description = "Foundry project resource name."
  type        = string
  default     = "launch-desk"
}

variable "project_display_name" {
  description = "Display name shown in Foundry for the project."
  type        = string
  default     = "Contoso Launch Desk"
}

variable "project_description" {
  description = "Description shown in Foundry for the project."
  type        = string
  default     = "Build 2026 recap demo project for MAF + Foundry Toolkit."
}

variable "ai_services_sku_name" {
  description = "SKU for the AI Services (Foundry) account."
  type        = string
  default     = "S0"
}

variable "allow_project_management" {
  description = "Enables creation of Foundry project child resources under the AI Services account."
  type        = bool
  default     = true
}

variable "public_network_access_enabled" {
  description = "Whether public network access is enabled for the AI Services account."
  type        = bool
  default     = true
}

variable "local_auth_enabled" {
  description = "Whether local key auth is enabled for the AI Services account."
  type        = bool
  default     = false
}

variable "custom_subdomain_name" {
  description = "Optional custom subdomain for token-based auth. If null, defaults to the generated account name."
  type        = string
  default     = null
}

variable "network_acls" {
  description = "Optional network ACL configuration for the AI Services account."
  type = object({
    default_action = string
    ip_rules       = optional(set(string))
    virtual_network_rules = optional(set(object({
      ignore_missing_vnet_service_endpoint = optional(bool)
      subnet_id                            = string
    })))
    bypass = optional(string)
  })
  default = null
}

variable "account_role_assignments" {
  description = "Optional role assignments to create at the AI Services account scope."
  type = map(object({
    role_definition_id_or_name             = string
    principal_id                           = string
    description                            = optional(string)
    skip_service_principal_aad_check       = optional(bool)
    condition                              = optional(string)
    condition_version                      = optional(string)
    delegated_managed_identity_resource_id = optional(string)
    principal_type                         = optional(string)
  }))
  default = {}
}

variable "project_role_assignments" {
  description = "Optional role assignments to create at the Foundry project scope."
  type = map(object({
    principal_id                           = string
    role_definition_name                   = optional(string)
    role_definition_id                     = optional(string)
    description                            = optional(string)
    principal_type                         = optional(string)
    condition                              = optional(string)
    condition_version                      = optional(string)
    delegated_managed_identity_resource_id = optional(string)
    skip_service_principal_aad_check       = optional(bool)
  }))
  default = {}

  validation {
    condition = alltrue([
      for assignment in values(var.project_role_assignments) :
      (
        (try(assignment.role_definition_name, null) != null ? 1 : 0) +
        (try(assignment.role_definition_id, null) != null ? 1 : 0)
      ) == 1
    ])
    error_message = "Each project_role_assignments entry must set exactly one of role_definition_name or role_definition_id."
  }
}

variable "cognitive_deployments" {
  description = "Optional OpenAI model deployments passed to the AVM Cognitive Services module."
  type        = map(any)
  default     = {}
}

variable "foundry_model_name" {
  description = "Model or deployment name the app should use when targeting the Foundry project endpoint."
  type        = string
  default     = "gpt-4o-mini"
}

variable "tags" {
  description = "Additional tags applied to resources."
  type        = map(string)
  default     = {}
}

variable "enable_telemetry" {
  description = "Controls AVM telemetry emitted by modules."
  type        = bool
  default     = false
}
