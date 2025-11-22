variable "artifactory_url" {
  description = "Base URL of the Artifactory instance (e.g., https://mycompany.jfrog.io)"
  type        = string
}

variable "artifactory_access_token" {
  description = "Access token for authenticating with Artifactory"
  type        = string
  sensitive   = true
}

variable "project_key" {
  description = "Key for the JFrog project; used as prefix for repository keys"
  type        = string
}
