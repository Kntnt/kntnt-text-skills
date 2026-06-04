# tinycache

![License](https://img.shields.io/badge/license-MIT-blue)
![PHP](https://img.shields.io/badge/PHP-8.1%2B-777bb4)
![Latest release](https://img.shields.io/github/v/release/acme/tinycache)

A tiny PSR-16 cache for PHP projects that want a dependency-free key–value store with optional file persistence.

## Description

tinycache is a small caching library for PHP. It implements the PSR-16 simple-cache interface, so it drops into any project that expects a standard cache, and it falls back to an in-memory store when no persistence directory is configured.

The library is aimed at small services and command-line tools where pulling in a full cache stack would be overkill, but where repeated computation or I/O still wants a cheap memoisation layer.

### Key Features

- A complete PSR-16 implementation, usable anywhere a `CacheInterface` is expected.
- In-memory by default, with optional file persistence behind the same API.
- Per-item time-to-live, with lazy expiry on read.
- No runtime dependencies beyond the PHP standard library.

### The problem

Small PHP projects often need to cache a handful of values — a parsed config, an API response, an expensive computation — but reaching for Redis or a framework cache means infrastructure and dependencies out of all proportion to the need.

### How this library helps

tinycache gives those projects a standards-compliant cache in a single package with no services to run. Start in memory, and switch to file persistence by passing a directory — the calling code does not change.

## Requirements

- PHP 8.1 or later.

## Installation

Install with Composer:

```bash
composer require acme/tinycache
```

## Usage

Create a cache and use it through the PSR-16 API:

```php
use Acme\TinyCache\Cache;

$cache = new Cache();
$cache->set('greeting', 'hello', 3600);
echo $cache->get('greeting');
```

To persist items between runs, pass a writable directory:

```php
$cache = new Cache('/var/tmp/tinycache');
```

## Questions, bugs, and feature requests

For questions, head over to our [Discussions](https://github.com/acme/tinycache/discussions) page. If you've found a bug or have a feature in mind, [open an issue](https://github.com/acme/tinycache/issues) — but do look through the existing ones first so we avoid duplicates.

## How you can contribute

Contributions are welcome, large or small — bug reports, pull requests, documentation, or translations. See [`CONTRIBUTING.md`](CONTRIBUTING.md) before you start.

## License

This project is licensed under the MIT Licence. See [`LICENSE.md`](LICENSE.md).

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md). This project adheres to Keep a Changelog and Semantic Versioning.
