# Task Breakdown: Telegram Entertainment Chatbot

## Overview
- **Total tasks**: 87
- **Parallelizable tasks**: 52
- **Estimated phases**: 6
- **Technology Stack**: Python 3.11+, asyncio, pymysql, MySQL, Faiss, python-telegram-bot
- **Testing Framework**: pytest, pytest-asyncio
- **TDD Approach**: Test tasks precede implementation tasks for all components

**Note**: This task breakdown follows Test-Driven Development (TDD) principles as required by the project constitution. All test tasks are positioned before their corresponding implementation tasks.

---

## Phase 1: Foundation Setup

**Goal**: Establish project structure, configuration, and base modules

### Task 1.1: Create Project Directory Structure
- **Type**: Setup
- **Files**: All directories and `__init__.py` files
- **Description**: Create complete project directory structure with all package init files
- **Dependencies**: None
- **Est. Complexity**: Low
- **Details**:
  ```
  Create directories:
  - src/handlers/, src/services/, src/integrations/
  - src/memory/, src/repositories/, src/models/
  - src/database/, src/utils/, tests/
  - tests/test_handlers/, tests/test_services/
  - tests/test_integrations/, tests/test_memory/
  - tests/test_repositories/
  
  Create __init__.py in all packages
  ```

### Task 1.2: Create requirements.txt [P]
- **Type**: Setup
- **Files**: `requirements.txt`
- **Description**: Define all Python dependencies with version constraints
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Details**:
  ```txt
  python-telegram-bot==20.7
  pymysql==1.1.0
  aiomysql==0.2.0
  faiss-cpu==1.7.4
  httpx==0.25.0
  python-dotenv==1.0.0
  pytest==7.4.0
  pytest-asyncio==0.21.0
  pylint==3.0.0
  black==23.7.0
  alembic==1.12.0
  ```

### Task 1.3: Create .env.example [P]
- **Type**: Setup
- **Files**: `.env.example`
- **Description**: Create environment configuration template
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Details**: Include all required config variables (BOT_TOKEN, MIMO_API_KEY, DB_HOST, etc.)

### Task 1.4: Create pyproject.toml [P]
- **Type**: Setup
- **Files**: `pyproject.toml`
- **Description**: Configure project metadata and tool settings
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Details**: Configure pylint (min 8.0/10), black, pytest

### Task 1.5: Create .pylintrc Configuration [P]
- **Type**: Setup
- **Files**: `.pylintrc`
- **Description**: Configure pylint with 8.0/10 minimum score requirement
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Details**: Set min score, disable unnecessary checks, configure PEP 8

### Task 1.6: Create pytest Configuration [P]
- **Type**: Setup
- **Files**: `tests/conftest.py`
- **Description**: Configure pytest with async support and test fixtures
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Details**: Configure pytest-asyncio, add database fixtures, mock fixtures

---

## Phase 2: Core Data Models (TDD)

**Goal**: Implement data models with validation

### Task 2.1: Write Tests for User Model
- **Type**: Testing
- **Files**: `tests/test_models/test_user.py`
- **Description**: Write unit tests for User model (validation, serialization)
- **Dependencies**: Task 1.6
- **Est. Complexity**: Low
- **Details**: Test field validation, dataclass creation, to_dict methods

### Task 2.2: Implement User Model
- **Type**: Implementation
- **Files**: `src/models/user.py`
- **Description**: Implement User dataclass with validation
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low
- **Details**: Dataclass with user_id, username, first_name, last_name, preferred_style

### Task 2.3: Write Tests for Conversation Model [P]
- **Type**: Testing
- **Files**: `tests/test_models/test_conversation.py`
- **Description**: Write unit tests for Conversation model
- **Dependencies**: Task 1.6
- **Est. Complexity**: Low
- **Details**: Test message role enum, field validation, timestamp handling

### Task 2.4: Implement Conversation Model
- **Type**: Implementation
- **Files**: `src/models/conversation.py`
- **Description**: Implement Conversation dataclass
- **Dependencies**: Task 2.3
- **Est. Complexity**: Low
- **Details**: Dataclass with id, chat_id, user_id, message_text, role, timestamp

### Task 2.5: Write Tests for Message Model [P]
- **Type**: Testing
- **Files**: `tests/test_models/test_message.py`
- **Description**: Write unit tests for Message model
- **Dependencies**: Task 1.6
- **Est. Complexity**: Low
- **Details**: Test message structure, validation

### Task 2.6: Implement Message Model
- **Type**: Implementation
- **Files**: `src/models/message.py`
- **Description**: Implement Message dataclass
- **Dependencies**: Task 2.5
- **Est. Complexity**: Low
- **Details**: Dataclass with text, role, timestamp, user_id, chat_id

### Task 2.7: Write Tests for Style Enum [P]
- **Type**: Testing
- **Files**: `tests/test_models/test_style.py`
- **Description**: Write unit tests for Style enum/constants
- **Dependencies**: Task 1.6
- **Est. Complexity**: Low
- **Details**: Test 6 style constants, style validation, prompt templates

