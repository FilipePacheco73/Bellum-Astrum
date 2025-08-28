# 🤖 Bellum Astrum - AI Agents Documentation

The AI Agents system provides intelligent autonomous players that compete in Bellum Astrum using Large Language Models (LLMs). These agents make strategic decisions, learn from experience, and compet## 📊 Analysis and Monitoring

### Real-time Statistics
- Performance metrics per agent with token consumption tracking
- Tool success rates and efficiency analysis
- Credit and XP progression tracking with detailed logging
- Performance rankings and comparisons
- Fallback decision frequency monitoring for model performance assessmentwithout human intervention.

---

## 🛠️ Technology Stack

- **AI Framework**: Local LLMs via HuggingFace Transformers with CUDA optimization
- **Decision Engine**: Strategic prompts with simplified personality-based behavior patterns
- **Memory System**: File-based JSON memory storage with detailed decision tracking
- **Logging**: Advanced dual logging system (debug + AI decisions tracking with token metrics)
- **Match System**: Automated tournament and training orchestration with real-time monitoring
- **Models**: TinyLlama-1.1B-Chat-v1.0 with 4-bit quantization for efficiency (shared across all agents)
- **GPU Support**: CUDA acceleration with memory optimization and smart prompt truncation

---

## 🏗️ Project Structure

```
AI_Agents/
├── .env                        # Environment variables (AI credentials)
├── .env.example               # Environment template
├── run_ai_match.py            # Main script to run AI matches
├── config/                    # Configuration modules
│   ├── env_config.py          # Environment and credentials configuration
│   ├── llm_config.py          # LLM models configuration
│   └── logging_config.py      # Dual logging system
├── core/                      # Core AI system modules
│   ├── ai_agent.py            # Base AI agent class
│   ├── ai_user_manager.py     # Automatic AI user management
│   ├── llm_manager.py         # LLM models management
│   ├── tool_caller.py         # Game API interface
│   ├── match_orchestrator.py  # Match management and orchestration
│   ├── memory_manager.py      # Memory management system
│   └── file_memory.py         # File-based memory system
├── prompts/                   # AI behavior prompts
│   ├── system_prompts.py      # Base game explanation prompts
│   ├── decision_prompts.py    # Decision-making prompts
│   └── personality_prompts.py # Personality-based behavior prompts
├── logs/                      # Dual logging system output
│   ├── debug.log              # Technical debug logs
│   └── ai_decisions.log       # AI decision tracking logs
├── memories/                  # AI learning data (auto-generated)
│   ├── AI_Warrior_Test_decisions.json
│   ├── AI_Guardian_Test_decisions.json
│   └── AI_Tactician_Test_decisions.json
└── models_cache/              # Downloaded LLM models cache
    └── models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/
```

---

## 🤖 AI Personalities

### AI_Warrior (Aggressive)
Strategic behavior focused on constant aggression and high-risk actions:
```yaml
Strategy: Combat first! High risk, high reward approach
Focus: Ships→BATTLE, No ships→ACTIVATE, Low credits→WORK, Damaged→REPAIR
Formation: AGGRESSIVE (always)
Behavior: Bold and direct combat engagement
LLM Model: TinyLlama-1.1B-Chat-v1.0 (shared model, aggressive personality prompts)
```

### AI_Guardian (Defensive) 
Strategic behavior focused on survival and sustainable growth:
```yaml
Strategy: Safety first! Calculated moves only
Focus: Damaged→REPAIR, No credits→WORK, Ready ships→BATTLE (safe)
Formation: DEFENSIVE (always)
Behavior: Prudent and calculated resource management
LLM Model: TinyLlama-1.1B-Chat-v1.0 (shared model, defensive personality prompts)
```

### AI_Tactician (Strategic)
Strategic behavior focused on calculated decisions and optimization:
```yaml
Strategy: Strategy first! Analyze then act
Focus: Assess→REPAIR if needed→WORK for credits→BATTLE when ready
Formation: TACTICAL (always)
Behavior: Smart and adaptable strategic planning
LLM Model: TinyLlama-1.1B-Chat-v1.0 (shared model, tactical personality prompts)
```

