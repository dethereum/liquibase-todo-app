data "github_repository" "gh-repo" {
  name = var.repo_name
}

resource "github_actions_variable" "jf_url_variable" {
  repository    = data.github_repository.gh-repo.name
  variable_name = "JF_URL"
  value         = var.artifactory_url
}

resource "github_actions_variable" "pypi_repository_variable" {
  repository    = data.github_repository.gh-repo.name
  variable_name = "PYPI_REPOSITORY"
  value         = artifactory_virtual_pypi_repository.pypi.key
}
