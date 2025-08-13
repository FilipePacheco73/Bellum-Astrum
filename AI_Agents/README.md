# 🤖 Bellum Astrum - AI Agents Documentation

The AI Agents system provides autonomous intelligent players that compete in Bellum Astrum using Large Language Models (LLMs). These AI agents make strategic decisions, learn from experience, and compete 24/7 without human intervention.

---

## 🛠️ Tech Stack

- **AI Framework**: Local LLMs via HuggingFace Transformers
- **Decision Engine**: Strategic prompts with personality-based behavior
- **Memory System**: File-based learning with JSON Lines format
- **Logging**: Dual logging system (debug + AI decisions)
- **Match System**: Automated tournament and training orchestration
- **Models**: DialoGPT, Mistral 7B, TinyLlama for different personalities

---

## 🏗️ Project Structure

```
AI_Agents/
├── .env                        # Environment variables (AI credentials)
├── .env.example               # Environment template
├── run_ai_match.py            # Main script to execute AI matches
├── example_logging.py         # Logging system usage examples
├── config/                    # Configuration modules
│   ├── env_config.py          # Environment and credentials configuration
│   ├── llm_config.py          # LLM models configuration
│   ├── logging_config.py      # Dual logging system setup
│   └── ai_personalities.py    # AI personality definitions
├── core/                      # Core AI system modules
│   ├── ai_agent.py            # Base AI agent class
│   ├── llm_manager.py         # LLM model management
│   ├── tool_caller.py         # Game API interface
│   ├── match_orchestrator.py  # Match management and orchestration
│   └── file_memory.py         # File-based memory system
├── prompts/                   # AI behavior prompts
│   ├── system_prompts.py      # Base game explanation prompts
│   ├── aggressive_prompts.py  # Warrior AI prompts
│   ├── defensive_prompts.py   # Guardian AI prompts
│   └── tactical_prompts.py    # Tactician AI prompts
├── logs/                      # Dual logging system output
│   ├── debug_YYYYMMDD.log     # Technical debug logs
│   ├── ai_decisions_YYYYMMDD.log # AI decision tracking logs
│   └── example_ai_decisions.log # Log format examples
├── memories/                  # AI learning data (auto-generated)
│   ├── AI_Warrior_Test_memory.jsonl
│   ├── AI_Guardian_Test_memory.jsonl
│   └── AI_Tactician_Test_memory.jsonl
└── models_cache/              # Downloaded LLM models cache
    ├── models--distilgpt2/
    └── models--gpt2/
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
LLM Model: DialoGPT-medium (fast responses for quick decisions)
```

### AI_Guardian (Defensive) 
Strategic behavior focused on survival and sustainable growth:
```yaml
Strategy: Survival-first with sustainable resource accumulation
Focus: Resource building, selective battle engagement
Formation: DEFENSIVE  
Behavior: Heavy work focus, safe battle choices
LLM Model: TinyLlama (conservative decision making)
```

### AI_Tactician (Strategic)
Strategic behavior focused on calculated decisions and optimization:
```yaml
Strategy: Data-driven analysis with calculated risk management
Focus: Resource optimization and strategic timing
Formation: Adaptive based on game context
Behavior: Balanced work-battle ratio with strategic planning
LLM Model: Mistral 7B (complex analysis capabilities)
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
tail -f logs/debug_YYYYMMDD.log

# AI decision tracking logs
tail -f logs/ai_decisions_YYYYMMDD.log
```

---

## 📊 Dual Logging System

### Debug Log (`debug_YYYYMMDD.log`)
Technical system monitoring and troubleshooting:
- API connections and authentication
- Technical errors and warnings  
- System performance and debug information
- Automatic rotation (10MB, 5 backups)

### AI Decisions Log (`ai_decisions_YYYYMMDD.log`)
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
- **Format**: JSON Lines (.jsonl) per agent
- **Location**: `memories/{agent_name}_memory.jsonl`
- **Content**: Complete action history and learning data

### Memory Entry Example
```json
{
  "timestamp": "2025-08-12T21:09:48",
  "round_number": 2,
  "tool_name": "work",
  "tool_params": {"sector": "residential"},
  "game_state_before": {"credits": 1500, "energy": 80},
  "game_state_after": {"credits": 1700, "energy": 60},
  "success": true,
  "result_data": {"credits_earned": 200, "energy_consumed": 20},
  "reasoning": "Need more credits for ship purchase"
}
```

### Memory Query Functions
- `get_recent_actions()`: Recent actions by time period
- `get_tool_success_rate()`: Success rate per tool type
- `get_average_credits_per_work()`: Average work earnings
- `get_battle_performance()`: Battle statistics and performance
- `get_memory_summary()`: Decision-making context summary

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

## 📈 Analysis and Monitoring

### Real-time Statistics
- Performance metrics per agent
- Tool success rates and efficiency
- Credit and XP progression tracking
- Performance rankings and comparisons

### Log Analysis Examples
```bash
# Filter decisions from specific agent
grep "AI_Warrior" logs/ai_decisions_*.log

# Analyze tool usage patterns
grep "TOOL_USED" logs/ai_decisions_*.log | grep "work"

# Check success/failure rates
grep "SUCCESS\|FAILED" logs/ai_decisions_*.log
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
