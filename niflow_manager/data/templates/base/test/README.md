The test directory may contain two subdirectories:

* `scripts` - analyses for testing and locally-defined tests
* `data` - data files that are needed for analyses and testing
(i.e. reference output).

This is the default place to keep these directories, but in `spec.yml`
the paths can be overwritten.

The `data` directory may contain large files and may be better handled
via [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) and
[DataLad](http://docs.datalad.org) than by directly including them in the repository.
(not implemented in TestKraken yet!)