### Task 2.8: Implement Style Enum
- **Type**: Implementation
- **Files**: `src/models/style.py`
- **Description**: Implement Style enum and prompt templates
- **Dependencies**: Task 2.7
- **Est. Complexity**: Low
- **Details**: Enum with 6 styles (HUMOROUS, GENTLE, TSUNDERE, SERIOUS, CUTE, INTELLECTUAL), system prompts

### Task 2.9: Write Tests for GroupSettings Model [P]
- **Type**: Testing
- **Files**: `tests/test_models/test_group_settings.py`
- **Description**: Write unit tests for GroupSettings model
- **Dependencies**: Task 1.6
- **Est. Complexity**: Low
- **Details**: Test field validation, default values

### Task 2.10: Implement GroupSettings Model
- **Type**: Implementation
- **Files**: `src/models/group_settings.py`
- **Description**: Implement GroupSettings dataclass
- **Dependencies**: Task 2.9
- **Est. Complexity**: Low
- **Details**: Dataclass with chat_id, group_style, created_at, updated_at

---

## Phase 3: Database Layer (TDD)

**Goal**: Implement database connectivity and repositories

### Task 3.1: Write Tests for Config Module
- **Type**: Testing
- **Files**: `tests/test_config.py`
- **Description**: Write unit tests for configuration loading and validation
- **Dependencies**: Task 1.3, Task 1.4
- **Est. Complexity**: Medium
- **Details**: Test .env loading, required field validation, type validation, defaults

### Task 3.2: Implement Config Module
- **Type**: Implementation
- **Files**: `src/config.py`
- **Description**: Implement Config class with .env loading and validation
- **Dependencies**: Task 3.1
- **Est. Complexity**: Medium
- **Details**: Load .env, validate required fields, define constants (styles, limits), handle errors

### Task 3.3: Write Tests for Database Connection Pool
- **Type**: Testing
- **Files**: `tests/test_database/test_connection.py`
- **Description**: Write unit tests for database connection pooling
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium
- **Details**: Test connection creation, pool management, retry logic, error handling

### Task 3.4: Implement Database Connection Pool
- **Type**: Implementation
- **Files**: `src/database/connection.py`
- **Description**: Implement async database connection pool with retry logic
- **Dependencies**: Task 3.3
- **Est. Complexity**: Medium
- **Details**: Use aiomysql for async pool, configure pool size (default 5), implement retry with exponential backoff

### Task 3.5: Write Database Schema SQL
- **Type**: Setup
- **Files**: `src/database/schema.sql`
- **Description**: Create initial database schema with all 5 tables
- **Dependencies**: Task 3.4
- **Est. Complexity**: Medium
- **Details**: Create users, conversations, conversation_vectors, group_settings, user_preferences tables with correct structure

### Task 3.6: Setup Alembic Migrations
- **Type**: Setup
- **Files**: `alembic.ini`, `src/database/migrations.py`, `migrations/versions/001_initial.py`
- **Description**: Configure Alembic and create initial migration script
- **Dependencies**: Task 3.5
- **Est. Complexity**: Medium
- **Details**: Setup alembic.ini, create env.py, generate initial migration from schema.sql

### Task 3.7: Write Tests for Base Repository [P]
- **Type**: Testing
- **Files**: `tests/test_repositories/test_base_repository.py`
- **Description**: Write unit tests for base repository with CRUD operations
- **Dependencies**: Task 3.4, Task 3.6
- **Est. Complexity**: Medium
- **Details**: Test async CRUD methods, connection handling, error scenarios

### Task 3.8: Implement Base Repository
- **Type**: Implementation
- **Files**: `src/repositories/base_repository.py`
- **Description**: Implement base repository class with async CRUD methods
- **Dependencies**: Task 3.7
- **Est. Complexity**: Medium
- **Details**: Abstract base class with create, read, update, delete, list methods

### Task 3.9: Write Tests for User Repository [P]
- **Type**: Testing
- **Files**: `tests/test_repositories/test_user_repository.py`
- **Description**: Write unit tests for User repository operations
- **Dependencies**: Task 3.8
- **Est. Complexity**: Medium
- **Details**: Test user CRUD, get by ID, get by username, update style, upsert logic

### Task 3.10: Implement User Repository
- **Type**: Implementation
- **Files**: `src/repositories/user_repository.py`
- **Description**: Implement User repository inheriting from base repository
- **Dependencies**: Task 3.9
- **Est. Complexity**: Medium
- **Details**: Extend BaseRepository, add user-specific queries (by_username, update_style)

### Task 3.11: Write Tests for Conversation Repository [P]
- **Type**: Testing
- **Files**: `tests/test_repositories/test_conversation_repository.py`
- **Description**: Write unit tests for Conversation repository
- **Dependencies**: Task 3.8
- **Est. Complexity**: Medium
- **Details**: Test conversation CRUD, get context (chat_id + user_id), pagination

