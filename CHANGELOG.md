# <bootstrap-title> Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0] - 2025-06-23
### Added
- Implement exporting bootstraps templates operation. See `py_bootstrap/operations/export_bootstrap.py` file for details.

## [0.5.0] - 2025-06-23
## Added
- Implement `FilesProcessors` functionality. See `py_bootstrap/files_processors/` directory for details.

### Changed
- Refactor operations functionality. See `py_bootstrap/operations/` directory for details.
- Rename `BaseOperationsDispatcher` to `BaseRecursiveOperationsContainer`, move it in a separated file. See `/py_bootstrap/base/operations/recursive_container.py` file for details.

### [0.4.0] - 2025-06-02
### Added
- Implement `RegisterBootstrapOperation` class for registering new customer's bootstraps. See `/py_bootstrap/operations/register_bootstrap.py` file for details.
- Prepare `template` bootstrap structure. See `/py_bootstrap/templates/template/` directory for details.

## [0.3.0] - 2025-06-01
### Added
- Prepare `application` bootstrap structure. See `/py_bootstrap/templates/application/` directory for details.

## [0.2.0] - 2025-06-01
### Added
- Prepare `package` bootstrap structure. See `/py_bootstrap/templates/package/` directory for details.
- Implement `BuildBootstrapOperation` class for generating a given bootstrap. See `/py_bootstrap/operations/build_bootstraps.py` file for details.
- Implement `ListBootstrapsOperation` class for printing enabled bootstraps. See `/py_bootstrap/operations/list_bootstraps.py` file for details.
- Implement the main script for running bootstrap operations. See `/py_bootstrap/scripts/bootstrap.py` file for details.
- Implement base functionality for operations. See `/py_bootstrap/base/operations.py` file for details.

### Added
- Prepare the project structure. See `/` directory for details.
- Implement the main CLI entrypoint. See `/py_bootstrap/cli_entrypoint.py` file for details.

## [0.1.0] - 2024-06-08

### Added
- Prepare a common skeleton based on tox automation.
