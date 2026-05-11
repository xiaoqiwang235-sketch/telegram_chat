# Implementation Plan: Telegram Entertainment Chatbot

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| **Language** | Python | 3.11+ | Async/await support required |
| **Telegram Library** | python-telegram-bot | 20.7+ | Async version required |
| **Database Driver** | pymysql | 1.1.0+ | Pure Python MySQL driver |
| **Database** | MySQL | 8.0+ | Vector storage via BLOB |
| **Vector Search** | Faiss | 1.7.4+ | CPU version sufficient |
| **HTTP Client** | httpx | 0.25.0+ | Async HTTP client for API calls |
| **LLM API** | XiaoMi MiMo API | Latest | OpenAI-compatible API |
| **Embedding API** | OpenAI text-embedding-ada-002 | Latest | For vector generation |
| **Environment** | python-dotenv | 1.0.0+ | Configuration management |
| **Code Quality** | pylint, black | Latest | PEP 8 compliance (NFR-014) |
| **Testing** | pytest, pytest-asyncio | Latest | Async test support |
| **Database Migrations** | Alembic | 1.12.0+ | Schema evolution (NFR-017) |

**Constraints:**
- Must use asyncio (not threading)
- Direct pymysql usage (no ORM)
- Local deployment only (no Docker/cloud)
- `.env` and `.venv` excluded from git

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **1. Code Quality** | ✅ | Enforced via pylint (8.0/10 min), PEP 8 compliance, black formatting |
| **2. Testing Standards** | ✅ | pytest with pytest-asyncio, comprehensive test coverage planned |
| **3. Documentation** | ✅ | Docstrings for all public APIs, inline comments for complex logic |
| **4. Architecture** | ✅ | Clear separation: handlers → services → repositories → database |
| **5. Performance** | ✅ | Faiss indexing, connection pooling, async I/O throughout |
| **6. Security** | ✅ | Input validation, SQL injection prevention, credential management via .env |
| **Workflow: Planning → Specification → Design** | ✅ | Following CodexSpec methodology |
| **Decision: Maintainability over optimization** | ✅ | Modular design, clear interfaces, no premature optimization |
| **Decision: Clarity over cleverness** | ✅ | Straightforward code, meaningful names, simple patterns |
| **Decision: Stability over features** | ✅ | Robust error handling, graceful degradation, comprehensive testing |
| **Decision: Security over convenience** | ✅ | Input sanitization, credential protection, SQL injection prevention |

**Constitution Compliance**: 100% - All principles explicitly addressed in technical design.

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Telegram Bot API                          │
│                    (python-telegram-bot)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Message Handlers Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Command  │  │ Message  │  │  Admin   │  │  Error   │       │
│  │ Handler  │  │ Handler  │  │ Handler  │  │ Handler  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Service Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Chat Service│  │ Style Service│  │  Memory      │         │
│  │              │  │              │  │  Service     │         │
│  └──────┬───────┘  └──────────────┘  └──────┬───────┘         │
└─────────┼───────────────────────────────────┼──────────────────┘
          │                                   │
          ▼                                   ▼
┌─────────────────────┐         ┌─────────────────────────────────┐
│   LLM Integration   │         │      Vector & Memory Layer       │
│  ┌───────────────┐  │         │  ┌──────────┐  ┌────────────┐  │
│  │ XiaoMi MiMo   │  │         │  │  Faiss   │  │  MySQL     │  │
│  │ API Client    │  │         │  │  Index   │  │  Repository│  │
│  └───────────────┘  │         │  └──────────┘  └────────────┘  │
│  ┌───────────────┐  │         │  ┌──────────┐  ┌────────────┐  │
│  │ OpenAI        │  │         │  │ Embedding│  │  User      │  │
│  │ Embedding API │  │         │  │ Service │  │  Repository│  │
│  └───────────────┘  │         │  └──────────┘  └────────────┘  │
└─────────────────────┘         └─────────────────────────────────┘
```

**Architecture Pattern**: Layered Architecture with Repository Pattern

**Data Flow:**
1. Telegram sends update → Message Handler
2. Handler validates → Service Layer
3. Service processes → LLM API + Memory/Vector Layer
4. Response generated → Handler → Telegram API

## 4. Component Structure

```
telegram_chat/
├── src/
│   ├── main.py                      # Application entry point
│   ├── config.py                    # Configuration loader (.env)
│   │
│   ├── handlers/                    # Telegram message handlers
│   │   ├── __init__.py
│   │   ├── base_handler.py         # Base handler class
│   │   ├── command_handlers.py     # /start, /help, /style, /setstyle, /clear
│   │   ├── admin_handlers.py       # /groupstyle, /resetuser, /stats
│   │   └── message_handlers.py     # Regular message processing
│   │
│   ├── services/                    # Business logic layer
│   │   ├── __init__.py
│   │   ├── chat_service.py         # Main chat orchestration
│   │   ├── style_service.py        # Style management logic
│   │   ├── memory_service.py       # Memory orchestration (short + long-term)
│   │   └── rate_limiter.py         # Rate limiting implementation
│   │
│   ├── integrations/                # External API integrations
│   │   ├── __init__.py
│   │   ├── mimo_client.py          # XiaoMi MiMo API client
│   │   ├── embedding_client.py     # OpenAI embedding API client
│   │   └── telegram_client.py      # Telegram bot wrapper
│   │
│   ├── memory/                      # Memory subsystem
│   │   ├── __init__.py
│   │   ├── short_term_memory.py    # In-memory conversation context
│   │   ├── long_term_memory.py     # Vector-based semantic search
│   │   ├── faiss_manager.py        # Faiss index management
│   │   └── vector_store.py         # Vector CRUD operations
│   │
│   ├── repositories/                # Data access layer
│   │   ├── __init__.py
│   │   ├── base_repository.py      # Base repository class
│   │   ├── user_repository.py      # User data access
│   │   ├── conversation_repository.py  # Conversation history
│   │   ├── vector_repository.py    # Vector data access
│   │   └── group_repository.py     # Group settings
│   │
│   ├── models/                      # Data models
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── conversation.py         # Conversation model
│   │   ├── message.py              # Message model
│   │   ├── style.py                # Style enum/constants
│   │   └── group_settings.py       # Group settings model
│   │
│   ├── database/                    # Database utilities
│   │   ├── __init__.py
│   │   ├── connection.py           # Database connection pooling
│   │   ├── migrations.py           # Alembic integration
│   │   └── schema.sql              # Initial schema (for reference)
│   │
│   └── utils/                       # Utilities
│       ├── __init__.py
│       ├── validators.py            # Input validation
│       ├── sanitizers.py            # Input sanitization
│       ├── logger.py               # Logging setup
│       └── helpers.py              # Helper functions
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── test_handlers/              # Handler tests
│   ├── test_services/              # Service tests
│   ├── test_integrations/          # Integration tests
│   ├── test_memory/                # Memory subsystem tests
│   └── test_repositories/          # Repository tests
│
├── .env                             # Environment configuration
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
├── alembic.ini                      # Alembic configuration
├── migrations/                      # Database migration scripts
│   └── versions/
├── pyproject.toml                   # Project metadata & tools config
├── .pylintrc                        # Pylint configuration (min 8.0/10)
├── README.md                        # Project documentation
└── CLAUDE.md                        # Project guidelines (already exists)
```

## 5. Module Dependency Graph

```
┌──────────────────┐
│  main.py         │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                  handlers/ (all modules)                │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    services/                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │chat_service  │  │style_service │  │memory_service│  │
│  └──────┬───────┘  └──────────────┘  └──────┬───────┘  │
└─────────┼───────────────────────────────────┼──────────┘
          │                                   │
          ▼                                   ▼
