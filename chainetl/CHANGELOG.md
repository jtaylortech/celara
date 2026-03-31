# Changelog

All notable changes to ChainETL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-31

### Added
- Published ChainETL to PyPI - now installable via `pip install chainetl`
- Automated PyPI publishing via GitHub Actions on version tags
- Integration test marker for network-dependent tests
- Comprehensive test suite with 91% code coverage

### Changed
- Updated installation instructions to use PyPI as primary method
- Improved test reliability by marking RPC tests as integration tests
- Enhanced CI/CD pipeline with automated testing and publishing

### Fixed
- Fixed all test failures in CI environment
- Fixed CLI error message output (stderr vs stdout)
- Fixed test mock interfaces to match actual implementations
- Fixed config test to handle Pydantic HttpUrl types

## [0.1.0] - 2025-11-16

### Added
- Initial release with core ETL functionality
- Support for Ethereum and Base L2 blockchains
- PostgreSQL loader with checkpointing
- CLI for syncing blocks and checking status
- Batch processing capabilities
- Chain reorganization detection
- Retry logic with exponential backoff
- Structured logging with structlog
- Comprehensive test suite

### Features
- Extract blocks, transactions, and metadata
- Resumable syncs with automatic checkpointing
- Multi-chain support with independent checkpoints
- Type-safe data models using Pydantic
- Production-ready with error handling and logging

[0.2.0]: https://github.com/jtaylortech/celara/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jtaylortech/celara/releases/tag/v0.1.0
