# Feature: Telegram Entertainment Chatbot

## Overview

A Telegram chatbot that provides entertaining conversations with multiple personality styles, equipped with both short-term and long-term memory capabilities. The bot integrates with large language models (XiaoMi MiMo API) and uses vector-based semantic search to maintain context and user preferences across conversations.

## Goals

- Provide an entertaining and interactive chat experience for Telegram users
- Support multiple conversation styles with personality switching
- Maintain conversation context and user preferences over time
- Support both group chats (with @mention trigger) and private chats
- Enable user customization of interaction preferences
- Ensure efficient memory retrieval using vector-based semantic search

## User Stories

### Story 1: Group Chat Interaction
**As a** Telegram group member
**I want** the bot to respond when I mention it
**So that** I can get entertaining responses without spamming the group

**Acceptance Criteria:**
- [ ] Bot only responds to messages that mention @bot_username in groups
- [ ] Bot responds to all messages in private chats
- [ ] Bot correctly identifies the user who sent the message
- [ ] Bot maintains separate conversation history for each group
- [ ] Bot can handle multiple simultaneous conversations

### Story 2: Personalized Conversation Style
**As a** user
**I want** to set my preferred conversation style
**So that** the bot responds in a way I enjoy

**Acceptance Criteria:**
- [ ] Users can set personal style preference using `/setstyle <style>` command
- [ ] Bot applies user's personal style over group style settings
- [ ] Style preference persists across different groups
- [ ] Users can view available styles using `/style` command
- [ ] Six styles are available: 幽默, 温柔, 傲娇, 严肃, 卖萌, 知性

### Story 3: Group Style Management
**As a** group administrator
**I want** to set a default conversation style for the group
**So that** all members get a consistent experience

**Acceptance Criteria:**
- [ ] Group admins can set group style using `/groupstyle <style>` command
- [ ] Group style applies to users without personal style preference
- [ ] Group style setting persists indefinitely
- [ ] Only group administrators can use `/groupstyle` command

### Story 4: Long-term Memory
**As a** user
**I want** the bot to remember our previous conversations
**So that** I don't have to repeat myself and get more personalized responses

**Acceptance Criteria:**
- [ ] Bot stores conversation history in MySQL database
- [ ] Bot uses vector embeddings for semantic search of past conversations
- [ ] Bot remembers user preferences across different groups
- [ ] Bot can retrieve relevant context from long-term memory
- [ ] User data is stored permanently unless explicitly cleared

### Story 5: Memory Management
**As a** user
**I want** to clear my conversation history
**So that** I can start fresh if needed

**Acceptance Criteria:**
- [ ] Users can clear their memory using `/clear` command
- [ ] `/clear` removes all conversation history (both short-term and long-term) but preserves user preferences (style settings)
- [ ] Confirmation prompt before clearing memory
- [ ] Admins can reset specific users using `/resetuser <user>` command

### Story 6: Conversation Context Awareness
**As a** user
**I want** the bot to remember what we discussed earlier in the conversation
**So that** I can have natural, contextual conversations

**Acceptance Criteria:**
- [ ] Bot maintains short-term memory of current conversation session
- [ ] Bot can reference previous messages in the current session
- [ ] Short-term memory includes recent messages from all participants (in groups)
- [ ] Bot correctly attributes messages to different users in groups

## Functional Requirements

### Core Functionality
- [REQ-001] Bot must connect to Telegram using Bot API token
- [REQ-002] Bot must send messages to XiaoMi MiMo API for response generation
- [REQ-003] Bot must support both group and private chat interactions
- [REQ-004] Bot must only respond to @mentions in group chats
- [REQ-005] Bot must respond to all messages in private chats
- [REQ-006] Bot must identify and track individual users in conversations

### Memory System
- [REQ-007] Bot must implement short-term conversation memory (current session)
- [REQ-008] Bot must implement long-term memory storage in MySQL
- [REQ-009] Bot must use Faiss for vector-based semantic search
- [REQ-009a] Bot must generate vector embeddings using OpenAI text-embedding-ada-002 API (or compatible service)
- [REQ-010] Bot must store conversation history with user and chat context
- [REQ-010a] Bot must query long-term memory for each user message and retrieve top 5 most relevant past conversations using vector search
- [REQ-011] Bot must store user preferences (style, personal info)
- [REQ-012] Bot must maintain separate conversation histories per group
- [REQ-013] Bot must allow user preferences to persist across groups
- [REQ-014] Bot must provide permanent storage of conversation data (conversation data is retained indefinitely unless manually cleared)