┌─────────────────────┐         ┌─────────────────────────────┐
│   integrations/     │         │       memory/               │
│  ┌───────────────┐  │         │  ┌──────────────────────┐  │
│  │ mimo_client   │  │         │  │ short_term_memory    │  │
│  └───────────────┘  │         │  └──────────────────────┘  │
│  ┌───────────────┐  │         │  ┌──────────────────────┐  │
│  │embedding_client│  │         │  │ long_term_memory     │  │
│  └───────────────┘  │         │  └──────────┬───────────┘  │
└─────────────────────┘         │             │              │
                                │             ▼              │
                                │  ┌──────────────────────┐  │
                                │  │ faiss_manager        │  │
                                │  └──────────────────────┘  │
                                └─────────────────────────────┘
                                             │
                                             ▼
                                ┌─────────────────────────────┐
                                │       repositories/          │
                                │  ┌──────────────────────┐  │
                                │  │ user_repository      │  │
                                │  │ conversation_repository│ │
                                │  │ vector_repository    │  │
                                │  │ group_repository     │  │
                                │  └──────────────────────┘  │
                                └──────────────┬──────────────┘
                                               │
                                               ▼
                                ┌─────────────────────────────┐
                                │       database/             │
                                │  connection.py (pool)       │
                                └─────────────────────────────┘