### Task 3.12: Implement Conversation Repository
- **Type**: Implementation
- **Files**: `src/repositories/conversation_repository.py`
- **Description**: Implement Conversation repository
- **Dependencies**: Task 3.11
- **Est. Complexity**: Medium
- **Details**: Extend BaseRepository, add get_context (LIMIT 50), get_recent_messages

### Task 3.13: Write Tests for Vector Repository [P]
- **Type**: Testing
- **Files**: `tests/test_repositories/test_vector_repository.py`
- **Description**: Write unit tests for Vector repository (BLOB storage)
- **Dependencies**: Task 3.8
- **Est. Complexity**: Medium
- **Details**: Test vector CRUD, BLOB serialization/deserialization, batch retrieval

### Task 3.14: Implement Vector Repository
- **Type**: Implementation
- **Files**: `src/repositories/vector_repository.py`
- **Description**: Implement Vector repository with BLOB handling
- **Dependencies**: Task 3.13
- **Est. Complexity**: Medium
- **Details**: Extend BaseRepository, handle embedding BLOB fields, batch retrieval, serialization

### Task 3.15: Write Tests for Group Repository [P]
- **Type**: Testing
- **Files**: `tests/test_repositories/test_group_repository.py`
- **Description**: Write unit tests for Group repository
- **Dependencies**: Task 3.8
- **Est. Complexity**: Low
- **Details**: Test group settings CRUD, get by chat_id, update style

### Task 3.16: Implement Group Repository
- **Type**: Implementation
- **Files**: `src/repositories/group_repository.py`
- **Description**: Implement Group repository
- **Dependencies**: Task 3.15
- **Est. Complexity**: Low
- **Details**: Extend BaseRepository, add group-specific methods (get_by_chat_id, update_style)

---

## Phase 4: Utilities and Infrastructure (TDD)

**Goal**: Implement utility modules and infrastructure

### Task 4.1: Write Tests for Validators
- **Type**: Testing
- **Files**: `tests/test_utils/test_validators.py`
- **Description**: Write unit tests for input validation functions
- **Dependencies**: None
- **Est. Complexity**: Low
- **Details**: Test username validation, style validation, message length validation, special character handling

### Task 4.2: Implement Validators
- **Type**: Implementation
- **Files**: `src/utils/validators.py`
- **Description**: Implement input validation functions
- **Dependencies**: Task 4.1
- **Est. Complexity**: Low
- **Details**: Functions for validating usernames, styles, message length, detecting SQL injection patterns

### Task 4.3: Write Tests for Sanitizers [P]
- **Type**: Testing
- **Files**: `tests/test_utils/test_sanitizers.py`
- **Description**: Write unit tests for input sanitization functions
- **Dependencies**: None
- **Est. Complexity**: Low
- **Details**: Test SQL injection sanitization, XSS prevention, special character handling

### Task 4.4: Implement Sanitizers
- **Type**: Implementation
- **Files**: `src/utils/sanitizers.py`
- **Description**: Implement input sanitization functions
- **Dependencies**: Task 4.3
- **Est. Complexity**: Low
- **Details**: Functions for sanitizing SQL inputs, HTML outputs, special characters

### Task 4.5: Write Tests for Logger [P]
- **Type**: Testing
- **Files**: `tests/test_utils/test_logger.py`
- **Description**: Write unit tests for logging configuration
- **Dependencies**: None
- **Est. Complexity**: Low
- **Details**: Test logger setup, log levels, structured logging format

### Task 4.6: Implement Logger
- **Type**: Implementation
- **Files**: `src/utils/logger.py`
- **Description**: Implement structured logging configuration
- **Dependencies**: Task 4.5
- **Est. Complexity**: Low
- **Details**: Configure JSON format logging, log levels, log rotation setup

### Task 4.7: Write Tests for Rate Limiter
- **Type**: Testing
- **Files**: `tests/test_services/test_rate_limiter.py`
- **Description**: Write unit tests for rate limiting logic
- **Dependencies**: None
- **Est. Complexity**: Medium
- **Details**: Test 20 msg/60 sec limit, TTL expiration, temporary ban, multiple users

### Task 4.8: Implement Rate Limiter
- **Type**: Implementation
- **Files**: `src/services/rate_limiter.py`
- **Description**: Implement in-memory rate limiter with TTL
- **Dependencies**: Task 4.7
- **Est. Complexity**: Medium
- **Details**: In-memory dict with timestamps, TTL cleanup, 20 msg/60 sec limit, ban on violation

---

## Phase 5: Memory Subsystem (TDD)

**Goal**: Implement short-term and long-term memory with Faiss

### Task 5.1: Write Tests for Short-term Memory
- **Type**: Testing
- **Files**: `tests/test_memory/test_short_term_memory.py`
- **Description**: Write unit tests for in-memory conversation context
- **Dependencies**: None
- **Est. Complexity**: Medium
- **Details**: Test add message, get context, clear, per-user/group isolation, max 50 messages

