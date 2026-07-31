variable "project_id" {
  type        = string
  description = "Google Cloud Project ID"
  default     = "gen-lang-client-0748552619"
}

variable "region" {
  type        = string
  description = "Google Cloud primary region for resources"
  default     = "us-central1"
}

variable "environment" {
  type        = string
  description = "Deployment environment name (dev/prod)"
  default     = "dev"
}
