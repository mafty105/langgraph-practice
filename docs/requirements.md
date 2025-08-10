# Email Assistant CLI Specification

## 1. Overview

### 1.1 Purpose
Email checking and improvement tool for IT marketing professionals (2-5 years experience, team leaders). Designed for gradual development with eventual integration into MA (Marketing Automation) tools.

### 1.2 Target Users
- IT marketing professionals
- Experience level: 2-5 years or team leader level
- Use case: Improving quality of email marketing campaigns

### 1.3 Technical Requirements
- **Architecture**: LangGraph
- **LLM**: OpenAI API or Gemini
- **Development Language**: Python
- **Interface**: CLI (planned for future API conversion)
- **Offline Operation**: Not required
- **Privacy**: Not deeply considered at sample stage

### 1.4 Localization Requirements
- **Target Market**: Japanese users
- **Input/Output Language**: Japanese
- **Internal Processing**: LLM prompts can think in English or Japanese but must output in Japanese
- **User Interface**: All CLI messages, error messages, and help text in Japanese
- **Configuration Files**: Support Japanese comments and values

## 2. Functional Requirements

### 2.1 Input Specification
```bash
# Text file
email-check --file "campaign.txt"

# Direct text input
email-check --text "件名: 新機能リリースのお知らせ..."

# Existing email improvement
email-check --file "existing.txt" --mode improve
```

### 2.2 Output Specification
```
📧 メール分析結果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 総合スコア: 82/100

⚠️ 問題点:
• 件名が長すぎます（現在32文字、推奨25文字以下）
• CTAボタンの文言が曖昧です
• セグメント（企業CTO）に対して技術的詳細が不足

💡 改善案:
• 件名: "新機能リリース" → "セキュリティ強化機能リリース"
• CTA: "詳細はこちら" → "技術仕様を確認する"
• 技術的なベネフィットを2-3行追加推奨

📝 書き直し案生成: [y/n]
```

## 3. Phase-based Feature Specification

### Phase 1: Basic Concepts (LangGraph Fundamentals)

#### 3.1.1 Command Specification
```bash
email-check --file <filename> [--type <email_type>]

# Parameters
--type: business | marketing | apology | report
--output: simple | detailed
--format: text | json
```

#### 3.1.2 Check Items
- **Keigo/Polite Language**: Appropriateness, consistency
- **Basic Structure**: Subject line, greeting, body, closing verification
- **Character Count**: Appropriate length (subject ≤25 chars, body 500-800 chars recommended)

#### 3.1.3 Workflow
```
[Email Input] → [Type Classification Node] → [Basic Check Node] → [Result Output Node]
```

### Phase 2: Conditional Branching and Parallel Processing

#### 3.2.1 Command Specification
```bash
email-check --file <filename> --type marketing --segment <segment>
email-check --file <filename> --detailed
email-check --file <filename> --parallel

# New Parameters
--segment: enterprise | startup | smb | individual
--industry: fintech | healthcare | education | ecommerce
--parallel: Enable parallel processing
```

#### 3.2.2 Additional Check Items
- **Marketing-Specific**:
  - CTA (Call To Action) effectiveness
  - Subject line open rate optimization
  - Segment-specific expression adjustment
- **Typos/Grammar**: Automatic detection and correction suggestions
- **Tone**: Consistency, brand tone compliance

#### 3.2.3 Workflow
```
[Email Input]
    ↓
[Type Classification Node] → Business? Marketing?
    ↓
┌─ Marketing Flow ─────┐    ┌─ Business Flow ──┐
│ [CTA Analysis Node]  │    │ [Keigo Analysis] │
│ [Segment Analysis]   │    │ [Structure Check]│
└─────────────────────┘    └──────────────────┘
    ↓                        ↓
[Result Integration Node] ← Merge parallel execution results
    ↓
[Improvement Suggestion Node]
```

### Phase 3: Agent Collaboration and Dynamic Adjustment

#### 3.3.1 Command Specification
```bash
email-check --file <filename> --collaborative
email-check --file <filename> --iterate --max-rounds <number>
email-check --file <filename> --save-checkpoint <name>
email-check --resume <checkpoint_name> [--modify-params]

# New Parameters
--collaborative: Enable inter-agent collaboration
--iterate: Iterative improvement mode
--max-rounds: Maximum improvement rounds (default 3)
--save-checkpoint: Checkpoint name
--resume: Resume from checkpoint
```

#### 3.3.2 Additional Check Items
- **Legal Risk**: Personal Information Protection Law, Fair Labeling Act compliance
- **Business Etiquette**: Delivery time, unsubscribe link verification
- **Spam Filter**: Avoidance probability check