### Task 5.2: Implement Short-term Memory
- **Type**: Implementation
- **Files**: `src/memory/short_term_memory.py`
- **Description**: Implement in-memory conversation context manager
- **Dependencies**: Task 5.1
- **Est. Complexity**: Medium
- **Details**: Dict-based storage, per (user_id, chat_id) keys, max 50 messages FIFO, add/get/clear methods

### Task 5.3: Write Tests for Embedding Client
- **Type**: Testing
- **Files**: `tests/test_integrations/test_embedding_client.py`
- **Description**: Write unit tests for OpenAI embedding API client
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium
- **Details**: Mock API calls, test embedding generation, error handling, retry logic

### Task 5.4: Implement Embedding Client
- **Type**: Implementation
- **Files**: `src/integrations/embedding_client.py`
- **Description**: Implement async OpenAI embedding API client
- **Dependencies**: Task 5.3
- **Est. Complexity**: Medium
- **Details**: Use httpx async, call /v1/embeddings, return List[float], retry on timeout, handle quota errors

### Task 5.5: Write Tests for Faiss Manager
- **Type**: Testing
- **Files**: `tests/test_memory/test_faiss_manager.py`
- **Description**: Write unit tests for Faiss index management
- **Dependencies**: Task 3.14, Task 5.4
- **Est. Complexity**: High
- **Details**: Test index building from MySQL, save/load, search, rebuild triggers (startup + 1000 vectors)

### Task 5.6: Implement Faiss Manager
- **Type**: Implementation
- **Files**: `src/memory/faiss_manager.py`
- **Description**: Implement Faiss index manager with persistence
- **Dependencies**: Task 5.5
- **Est. Complexity**: High
- **Details**: Build index from vectors in MySQL, save to file, load on startup, search top-k, rebuild when >1000 new vectors

### Task 5.7: Write Tests for Long-term Memory [P]
- **Type**: Testing
- **Files**: `tests/test_memory/test_long_term_memory.py`
- **Description**: Write unit tests for vector-based semantic search
- **Dependencies**: Task 5.6
- **Est. Complexity**: High
- **Details**: Test semantic search, top-k retrieval, fallback to recent messages, user-specific search

### Task 5.8: Implement Long-term Memory
- **Type**: Implementation
- **Files**: `src/memory/long_term_memory.py`
- **Description**: Implement vector-based semantic search service
- **Dependencies**: Task 5.7
- **Est. Complexity**: High
- **Details**: Search using Faiss, retrieve top-5 relevant conversations, return in order, fallback to recent if no results

### Task 5.9: Write Tests for Memory Service [P]
- **Type**: Testing
- **Files**: `tests/test_services/test_memory_service.py`
- **Description**: Write unit tests for memory orchestration service
- **Dependencies**: Task 5.2, Task 5.8
- **Est. Complexity**: High
- **Details**: Test context retrieval (short + long-term), memory persistence, vector generation, integration

### Task 5.10: Implement Memory Service
- **Type**: Implementation
- **Files**: `src/services/memory_service.py`
- **Description**: Implement memory orchestration (short + long-term)
- **Dependencies**: Task 5.9
- **Est. Complexity**: High
- **Details**: Combine short-term and long-term memory, generate embeddings, store to MySQL, rebuild Faiss, retrieve context

---

## Phase 6: External API Integrations (TDD)

**Goal**: Implement XiaoMi MiMo API client

### Task 6.1: Write Tests for XiaoMi MiMo Client
- **Type**: Testing
- **Files**: `tests/test_integrations/test_mimo_client.py`
- **Description**: Write unit tests for XiaoMi MiMo API client
- **Dependencies**: Task 3.2
- **Est. Complexity**: High
- **Details**: Mock API calls, test chat_completion, style prompts, error handling, retry with exponential backoff

### Task 6.2: Implement XiaoMi MiMo Client
- **Type**: Implementation
- **Files**: `src/integrations/mimo_client.py`
- **Description**: Implement async XiaoMi MiMo API client
- **Dependencies**: Task 6.1
- **Est. Complexity**: High
- **Details**: Use httpx async, POST /v1/chat/completions, add style system prompt, retry logic, timeout handling

---

## Phase 7: Business Logic Services (TDD)

**Goal**: Implement style and chat services

### Task 7.1: Write Tests for Style Service
- **Type**: Testing
- **Files**: `tests/test_services/test_style_service.py`
- **Description**: Write unit tests for style management service
- **Dependencies**: Task 3.10, Task 3.16
- **Est. Complexity**: Medium
- **Details**: Test style priority logic (user > group > default), get effective style, style validation

### Task 7.2: Implement Style Service
- **Type**: Implementation
- **Files**: `src/services/style_service.py`
- **Description**: Implement style management service
- **Dependencies**: Task 7.1
- **Est. Complexity**: Medium
- **Details**: Implement get_effective_style(user_id, chat_id), check user preference, then group, then default

### Task 7.3: Write Tests for Chat Service
- **Type**: Testing
- **Files**: `tests/test_services/test_chat_service.py`
- **Description**: Write unit tests for main chat orchestration service
- **Dependencies**: Task 5.10, Task 6.2, Task 7.2
- **Est. Complexity**: High
- **Details**: Test response generation, memory integration, style application, long message chunking