---

## 🛠️ Available Tools

### Battle System
- `battle(opponent_id, formation, ships)` → Engage in combat
- `activate_ship(ship_number)` → Activate ship for battle
- `deactivate_ship(ship_number)` → Deactivate ship

### Economy System  
- `work(sector)` → Work to earn credits
- `buy_ship(ship_id)` → Purchase new ship
- `repair_ship(ship_number)` → Repair damaged ship

### Information System
- `get_user_status()` → Current player status
- `list_opponents()` → Available opponents list
- `get_fleet_status()` → Current fleet status

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure AI agent credentials (copy from .env.example)
cp .env.example .env
# Edit .env with your AI agent account credentials
```

### 2. Run Training Match
```bash
# Execute training match between AI agents for 30 rounds
python run_ai_match.py
```

### 3. Monitor Real-time Activity
```bash
# Technical debug logs
tail -f logs/debug.log

# AI decision tracking logs
tail -f logs/ai_decisions.log
```

---

## 📊 Dual Logging System

### Debug Log (`debug.log`)
Technical system monitoring and troubleshooting:
- API connections and authentication status
- Technical errors, warnings, and system diagnostics
- System performance metrics and debug information
- Automatic log rotation (10MB files, 5 backups with UTF-8 encoding)

### AI Decisions Log (`ai_decisions.log`)
Detailed AI behavior tracking and performance analysis:
```
2025-08-28 15:32:15 | Round 003 | [AI_Warrior_Test] | ACTION: perform_work | SUCCESS | tokens: 247→12
2025-08-28 15:32:20 | Round 004 | [AI_Guardian_Test] | ACTION: get_my_status | SUCCESS | credits: 1200
```
- Comprehensive decision logs for each AI agent with token usage metrics
- Tools used with specific parameters and success/failure tracking
- Action results, reasoning, and performance consequences
- Structured format optimized for performance analysis and learning
- Automatic log rotation (10MB files, 10 backups with UTF-8 encoding)

---

## 🧠 Memory System

### File-Based Learning Architecture
- **Format**: JSON per agent with comprehensive decision and token tracking
- **Location**: `memories/{agent_name}_decisions.json`
- **Content**: Complete action history, AI reasoning, token metrics, and performance data
- **Persistence**: Automatic storage with error recovery and corrupted entry handling

### Memory Entry Example
```json
{
  "timestamp": "2025-08-28T15:30:45.123456",
  "round_number": 5,
  "action": "engage_battle",
  "reason": "found combat opportunity with 2 ships vs WeakOpponent",
  "success": true,
  "input_tokens": 287,
  "output_tokens": 15,
  "ai_reasoning": "Analyzing game state: sufficient credits (1500), active ships available (2), opponent found with favorable matchup. Strategic decision: engage in combat for XP and credit gains."
}
```

### Memory Query Functions
- `get_recent_decisions()`: Recent decisions with filtering by round count and success status
- `get_memory_summary()`: Formatted summary for AI prompt inclusion with token metrics
- `store_decision()`: Enhanced decision storage with detailed AI reasoning and fallback information
- `cleanup_old_entries()`: Intelligent memory management to prevent file bloat
- `cleanup_empty_files()`: Automatic removal of unused memory files

---

## 🏟️ Match System

### Match Types
Strategic AI competition formats:
- **TRAINING**: Limited-round training matches with learning focus
- **CONTINUOUS**: Ongoing matches until specific conditions
- **TOURNAMENT**: Elimination-style tournaments between AI agents
- **FREE_FOR_ALL**: All agents compete simultaneously

### Match Configuration
```python
config = MatchConfig(
    match_type=MatchType.TRAINING,
    max_rounds=30,
    round_delay=2.0,  # seconds between rounds
    enable_learning=True,  # activate memory system
    save_logs=True  # save detailed logs
)
```

---

## ⚡ Performance & Optimization

### GPU Acceleration
- **CUDA Support**: Automatic GPU detection with CPU fallback capability
- **Memory Management**: 4-bit quantization reduces VRAM usage by ~75%
- **Model Sharing**: Single TinyLlama instance shared across all agent types
- **Flash Attention**: Enhanced attention mechanism for faster inference
- **Model Caching**: Local model cache prevents repeated downloads
- **Smart Prompt Truncation**: Preserves critical instructions when managing context limits

### Resource Usage
- **Memory Footprint**: ~550MB VRAM per model instance (with 4-bit quantization)
- **Model Sharing**: Single TinyLlama instance shared across all agents reduces total VRAM to ~550MB
- **CPU Usage**: Minimal when using GPU acceleration
- **Storage**: ~2.2GB per cached model, ~1MB per agent memory file
- **Token Efficiency**: Smart prompt truncation preserves critical instructions while managing context limits

### Configuration Options
```python
# GPU optimization settings with smart prompt management
GLOBAL_CONFIG = {
    "device": "cuda",  # Auto-detect GPU with fallback to CPU
    "max_memory_per_gpu": "5GB",  # Optimized for RTX 4050 and similar cards
    "torch_dtype": torch.float16,  # Half precision for memory efficiency
    "load_in_4bit": True,  # 4-bit quantization reduces VRAM by ~75%
    "attn_implementation": "flash_attention_2",  # Enhanced attention mechanism
    "model_sharing": True,  # Single model instance shared across agents
    "smart_truncation": True  # Preserve critical instructions when truncating prompts
}
```

---

## � Analysis and Monitoring

### Real-time Statistics
- Performance metrics per agent
- Tool success rates and efficiency
- Credit and XP progression tracking
- Performance rankings and comparisons

### Log Analysis Examples
```bash
# Filter decisions from specific agent
grep "AI_Warrior_Test" logs/ai_decisions.log

