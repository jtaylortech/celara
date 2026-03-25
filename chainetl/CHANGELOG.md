# Changelog

All notable changes to ChainETL will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Polygon PoS chain support
- Arbitrum One chain support
- `chainetl chains` command to list supported blockchains
- GitHub Actions CI pipeline (Python 3.11–3.13, lint, type check, tests)
- `block_hash` field on Log model

### Changed
- Unified all EVM extractors into single `EVMExtractor` base class
- Chain-specific extractors are now thin wrappers (DRY refactor, -490 lines)
- CLI uses chain registry pattern instead of if/else branching
- Tests fully mocked — no live RPC calls in CI

### Fixed
- Extractor tests hitting live RPC endpoints (403 errors)
- CLI test fakes with wrong method signatures
- Config test not accounting for Pydantic HttpUrl normalization

## [0.1.0] - 2025-12-08

### Added
- Ethereum mainnet block extraction
- Base L2 block extraction
- Resumable sync with checkpoints
- Chain reorganization detection
- Batch block processing with progress bars
- PostgreSQL loader with SQLAlchemy
- Transaction extraction (legacy + EIP-1559)
- Log/event extraction from receipts
- ERC-20 and ERC-721 token transfer parsing
- CLI with `sync` and `status` commands
- Docker deployment support
- 36 tests, 89% coverage

[Unreleased]: https://github.com/jtaylortech/celara-homepage/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jtaylortech/celara-homepage/releases/tag/v0.1.0