Dependencies Flow:
handlers → services → integrations/memory → repositories → database
handlers → services → utils (validators, sanitizers, logger)
```

## 6. Module Specifications

### Module: main.py
- **Responsibility**: Application entry point, bot initialization, handler registration
- **Dependencies**: handlers/, config/, database/connection.py
- **Interface**: None (entry point)
- **Files**:
  - `src/main.py` - Already exists, will be refactored

### Module: config.py
- **Responsibility**: Load and validate configuration from .env
- **Dependencies**: None
- **Interface**: `Config` class with configuration properties
- **Files**:
  - `src/config.py` - New file

### Module: handlers/
- **Responsibility**: Process Telegram updates, route to appropriate handlers
- **Dependencies**: services/, utils/validators, utils/sanitizers
- **Interface**: Handler functions decorated with Telegram routing
- **Files**:
  - `src/handlers/base_handler.py` - Base handler with common logic
  - `src/handlers/command_handlers.py` - /start, /help, /style, /setstyle, /clear
  - `src/handlers/admin_handlers.py` - /groupstyle, /resetuser, /stats
  - `src/handlers/message_handlers.py` - Regular message processing

### Module: services/chat_service.py
- **Responsibility**: Orchestrate chat responses, integrate LLM and memory
- **Dependencies**: integrations/mimo_client, services/memory_service, services/style_service
- **Interface**: `async def generate_response(user_message, user_id, chat_id) -> str`
- **Files**:
  - `src/services/chat_service.py` - New file

### Module: services/style_service.py
- **Responsibility**: Manage conversation styles (user/group preferences, priority logic)
- **Dependencies**: repositories/user_repository, repositories/group_repository
- **Interface**: `async def get_effective_style(user_id, chat_id) -> Style`
- **Files**:
  - `src/services/style_service.py` - New file

### Module: services/memory_service.py
- **Responsibility**: Orchestrate short-term and long-term memory
- **Dependencies**: memory/, repositories/
- **Interface**: `async def get_context(user_id, chat_id) -> List[Message]`
- **Files**:
  - `src/services/memory_service.py` - New file

### Module: services/rate_limiter.py
- **Responsibility**: Enforce rate limiting (20 messages/60 seconds per user)
- **Dependencies**: None (in-memory storage with TTL)
- **Interface**: `async def check_rate_limit(user_id) -> bool`
- **Files**:
  - `src/services/rate_limiter.py` - New file

### Module: integrations/mimo_client.py
- **Responsibility**: Communicate with XiaoMi MiMo API
- **Dependencies**: config.py, httpx
- **Interface**: `async def chat_completion(messages, style) -> str`
- **Files**:
  - `src/integrations/mimo_client.py` - New file

### Module: integrations/embedding_client.py
- **Responsibility**: Generate vector embeddings via OpenAI API
- **Dependencies**: config.py, httpx
- **Interface**: `async def generate_embedding(text) -> List[float]`
- **Files**:
  - `src/integrations/embedding_client.py` - New file

### Module: memory/short_term_memory.py
- **Responsibility**: Manage in-memory conversation context (current session)
- **Dependencies**: None
- **Interface**: `class ShortTermMemory` with add/get/clear methods
- **Files**:
  - `src/memory/short_term_memory.py` - New file

### Module: memory/long_term_memory.py
- **Responsibility**: Semantic search using vector embeddings
- **Dependencies**: memory/faiss_manager, repositories/vector_repository
- **Interface**: `async def search_relevant(user_id, query, top_k=5) -> List[Conversation]`
- **Files**:
  - `src/memory/long_term_memory.py` - New file

### Module: memory/faiss_manager.py
- **Responsibility**: Manage Faiss index (build, save, load, search)
- **Dependencies**: repositories/vector_repository, config.py
- **Interface**: `class FaissManager` with rebuild/search methods
- **Files**:
  - `src/memory/faiss_manager.py` - New file

### Module: repositories/
- **Responsibility**: Data access layer (CRUD operations)
- **Dependencies**: database/connection.py, models/
- **Interface**: Repository classes with async CRUD methods
- **Files**:
  - `src/repositories/base_repository.py` - Base repository with common methods
  - `src/repositories/user_repository.py` - User CRUD operations
  - `src/repositories/conversation_repository.py` - Conversation history CRUD
  - `src/repositories/vector_repository.py` - Vector data CRUD
  - `src/repositories/group_repository.py` - Group settings CRUD

### Module: models/
- **Responsibility**: Data models and validation
- **Dependencies**: None
- **Interface**: Dataclasses/Pydantic models for type safety
- **Files**:
  - `src/models/user.py` - User model
  - `src/models/conversation.py` - Conversation model
  - `src/models/message.py` - Message model
  - `src/models/style.py` - Style enum/constants
  - `src/models/group_settings.py` - Group settings model

### Module: database/
- **Responsibility**: Database connection pooling and migrations
- **Dependencies**: config.py
- **Interface**: `get_connection()` context manager
- **Files**:
  - `src/database/connection.py` - Connection pool management
  - `src/database/migrations.py` - Alembic integration
  - `src/database/schema.sql` - Initial schema reference

### Module: utils/
- **Responsibility**: Utility functions (validation, sanitization, logging)
- **Dependencies**: None
- **Interface**: Utility functions
- **Files**:
  - `src/utils/validators.py` - Input validation functions
  - `src/utils/sanitizers.py` - Input sanitization functions
  - `src/utils/logger.py` - Logging configuration
  - `src/utils/helpers.py` - Helper functions

## 7. Data Models

### User
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| user_id | bigint | Telegram user ID | PRIMARY KEY |
| username | varchar(255) | Telegram username | Nullable, Indexed |
| first_name | varchar(255) | User's first name | Nullable |
| last_name | varchar(255) | User's last name | Nullable |
| preferred_style | varchar(50) | User's preferred style | Default: 'default' |
| created_at | timestamp | Account creation time | DEFAULT CURRENT_TIMESTAMP |
| updated_at | timestamp | Last update time | ON UPDATE CURRENT_TIMESTAMP |

### Conversation
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | int | Conversation ID | PRIMARY KEY, AUTO_INCREMENT |
| chat_id | bigint | Telegram chat ID | Indexed |
| user_id | bigint | Telegram user ID | FOREIGN KEY → users(user_id) |
| message_text | text | Message content | Not Null |
| role | enum | Message role | 'user', 'assistant', 'system' |
| timestamp | timestamp | Message time | DEFAULT CURRENT_TIMESTAMP |
| **Indexes**: (chat_id, user_id, timestamp) | | |

### Conversation Vector
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | int | Vector ID | PRIMARY KEY, AUTO_INCREMENT |
| conversation_id | int | Reference to conversation | FOREIGN KEY → conversations(id) |
| user_id | bigint | Telegram user ID | FOREIGN KEY → users(user_id) |
| chat_id | bigint | Telegram chat ID | Indexed |
| message_text | text | Original message | Not Null |
| embedding | blob | Vector embedding (binary) | Not Null |
| created_at | timestamp | Creation time | DEFAULT CURRENT_TIMESTAMP |
| **Indexes**: (user_id, chat_id) | | |

### Group Settings
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| chat_id | bigint | Telegram group chat ID | PRIMARY KEY |
| group_style | varchar(50) | Group's default style | Default: 'default' |
| created_at | timestamp | Settings creation time | DEFAULT CURRENT_TIMESTAMP |
| updated_at | timestamp | Last update time | ON UPDATE CURRENT_TIMESTAMP |

### User Preferences
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | int | Preference ID | PRIMARY KEY, AUTO_INCREMENT |
| user_id | bigint | Telegram user ID | FOREIGN KEY → users(user_id) |
| preference_key | varchar(100) | Preference key | Not Null |
| preference_value | text | Preference value | Not Null |
| created_at | timestamp | Creation time | DEFAULT CURRENT_TIMESTAMP |
| updated_at | timestamp | Last update time | ON UPDATE CURRENT_TIMESTAMP |
| **Unique**: (user_id, preference_key) | | |

## 8. API Contracts

### Telegram Bot API (Consumed)

#### Message Received (Incoming)
- **Event**: `Update` object from python-telegram-bot
- **Fields**:
  - `message.chat_id`:bigint - Chat identifier
  - `message.from_user.id`:bigint - User identifier
  - `message.text`:string - Message content
  - `message.entities`:array - Mention entities (for @bot detection)

#### Message Sent (Outgoing)
- **Method**: `await update.message.reply_text(text)`
- **Parameters**:
  - `text`:string - Response message
- **Errors**: Network timeout, API rate limit

### XiaoMi MiMo API (Consumed)

#### POST /v1/chat/completions
- **Request**:
  ```json
  {
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "你是一个幽默搞笑的聊天助手..."},
      {"role": "user", "content": "用户消息"},
      ... (retrieved context)
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }
  ```
- **Response**:
  ```json
  {
    "id": "chatcmpl-123",
    "choices": [{
      "message": {
        "role": "assistant",
        "content": "AI回复内容"
      }
    }]
  }
  ```
- **Errors**: Timeout (retry with exponential backoff), rate limit (queue), invalid response (fallback)

### OpenAI Embedding API (Consumed)

#### POST /v1/embeddings
- **Request**:
  ```json
  {
    "model": "text-embedding-ada-002",
    "input": "要生成向量的文本"
  }
  ```
- **Response**:
  ```json
  {
    "data": [{
      "embedding": [0.1, 0.2, ...] // 1536-dimensional vector
    }]
  }
  ```
- **Errors**: Timeout (retry), quota exceeded (log warning, skip embedding)

### Database SQL (Executed)

#### Queries (via pymysql)
- **Insert Conversation**: `INSERT INTO conversations (...) VALUES (...)`
- **Fetch Context**: `SELECT * FROM conversations WHERE chat_id=? AND user_id=? ORDER BY timestamp DESC LIMIT 50`
- **Fetch Vectors**: `SELECT * FROM conversation_vectors WHERE user_id=?`
- **Update Style**: `UPDATE users SET preferred_style=? WHERE user_id=?`
- **Errors**: Connection lost (reconnect), duplicate key (upsert)

### Bot Commands (Exposed to Users)

#### `/start`
- **Permission**: Any user
- **Response**: Welcome message + basic commands list
- **Example**: "你好！我是你的聊天助手～ 使用 /help 查看可用命令"

#### `/help`
- **Permission**: Any user
- **Response**: All available commands with descriptions
- **Example**: Lists /style, /setstyle, /clear commands

#### `/style`
- **Permission**: Any user
- **Response**: Lists all 6 available styles
- **Example**: "可用风格：幽默搞笑, 温柔体贴, 傲娇, 严肃专业, 卖萌可爱, 知性理性"

#### `/setstyle <style>`
- **Permission**: Any user
- **Response**: Confirms style change
- **Example**: "已设置为傲娇风格！"
- **Error**: Invalid style → shows valid options

#### `/clear`
- **Permission**: Any user
- **Response**: Asks for confirmation
- **Confirmation**: "确认清除所有对话记忆？（偏好设置将保留）"
- **Action**: Deletes all conversation history, preserves user preferences

#### `/groupstyle <style>` (Admin Only)
- **Permission**: Group administrators only
- **Response**: Confirms group style change
- **Error**: Non-admin → "此命令仅管理员可用"

#### `/resetuser @user` (Admin Only)
- **Permission**: Group administrators only
- **Response**: Confirms user memory reset
- **Error**: Non-admin → "此命令仅管理员可用"

#### `/stats` (Admin Only)
- **Permission**: Group administrators only
- **Response**: Usage statistics
- **Example**: "总用户数: 127, 今日消息数: 1,542, 活跃群组: 8"

## 9. Implementation Phases

### Phase 1: Foundation Setup
**Goal**: Establish project structure and infrastructure

- [ ] **Task 1.1**: Create project directory structure
  - Create all module directories (handlers, services, integrations, memory, repositories, models, database, utils)
  - Create `__init__.py` files for all packages
  - Setup test directory structure

- [ ] **Task 1.2**: Configure development environment
  - Create `requirements.txt` with all dependencies
  - Create `.env.example` with configuration template
  - Setup `pyproject.toml` for project metadata
  - Configure `.pylintrc` (min score 8.0/10)
  - Configure `black` for code formatting
  - Configure `pytest` and `pytest-asyncio`

- [ ] **Task 1.3**: Implement configuration management
  - Create `config.py` with Config class
  - Load and validate .env configuration
  - Define constants (styles, limits, thresholds)
  - Add configuration validation (required fields, value ranges)

- [ ] **Task 1.4**: Setup database layer
  - Create `database/connection.py` with connection pooling
  - Write initial schema.sql (all 5 tables with correct structure)
  - Setup Alembic for migrations (`alembic.ini`, `migrations/versions/`)
  - Create migration script for initial schema
  - Implement auto-table creation on first run
  - Add connection retry logic

- [ ] **Task 1.5**: Implement base repository and models
  - Create `repositories/base_repository.py` with async CRUD methods
  - Create all model classes in `models/` (User, Conversation, Message, Style, GroupSettings)
  - Add model validation and serialization
  - Write unit tests for models

**Deliverables**:
- Complete project structure
- Working configuration system
- Database connectivity with migrations
- Base repository pattern

**Success Criteria**:
- ✅ All imports work without errors
- ✅ Database connection pool established
- ✅ Configuration loads from .env
- ✅ Alembic migrations run successfully

---

### Phase 2: Core Functionality
**Goal**: Implement basic bot with LLM integration and short-term memory

- [ ] **Task 2.1**: Implement Telegram bot foundation
  - Refactor `main.py` to use new architecture
  - Create `handlers/base_handler.py` with common handler logic
  - Implement basic message routing (commands vs. messages)
  - Add error handling at handler level
  - Implement logging setup (`utils/logger.py`)

- [ ] **Task 2.2**: Implement XiaoMi MiMo API integration
  - Create `integrations/mimo_client.py`
  - Implement `chat_completion()` method with style prompts
  - Add retry logic with exponential backoff
  - Add timeout handling
  - Add error handling and fallback responses
  - Write unit tests for API client

- [ ] **Task 2.3**: Implement basic command handlers
  - Create `handlers/command_handlers.py`
  - Implement `/start` command (welcome message)
  - Implement `/help` command (list commands)
  - Add command validation and error handling
  - Write unit tests for commands

- [ ] **Task 2.4**: Implement message handler (no memory yet)
  - Create `handlers/message_handlers.py`
  - Implement @mention detection for groups
  - Implement rate limiting check (via `services/rate_limiter.py`)
  - Implement input validation and sanitization
  - Connect to LLM API and send response
  - Add error handling and logging

- [ ] **Task 2.5**: Implement short-term memory
  - Create `memory/short_term_memory.py`
  - Implement in-memory conversation context (per user/group)
  - Store last N messages (configurable, default 50)
  - Add context retrieval for LLM calls
  - Integrate with message handler
  - Write unit tests for memory

- [ ] **Task 2.6**: Implement rate limiting
  - Create `services/rate_limiter.py`
  - Implement in-memory rate limiting (20 msg/60 sec per user)
  - Add TTL for old records
  - Add temporary ban for violations
  - Integrate with message handler
  - Write unit tests for rate limiter

- [ ] **Task 2.7**: Implement basic repositories
  - Create `repositories/user_repository.py`
  - Create `repositories/conversation_repository.py`
  - Implement CRUD operations
  - Add connection error handling
  - Write unit tests for repositories

**Deliverables**:
- Working bot that responds to @mentions
- Basic commands (/start, /help)
- LLM integration
- Short-term memory
- Rate limiting

**Success Criteria**:
- ✅ Bot responds to messages in private chats
- ✅ Bot responds only to @mentions in groups
- ✅ LLM generates responses
- ✅ Short-term memory maintains context
- ✅ Rate limiting enforced

---

### Phase 3: Style System and Long-term Memory
**Goal**: Implement conversation styles and vector-based semantic search

- [ ] **Task 3.1**: Implement style service
  - Create `services/style_service.py`
  - Define style constants and prompts
  - Implement style priority logic (user > group > default)
  - Create `repositories/group_repository.py`
  - Implement style CRUD operations
  - Write unit tests for style service

- [ ] **Task 3.2**: Implement style commands
  - Add `/style` command (list available styles)
  - Add `/setstyle <style>` command (user style preference)
  - Add `/groupstyle <style>` command (group style, admin only)
  - Implement admin permission checking
  - Add style validation and error handling
  - Write unit tests for style commands

- [ ] **Task 3.3**: Implement OpenAI embedding integration
  - Create `integrations/embedding_client.py`
  - Implement `generate_embedding()` method
  - Add retry logic and error handling
  - Add API quota handling
  - Write unit tests for embedding client

- [ ] **Task 3.4**: Implement vector repository
  - Create `repositories/vector_repository.py`
  - Implement vector CRUD operations (BLOB storage)
  - Implement batch vector retrieval
  - Add connection error handling
  - Write unit tests for vector repository

- [ ] **Task 3.5**: Implement Faiss manager
  - Create `memory/faiss_manager.py`
  - Implement Faiss index building from MySQL
  - Implement index persistence (save/load)
  - Implement index search functionality
  - Add index rebuild trigger (startup + 1000 new vectors)
  - Write unit tests for Faiss manager

- [ ] **Task 3.6**: Implement long-term memory service
  - Create `memory/long_term_memory.py`
  - Implement semantic search using Faiss
  - Integrate with vector repository
  - Implement top-k retrieval (default k=5)
  - Add fallback to recent messages if no results
  - Write unit tests for long-term memory

- [ ] **Task 3.7**: Implement memory orchestration service
  - Create `services/memory_service.py`
  - Integrate short-term and long-term memory
  - Implement context retrieval logic
  - Add memory persistence on every message
  - Implement vector generation and storage
  - Write unit tests for memory service

- [ ] **Task 3.8**: Integrate memory with chat service
  - Create `services/chat_service.py`
  - Orchestrate LLM calls with memory context
  - Apply style prompts based on user/group preferences
  - Handle long messages (>4000 chars) with chunking
  - Add error handling and fallbacks
  - Write unit tests for chat service

- [ ] **Task 3.9**: Update message handler with full features
  - Integrate chat service
  - Integrate memory service
  - Integrate style service
  - Add comprehensive logging
  - Add performance monitoring
  - Update error handling

**Deliverables**:
- Complete style system (user/group preferences)
- Vector embedding generation
- Faiss-based semantic search
- Long-term memory integration
- Full chat orchestration

**Success Criteria**:
- ✅ All 6 styles work correctly
- ✅ Style priority logic works (user > group > default)
- ✅ Long-term memory retrieves relevant past conversations
- ✅ Faiss index rebuilds correctly
- ✅ Vectors persist in MySQL

---

### Phase 4: Admin Features and Memory Management
**Goal**: Implement admin commands and user memory management

- [ ] **Task 4.1**: Implement `/clear` command
  - Add command handler for `/clear`
  - Implement confirmation prompt
  - Delete all conversation history (conversations + vectors)
  - Preserve user preferences (styles)
  - Add confirmation message
  - Write unit tests

- [ ] **Task 4.2**: Implement `/resetuser @user` command
  - Add command handler for `/resetuser`
  - Implement admin permission check
  - Parse @username parameter
  - Delete specified user's conversation history
  - Add confirmation message
  - Write unit tests

- [ ] **Task 4.3**: Implement `/stats` command
  - Add command handler for `/stats`
  - Implement admin permission check
  - Query database for statistics:
    - Total user count
    - Today's message count
    - Active group count
  - Format and display stats
  - Write unit tests

- [ ] **Task 4.4**: Implement user preference repository
  - Create `repositories/user_preferences_repository.py`
  - Implement key-value CRUD operations
  - Add upsert logic (ON DUPLICATE KEY UPDATE)
  - Write unit tests

- [ ] **Task 4.5**: Enhance style system with user preferences
  - Store user style preferences in user_preferences table
  - Update style service to use preferences
  - Add migration to move from users.preferred_style to user_preferences
  - Update all style-related commands
  - Write integration tests

- [ ] **Task 4.6**: Implement comprehensive error handling
  - Create `handlers/error_handler.py`
  - Handle API errors gracefully
  - Handle database errors with reconnection
  - Handle network timeouts with retries
  - Add user-friendly error messages
  - Add comprehensive error logging
  - Write unit tests for error scenarios

**Deliverables**:
- All admin commands working
- User memory management
- Comprehensive error handling
- User preferences system

**Success Criteria**:
- ✅ `/clear` deletes conversations but preserves preferences
- ✅ `/resetuser` works for admins only
- ✅ `/stats` displays accurate statistics
- ✅ All error scenarios handled gracefully

---

### Phase 5: Testing and Quality Assurance
**Goal**: Comprehensive testing and code quality enforcement

- [ ] **Task 5.1**: Write unit tests for all modules
  - Test all handlers (command_handlers, admin_handlers, message_handlers)
  - Test all services (chat_service, style_service, memory_service, rate_limiter)
  - Test all integrations (mimo_client, embedding_client)
  - Test all memory modules (short_term, long_term, faiss_manager)
  - Test all repositories
  - Target: >80% code coverage

- [ ] **Task 5.2**: Write integration tests
  - Test full message flow (Telegram → Handler → Service → LLM → Response)
  - Test memory persistence (MySQL + Faiss)
  - Test style priority logic
  - Test admin commands
  - Test error scenarios (API failures, database errors)
  - Test rate limiting
  - Test long message handling

- [ ] **Task 5.3**: Write end-to-end tests
  - Test complete user journeys (new user onboarding, style changes, memory queries)
  - Test group interactions (multiple users, @mentions, admin commands)
  - Test edge cases (empty messages, special characters, rapid flooding)
  - Test concurrent operations (multiple users, multiple groups)

- [ ] **Task 5.4**: Enforce code quality standards
  - Run pylint on all modules (min score 8.0/10)
  - Fix all pylint warnings
  - Run black formatter on all files
  - Run pytest with coverage reporting
  - Fix any failing tests
  - Ensure >80% test coverage

- [ ] **Task 5.5**: Performance testing
  - Test response time (target: <5 seconds under normal load)
  - Test concurrent conversations (target: 10 simultaneous)
  - Test vector search performance (target: <1 second for 10,000 vectors)
  - Test database query performance (optimize with EXPLAIN)
  - Add benchmarks for critical paths

- [ ] **Task 5.6**: Security testing
  - Test SQL injection prevention (validate all inputs)
  - Test XSS prevention (sanitize all outputs)
  - Test credential protection (no .env in git)
  - Test rate limiting enforcement
  - Test admin permission checks
  - Verify no sensitive data in logs

- [ ] **Task 5.7**: Load testing
  - Simulate 50 concurrent users
  - Simulate 1000 messages/minute
  - Test database connection pooling under load
  - Test Faiss index performance under load
  - Identify and fix bottlenecks

**Deliverables**:
- Comprehensive test suite (>80% coverage)
- All code quality checks passing (pylint ≥8.0/10)
- Performance benchmarks meeting NFRs
- Security audit passed

**Success Criteria**:
- ✅ All tests passing (unit, integration, e2e)
- ✅ Code coverage >80%
- ✅ pylint score ≥8.0/10 for all modules
- ✅ All NFRs met (performance, security, reliability)

---

### Phase 6: Documentation and Deployment
**Goal**: Complete documentation and prepare for deployment

- [ ] **Task 6.1**: Write technical documentation
  - Update README.md with setup instructions
  - Document architecture (module dependencies, data flow)
  - Document API contracts (Telegram, XiaoMi MiMo, OpenAI)
  - Document database schema (all tables, indexes, foreign keys)
  - Document configuration (.env variables)
  - Add inline code comments where complex

- [ ] **Task 6.2**: Write user documentation
  - Create user guide for all commands
  - Document style system with examples
  - Document memory management features
  - Add troubleshooting section
  - Add FAQ section

- [ ] **Task 6.3**: Prepare deployment artifacts
  - Create `.env.example` with all required variables
  - Create `requirements.txt` with pinned versions
  - Create database setup script (`schema.sql`)
  - Create Alembic migration scripts
  - Create startup script (`run.py` or `start.sh`)
  - Create systemd service file (optional)

- [ ] **Task 6.4**: Setup monitoring and logging
  - Configure structured logging (JSON format)
  - Add log rotation (prevent disk filling)
  - Add performance metrics logging (response times, API calls)
  - Add error tracking (exception logs)
  - Document log locations and formats

- [ ] **Task 6.5**: Deployment testing
  - Test on fresh environment (clean .venv, fresh database)
  - Test database migration from scratch
  - Test bot startup and initialization
  - Test all commands in deployed environment
  - Test memory system under load
  - Test error recovery (restart after crash)

- [ ] **Task 6.6**: Final quality checks
  - Run full test suite one more time
  - Verify all NFRs are met
  - Check git status (no .env, no .venv, no temporary files)
  - Verify .gitignore is correct
  - Run final pylint check
  - Document any known issues or limitations

**Deliverables**:
- Complete documentation (technical + user)
- Deployment-ready artifacts
- Monitoring and logging configured
- Deployment tested on fresh environment

**Success Criteria**:
- ✅ Bot can be deployed on fresh environment in <30 minutes
- ✅ All documentation is clear and accurate
- ✅ Monitoring captures all critical metrics
- ✅ All quality checks passing

---

## 10. Technical Decisions

### Decision 1: Layered Architecture with Repository Pattern
- **Choice**: 4-layer architecture (Handlers → Services → Integrations/Memory → Repositories → Database)
- **Rationale**:
  - Separation of concerns (each layer has single responsibility)
  - Testability (each layer can be mocked independently)
  - Maintainability (changes in one layer don't affect others)
  - Scalability (layers can be optimized independently)
- **Alternatives Considered**:
  - Monolithic handlers (all logic in handlers) - Rejected: Hard to test, maintain
  - Microservices (separate services for each feature) - Rejected: Overkill for single bot, adds complexity
- **Trade-offs**:
  - More files and indirection (offset by better organization)
  - Slightly more boilerplate (offset by reusability)

### Decision 2: Async IO Throughout (asyncio)
- **Choice**: Use async/await for all I/O operations (HTTP, database, Telegram)
- **Rationale**:
  - Specified by user (asyncio requirement)
  - Better performance for concurrent operations
  - Native support in python-telegram-bot 20.7+
  - Efficient resource utilization (single-threaded concurrent I/O)
- **Alternatives Considered**:
  - Threading - Rejected: GIL limitations, more complex synchronization
  - Synchronous - Rejected: Poor performance under load
- **Trade-offs**:
  - All dependencies must support async (limits library choices)
  - Debugging can be harder (offset by better tooling support)

### Decision 3: Direct pymysql Usage (No ORM)
- **Choice**: Use pymysql directly instead of SQLAlchemy/Django ORM
- **Rationale**:
  - Specified by user ("直接用pymysql")
  - More control over SQL queries (performance optimization)
  - Simpler dependency (one less library)
  - Learning requirement from constitution (avoid abstractions when unnecessary)
- **Alternatives Considered**:
  - SQLAlchemy - Rejected: User specified pymysql, ORM adds complexity
  - Peewee - Rejected: User specified pymysql, smaller ecosystem
- **Trade-offs**:
  - More manual SQL writing (offset by performance and clarity)
  - Manual schema management (mitigated by Alembic)
  - No automatic relationship loading (acceptable for this use case)

### Decision 4: Faiss with MySQL Hybrid Storage
- **Choice**: Store vectors in MySQL BLOB fields, use Faiss for in-memory indexing
- **Rationale**:
  - MySQL provides persistent storage and queryability
  - Faiss provides fast vector search in memory
  - Simpler than dedicated vector databases (no additional infrastructure)
  - Rebuildable from MySQL (data durability)
- **Alternatives Considered**:
  - Pure Faiss (file-based) - Rejected: No queryability, harder to manage metadata
  - Dedicated vector DB (Qdrant, Milvus) - Rejected: Overkill for local deployment, user wanted Faiss
  - Chroma - Rejected: User selected Faiss
- **Trade-offs**:
  - Vector search slower than dedicated solutions (acceptable for <10,000 vectors)
  - Manual index rebuild management (mitigated by automated triggers)
  - BLOB storage less efficient than binary formats (acceptable trade-off)

### Decision 5: OpenAI text-embedding-ada-002 for Embeddings
- **Choice**: Use OpenAI's text-embedding-ada-002 API for vector generation
- **Rationale**:
  - Industry-standard, high-quality embeddings
  - 1536 dimensions (good balance of quality and performance)
  - Reliable API with good uptime
  - Easy integration with async HTTP client
- **Alternatives Considered**:
  - Local embedding models (sentence-transformers) - Rejected: Requires GPU for good performance, adds dependency complexity
  - XiaoMi MiMo embedding API - Rejected: Unclear if they offer embedding API, not specified in docs
  - Other embedding APIs (Cohere, HuggingFace) - Rejected: OpenAI is industry standard
- **Trade-offs**:
  - API cost per embedding (offset by quality and simplicity)
  - External dependency (mitigated by fallback logic)
  - Rate limits (mitigated by retry logic)

### Decision 6: In-Memory Short-term Memory
- **Choice**: Use Python dict for short-term conversation context
- **Rationale**:
  - Fast access (no database round-trips)
  - Simple implementation (no additional dependencies)
  - Automatic cleanup on restart (acceptable for "short-term" data)
  - Low memory footprint (only recent messages)
- **Alternatives Considered**:
  - Redis - Rejected: Overkill for local deployment, adds infrastructure dependency
  - Temporary MySQL table - Rejected: Slower, unnecessary persistence
- **Trade-offs**:
  - Data lost on restart (acceptable for "short-term" memory)
  - No persistence (acceptable, long-term memory provides persistence)

### Decision 7: Style Prompts via System Messages
- **Choice**: Apply conversation styles via LLM system messages
- **Rationale**:
  - Standard approach for LLM personality customization
  - Flexible (easy to add new styles)
  - No need for fine-tuning (saves time and cost)
  - Works with OpenAI-compatible APIs
- **Alternatives Considered**:
  - Fine-tuned models - Rejected: Expensive, time-consuming, hard to maintain
  - Prompt injection in user messages - Rejected: Less reliable, harder to manage
- **Trade-offs**:
  - Style adherence depends on LLM quality (acceptable for use case)
  - System message token costs (minimal impact)

### Decision 8: Rate Limiting via In-Memory Storage
- **Choice**: Implement rate limiting with in-memory dict + TTL
- **Rationale**:
  - Simple implementation (no additional infrastructure)
  - Fast access (no database round-trips)
  - Automatic cleanup (TTL-based expiration)
  - Sufficient for single-instance deployment
- **Alternatives Considered**:
  - Redis - Rejected: Overkill for local deployment
  - MySQL-based rate limiting - Rejected: Slower, unnecessary persistence
- **Trade-offs**:
  - Data lost on restart (acceptable, rate limits reset on restart)
  - Not scalable across multiple instances (acceptable for local deployment)

### Decision 9: Long Message Chunking at Sentence Boundaries
- **Choice**: Split messages >4000 chars at sentence boundaries, send to API separately, synthesize response
- **Rationale**:
  - Preserves context (better than arbitrary truncation)
  - Token limits respected (avoids API errors)
  - Better user experience (no content loss)
- **Alternatives Considered**:
  - Truncation - Rejected: Loses context, poor UX
  - Single chunk regardless of length - Rejected: May exceed token limits
- **Trade-offs**:
  - More complex implementation (mitigated by clear algorithm)
  - Slower response time (multiple API calls, acceptable for long messages)

### Decision 10: Alembic for Database Migrations
- **Rationale**: Automated schema evolution, version control, rollback support
- **Trade-offs**: Additional setup time (offset by long-term maintainability)

### Decision 11: Pylint + Black for Code Quality
- **Rationale**: Automated enforcement of PEP 8, consistent code style, measurable quality (8.0/10 target)
- **Trade-offs**: Strict rules may slow initial development (offset by long-term maintainability)

### Decision 12: Comprehensive Logging with Structured Format
- **Rationale**: Debugging, monitoring, error tracking, performance analysis
- **Trade-offs**: Slightly more verbose code (offset by operational benefits)

---

## Appendix: Non-Functional Requirements Mapping

| NFR | Implementation Strategy |
|-----|------------------------|
| **NFR-001**: <5s response | Async I/O, connection pooling, efficient queries |
| **NFR-002**: 10 concurrent | asyncio, connection pooling, rate limiting |
| **NFR-003**: <1s vector search | Faiss in-memory indexing, periodic rebuilds |
| **NFR-004**: Optimized queries | Indexes on (chat_id, user_id, timestamp), EXPLAIN analysis |
| **NFR-005**: Credentials in .env | Config loader, .env.example, .gitignore enforcement |
| **NFR-006**: No credential exposure | Input sanitization, log filtering |
| **NFR-007**: SQL injection prevention | Parameterized queries, input validation |
| **NFR-008**: Input sanitization | Sanitizers module, whitelist validation |
| **NFR-009**: .env, .venv excluded | .gitignore validation |
| **NFR-010**: Graceful failure handling | Retry logic, fallback responses, error handlers |
| **NFR-011**: Auto-reconnection | Connection pool with retry, exponential backoff |
| **NFR-012**: Error logging | Structured logging, log levels, log rotation |
| **NFR-013**: Data consistency | Database transactions, locking for concurrent updates |
| **NFR-014**: PEP 8 compliance | pylint (8.0/10), black formatter, pre-commit hooks |
| **NFR-015**: Single-purpose functions | Module design, function size limits |
| **NFR-016**: Meaningful names | Naming conventions, code review |
| **NFR-017**: Migration support | Alembic integration, version control |
| **NFR-018**: Scalable schema | Indexed queries, efficient data types, pagination |
| **NFR-019**: Faiss rebuild | Automated triggers (startup, 1000 vectors) |
| **NFR-020**: Extensible styles | Style enum/constants, prompt templates |

---

## Conclusion

This technical implementation plan provides a comprehensive roadmap for building the Telegram Entertainment Chatbot. The plan respects all constitutional principles, addresses all functional and non-functional requirements, and provides clear implementation phases with measurable success criteria.

**Key Strengths:**
- ✅ Clear separation of concerns (layered architecture)
- ✅ Comprehensive testing strategy (>80% coverage)
- ✅ Measurable quality standards (pylint 8.0/10)
- ✅ Robust error handling and resilience
- ✅ Security-first design
- ✅ Performance-optimized approach
- ✅ Maintainable and extensible codebase

**Estimated Effort**: 120-160 hours (3-4 weeks for solo developer)

**Next Steps**:
1. Review this technical plan
2. Run `/codexspec.review-plan` to validate quality
3. Run `/codexspec.plan-to-tasks` to break down into actionable tasks
4. Begin implementation with Phase 1: Foundation Setup
