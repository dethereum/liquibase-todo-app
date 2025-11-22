resource "artifactory_local_pypi_repository" "pypi-local" {
  key                  = "${var.project_key}-pypi-local"
  repo_layout_ref      = "simple-default"
  project_environments = ["DEV"]

  lifecycle {
    ignore_changes = [
      project_key
    ]
  }
}

resource "artifactory_remote_pypi_repository" "pypi-remote" {
  key                    = "${var.project_key}-pypi-remote"
  url                    = "https://files.pythonhosted.org"
  pypi_registry_url      = "https://pypi.org"
  pypi_repository_suffix = "simple"
  project_environments   = ["DEV"]

  lifecycle {
    ignore_changes = [
      project_key
    ]
  }
}

resource "artifactory_virtual_pypi_repository" "pypi" {
  key                  = "${var.project_key}-pypi"
  repo_layout_ref      = "simple-default"
  project_environments = ["DEV"]

  lifecycle {
    ignore_changes = [
      project_key
    ]
  }

  repositories = [
    artifactory_local_pypi_repository.pypi-local.key,
    artifactory_remote_pypi_repository.pypi-remote.key
  ]
}

resource "project" "lta" {
  key          = var.project_key
  display_name = var.repo_name
  admin_privileges {
    manage_members   = true
    manage_resources = true
    index_resources  = true
  }
}

locals {
  repo_keys = {
    "${var.project_key}-pypi-local"  = artifactory_local_pypi_repository.pypi-local.key
    "${var.project_key}-pypi-remote" = artifactory_remote_pypi_repository.pypi-remote.key
    "${var.project_key}-pypi"        = artifactory_virtual_pypi_repository.pypi.key
  }
}

resource "project_repository" "pypi" {
  for_each    = local.repo_keys
  project_key = project.lta.key
  key         = each.value
}