### Task 7.4: Implement Chat Service
- **Type**: Implementation
- **Files**: `src/services/chat_service.py`
- **Description**: Implement main chat orchestration service
- **Dependencies**: Task 7.3
- **Est. Complexity**: High
- **Details**: Orchestrate LLM call + memory + style, handle >4000 char chunking, apply style prompt, return response

---

## Phase 8: Telegram Bot Handlers (TDD)

**Goal**: Implement Telegram message and command handlers

### Task 8.1: Write Tests for Base Handler
- **Type**: Testing
- **Files**: `tests/test_handlers/test_base_handler.py`
- **Description**: Write unit tests for base handler class
- **Dependencies**: Task 3.2
- **Est. Complexity**: Low
- **Details**: Test common handler logic, error handling, logging

### Task 8.2: Implement Base Handler
- **Type**: Implementation
- **Files**: `src/handlers/base_handler.py`
- **Description**: Implement base handler class with common logic
- **Dependencies**: Task 8.1
- **Est. Complexity**: Low
- **Details**: Base class with error handling, logging, common utilities

### Task 8.3: Write Tests for Command Handlers (/start, /help)
- **Type**: Testing
- **Files**: `tests/test_handlers/test_command_handlers.py`
- **Description**: Write unit tests for basic command handlers
- **Dependencies**: Task 8.2
- **Est. Complexity**: Medium
- **Details**: Test /start (welcome), /help (command list), error handling

### Task 8.4: Implement Command Handlers (/start, /help)
- **Type**: Implementation
- **Files**: `src/handlers/command_handlers.py`
- **Description**: Implement /start and /help command handlers
- **Dependencies**: Task 8.3
- **Est. Complexity**: Medium
- **Details**: /start sends welcome message, /help lists commands

### Task 8.5: Write Tests for Style Commands (/style, /setstyle)
- **Type**: Testing
- **Files**: `tests/test_handlers/test_command_handlers.py` (extend)
- **Description**: Write unit tests for style commands
- **Dependencies**: Task 7.2
- **Est. Complexity**: Medium
- **Details**: Test /style (list), /setstyle (set user preference), invalid style handling

### Task 8.6: Implement Style Commands (/style, /setstyle)
- **Type**: Implementation
- **Files**: `src/handlers/command_handlers.py` (extend)
- **Description**: Implement /style and /setstyle command handlers
- **Dependencies**: Task 8.5
- **Est. Complexity**: Medium
- **Details**: /style lists 6 styles, /setstyle updates user preference

### Task 8.7: Write Tests for /clear Command
- **Type**: Testing
- **Files**: `tests/test_handlers/test_command_handlers.py` (extend)
- **Description**: Write unit tests for /clear command
- **Dependencies**: Task 3.10, Task 3.12
- **Est. Complexity**: Medium
- **Details**: Test confirmation prompt, delete conversations, preserve preferences

### Task 8.8: Implement /clear Command
- **Type**: Implementation
- **Files**: `src/handlers/command_handlers.py` (extend)
- **Description**: Implement /clear command handler
- **Dependencies**: Task 8.7
- **Est. Complexity**: Medium
- **Details**: Ask confirmation, delete all conversations + vectors, preserve user preferences

### Task 8.9: Write Tests for Admin Commands (/groupstyle, /resetuser, /stats)
- **Type**: Testing
- **Files**: `tests/test_handlers/test_admin_handlers.py`
- **Description**: Write unit tests for admin commands
- **Dependencies**: Task 7.2, Task 3.10, Task 3.16
- **Est. Complexity**: High
- **Details**: Test admin permission checks, /groupstyle, /resetuser, /stats commands

### Task 8.10: Implement Admin Commands (/groupstyle, /resetuser, /stats)
- **Type**: Implementation
- **Files**: `src/handlers/admin_handlers.py`
- **Description**: Implement admin command handlers
- **Dependencies**: Task 8.9
- **Est. Complexity**: High
- **Details**: Check admin status, /groupstyle updates group, /resetuser deletes user data, /stats shows metrics

### Task 8.11: Write Tests for Message Handler
- **Type**: Testing
- **Files**: `tests/test_handlers/test_message_handlers.py`
- **Description**: Write unit tests for main message handler
- **Dependencies**: Task 4.8, Task 7.4
- **Est. Complexity**: High
- **Details**: Test @mention detection, rate limiting, input validation, chat service integration

### Task 8.12: Implement Message Handler
- **Type**: Implementation
- **Files**: `src/handlers/message_handlers.py`
- **Description**: Implement main message handler
- **Dependencies**: Task 8.11
- **Est. Complexity**: High
- **Details**: Check @mention (groups only), check rate limit, validate input, call chat service, send response

---

## Phase 9: Bot Entry Point and Integration (TDD)

**Goal**: Integrate all components into working bot

