terraform {
  required_providers {
    artifactory = {
      source  = "jfrog/artifactory"
      version = "12.3.3"
    }

    project = {
      source  = "jfrog/project"
      version = "1.9.5"
    }

    github = {
      source  = "integrations/github"
      version = "6.8.3"
    }
  }
}

provider "artifactory" {
  url          = "${var.artifactory_url}/artifactory"
  access_token = var.artifactory_access_token
}

provider "project" {
  url = var.artifactory_url
  access_token = var.artifactory_access_token
}

provider "github" {
  token = var.github_access_token
}
