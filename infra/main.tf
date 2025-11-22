resource "artifactory_local_pypi_repository" "pypi-libs" {
  key             = "pypi-libs"
  repo_layout_ref = "simple-default"
  description     = "A pypi repository for python packages"
}