### Task 9.1: Write Integration Tests for Bot Startup
- **Type**: Testing
- **Files**: `tests/test_main.py`
- **Description**: Write integration tests for bot initialization and startup
- **Dependencies**: All previous tasks
- **Est. Complexity**: High
- **Details**: Test bot initialization, handler registration, database connection, Faiss rebuild

### Task 9.2: Implement Bot Entry Point (main.py)
- **Type**: Implementation
- **Files**: `src/main.py`
- **Description**: Implement bot entry point with handler registration
- **Dependencies**: Task 9.1
- **Est. Complexity**: High
- **Details**: Load config, initialize bot, register handlers, run polling, handle startup errors

---

## Phase 10: End-to-End Testing and Quality Assurance

**Goal**: Comprehensive testing and quality enforcement

### Task 10.1: Write End-to-End Tests for User Journeys
- **Type**: Testing
- **Files**: `tests/test_e2e/test_user_journeys.py`
- **Description**: Write e2e tests for complete user workflows
- **Dependencies**: Task 9.2
- **Est. Complexity**: High
- **Details**: Test new user onboarding, style changes, memory queries, command usage

### Task 10.2: Write End-to-End Tests for Group Interactions
- **Type**: Testing
- **Files**: `tests/test_e2e/test_group_interactions.py`
- **Description**: Write e2e tests for multi-user group scenarios
- **Dependencies**: Task 9.2
- **Est. Complexity**: High
- **Details**: Test multiple users, @mentions, admin commands, concurrent operations

### Task 10.3: Write End-to-End Tests for Edge Cases
- **Type**: Testing
- **Files**: `tests/test_e2e/test_edge_cases.py`
- **Description**: Write e2e tests for edge cases
- **Dependencies**: Task 9.2
- **Est. Complexity**: High
- **Details**: Test empty messages, special characters, rapid flooding, long messages, errors

### Task 10.4: Run Pylint and Fix Issues
- **Type**: Quality
- **Files**: All Python files
- **Description**: Run pylint on all modules and fix to achieve 8.0/10 minimum
- **Dependencies**: Task 9.2
- **Est. Complexity**: Medium
- **Details**: Run pylint, fix warnings, ensure min 8.0/10 score, document any necessary disables

### Task 10.5: Run Black Formatter
- **Type**: Quality
- **Files**: All Python files
- **Description**: Format all code with black for consistent style
- **Dependencies**: Task 9.2
- **Est. Complexity**: Low
- **Details**: Run black on all files, verify formatting

### Task 10.6: Run Test Suite with Coverage
- **Type**: Testing
- **Files**: All tests
- **Description**: Run full test suite and verify >80% coverage
- **Dependencies**: Task 10.1, 10.2, 10.3
- **Est. Complexity**: Medium
- **Details**: Run pytest with coverage, generate report, verify >80% coverage, fix gaps

### Task 10.7: Performance Testing
- **Type**: Testing
- **Files**: `tests/test_performance/`
- **Description**: Run performance tests to verify NFRs
- **Dependencies**: Task 9.2
- **Est. Complexity**: High
- **Details**: Test <5s response, 10 concurrent, <1s vector search (10K vectors), optimize queries

### Task 10.8: Security Testing
- **Type**: Testing
- **Files**: `tests/test_security/`
- **Description**: Run security tests to verify NFRs
- **Dependencies**: Task 9.2
- **Est. Complexity**: High
- **Details**: Test SQL injection prevention, XSS prevention, credential protection, rate limiting, admin permissions

### Task 10.9: Load Testing
- **Type**: Testing
- **Files**: `tests/test_load/`
- **Description**: Run load tests to verify scalability
- **Dependencies**: Task 9.2
- **Est. Complexity**: High
- **Details**: Test 50 concurrent users, 1000 msg/min, connection pool, Faiss performance

---

## Phase 11: Documentation and Deployment

**Goal**: Complete documentation and deployment preparation

### Task 11.1: Update README.md [P]
- **Type**: Documentation
- **Files**: `README.md`
- **Description**: Write comprehensive setup and usage documentation
- **Dependencies**: Task 9.2
- **Est. Complexity**: Medium
- **Details**: Setup instructions, architecture overview, API documentation, configuration guide

### Task 11.2: Write Technical Documentation [P]
- **Type**: Documentation
- **Files**: `docs/ARCHITECTURE.md`, `docs/API.md`, `docs/DATABASE.md`
- **Description**: Write technical documentation
- **Dependencies**: Task 9.2
- **Est. Complexity**: High
- **Details**: Document architecture, module dependencies, API contracts, database schema

### Task 11.3: Write User Guide [P]
- **Type**: Documentation
- **Files**: `docs/USER_GUIDE.md`
- **Description**: Write user-facing documentation
- **Dependencies**: Task 9.2
- **Est. Complexity**: Medium
- **Details**: Command reference, style guide, memory features, troubleshooting, FAQ

### Task 11.4: Create Deployment Artifacts [P]
- **Type**: Setup
- **Files**: `run.py` or `start.sh`, `systemd/telegram-bot.service`
- **Description**: Create deployment scripts and service files
- **Dependencies**: Task 9.2
- **Est. Complexity**: Medium
- **Details**: Create startup script, systemd service file for auto-restart, deployment checklist