# Analyze action patterns and success rates
grep "ACTION.*perform_work" logs/ai_decisions.log

# Monitor token usage patterns across agents
grep "tokens.*→" logs/ai_decisions.log

# Check AI reasoning and decision quality
grep "ai_reasoning" memories/AI_*.json

# Track fallback decision usage
grep "fallback" logs/ai_decisions.log
```

---

## 🔧 Development

### Decision Making System Architecture
The AI agents use a streamlined prompt system optimized for small language models:

- **System Prompts**: Core game mechanics and response format instructions
- **Personality Prompts**: Concise behavior patterns specific to each agent type  
- **Decision Templates**: Standardized format with mandatory ACTION and EXPLANATION fields
- **Memory Integration**: Recent decisions included as context for learning

#### Enhanced Decision Processing
- **Token Tracking**: Comprehensive monitoring of input/output token usage
- **Smart Truncation**: Intelligent prompt shortening that preserves critical instructions
- **Fallback System**: Robust decision-making when LLM fails with detailed reasoning
- **Format Parsing**: Advanced parsing of AI responses with fallback keyword detection
- **Error Recovery**: Graceful handling of malformed responses and API failures

### Adding New AI Personality
1. Create behavior prompts in `prompts/`
2. Define personality in `config/ai_personalities.py`
3. Configure agent in `run_ai_match.py`

### Adding New Tools
1. Implement in `core/tool_caller.py`
2. Add appropriate logging calls
3. Document parameters and expected results

### Debugging and Troubleshooting
- Check `logs/debug.log` for technical issues and system errors
- Analyze `logs/ai_decisions.log` for AI behavior patterns and token usage
- Review `memories/{agent_name}_decisions.json` for learning data and decision history
- Monitor token consumption patterns to optimize prompt efficiency
- Use fallback decision logs to identify model performance issues

---

*This AI system demonstrates autonomous gameplay, machine learning integration, and strategic decision making in a competitive gaming environment.*

---

## 🔗 Navigation

- **← [Project Overview](../README.md)** - Main project documentation and overview
- **⚙️ [Backend Documentation](../backend/README.md)** - FastAPI backend and API endpoints
- **🗄️ [Database Documentation](../database/README.md)** - Database schema, models, and setup
- **🎨 [Frontend Documentation](../frontend/README.md)** - React frontend and UI components

---