# Adding a New Chain

Any EVM-compatible chain works. Three files to touch.

## 1. Create the Extractor

```python
# src/chainetl/extractors/optimism.py
from chainetl.extractors.evm import EVMExtractor

class OptimismExtractor(EVMExtractor):
    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="optimism")
```

That's it. All extraction logic (blocks, transactions, logs, token transfers) is inherited from `EVMExtractor`.

## 2. Add the RPC URL to Config

```python
# src/chainetl/config.py
class Settings(BaseSettings):
    # ... existing URLs ...
    optimism_rpc_url: HttpUrl = HttpUrl("https://mainnet.optimism.io")
```

## 3. Register in the CLI

```python
# src/chainetl/cli.py
from chainetl.extractors.optimism import OptimismExtractor

SUPPORTED_CHAINS: dict[str, tuple[type[BaseExtractor], str]] = {
    # ... existing chains ...
    "optimism": (OptimismExtractor, str(settings.optimism_rpc_url)),
}
```

## 4. Add to API (optional)

```python
# src/chainetl/api.py
RPCS: dict[str, str] = {
    # ... existing chains ...
    "optimism": "https://mainnet.optimism.io",
}
```

## 5. Test

```bash
chainetl sync --chain optimism --start-block 100000000 --count 5
chainetl status --chain optimism
```