### Task 11.5: Setup Monitoring and Logging [P]
- **Type**: Setup
- **Files**: `src/utils/logger.py` (update), `docs/MONITORING.md`
- **Description**: Configure structured logging and monitoring
- **Dependencies**: Task 9.2
- **Est. Complexity**: Medium
- **Details**: Configure JSON logging, log rotation, performance metrics, error tracking

### Task 11.6: Deployment Testing
- **Type**: Testing
- **Files**: Fresh environment test
- **Description**: Test deployment on fresh environment
- **Dependencies**: Task 11.4
- **Est. Complexity**: High
- **Details**: Test on clean .venv, fresh database, verify <30 min deployment time

### Task 11.7: Final Quality Checks
- **Type**: Quality
- **Files**: All files
- **Description**: Run final quality checks before release
- **Dependencies**: All previous tasks
- **Est. Complexity**: Medium
- **Details**: Verify .gitignore, no .env committed, all tests pass, pylint OK, docs complete

---

## Execution Order

```
Phase 1: Foundation
Task 1.1 ──► ┌─► Task 1.2 [P]
             │
             ├─► Task 1.3 [P]
             │
             ├─► Task 1.4 [P]
             │
             ├─► Task 1.5 [P]
             │
             └─► Task 1.6 [P]

Phase 2: Core Data Models (TDD)
┌───────────── Task 2.1 ──► Task 2.2 [P] ┐
│                                        │
├───────────── Task 2.3 ──► Task 2.4 [P] ┤
│                                        │
├───────────── Task 2.5 ─�─► Task 2.6 [P] ┤
│                                        │
├───────────── Task 2.7 ──► Task 2.8 [P] ┤
│                                        │
└───────────── Task 2.9 ──► Task 2.10 [P] ┘

Phase 3: Database Layer (TDD)
Task 3.1 ──► Task 3.2 ──► Task 3.3 ──► Task 3.4 ──► Task 3.5 ──► Task 3.6
                                                                       │
┌────────────────────────────────────────────────────────────────────┘
│
├─► Task 3.7 ──► Task 3.8 ──► ┌─► Task 3.9 ──► Task 3.10 [P]
                             │
                             ├─► Task 3.11 ──► Task 3.12 [P]
                             │
                             ├─► Task 3.13 ──► Task 3.14 [P]
                             │
                             └─► Task 3.15 ──► Task 3.16 [P]

Phase 4: Utilities and Infrastructure (TDD)
┌─► Task 4.1 ──► Task 4.2 [P]
│
├─► Task 4.3 ──► Task 4.4 [P]
│
├─► Task 4.5 ──► Task 4.6 [P]
│
└─► Task 4.7 ──► Task 4.8

Phase 5: Memory Subsystem (TDD)
Task 5.1 ──► Task 5.2 ──► ┌─► Task 5.3 ──► Task 5.4 [P]
                          │
                          └─► Task 5.5 ──► Task 5.6 ──► ┌─► Task 5.7 ──► Task 5.8 [P]
                                                        │
                                                        └─► Task 5.9 ──► Task 5.10 [P]

Phase 6: External API Integrations (TDD)
Task 6.1 ──► Task 6.2

Phase 7: Business Logic Services (TDD)
Task 7.1 ──► Task 7.2 ──► ┌─► Task 7.3 ──► Task 7.4
                          │
                          └─► (depends on Task 5.10, 6.2, 7.2)

Phase 8: Telegram Bot Handlers (TDD)
Task 8.1 ──► Task 8.2 ──► ┌─► Task 8.3 ──► Task 8.4 [P]
                          │
                          ├─► Task 8.5 ──► Task 8.6 [P]
                          │
                          ├─► Task 8.7 ──► Task 8.8 [P]
                          │
                          ├─► Task 8.9 ──► Task 8.10 [P]
                          │
                          └─► Task 8.11 ──► Task 8.12

Phase 9: Bot Entry Point and Integration (TDD)
Task 9.1 ──► Task 9.2

Phase 10: End-to-End Testing and Quality Assurance
┌─► Task 10.1 [P]
│
├─► Task 10.2 [P]
│
├─► Task 10.3 [P]
│
└─► Task 10.7 ──► Task 10.8 ──► Task 10.9 ──► ┌─► Task 10.4
                                          │
                                          ├─► Task 10.5
                                          │
                                          └─► Task 10.6

Phase 11: Documentation and Deployment
┌─► Task 11.1 [P]
│
├─► Task 11.2 [P]
│
├─► Task 11.3 [P]
│
├─► Task 11.4 [P]
│
├─► Task 11.5 [P]
│
└─► Task 11.6 ──► Task 11.7
```

---

## Checkpoints

### ✅ Checkpoint 1: Foundation Complete
**After**: Phase 1 (Tasks 1.1-1.6)
**Verify**:
- [ ] All directories created with __init__.py
- [ ] requirements.txt includes all dependencies
- [ ] .env.example has all configuration variables
- [ ] pyproject.toml configured with pylint, black, pytest
- [ ] pytest can run successfully (even with no tests)