### Conversation Style System
- [REQ-015] Bot must support six conversation styles: 幽默搞笑, 温柔体贴, 傲娇, 严肃专业, 卖萌可爱, 知性理性
- [REQ-016] Bot must apply style priority: user personal > group > default
- [REQ-017] Bot must store user style preferences in database
- [REQ-018] Bot must store group style preferences in database
- [REQ-019] Bot must provide '幽默搞笑' (humorous) as default style when no preference is set

### User Commands
- [REQ-020] Bot must support `/start` command for onboarding
- [REQ-021] Bot must support `/help` command showing usage instructions
- [REQ-022] Bot must support `/style` command listing available styles
- [REQ-023] Bot must support `/setstyle <style>` command for personal style setting
- [REQ-024] Bot must support `/clear` command to clear conversation history
- [REQ-025] Bot must require confirmation before clearing memory

### Admin Commands
- [REQ-026] Bot must support `/groupstyle <style>` command for group style setting
- [REQ-027] Bot must restrict `/groupstyle` to group administrators only
- [REQ-028] Bot must support `/resetuser <user>` command to reset user memory
- [REQ-029] Bot must restrict `/resetuser` to group administrators only
- [REQ-030] Bot must support `/stats` command showing usage statistics

### Database & Configuration
- [REQ-031] Bot must read configuration from `.env` file
- [REQ-032] Bot must auto-create database tables on first run
- [REQ-033] Bot must provide SQL scripts for manual table creation
- [REQ-034] Bot must store vector embeddings in MySQL BLOB fields
- [REQ-035] Bot must maintain Faiss index in memory for acceleration
- [REQ-036] Bot must rebuild Faiss index from MySQL on startup

