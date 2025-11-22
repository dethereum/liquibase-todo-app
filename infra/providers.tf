terraform {
  required_providers {
      artifactory = {
        source  = "jfrog/artifactory"
        version = "12.3.3"
      }
  }
}

provider "artifactory" {
  url           = "${var.artifactory_url}/artifactory"
  access_token  = "${var.artifactory_access_token}"
}