#### 3.3.3 Workflow
```
[Email Input]
    ↓
[Parallel Analysis: Multiple Specialist Agents]
├─ [Keigo Agent] ─────┐
├─ [Marketing Agent] ─┼─ [Coordination Meeting Node] → Conflict resolution
├─ [Legal Agent] ─────┘           ↓
└─ [Structure Agent] ─────────────┘
    ↓
🛑 Checkpoint: "analysis-complete"
    ↓
[Improvement Generation Node]
    ↓
[Quality Evaluation Node] → Retry if below threshold
    ↓
🛑 Checkpoint: "improvement-complete"
    ↓
[Final Recommendation Node]
```

#### 3.3.4 Checkpoint Functionality
```bash
# Checkpoint List
- "basic-complete": After basic checks completed
- "analysis-complete": After specialist analysis completed
- "improvement-complete": After improvement suggestions generated

# Usage Examples
email-check --file email.txt --save-checkpoint "after-analysis"
# → Pause after analysis completion

email-check --resume "after-analysis" --segment startup
# → Resume with changed segment
```

### Phase 4: Learning & Customization Features

#### 3.4.1 Command Specification
```bash
email-check --file <filename> --rules <rules_file>
email-check --file <filename> --learn-from-feedback
email-check --file <filename> --generate-variants <number>
email-check --profile <profile_name> --save-as-default

# New Parameters
--rules: Custom rules file (YAML)
--learn-from-feedback: Feedback learning mode
--generate-variants: Number of A/B test variations
--profile: User profile name
```

#### 3.4.2 Custom Rules Configuration Example
```yaml
# company-style.yaml
company_profile:
  name: "テックスタートアップA社"
  tone: "フレンドリーだが専門的"
  industry: "SaaS"

target_segments:
  enterprise_cto:
    tone: "formal"
    technical_level: "high"
    pain_points: ["セキュリティ", "スケーラビリティ"]

custom_rules:
  - rule: "製品名表記統一"
    pattern: "○○○"
    required: true
  - rule: "価格表示"
    format: "税込み表示必須"
  - rule: "競合言及"
    action: "禁止"

learning_preferences:
  feedback_weight: 0.8
  historical_data_weight: 0.6
  industry_benchmark_weight: 0.4
```

#### 3.4.3 Additional Features
- **Custom Rule Settings**: Company-specific notation rules, brand guidelines
- **User Preference Learning**: Learning past correction patterns, approval tendencies
- **A/B Test Support**: Automatic generation of multiple variations
- **Effect Prediction**: Open rate and click rate prediction (optional)

## 4. Technical Specification

### 4.1 Architecture
```
src/
└── email_assistant/
    ├── cli/              # CLI Interface
    ├── core/             # Core Logic & Models
    ├── agents/           # LangGraph Agents
    ├── graph/            # Workflow Definitions
    ├── tools/            # External Tool Integration
    ├── config/           # Configuration Management
    └── storage/          # Checkpoint & Learning Data
```

### 4.2 State Management
```python
class EmailState(TypedDict):
    # Input
    original_text: str
    email_type: str
    segment: Optional[str]
    custom_rules: Optional[Dict]

    # Processing State
    current_checkpoint: str
    processing_history: List[str]

    # Check Results
    basic_checks: Dict[str, Any]
    advanced_checks: Dict[str, Any]
    agent_results: Dict[str, Any]

    # Output
    final_score: int
    issues: List[str]
    suggestions: List[str]
    variants: Optional[List[str]]
```

### 4.3 External Dependencies
- **LLM API**: OpenAI GPT-4 or Google Gemini
- **Configuration Storage**: Local files (YAML/JSON)
- **Checkpoint Storage**: Local storage

### 4.4 Language Processing Requirements
- **LLM Prompt Strategy**:
  - System prompts can be in English for efficiency
  - Thinking process can be in English or Japanese
  - All outputs must be in Japanese
  - Context understanding must account for Japanese business culture
- **Japanese Text Processing**:
  - Proper handling of Kanji, Hiragana, Katakana
  - Understanding of Japanese business email conventions
  - Keigo (honorific language) analysis capabilities
  - Japanese character count considerations (full-width vs half-width)

## 5. Success Criteria

### 5.1 Phase-based Goals
- **Phase 1**: Understanding LangGraph basic concepts, working prototype
- **Phase 2**: Practical email checking functionality, understanding conditional branching
- **Phase 3**: Advanced workflow, understanding agent collaboration
- **Phase 4**: Complete functionality, ready for MA tool integration

### 5.2 Technical Learning Goals
- Understanding LangGraph core concepts (nodes, edges, state, checkpoints)
- Ability to design and implement complex workflows
- Building architecture suitable for MA tool integration
- Proficiency in handling Japanese language processing requirements
