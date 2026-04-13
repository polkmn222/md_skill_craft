# [PROJECT_NAME]

## Project
[One-line CLI tool description]
**Stack**: Clap / Structopt, Rust, cargo

## Setup
```bash
cargo build
cargo run -- --help
# or: cargo run --release
```

## Key Commands
| Task | Command |
|------|---------|
| Build Debug | `cargo build` |
| Build Release | `cargo build --release` |
| Run | `cargo run -- [args]` |
| Tests | `cargo test` |
| Clippy Lint | `cargo clippy -- -D warnings` |
| Format | `cargo fmt` |
| Doc | `cargo doc --open` |

## Architecture
- `src/` — Source code
  - `main.rs` — Application entry point
  - `lib.rs` — Library exports (if applicable)
  - `cli/` — Command-line interface
    - `mod.rs` — Module definition
    - `args.rs` — Argument parsing (Clap structs)
    - `commands/` — Command implementations
      - `mod.rs`
      - `[command_name].rs`
  - `core/` — Core logic
    - `mod.rs`
    - `processor.rs`
    - `errors.rs`
  - `utils/` — Utilities
    - `mod.rs`
    - `formatting.rs`
    - `validation.rs`
- `tests/` — Integration tests
  - `cli.rs` — CLI integration tests
- `Cargo.toml` — Project metadata and dependencies

## Conventions
- Rust idioms: snake_case for functions/variables, PascalCase for types
- Error handling: Result<T, E> everywhere (no panics in libraries)
- Ownership-first design (no Rc/RefCell unless necessary)
- Derive macros for common traits
- Tests in `tests/` directory for integration tests
- Module hierarchy mirrors directory structure
- Doc comments with `///` on public items
- No `unwrap()` in production code (use `?` operator)

## Key Dependencies
- **clap** — CLI argument parsing (derive macro)
- **anyhow** or **thiserror** — Error handling
- **serde** / **serde_json** — Serialization
- **tokio** — Async runtime (if needed)
- **log** / **env_logger** — Logging

## Clap Argument Structure

```rust
// src/cli/args.rs
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "mytool")]
#[command(about = "Tool description", long_about = None)]
struct Args {
    #[command(subcommand)]
    command: Commands,
    
    #[arg(long, global = true)]
    verbose: bool,
}

#[derive(Subcommand)]
enum Commands {
    /// Process a file
    Process {
        #[arg(value_name = "FILE")]
        input: String,
        
        #[arg(short, long)]
        output: Option<String>,
    },
    
    /// Validate input
    Validate {
        #[arg(value_name = "FILE")]
        input: String,
    },
}

// src/main.rs
mod cli;
mod core;

use cli::args::{Args, Commands};
use clap::Parser;

fn main() -> anyhow::Result<()> {
    let args = Args::parse();
    
    match args.command {
        Commands::Process { input, output } => {
            cli::commands::process(&input, output.as_deref())?;
        }
        Commands::Validate { input } => {
            cli::commands::validate(&input)?;
        }
    }
    
    Ok(())
}
```

## Error Handling

```rust
// src/core/errors.rs
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("file not found: {0}")]
    FileNotFound(String),
    
    #[error("invalid format: {0}")]
    InvalidFormat(String),
    
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

// In functions
fn read_file(path: &str) -> Result<String, AppError> {
    std::fs::read_to_string(path)
        .map_err(|_| AppError::FileNotFound(path.to_string()))
}

// Use ? operator for early return
fn process(input: &str) -> Result<String, AppError> {
    let content = read_file(input)?;  // Returns error early if fails
    Ok(content)
}
```

## Testing

```rust
// src/core.rs
pub fn calculate_value(x: i32, y: i32) -> i32 {
    x + y
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_calculate() {
        assert_eq!(calculate_value(2, 3), 5);
    }
}

// tests/cli.rs (Integration test)
#[test]
fn test_process_command() {
    let output = std::process::Command::new("cargo")
        .args(&["run", "--", "process", "input.txt"])
        .output()
        .expect("failed to run");
    
    assert!(output.status.success());
}
```

## Logging

```rust
use log::info;

fn main() -> anyhow::Result<()> {
    env_logger::init();
    
    info!("Starting application");
    
    // ... application code ...
    
    Ok(())
}
```

## File I/O Pattern

```rust
use std::fs;
use std::path::Path;

fn read_file<P: AsRef<Path>>(path: P) -> anyhow::Result<String> {
    fs::read_to_string(path)
        .map_err(|e| anyhow::anyhow!("Failed to read file: {}", e))
}

fn write_file<P: AsRef<Path>>(path: P, content: &str) -> anyhow::Result<()> {
    fs::write(path, content)?;
    Ok(())
}
```

## Anti-Patterns
- ❌ Using `unwrap()` or `expect()` in production code
- ❌ Ignoring the Result type
- ❌ Global mutable state
- ❌ Cloning large data structures unnecessarily
- ❌ No error context (use `context()` from anyhow)
- ❌ Hardcoded paths or strings

## Release Optimization

```toml
# Cargo.toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

## Development Workflow
1. Define CLI structure in `src/cli/args.rs`
2. Implement command logic in `src/cli/commands/`
3. Create core logic in `src/core/`
4. Write unit tests in respective module files
5. Write integration tests in `tests/`
6. Run `cargo test` to verify all tests pass
7. Run `cargo clippy` to check for warnings
8. Run `cargo fmt` to format code
9. Build release binary: `cargo build --release`
10. Commit and push

## Deployment
```bash
# Build optimized binary
cargo build --release

# Binary location: target/release/[project-name]
# Distribute the binary or publish to crates.io
```

## Publishing to crates.io
```bash
# Prepare metadata in Cargo.toml
# Then publish
cargo publish
```

## Skills
@skills/coding-standards.md @skills/validation.md @skills/orchestration.md

## References
- [Clap Documentation](https://docs.rs/clap/latest/clap/)
- [Rust Book](https://doc.rust-lang.org/book/)
- [Error Handling in Rust](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [Clippy Lints](https://doc.rust-lang.org/clippy/)
