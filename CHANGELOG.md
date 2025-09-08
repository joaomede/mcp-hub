# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [1.0.3](https://github.com/joaomede/mcp-hub/compare/v1.0.2...v1.0.3) (2025-09-08)

### [1.0.2](https://github.com/joaomede/mcp-hub/compare/v1.0.1...v1.0.2) (2025-09-08)

### [1.0.1](https://github.com/joaomede/mcp-hub/compare/v0.0.17...v1.0.1) (2025-09-08)


### Features

* **docs:** add demo changelog entry ([dd95b3f](https://github.com/joaomede/mcp-hub/commit/dd95b3f4b6164a04f3c1cd36c739c6e823d664be))
* **proxy:** return MCP-compliant envelopes and include sessionId in initialize; derive stable anon session for n8n; tests: call initialize before tools/list ([5247f46](https://github.com/joaomede/mcp-hub/commit/5247f46e5ba628e98ff94e268f6978c8f376839d))
* **proxy:** tolerate 'initialize' method in HTTP proxy for n8n and similar clients ([6fc0bb3](https://github.com/joaomede/mcp-hub/commit/6fc0bb3e244143f400c2b065b2161325aec14e30))


### Bug Fixes

* **compose:** remove --log-level from command (not supported by mcp-hub CLI) ([9f8ed75](https://github.com/joaomede/mcp-hub/commit/9f8ed75f91b71bf314a8dc80ed6d4951850f1802))
* handshake, proxy, and test improvements\n\n- Always call initialize() on MCP sub-app startup for FastMCP compatibility\n- Patch proxy to omit empty/null arguments in tools/call\n- Fix config watcher type hints for async reload\n- Integration test: dynamic server discovery, git repo mount\n- Update test_config.json for all official servers\n- Fix editable package name in uv.lock\n- Remove debug/test artifacts ([c10f5c5](https://github.com/joaomede/mcp-hub/commit/c10f5c5c2df29f503cc0aae041677b063f66ca31))
* **proxy:** tolerate notifications/initialized as no-op, return JSON-RPC error for unknown methods, never 500 on HTTPException ([16bf431](https://github.com/joaomede/mcp-hub/commit/16bf431cb989f6f97014c26f8ece04084665124c))

## [1.0.0] - 2025-09-07

### 🚀 Initial Release

**MCP Hub** - A pure stdio MCP Gateway for aggregating multiple Model Context Protocol servers.

### Features

- ✅ **Pure stdio MCP Protocol**: Direct stdio MCP protocol proxying without any conversion
- ✅ **Multi-Server Aggregation**: Manage multiple stdio MCP servers through a single endpoint
- ✅ **Smart Routing**: Clean path-based routing at `/[server-name]/mcp` endpoints
- ✅ **Unified Authentication**: Centralized API key authentication for all servers
- ✅ **Hot Reload**: Dynamic configuration reloading without service restart
- ✅ **CORS Support**: Configurable cross-origin resource sharing
- ✅ **Graceful Shutdown**: Proper connection cleanup and server lifecycle management
- ✅ **Docker Support**: Full containerization with health checks
- ✅ **Integration Testing**: Comprehensive test suite with real MCP server validation

### Supported MCP Server Types

- **stdio**: Standard input/output MCP servers (ONLY supported transport)

### Architecture

MCP Hub acts as a pure stdio gateway, maintaining full MCP protocol semantics while providing:
- Centralized endpoint management
- Unified security layer
- Configuration-driven server mounting
- Real-time configuration updates

### Configuration

Supports Claude Desktop compatible configuration format for stdio servers:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command",
      "args": ["arg1", "arg2"]
    }
  }
}
```

### Testing

- **Unit Tests**: Comprehensive pytest test suite
- **Integration Tests**: Docker-based testing with real MCP servers
- **Validation**: 23+ tools across memory, filesystem, and time servers

### Acknowledgments

This project is inspired by and evolved from [mcpo](https://github.com/open-webui/mcpo) by Timothy Jaeryang Baek. MCP Hub focuses specifically on pure stdio MCP protocol forwarding, providing a clean gateway solution for MCP server aggregation.

---

**Migration from mcpo**: If you're coming from mcpo, the main difference is that MCP Hub provides pure stdio MCP endpoints at `/[server-name]/mcp` instead of REST API endpoints. Connect your MCP clients directly to these endpoints for native protocol communication.

## [0.0.17] - 2025-07-22

### Added

- 🔄 **Hot Reload Support for Configuration Files**: Added \`--hot-reload\` flag to watch your config file for changes and dynamically reload MCP servers without restarting the application—enabling seamless development workflows and runtime configuration updates.
- 🤫 **HTTP Request Filtering for Cleaner Logs**: Added configurable log filtering to reduce noise from frequent HTTP requests, making debugging and monitoring much clearer in production environments.

### Changed

- ⬆️ **Updated MCP Package to v1.12.1**: Upgraded MCP dependency to resolve compatibility issues with Pydantic and improve overall stability and performance.
- 🔧 **Normalized Streamable HTTP Configuration**: Streamlined configuration syntax for streamable-http servers to align with MCP standards while maintaining backward compatibility.

## [0.0.16] - 2025-07-02

### Added

- 🔁 **Enhanced Endpoint Support for Arbitrary Return Types**: Endpoints can now return any JSON-serializable value—removing limitations on tool outputs and enabling support for more diverse workflows, including advanced data structures or dynamic return formats.
- 🪵 **Improved Log Clarity with Streamlined Print Trace Output**: Internal logging has been upgraded with more structured and interpretable print traces, giving users clearer visibility into backend tool behavior and execution flow—especially helpful when debugging multi-agent sequences or nested toolchains.

### Fixed

- 🔄 **Resolved Infinite Loop Edge Case in Custom Schema Inference**: Fixed a bug where circular references ($ref) caused schema processing to hang or crash in rare custom schema setups—ensuring robust and reliable auto-documentation even for deeply nested models.

## [0.0.15] - 2025-06-06

### Added

- 🔐 **Support for Custom Headers in SSE and Streamable Http MCP Connections**: You can now pass custom HTTP headers (e.g., for authentication tokens or trace IDs) when connecting to SSE or streamable_http servers—enabling seamless integration with remote APIs that require secure or contextual headers.
- 📘 **MCP Server Instructions Exposure**: mcpo now detects and exposes instructions output by MCP tools, bringing descriptive setup guidelines and usage help directly into the OpenAPI schema—so users, UIs, and LLM agents can better understand tool capabilities with zero additional config.
- 🧪 **MCP Exception Stacktrace Printing During Failures**: When a connected MCP server raises an internal error, mcpo now displays the detailed stacktrace from the tool directly in the logs—making debugging on failure dramatically easier for developers and MLops teams working on complex flows.

### Fixed

- 🧽 **Corrected Handling of Underscore Prefix Parameters in Pydantic Modes**: Parameters with leading underscores (e.g. _token) now work correctly without conflict or omission in auto-generated schemas—eliminating validation issues and improving compatibility with tools relying on such parameter naming conventions.

## [0.0.14] - 2025-05-11

### Added

- 🌐 **Streamable HTTP Transport Support**: mcpo now supports MCP servers using the Streamable HTTP transport. This allows for more flexible and robust communication, including session management and resumable streams. Configure via CLI with '--server-type "streamable_http" -- <URL>' or in the config file with 'type: "streamable_http"' and a 'url'.

## [0.0.13] - 2025-05-01

### Added

- 🧪 **Support for Mixed and Union Types (anyOf/nullables)**: mcpo now accurately exposes OpenAPI schemas with anyOf compositions and nullable fields.
- 🧷 **Authentication-Required Docs Access with --strict-auth**: When enabled, the new --strict-auth option restricts access to both the tool endpoints and their interactive documentation pages—ensuring sensitive internal services aren’t inadvertently exposed to unauthenticated users or LLMs.
- 🧬 **Custom Schema Definitions for Complex Models**: Developers can now register custom BaseModel schemas with arbitrary nesting and field variants, allowing precise OpenAPI representations of deeply structured payloads—ensuring crystal-clear docs and compatibility for multi-layered data workflows.
- 🔄 **Smarter Schema Inference Across Data Types**: Schema generation has been enhanced to gracefully handle nested unions, nulls, and fallback types, dramatically improving accuracy in tools using variable output formats or flexible data contracts.

## [0.0.12] - 2025-04-14

### Fixed

- ⏳ **Disabled SSE Read Timeout to Prevent Inactivity Errors**: Resolved an issue where Server-Sent Events (SSE) MCP tools would unexpectedly terminate after 5 minutes of no activity—ensuring durable, always-on connections for real-time workflows like streaming updates, live dashboards, or long-running agents.

## [0.0.11] - 2025-04-12

### Added

- 🌊 **SSE-Based MCP Server Support**: mcpo now supports SSE (Server-Sent Events) MCP servers out of the box—just pass 'mcpo --server-type "sse" -- http://127.0.0.1:8001/sse' when launching or use the standard "url" field in your config for seamless real-time integration with streaming MCP endpoints; see the README for full examples and enhanced workflows with live progress, event pushes, and interactive updates.

## [0.0.10] - 2025-04-10

### Added

- 📦 **Support for --env-path to Load Environment Variables from File**: Use the new --env-path flag to securely pass environment variables via a .env-style file—making it easier than ever to manage secrets and config without cluttering your CLI or exposing sensitive data.
- 🧪 **Enhanced Support for Nested Object and Array Types in OpenAPI Schema**: Tools with complex input/output structures (e.g., JSON payloads with arrays or nested fields) are now correctly interpreted and exposed with accurate OpenAPI documentation—making form-based testing in the UI smoother and integrations far more predictable.
- 🛑 **Smart HTTP Exceptions for Better Debugging**: Clear, structured HTTP error responses are now automatically returned for bad requests or internal tool errors—helping users immediately understand what went wrong without digging through raw traces.

### Fixed

- 🪛 **Fixed --env Flag Behavior for Inline Environment Variables**: Resolved issues where the --env CLI flag silently failed or misbehaved—environment injection is now consistent and reliable whether passed inline with --env or via --env-path.

## [0.0.9] - 2025-04-06

### Added

- 🧭 **Clearer Docs Navigation with Path Awareness**: Optimized the /docs and /[tool]/docs pages to clearly display full endpoint paths when using mcpo --config, making it obvious where each tool is hosted—no more guessing or confusion when running multiple tools under different routes.
- 🛤️ **New --path-prefix Option for Precise Routing Control**: Introduced optional --path-prefix flag allowing you to customize the route prefix for all mounted tools—great for integrating mcpo into existing infrastructures, reverse proxies, or multi-service APIs without route collisions.
- 🐳 **Official Dockerfile for Easy Deployment**: Added a first-party Dockerfile so you can containerize mcpo in seconds—perfect for deploying to production, shipping models with standardized dependencies, and running anywhere with a consistent environment.

## [0.0.8] - 2025-04-03

### Added

- 🔒 **SSL Support via '--ssl-certfile' and '--ssl-keyfile'**: Easily enable HTTPS for your mcpo servers by passing certificate and key files—ideal for securing deployments in production, enabling encrypted communication between clients (e.g. browsers, AI agents) and your MCP tools without external proxies.

## [0.0.7] - 2025-04-03

### Added

- 🖼️ **Image Content Output Support**: mcpo now gracefully handles image outputs from MCP tools—returning them directly as binary image content so users can render or download visuals instantly, unlocking powerful new use cases like dynamic charts, AI art, and diagnostics through any standard HTTP client or browser.

## [0.0.6] - 2025-04-02

### Added

- 🔐 **CLI Auth with --api-key**: Secure your endpoints effortlessly with the new --api-key option, enabling basic API key authentication for instant protection without custom middleware or external auth systems—ideal for public or multi-agent deployments.
- 🌐 **Flexible CORS Access via --cors-allow-origins**: Unlock controlled cross-origin access with the new --cors-allow-origins CLI flag—perfect for integrating mcpo with frontend apps, remote UIs, or cloud dashboards while maintaining CORS security.

### Fixed

- 🧹 **Cleaner Proxy Output**: Dropped None arguments from proxy requests, resulting in reduced clutter and improved interoperability with servers expecting clean inputs—ensuring more reliable downstream performance with MCP tools.
