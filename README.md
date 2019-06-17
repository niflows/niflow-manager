# niflow-manager: Niflow package manager tool

[![codecov](https://codecov.io/gh/niflows/niflow-manager/branch/master/graph/badge.svg)](https://codecov.io/gh/niflows/niflow-manager)

Niflows are an organizational structure that is targeted at making neuroimaging
tools and analyses FAIR (findable, accessible, interoperable, and reusable) ith
strong assurances of compatibility across environments.

`niflow-manager`, which provides the `nfm` command-line tool, aims to support
niflow creation, testing, and packaging.
It provides the following sub-commands:

* `nfm init` - Create a stub workflow, with templates for desired languages
* `nfm build` - Package a workflow into supported formats, including
  [Singularity](https://www.sylabs.io/singularity/) and language-specific formats
* `nfm test` - Comprehensive testing across ranges of environments and dependency
  versions
* `nfm install` - Install niflows from an online registry or source

## Other resources

* [Introduction to Niflows](https://effigies.github.io/niflows-intro/#1)