### API Integration
- [REQ-037] Bot must connect to XiaoMi MiMo API (https://api.xiaomimimo.com/v1/chat/completions)
- [REQ-038] Bot must use OpenAI-compatible API format
- [REQ-039] Bot must handle API errors gracefully
- [REQ-040] Bot must implement retry logic for failed API calls

## Non-Functional Requirements

### Performance
- [NFR-001] Bot must respond to user messages within 5 seconds under normal conditions
- [NFR-002] Bot must handle at least 10 concurrent conversations without degradation
- [NFR-003] Vector search must return results within 1 second for up to 10,000 stored vectors
- [NFR-004] Database queries must be optimized with appropriate indexes

### Security
- [NFR-005] Bot must store sensitive credentials (API keys, tokens) in `.env` file
- [NFR-006] Bot must not expose API keys or database credentials in logs
- [NFR-007] Bot must validate all user inputs to prevent SQL injection
- [NFR-008] Bot must sanitize user messages before API calls
- [NFR-009] `.env` and `.venv` directories must be excluded from git

### Reliability
- [NFR-010] Bot must handle network failures gracefully
- [NFR-011] Bot must implement automatic reconnection to Telegram API
- [NFR-012] Bot must log errors for troubleshooting
- [NFR-013] Bot must maintain data consistency during concurrent operations

### Maintainability
- [NFR-014] Code must follow PEP 8 style guide and pass pylint with minimum score of 8.0/10
- [NFR-015] Functions must be focused and single-purpose
- [NFR-016] Code must use meaningful variable and function names
- [NFR-017] Database schema must support future migrations using Alembic or custom migration scripts

### Scalability
- [NFR-018] Database schema must support increasing user base
- [NFR-019] Faiss index must be rebuilt on startup and when accumulated new vectors exceed 1000 entries
- [NFR-020] Code must support adding new conversation styles without major refactoring

## Acceptance Criteria (Test Cases)

### Core Functionality Tests
- [TC-001] Send message to bot in private chat → receive response
- [TC-002] Send message without @mention in group → bot does not respond
- [TC-003] Send @mention to bot in group → bot responds
- [TC-004] Multiple users in group interact with bot → responses address correct users
- [TC-005] Bot handles simultaneous messages from different chats

### Memory System Tests
- [TC-006] User has conversation → references previous message → bot remembers context
- [TC-007] User sets preference in group A → user interacts in group B → preference persists
- [TC-008] New user interacts → bot has no memory of user → creates new profile
- [TC-009] User clears memory → previous context is forgotten → fresh conversation starts
- [TC-010] Vector search returns relevant past conversations

### Conversation Style Tests
- [TC-011] User sets style to "幽默" → bot responds with humorous tone
- [TC-012] Admin sets group style to "严肃" → user without personal style gets serious responses
- [TC-013] User has personal style "温柔" + group style "严肃" → personal style takes priority
- [TC-014] User lists styles → all six styles are displayed
- [TC-015] Invalid style is set → bot shows error message with valid options

### Command Tests
- [TC-016] New user sends `/start` → bot welcomes and shows basic commands
- [TC-017] User sends `/help` → bot shows all available commands
- [TC-018] User sends `/style` → bot lists all available styles
- [TC-019] User sends `/setstyle 傲娇` → bot confirms style change
- [TC-020] User sends `/clear` → bot asks for confirmation
- [TC-021] User confirms `/clear` → conversation memory is deleted
- [TC-022] Non-admin sends `/groupstyle 严肃` → bot shows permission error
- [TC-023] Admin sends `/groupstyle 严肃` → group style is updated
- [TC-024] Admin sends `/resetuser @user` → user memory is cleared
- [TC-025] Admin sends `/stats` → bot shows usage statistics

### Database Tests
- [TC-026] Bot runs for first time → tables are created automatically
- [TC-027] Manual SQL script is executed → tables are created correctly
- [TC-028] User data is saved → persists across bot restarts
- [TC-029] Vector data is stored → can be retrieved from MySQL
- [TC-030] Faiss index is rebuilt on startup → search works correctly

### Error Handling Tests
- [TC-031] XiaoMi MiMo API is down → bot responds with error message
- [TC-032] Database connection fails → bot logs error and attempts reconnection
- [TC-033] Invalid command is sent → bot shows usage hint
- [TC-034] Malformed user input → bot handles gracefully without crashing
- [TC-035] Network timeout occurs → bot retries API call

### Edge Case Tests
- [TC-036] User sends very long message (>4000 chars) → bot handles appropriately
- [TC-037] User sends special characters and emoji → bot processes correctly
- [TC-038] Bot is added to new group → bot initializes group-specific data
- [TC-039] Bot is removed from group → group data is preserved
- [TC-040] Same user in multiple groups → conversations remain independent

## Edge Cases

### Message Handling
- **Empty message**: Bot ignores or asks for input
- **Very long message**: Messages >4000 characters are split into chunks at sentence boundaries, each sent to API separately, with bot synthesizing combined response
- **Special characters/emoji**: Sanitize and preserve meaning
- **Rapid message flooding**: Implement rate limiting - maximum 20 messages per user per 60 seconds, with temporary ban for violations
- **Edit/deleted messages**: Handle Telegram update events gracefully
- **Bot is mentioned multiple times in one message**: Process once and respond

### User Management
- **User leaves and rejoins group**: Preserve or reset user data (configurable)
- **User changes username**: Update database with new username
- **Bot added to existing group**: Initialize without responding to old messages
- **Bot removed from group**: Keep group data for potential re-add
- **Deleted Telegram accounts**: Handle orphaned user IDs gracefully

### Memory Management
- **Database connection lost**: Reconnect and retry operations
- **Faiss index corruption**: Rebuild from MySQL data
- **Out of memory errors**: Implement graceful degradation
- **Very long conversation history**: Implement pagination or summarization
- **Vector search returns no results**: Fall back to recent messages only

### API Failures
- **XiaoMi MiMo API timeout**: Implement retry with exponential backoff
- **API rate limiting**: Queue requests and delay responses
- **Invalid API response**: Log error and use fallback response
- **Network unavailable**: Cache responses or show error message
- **API key expires**: Support key rotation without restart

### Concurrency Issues
- **Multiple users update same record**: Use database transactions/locking
- **Race conditions in style updates**: Last write wins with timestamp
- **Simultaneous command executions**: Queue processing per user

## Output Examples

### User Interaction Examples

#### Example 1: Private Chat with Style Setting
```
User: /start
Bot: 你好！我是你的聊天助手～ 使用 /help 查看可用命令

User: /style
Bot: 可用风格：
- 幽默搞笑
- 温柔体贴
- 傲娇
- 严肃专业
- 卖萌可爱
- 知性理性

User: /setstyle 傲娇
Bot: 好啦好啦，本小姐知道了～ 已设置为傲娇风格！

User: 你好
Bot: 哼，有事吗？本小姐现在可是很忙的哦～
```

#### Example 2: Group Chat Interaction
```
User A: @bot 今天天气怎么样？
Bot: [幽默风格] 哈哈，我不知道天气，但我知道问我就对了！要不要我给你编一个天气预报？☀️🌧️

User B: 大家好
Bot: [无响应，因为没有@bot]

User B: @bot 你好呀
Bot: [幽默风格] 嘿嘿，你好你好！今天心情怎么样？要不要聊聊天？
```

#### Example 3: Style Priority
```
Group style: 严肃
User A personal style: (not set)
User A: @bot 解释一下什么是人工智能
Bot: [严肃风格] 人工智能（Artificial Intelligence）是计算机科学的一个分支...

User B personal style: 卖萌
User B: @bot 解释一下什么是人工智能
Bot: [卖萌风格] 呐～人工智能就是一种让计算机变聪明的魔法哦～ ✨
```

#### Example 4: Memory Context
```
User: 我叫小明
Bot: 好的，小明！很高兴认识你～

[30 minutes later]

User: 我刚才说我叫什么来着？
Bot: 你刚才说你是小明呀！
```

#### Example 5: Admin Commands
```
Admin: /groupstyle 严肃
Bot: ✅ 群组风格已设置为"严肃专业"

User: @bot 讲个笑话
Bot: [严肃风格] 抱歉，我的功能是提供严肃的对话和帮助。如果您有具体问题，我很乐意为您解答。

Admin: /stats
Bot: 📊 统计信息：
- 总用户数: 127
- 今日消息数: 1,542
- 活跃群组: 8
```

### Database Schema Examples

#### users Table
```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    preferred_style VARCHAR(50) DEFAULT 'default',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX(username)
);
```

#### conversations Table
```sql
CREATE TABLE conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    chat_id BIGINT,
    user_id BIGINT,
    message_text TEXT,
    role ENUM('user', 'assistant', 'system'),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX(chat_id, user_id, timestamp),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

#### conversation_vectors Table
```sql
CREATE TABLE conversation_vectors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT,
    user_id BIGINT,
    chat_id BIGINT,
    message_text TEXT,
    embedding BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX(user_id, chat_id),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

#### group_settings Table
```sql
CREATE TABLE group_settings (
    chat_id BIGINT PRIMARY KEY,
    group_style VARCHAR(50) DEFAULT 'default',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### user_preferences Table
```sql
CREATE TABLE user_preferences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    preference_key VARCHAR(100),
    preference_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY(user_id, preference_key),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### API Request/Response Examples

#### XiaoMi MiMo API Request
```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "你是一个幽默搞笑的聊天助手，用轻松诙谐的语气回应。"
    },
    {
      "role": "user",
      "content": "你好"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

#### API Response
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "哈哈，你好你好！今天心情怎么样？要不要聊聊天？😄"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 30,
    "total_tokens": 50
  }
}
```

### .env Configuration Example
```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here

# XiaoMi MiMo API Configuration
MIMO_API_KEY=your_api_key_here
MIMO_BASE_URL=https://api.xiaomimimo.com/v1/chat/completions

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=telegram_chatbot
DB_USER=your_username
DB_PASSWORD=your_password

# Bot Configuration
DEFAULT_STYLE=幽默
MAX_CONVERSATION_HISTORY=50
VECTOR_SEARCH_RESULTS=5
API_TIMEOUT=30
MAX_RETRIES=3

# Faiss Configuration
FAISS_INDEX_PATH=./data/faiss.index
INDEX_DIMENSION=1536
```

## Out of Scope

### Features Not Included in Initial Release
- Voice message support (transcription or voice responses)
- Image generation or analysis
- File sharing or document processing
- Integration with other platforms (Discord, Slack, etc.)
- Multi-language support (initially Chinese only)
- User authentication or account linking
- Payment processing or premium features
- Web dashboard or admin panel
- Bot analytics beyond basic `/stats` command
- Scheduled messages or reminders
- Chat export functionality
- End-to-end encryption
- Plugin system or extensibility
- Conversation summarization
- Sentiment analysis
- Explicit content filtering
- Rate limiting beyond basic flood control
- A/B testing for conversation styles
- Multi-bot orchestration
- Interactive keyboards or inline buttons
- Telegram Games integration
- Location-based features

### Technical Exclusions
- Docker containerization (local deployment only)
- Cloud deployment configuration
- CI/CD pipeline setup
- Load balancing or horizontal scaling
- Caching layer (Redis, etc.)
- Message queue system
- Advanced monitoring and alerting
- Automated backup strategies
- Disaster recovery procedures
- Database sharding or replication
- GraphQL API
- REST API for third-party integration

### Future Considerations
These features may be considered for future releases but are not part of the current specification:
- Support for additional LLM providers
- Fine-tuning models on conversation data
- Advanced context window management
- Conversation branching or forking
- Collaborative conversations between multiple users
- Bot personality learning from user feedback
- Integration with external knowledge bases
- Real-time translation
- Accessibility features (screen reader support, etc.)
