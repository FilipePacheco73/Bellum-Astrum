# 🤖 Bellum Astrum - AI Agents Documentation

The AI Agents system provides intelligent autonomous players that compete in Bellum Astrum using Large Language Models (LLMs). These agents make strategic decisions, learn from experience, and compete 24/7 without human intervention.

---

## 🛠️ Technology Stack

- **AI Framework**: Local LLMs via HuggingFace Transformers with CUDA optimization
- **Decision Engine**: Strategic prompts with personality-based behavior patterns
- **Memory System**: SQLite-based learning with JSON fallback for persistence
- **Logging**: Dual logging system (debug + AI decisions tracking)
- **Match System**: Automated tournament and training orchestration
- **Models**: TinyLlama-1.1B-Chat-v1.0 with 4-bit quantization for efficiency
- **GPU Support**: CUDA acceleration with memory optimization for RTX cards

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
Strategy: Constant attacks with high-risk, high-reward approach
Focus: Frequent battles, rapid growth through combat
Formation: AGGRESSIVE
Behavior: Minimal work, maximum battle engagement
LLM Model: TinyLlama-1.1B-Chat-v1.0 (temperature: 0.8, high creativity)
```

### AI_Guardian (Defensive) 
Strategic behavior focused on survival and sustainable growth:
```yaml
Strategy: Survival-first with sustainable resource accumulation
Focus: Resource building, selective battle engagement
Formation: DEFENSIVE  
Behavior: Heavy work focus, safe battle choices
LLM Model: TinyLlama-1.1B-Chat-v1.0 (temperature: 0.4, conservative decisions)
```

### AI_Tactician (Strategic)
Strategic behavior focused on calculated decisions and optimization:
```yaml
Strategy: Data-driven analysis with calculated risk management
Focus: Resource optimization and strategic timing
Formation: Adaptive based on game context
Behavior: Balanced work-battle ratio with strategic planning
LLM Model: TinyLlama-1.1B-Chat-v1.0 (temperature: 0.6, balanced approach)
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
- API connections and authentication
- Technical errors and warnings  
- System performance and debug information
- Automatic rotation (10MB, 5 backups)

### AI Decisions Log (`ai_decisions.log`)
Detailed AI behavior tracking and analysis:
```
2025-08-12 21:09:47 | Round 002 | [AI_Warrior] | DECISION_MAKING | credits: 1500 | energy: 80
2025-08-12 21:09:48 | Round 002 | [AI_Warrior] | TOOL_USED: work → SUCCESS | param_sector: residential | result_credits_earned: 200
```
- Detailed decision logs for each AI agent
- Tools used with specific parameters
- Action results and consequences
- Structured format for performance analysis

---

## 🧠 Memory System

### File-Based Learning Architecture
- **Format**: JSON per agent (decisions and performance data)
- **Location**: `memories/{agent_name}_decisions.json`
- **Content**: Complete action history, reasoning, and performance metrics

### Memory Entry Example
```json
{
  "timestamp": "2025-08-27T21:08:22.829954",
  "round_number": 1,
  "action": "get_my_status",
  "reason": "First round mandatory status check",
  "success": true,
  "input_tokens": 0,
  "output_tokens": 0,
  "ai_reasoning": "Mandatory first round status check"
}
```

### Memory Query Functions
- `get_recent_actions()`: Recent actions by time period and type
- `get_action_success_rate()`: Success rate per action type
- `get_average_credits_per_work()`: Average work earnings analysis
- `get_opponent_profile()`: Detailed opponent analysis and threat assessment
- `get_winnable_opponents()`: List of opponents with win probability
- `get_memory_summary()`: Comprehensive decision-making context summary
- `cleanup_old_memories()`: Memory management and cleanup

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
- **CUDA Support**: Automatic GPU detection and utilization
- **Memory Management**: 4-bit quantization reduces VRAM usage by ~75%
- **Flash Attention**: Enhanced attention mechanism for faster inference
- **Model Caching**: Local model cache prevents repeated downloads

### Resource Usage
- **Memory Footprint**: ~550MB VRAM per agent (with quantization)
- **CPU Usage**: Minimal when using GPU acceleration
- **Storage**: ~2.2GB per cached model, ~1MB per agent memory file

### Configuration Options
```python
# GPU optimization settings
GLOBAL_CONFIG = {
    "device": "cuda",  # Auto-detect GPU
    "max_memory_per_gpu": "5GB",  # Optimized for RTX 4050
    "torch_dtype": torch.float16,  # Half precision
    "load_in_4bit": True,  # Quantization
    "attn_implementation": "flash_attention_2"
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
grep "AI_Warrior" logs/ai_decisions.log

# Analyze action patterns
grep "action.*work" logs/ai_decisions.log

# Check success/failure rates
grep -E "success.*true|success.*false" logs/ai_decisions.log

# Monitor token usage
grep "tokens" logs/ai_decisions.log
```

---

## 🔧 Development

### Adding New AI Personality
1. Create behavior prompts in `prompts/`
2. Define personality in `config/ai_personalities.py`
3. Configure agent in `run_ai_match.py`

### Adding New Tools
1. Implement in `core/tool_caller.py`
2. Add appropriate logging calls
3. Document parameters and expected results

### Debugging and Troubleshooting
- Check `logs/debug_*.log` for technical issues
- Analyze `logs/ai_decisions_*.log` for AI behavior patterns
- Review `memories/` for learning data and decision history

---

*This AI system demonstrates autonomous gameplay, machine learning integration, and strategic decision making in a competitive gaming environment.*

---

## 🔗 Navigation

- **← [Project Overview](../README.md)** - Main project documentation and overview
- **⚙️ [Backend Documentation](../backend/README.md)** - FastAPI backend and API endpoints
- **🗄️ [Database Documentation](../database/README.md)** - Database schema, models, and setup
- **🎨 [Frontend Documentation](../frontend/README.md)** - React frontend and UI components

---