### ✅ Checkpoint 2: Data Models Complete
**After**: Phase 2 (Tasks 2.1-2.10)
**Verify**:
- [ ] All model tests pass (User, Conversation, Message, Style, GroupSettings)
- [ ] All models implemented with validation
- [ ] pylint score ≥8.0/10 for all model files
- [ ] Code coverage >80% for models

### ✅ Checkpoint 3: Database Layer Complete
**After**: Phase 3 (Tasks 3.1-3.16)
**Verify**:
- [ ] Database connection pool works
- [ ] Alembic migrations run successfully
- [ ] All repository tests pass
- [ ] Can CRUD data through repositories
- [ ] pylint score ≥8.0/10 for database layer

### ✅ Checkpoint 4: Infrastructure Complete
**After**: Phases 4-6 (Tasks 4.1-6.2)
**Verify**:
- [ ] All utilities tested and working
- [ ] Rate limiter enforces 20 msg/60 sec
- [ ] Short-term memory stores and retrieves context
- [ ] Faiss index builds and searches correctly
- [ ] Embedding client generates vectors
- [ ] XiaoMi MiMo client integrates with LLM API
- [ ] pylint score ≥8.0/10 for all infrastructure

### ✅ Checkpoint 5: Business Logic Complete
**After**: Phase 7 (Tasks 7.1-7.4)
**Verify**:
- [ ] Style service priority logic works (user > group > default)
- [ ] Chat service orchestrates LLM + memory + style
- [ ] Long messages (>4000 chars) are chunked correctly
- [ ] Memory integration works (short + long-term)
- [ ] pylint score ≥8.0/10 for services

### ✅ Checkpoint 6: Handlers Complete
**After**: Phase 8 (Tasks 8.1-8.12)
**Verify**:
- [ ] All command handlers work (/start, /help, /style, /setstyle, /clear)
- [ ] All admin handlers work (/groupstyle, /resetuser, /stats)
- [ ] Message handler detects @mentions correctly
- [ ] Rate limiting enforced in message handler
- [ ] Input validation and sanitization working
- [ ] pylint score ≥8.0/10 for handlers

### ✅ Checkpoint 7: Bot Integration Complete
**After**: Phase 9 (Tasks 9.1-9.2)
**Verify**:
- [ ] Bot starts without errors
- [ ] All handlers registered correctly
- [ ] Database connection established
- [ ] Faiss index rebuilt on startup
- [ ] Bot responds to test messages
- [ ] pylint score ≥8.0/10 for main.py

### ✅ Checkpoint 8: Testing Complete
**After**: Phase 10 (Tasks 10.1-10.9)
**Verify**:
- [ ] All e2e tests pass (user journeys, groups, edge cases)
- [ ] Code coverage >80%
- [ ] pylint score ≥8.0/10 for all modules
- [ ] All NFRs met (performance <5s, 10 concurrent, <1s vector search)
- [ ] Security tests pass (no SQL injection, XSS, credential leaks)
- [ ] Load tests pass (50 concurrent, 1000 msg/min)

### ✅ Checkpoint 9: Documentation and Deployment Complete
**After**: Phase 11 (Tasks 11.1-11.7)
**Verify**:
- [ ] README.md is comprehensive
- [ ] Technical documentation complete
- [ ] User guide is clear and accurate
- [ ] Deployment artifacts created (run.sh, systemd service)
- [ ] Monitoring and logging configured
- [ ] Deployment tested on fresh environment (<30 min)
- [ ] Final quality checks passed (no .env in git, all tests pass)

---

## Summary Statistics

- **Total Tasks**: 87
- **Test Tasks**: 44 (51%)
- **Implementation Tasks**: 43 (49%)
- **Parallelizable Tasks**: 52 (60%)
- **Setup Tasks**: 7 (8%)
- **Quality Tasks**: 6 (7%)
- **Documentation Tasks**: 7 (8%)

**Estimated Effort by Phase**:
- Phase 1 (Foundation): 6 tasks (~8 hours)
- Phase 2 (Models): 10 tasks (~12 hours)
- Phase 3 (Database): 16 tasks (~20 hours)
- Phase 4 (Utilities): 8 tasks (~10 hours)
- Phase 5 (Memory): 10 tasks (~25 hours)
- Phase 6 (APIs): 2 tasks (~8 hours)
- Phase 7 (Services): 4 tasks (~12 hours)
- Phase 8 (Handlers): 12 tasks (~20 hours)
- Phase 9 (Integration): 2 tasks (~10 hours)
- Phase 10 (Testing): 9 tasks (~20 hours)
- Phase 11 (Docs/Deploy): 7 tasks (~15 hours)

**Total Estimated Effort**: 87 tasks (~160 hours)

**TDD Compliance**: ✅ All implementation tasks have preceding test tasks

**Constitution Compliance**: ✅ Quality standards built into every phase
