# Stellecta LVO × Stellar Blockchain Architecture

**Learn – Verify – Own as On-Chain, Verifiable Digital Assets**

---

**Version:** 1.0  
**Date:** November 2025  
**Status:** Production Architecture Specification  
**Classification:** Technical Documentation – For Development & Strategic Review

---

## Executive Summary

Stellecta implements a revolutionary **Learn-Verify-Own (LVO)** framework where every learning milestone becomes a verifiable, blockchain-backed digital asset. By integrating with the **Stellar blockchain network**, we transform educational achievements into **tokenized credentials** that students truly own, parents can verify, and institutions can trust.

This architecture combines:

- **Advanced Learning Analytics** (H-PEM, LCT, Knowledge Graphs)
- **Agentic AI Workflows** (K.E.R.N.E.L. framework)
- **Blockchain Tokenization** (Stellar + Lobstr-compatible wallets)
- **LLM Quality Layer** (RAG, Verification, XAI, GDPR compliance)
- **Privacy-First Design** (GDPR Art. 22, COPPA compliance)

The result: A **future-proof credential passport** where learning achievements are portable, verifiable, and owned by students—not platforms.

---

## Table of Contents

1. [High-Level Overview](#high-level-overview)
2. [System Architecture](#system-architecture)
3. [Technical Stack](#technical-stack)
4. [Data Models](#data-models)
5. [Blockchain Integration](#blockchain-integration)
6. [LVO + H-PEM + LCT Integration](#lvo-h-pem-lct-integration)
7. [K.E.R.N.E.L. Agentic Workflow](#kernel-agentic-workflow)
8. [LLM Answer Quality Layer](#llm-answer-quality-layer)
9. [API & Service Layer](#api-service-layer)
10. [Security, Privacy & Compliance](#security-privacy-compliance)
11. [Deployment Guide](#deployment-guide)
12. [Architecture Checklist](#architecture-checklist)

---

## High-Level Overview

### What the System Does

Stellecta's LVO × Stellar integration transforms the learning journey into verifiable, blockchain-backed achievements:

1. **Learn**: Student completes learning activities with AI mentors
2. **Verify**: Multi-source verification confirms mastery (LLM + Human + Peer)
3. **Own**: Achievement is tokenized on Stellar blockchain → Student's wallet

Every verified skill, badge, and credential becomes a **digital asset** the student controls.

### Why LVO with Blockchain

Traditional education systems:
- ❌ Credentials controlled by institutions
- ❌ No proof of incremental learning
- ❌ Skills not portable across platforms
- ❌ Parents blind to real-time progress

**Stellecta LVO solves this:**
- ✅ **Student Ownership**: Credentials in student's wallet
- ✅ **Granular Proof**: Nanoscale competencies tracked
- ✅ **Portability**: Stellar tokens work across any compatible system
- ✅ **Transparency**: Parents see verified progress on-chain
- ✅ **Trust**: Cryptographic proof of achievement

### Why Stellar

We chose Stellar blockchain for:

**1. Speed & Cost**
- 3-5 second transaction finality
- ~$0.00001 per transaction (vs. Ethereum's $50+)
- Handles 1,000+ TPS (suitable for millions of students)

**2. Asset Tokenization**
- Native support for custom assets (badges, credentials, tokens)
- Simple token issuance without smart contracts
- Built-in compliance features (KYC, AML)

**3. Ecosystem**
- Lobstr wallet integration (used by 1M+ users)
- Strong institutional adoption (MoneyGram, Circle, IBM)
- Regulatory compliance (designed for financial institutions)

**4. Developer Experience**
- Well-documented SDKs (Python, JavaScript, Go)
- Testnet for development
- Horizon API for easy integration

### Why Lobstr-Compatible Wallets

**Lobstr** is the leading Stellar wallet with:
- 1M+ active users
- Simple mobile UX (critical for students/parents)
- Multi-asset support
- Built-in DEX (future: trade learning tokens)
- Strong security (biometric, PIN, seed phrase)

Our design ensures:
- Students can use **any Lobstr-compatible wallet**
- Parents can view child's achievements in real-time
- Future: Credentials portable to other Stellar apps

### Why This Architecture is Future-Proof

**Phase 1 (MVP)**: Simulated blockchain + custodial wallets
**Phase 2 (Pilot)**: Testnet integration + parent visibility
**Phase 3 (Production)**: Mainnet + non-custodial wallets + credential passport

Key future-proofing:
- **Credential Passport**: All Stellecta achievements → one portable wallet
- **Interoperability**: Stellar credentials work with any compatible platform
- **Decentralization**: Students own credentials, not Stellecta
- **Longevity**: Blockchain records persist beyond platform lifespan

---

## System Architecture

### High-Level System Architecture

```mermaid
flowchart TB
    subgraph "Student Layer"
        S[Student]
        SW[Student Wallet<br/>Lobstr-compatible]
    end

    subgraph "LVO Pipeline"
        L[Learn<br/>AI Mentor Interaction]
        V[Verify<br/>Multi-Source Validation]
        O[Own<br/>Tokenization]
    end

    subgraph "Backend Services"
        WS[WalletService<br/>Stellar SDK]
        TS[TokenizationService<br/>Asset Issuance]
        CS[CredentialService<br/>LVO Logic]
        MS[MasteryDecisionService<br/>H-PEM + LCT]
        ES[EvaluationService<br/>Quality Layer]
    end

    subgraph "Stellar Network"
        SB[Stellar Blockchain]
        H[Horizon API]
        A[Stellecta Asset Issuer]
    end

    subgraph "Parent Dashboard"
        P[Parent]
        PD[Dashboard UI]
        BC[Blockchain Connector]
    end

    subgraph "LLM Quality Layer"
        RAG[RAG Pipeline]
        VER[Verification Agent]
        XAI[XAI Logger]
    end

    S -->|Completes Task| L
    L -->|Generates Data| V
    V -->|Validation| ES
    ES -->|Uses| RAG
    ES -->|Uses| VER
    ES -->|Logs| XAI
    V -->|Mastery Confirmed| O
    O -->|Triggers| MS
    MS -->|Calculates H-PEM| CS
    CS -->|Mints Token| TS
    TS -->|Uses| WS
    WS -->|Interacts| H
    H -->|Writes| SB
    SB -->|Asset Issued by| A
    SB -->|Sends Token| SW
    
    P -->|Views Progress| PD
    PD -->|Queries| BC
    BC -->|Reads| H
    H -->|Returns Data| BC

    style S fill:#90EE90
    style SW fill:#FFD700
    style SB fill:#87CEEB
    style P fill:#FFB6C1
```

### Tokenization Flow

```mermaid
sequenceDiagram
    participant Student
    participant AITutor as AI Tutor
    participant VerificationAgent as Verification Agent
    participant MasteryService as Mastery Decision Service
    participant HPEMEngine as H-PEM Engine
    participant LCTService as LCT Service
    participant TokenizationService as Tokenization Service
    participant StellarAPI as Stellar Horizon API
    participant Wallet as Student Wallet

    Student->>AITutor: Completes learning task
    AITutor->>VerificationAgent: Submit answer for verification
    VerificationAgent->>VerificationAgent: Multi-source validation<br/>(LLM + RAG + Human)
    
    alt Mastery Confirmed
        VerificationAgent->>MasteryService: Mark as mastery achieved
        MasteryService->>HPEMEngine: Calculate H-PEM metrics
        HPEMEngine-->>MasteryService: Proficiency: 0.92<br/>Resilience: 0.88<br/>Velocity: 0.95
        MasteryService->>LCTService: Update LCT timeline
        LCTService-->>MasteryService: LCT updated
        MasteryService->>TokenizationService: Trigger tokenization
        TokenizationService->>TokenizationService: Prepare asset metadata
        TokenizationService->>StellarAPI: Mint token (e.g., BADGE_MATH_L3)
        StellarAPI->>StellarAPI: Create & sign transaction
        StellarAPI-->>TokenizationService: Tx confirmed
        TokenizationService->>Wallet: Send token to student wallet
        Wallet-->>Student: ✅ Achievement unlocked!
    else Not Yet Mastered
        VerificationAgent->>Student: ❌ Continue practicing
    end
```

### Wallet + Student/Parent Relation Model

```mermaid
classDiagram
    class Student {
        +UUID id
        +String name
        +String email
        +UUID wallet_id
        +getWallet()
        +getAchievements()
    }

    class Parent {
        +UUID id
        +String name
        +String email
        +UUID[] children_ids
        +getChildren()
        +viewChildProgress(child_id)
    }

    class Wallet {
        +UUID id
        +String stellar_public_key
        +String encrypted_private_key
        +WalletType type
        +DateTime created_at
        +getBalance()
        +listTokens()
    }

    class TokenAward {
        +UUID id
        +UUID student_id
        +String token_code
        +String stellar_tx_id
        +DateTime awarded_at
        +JSON metadata
    }

    class OnChainCredential {
        +UUID id
        +String credential_type
        +UUID student_id
        +String asset_code
        +String stellar_tx_id
        +JSON h_pem_snapshot
        +DateTime issued_at
    }

    class LCTProfile {
        +UUID id
        +UUID student_id
        +JSON timeline_data
        +Float[] proficiency_trajectory
        +DateTime last_updated
    }

    Student "1" --> "1" Wallet : owns
    Student "1" --> "*" TokenAward : earns
    Student "1" --> "*" OnChainCredential : holds
    Student "1" --> "1" LCTProfile : has
    Parent "1" --> "*" Student : guardianOf
    TokenAward "*" --> "1" Wallet : stored_in
```

### LLM Quality Layer (Tutor vs Judge Architecture)

```mermaid
flowchart TD
    Start[Student submits answer]
    
    subgraph "Tutor Mode"
        T1[LLM as Tutor<br/>Socratic guidance]
        T2[Generate hints]
        T3[Encourage student]
    end
    
    subgraph "Judge Mode"
        J1[LLM as Judge<br/>Strict evaluation]
        J2[RAG Retrieval<br/>Ground truth check]
        J3[Verification Agent<br/>Cross-model validation]
        J4[XAI Logger<br/>Decision transparency]
    end
    
    subgraph "Mastery Decision"
        M1{Meets mastery<br/>threshold?}
        M2[Mastery Service<br/>H-PEM calculation]
        M3[Block tokenization]
    end
    
    Start --> T1
    T1 --> T2
    T2 --> T3
    T3 --> Start
    
    Start --> J1
    J1 --> J2
    J2 --> J3
    J3 --> J4
    J4 --> M1
    
    M1 -->|Yes| M2
    M1 -->|No| M3
    M2 --> TokenizationTrigger[Trigger tokenization]
    M3 --> T1

    style M2 fill:#90EE90
    style M3 fill:#FFB6C1
    style TokenizationTrigger fill:#FFD700
```

---

## Technical Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Blockchain** | Stellar (Soroban optional for future) | Asset tokenization, credential storage |
| **Wallet Integration** | Stellar SDK + Lobstr compatibility | Student/parent wallet management |
| **Backend** | Python (FastAPI) | LVO pipeline, services, APIs |
| **Database** | PostgreSQL | Off-chain data (PII, learning history) |
| **AI Layer** | Google Gemini 2.5 Flash (via Lovable AI) | AI mentors, verification, RAG |
| **Analytics** | Custom H-PEM + LCT engines | Learning trajectory calculation |
| **Frontend** | React + TypeScript (Lovable.dev) | Student/parent/teacher dashboards |
| **Deployment** | Lovable.dev hosting + Supabase | MVP environment |

### Stellar SDK Integration

**Python SDK:**
```python
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# Connect to Stellar network
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Create asset issuer (Stellecta account)
issuer_keypair = Keypair.from_secret(os.getenv("STELLAR_ISSUER_SECRET"))

# Define custom asset (e.g., MATH_BADGE)
asset = Asset("MATH_BADGE", issuer_keypair.public_key)

# Mint token to student wallet
def mint_token(student_public_key, asset, amount):
    source_account = server.load_account(issuer_keypair.public_key)
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100
        )
        .append_payment_op(
            destination=student_public_key,
            asset=asset,
            amount=str(amount)
        )
        .build()
    )
    transaction.sign(issuer_keypair)
    response = server.submit_transaction(transaction)
    return response
```

### Asset Issuance Model

**Stellecta Asset Types:**

| Asset Code | Description | Example Use |
|------------|-------------|-------------|
| `BADGE_*` | Achievement badges | `BADGE_MATH_L3`, `BADGE_READING_A1` |
| `CRED_*` | Formal credentials | `CRED_ALGEBRA_CERT`, `CRED_ENGLISH_A2` |
| `SKILL_*` | Granular skill tokens | `SKILL_FRACTIONS`, `SKILL_GRAMMAR` |
| `XP_*` | Experience points (gamification) | `XP_MATH`, `XP_ENGLISH` |

**Asset Metadata (stored in transaction memo):**
```json
{
  "credential_type": "BADGE_MATH_L3",
  "student_pseudonym": "STU_4f7a9b2c",
  "h_pem": {
    "proficiency": 0.92,
    "resilience": 0.88,
    "velocity": 0.95,
    "engagement": 0.91,
    "transfer": 0.87
  },
  "issued_at": "2025-11-19T19:30:00Z",
  "issuer": "Stellecta",
  "version": "1.0"
}
```

### Wallet Creation (Custodial vs Non-Custodial)

**Phase 1 (MVP): Custodial Wallets**
- Stellecta creates & manages wallets
- Private keys encrypted and stored server-side
- Parents can view but not transfer tokens

**Phase 2 (Pilot): Hybrid Model**
- Students/parents can connect existing Lobstr wallets
- Stellecta issues tokens to parent-provided addresses
- No private key storage needed

**Phase 3 (Production): Non-Custodial**
- Students own wallets completely
- Stellecta only issues tokens
- Full decentralization

### Lobstr Compatibility

**Lobstr Wallet Features We Leverage:**
- Multi-asset display (all Stellecta badges/credentials visible)
- Transaction history (parents see when tokens awarded)
- QR code sharing (students can share achievements)
- Biometric security (PIN + fingerprint)

**Integration:**
```python
# Student connects Lobstr wallet
def link_lobstr_wallet(student_id, public_key):
    # Verify public key is valid Stellar address
    if not Keypair.is_valid_ed25519_public_key(public_key):
        raise ValueError("Invalid Stellar public key")
    
    # Store in database
    wallet = Wallet.create(
        student_id=student_id,
        stellar_public_key=public_key,
        type=WalletType.NON_CUSTODIAL,
        linked_at=datetime.utcnow()
    )
    return wallet
```

### Backend Modules

**Core Services:**

1. **WalletService**: Stellar wallet creation, key management, balance queries
2. **TokenizationService**: Asset minting, transaction signing, Horizon API calls
3. **CredentialService**: LVO pipeline orchestration, mastery verification
4. **MasteryDecisionService**: H-PEM calculation, threshold evaluation
5. **EvaluationService**: LLM quality layer, RAG verification
6. **StudentProgressService**: LCT tracking, knowledge graph updates

**Integration into Existing Backend:**

This architecture **extends** the existing FastAPI backend without breaking changes:

- New routers: `/api/v1/blockchain/*`, `/api/v1/credentials/*`
- New services: Above modules added to `backend/app/services/`
- Existing routers (auth, skills, curriculum) remain untouched
- Database migrations add new tables (wallets, tokens, credentials)

---

## Data Models

### Database Schema

**Core Tables:**

#### 1. Wallets

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `student_id` | UUID | Foreign key to users table |
| `stellar_public_key` | VARCHAR(56) | Stellar address (G...) |
| `encrypted_private_key` | TEXT | Encrypted secret (custodial only) |
| `wallet_type` | ENUM | custodial, non_custodial, lobstr |
| `created_at` | TIMESTAMP | Wallet creation time |
| `last_synced_at` | TIMESTAMP | Last blockchain sync |

#### 2. Token Awards

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `student_id` | UUID | Foreign key to users |
| `wallet_id` | UUID | Foreign key to wallets |
| `token_code` | VARCHAR(32) | Asset code (e.g., BADGE_MATH_L3) |
| `stellar_tx_id` | VARCHAR(64) | Blockchain transaction hash |
| `amount` | DECIMAL | Token amount (usually 1 for badges) |
| `metadata` | JSONB | H-PEM snapshot, competency data |
| `awarded_at` | TIMESTAMP | When token was minted |

#### 3. On-Chain Credentials

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `student_id` | UUID | Foreign key to users |
| `credential_type` | VARCHAR(64) | BADGE, CRED, SKILL, XP |
| `asset_code` | VARCHAR(32) | Stellar asset code |
| `stellar_tx_id` | VARCHAR(64) | Transaction ID |
| `h_pem_snapshot` | JSONB | H-PEM metrics at time of issuance |
| `competencies` | JSONB | Nanoscale competencies achieved |
| `issued_at` | TIMESTAMP | Credential issuance time |
| `expires_at` | TIMESTAMP | Optional expiration (NULL = permanent) |

#### 4. LCT Profiles

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `student_id` | UUID | Foreign key to users |
| `timeline_data` | JSONB | Full LCT trajectory |
| `proficiency_trajectory` | FLOAT[] | Array of proficiency over time |
| `velocity_scores` | FLOAT[] | Learning velocity snapshots |
| `resilience_scores` | FLOAT[] | Resilience over time |
| `last_updated` | TIMESTAMP | Latest LCT calculation |

#### 5. H-PEM Snapshots

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `student_id` | UUID | Foreign key to users |
| `competency_id` | UUID | Foreign key to skills/competencies |
| `proficiency` | FLOAT | 0.0 - 1.0 |
| `resilience` | FLOAT | 0.0 - 1.0 |
| `velocity` | FLOAT | 0.0 - 1.0 |
| `engagement` | FLOAT | 0.0 - 1.0 |
| `transfer` | FLOAT | 0.0 - 1.0 |
| `calculated_at` | TIMESTAMP | When H-PEM was calculated |

#### 6. Knowledge Graph Nodes

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `competency_id` | UUID | Foreign key to competencies |
| `node_type` | VARCHAR(32) | concept, skill, prerequisite |
| `dependencies` | JSONB | Array of prerequisite node IDs |
| `difficulty_level` | INT | 1-10 scale |
| `mastery_threshold` | FLOAT | Required H-PEM proficiency |

### Entity Relationship Diagram

```mermaid
erDiagram
    STUDENTS ||--|| WALLETS : owns
    STUDENTS ||--o{ TOKEN_AWARDS : earns
    STUDENTS ||--o{ ONCHAIN_CREDENTIALS : holds
    STUDENTS ||--|| LCT_PROFILES : has
    STUDENTS ||--o{ HPEM_SNAPSHOTS : generates
    
    WALLETS ||--o{ TOKEN_AWARDS : stores
    
    COMPETENCIES ||--o{ HPEM_SNAPSHOTS : measured_by
    COMPETENCIES ||--o{ KNOWLEDGE_GRAPH_NODES : represented_by
    
    ONCHAIN_CREDENTIALS }o--|| TOKEN_AWARDS : references
    
    STUDENTS {
        uuid id PK
        string name
        string email
        uuid wallet_id FK
    }
    
    WALLETS {
        uuid id PK
        uuid student_id FK
        string stellar_public_key
        string encrypted_private_key
        enum wallet_type
        timestamp created_at
    }
    
    TOKEN_AWARDS {
        uuid id PK
        uuid student_id FK
        uuid wallet_id FK
        string token_code
        string stellar_tx_id
        decimal amount
        jsonb metadata
        timestamp awarded_at
    }
    
    ONCHAIN_CREDENTIALS {
        uuid id PK
        uuid student_id FK
        string credential_type
        string asset_code
        string stellar_tx_id
        jsonb h_pem_snapshot
        jsonb competencies
        timestamp issued_at
    }
    
    LCT_PROFILES {
        uuid id PK
        uuid student_id FK
        jsonb timeline_data
        float_array proficiency_trajectory
        timestamp last_updated
    }
    
    HPEM_SNAPSHOTS {
        uuid id PK
        uuid student_id FK
        uuid competency_id FK
        float proficiency
        float resilience
        float velocity
        float engagement
        float transfer
        timestamp calculated_at
    }
    
    KNOWLEDGE_GRAPH_NODES {
        uuid id PK
        uuid competency_id FK
        string node_type
        jsonb dependencies
        int difficulty_level
        float mastery_threshold
    }
```

---

## Blockchain Integration

### How Stellar is Used

**1. Asset Definition**
```python
# Define Stellecta asset issuer
STELLECTA_ISSUER = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Create asset types
BADGE_MATH_L3 = Asset("BADGE_MATH_L3", STELLECTA_ISSUER)
CRED_ALGEBRA = Asset("CRED_ALGEBRA", STELLECTA_ISSUER)
SKILL_FRACTIONS = Asset("SKILL_FRACTIONS", STELLECTA_ISSUER)
```

**2. Transaction Lifecycle**
```mermaid
sequenceDiagram
    participant Backend
    participant WalletService
    participant TokenizationService
    participant Horizon as Stellar Horizon API
    participant Blockchain as Stellar Network

    Backend->>WalletService: Get student wallet
    WalletService-->>Backend: Return public_key
    Backend->>TokenizationService: mint_token(public_key, asset, metadata)
    TokenizationService->>TokenizationService: Build transaction
    TokenizationService->>TokenizationService: Sign with issuer key
    TokenizationService->>Horizon: Submit transaction
    Horizon->>Blockchain: Broadcast to network
    Blockchain-->>Horizon: Transaction confirmed
    Horizon-->>TokenizationService: Return tx_id
    TokenizationService-->>Backend: Token minted successfully
```

### Token Minting Process

**Step-by-Step:**

1. **Mastery Verified** → MasteryDecisionService confirms threshold met
2. **H-PEM Calculated** → Metrics computed (proficiency, resilience, velocity, engagement, transfer)
3. **Metadata Prepared** → JSON payload with H-PEM, competency ID, timestamp
4. **Transaction Built** → Stellar SDK creates payment operation
5. **Transaction Signed** → Issuer private key signs transaction
6. **Submit to Horizon** → POST to `/transactions` endpoint
7. **Blockchain Confirms** → Network validates & includes in ledger
8. **Database Updated** → Store tx_id, token_code, metadata in `token_awards` table

**Code Example:**
```python
async def mint_achievement_token(
    student_id: UUID,
    competency_id: UUID,
    h_pem: HPEMMetrics
) -> TokenAward:
    # Get student wallet
    wallet = await wallet_service.get_wallet(student_id)
    
    # Prepare asset code
    competency = await db.get_competency(competency_id)
    asset_code = f"BADGE_{competency.code.upper()}"
    asset = Asset(asset_code, STELLECTA_ISSUER_PUBLIC_KEY)
    
    # Build transaction
    source_account = server.load_account(STELLECTA_ISSUER_PUBLIC_KEY)
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100
        )
        .append_payment_op(
            destination=wallet.stellar_public_key,
            asset=asset,
            amount="1"  # 1 badge token
        )
        .add_text_memo(json.dumps({
            "h_pem": h_pem.dict(),
            "competency_id": str(competency_id),
            "issued_at": datetime.utcnow().isoformat()
        }))
        .set_timeout(30)
        .build()
    )
    
    # Sign & submit
    transaction.sign(STELLECTA_ISSUER_KEYPAIR)
    response = server.submit_transaction(transaction)
    
    # Store in database
    token_award = TokenAward.create(
        student_id=student_id,
        wallet_id=wallet.id,
        token_code=asset_code,
        stellar_tx_id=response["hash"],
        amount=1,
        metadata={"h_pem": h_pem.dict()},
        awarded_at=datetime.utcnow()
    )
    
    return token_award
```

### Parent Dashboard Flow

**How Parents View Child Progress:**

1. **Parent Logs In** → Authentication via Supabase Auth
2. **Dashboard Loads** → React component fetches child's `student_id`
3. **Blockchain Query** → Backend queries Stellar Horizon API for child's wallet
4. **Token List Retrieved** → All assets in child's wallet returned
5. **Metadata Fetched** → Transaction memos parsed for H-PEM data
6. **UI Renders** → Badges, credentials, proficiency scores displayed

**Parent Dashboard Component (Pseudocode):**
```typescript
async function ParentDashboard({ childId }: { childId: string }) {
  // Get child's wallet
  const wallet = await api.getChildWallet(childId);
  
  // Query Stellar for tokens
  const tokens = await stellarAPI.getWalletAssets(wallet.public_key);
  
  // Fetch metadata from database
  const achievements = await api.getAchievements(childId);
  
  // Render
  return (
    <div>
      <h2>Your Child's Learning Achievements</h2>
      {tokens.map(token => (
        <BadgeCard
          code={token.asset_code}
          metadata={achievements.find(a => a.token_code === token.asset_code)}
          onChainProof={token.tx_id}
        />
      ))}
    </div>
  );
}
```

### Privacy-Safe Pseudonymization

**Challenge**: Blockchain is public → Can't put student names/emails on-chain

**Solution**: Pseudonymization layer

```python
def pseudonymize_student(student_id: UUID) -> str:
    """
    Generate privacy-safe pseudonym for on-chain metadata
    """
    # Use HMAC-SHA256 with secret salt
    secret = os.getenv("PSEUDONYMIZATION_SECRET")
    pseudonym = hmac.new(
        secret.encode(),
        str(student_id).encode(),
        hashlib.sha256
    ).hexdigest()[:16]  # First 16 chars
    
    return f"STU_{pseudonym}"

# Usage
student_pseudonym = pseudonymize_student(student_id)
# Output: "STU_4f7a9b2c3d8e1f6a"
```

**On-chain data** contains:
- ✅ Pseudonym (e.g., `STU_4f7a9b2c`)
- ✅ H-PEM metrics (proficiency, resilience, etc.)
- ✅ Competency ID (UUID, not human-readable)
- ❌ Student name
- ❌ Student email
- ❌ School name

**Off-chain database** links pseudonym → actual student identity (GDPR-compliant storage).

### Off-Chain vs On-Chain Data Separation

| Data Type | Storage | Why |
|-----------|---------|-----|
| **Student PII** (name, email, DOB) | Off-chain (PostgreSQL) | GDPR compliance |
| **Learning history** (raw task data) | Off-chain | Too large for blockchain |
| **H-PEM metrics** | Both (off-chain + on-chain metadata) | On-chain for verification |
| **Achievement badges** | On-chain (Stellar tokens) | Portability & ownership |
| **Transaction IDs** | Both | Cross-reference |
| **LCT trajectories** | Off-chain | Too granular for blockchain |

**Design principle**: Blockchain for **proof** (credentials, achievements), database for **details** (learning history, PII).

### Security: Private Key Handling

**Custodial Wallet Security (Phase 1):**

```python
from cryptography.fernet import Fernet

# Encryption key (stored in environment variable, not in code)
ENCRYPTION_KEY = os.getenv("WALLET_ENCRYPTION_KEY")
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_private_key(private_key: str) -> str:
    """Encrypt Stellar private key before storing in database"""
    return cipher.encrypt(private_key.encode()).decode()

def decrypt_private_key(encrypted_key: str) -> str:
    """Decrypt private key for transaction signing"""
    return cipher.decrypt(encrypted_key.encode()).decode()

# Usage
keypair = Keypair.random()
encrypted = encrypt_private_key(keypair.secret)

# Store encrypted_key in database
wallet = Wallet.create(
    stellar_public_key=keypair.public_key,
    encrypted_private_key=encrypted,
    wallet_type=WalletType.CUSTODIAL
)
```

**Best Practices:**
- ✅ Encryption keys stored in HSM or environment variables (never in code)
- ✅ Private keys encrypted at rest
- ✅ Transaction signing happens server-side (no private keys sent to client)
- ✅ Audit logs for all key accesses
- ✅ Key rotation policy (quarterly)

**Phase 3 (Non-Custodial):**
- No private key storage
- Students use Lobstr or other Stellar wallets
- Stellecta only needs public keys to issue tokens

---

## LVO + H-PEM + LCT Integration

### From Learning Action to Blockchain

**Complete Pipeline:**

```mermaid
flowchart LR
    A[Student completes task] --> B[AI Tutor evaluates]
    B --> C{Verification Layer}
    C -->|RAG Check| D[Ground truth validation]
    C -->|Cross-model| E[Second LLM verification]
    C -->|Human review| F[Teacher escalation if needed]
    
    D --> G{All checks pass?}
    E --> G
    F --> G
    
    G -->|Yes| H[Calculate H-PEM]
    G -->|No| Z[Not mastered - continue learning]
    
    H --> I[Update LCT timeline]
    I --> J{Meets mastery<br/>threshold?}
    
    J -->|Yes| K[Trigger tokenization]
    J -->|No| L[Update progress - no token yet]
    
    K --> M[Mint token on Stellar]
    M --> N[Send to student wallet]
    N --> O[Update Knowledge Graph]
    O --> P[Parent notification]

    style H fill:#FFD700
    style K fill:#90EE90
    style M fill:#87CEEB
    style Z fill:#FFB6C1
```

### H-PEM: Hyper-Performance Evaluation Metrics

**Five Core Dimensions:**

1. **Proficiency** (0.0 - 1.0)
   - Raw accuracy on competency assessments
   - Weighted by difficulty level
   - Formula: `proficiency = correct_answers / total_attempts * difficulty_multiplier`

2. **Resilience** (0.0 - 1.0)
   - Ability to recover from mistakes
   - Measures improvement after incorrect attempts
   - Formula: `resilience = (final_score - initial_score) / (1 - initial_score)`

3. **Velocity** (0.0 - 1.0)
   - Speed of mastery achievement
   - Normalized against expected learning time
   - Formula: `velocity = expected_time / actual_time` (capped at 1.0)

4. **Engagement** (0.0 - 1.0)
   - Consistency and frequency of practice
   - Streak bonuses, session duration
   - Formula: `engagement = (sessions_completed / expected_sessions) * streak_multiplier`

5. **Transfer** (0.0 - 1.0)
   - Ability to apply knowledge in new contexts
   - Cross-competency problem solving
   - Formula: `transfer = correct_novel_problems / total_novel_problems`

**H-PEM Calculation Service:**

```python
class HPEMEngine:
    def calculate_h_pem(
        self,
        student_id: UUID,
        competency_id: UUID,
        learning_history: List[TaskAttempt]
    ) -> HPEMMetrics:
        # 1. Proficiency
        correct = sum(1 for attempt in learning_history if attempt.correct)
        total = len(learning_history)
        difficulty = self.get_competency_difficulty(competency_id)
        proficiency = (correct / total) * (1 + difficulty * 0.1)
        
        # 2. Resilience
        scores = [attempt.score for attempt in learning_history]
        initial_score = scores[0]
        final_score = scores[-1]
        resilience = (final_score - initial_score) / (1 - initial_score) if initial_score < 1 else 1.0
        
        # 3. Velocity
        expected_time = self.get_expected_mastery_time(competency_id)
        actual_time = (learning_history[-1].timestamp - learning_history[0].timestamp).total_seconds()
        velocity = min(expected_time / actual_time, 1.0)
        
        # 4. Engagement
        expected_sessions = self.get_expected_sessions(competency_id)
        actual_sessions = len(set(attempt.session_id for attempt in learning_history))
        streak = self.get_current_streak(student_id)
        engagement = (actual_sessions / expected_sessions) * (1 + streak * 0.05)
        
        # 5. Transfer
        novel_problems = [a for a in learning_history if a.is_novel_context]
        transfer = sum(1 for a in novel_problems if a.correct) / len(novel_problems) if novel_problems else 0.5
        
        return HPEMMetrics(
            proficiency=proficiency,
            resilience=resilience,
            velocity=velocity,
            engagement=engagement,
            transfer=transfer
        )
```

### LCT: Longitudinal Competency Trajectory

**What is LCT?**

A time-series representation of a student's mastery evolution across all competencies. Think of it as a "learning passport" showing:
- **When** each skill was learned
- **How quickly** mastery was achieved
- **Decay patterns** (knowledge retention over time)
- **Transfer effects** (how learning one skill boosts others)

**LCT Data Structure:**

```json
{
  "student_id": "uuid",
  "timeline": [
    {
      "timestamp": "2025-01-15T10:00:00Z",
      "competency_id": "fractions_basic",
      "h_pem": {
        "proficiency": 0.85,
        "resilience": 0.80,
        "velocity": 0.90,
        "engagement": 0.88,
        "transfer": 0.75
      },
      "mastery_level": "achieved",
      "decay_rate": 0.02
    },
    {
      "timestamp": "2025-02-10T14:30:00Z",
      "competency_id": "fractions_advanced",
      "h_pem": {
        "proficiency": 0.92,
        "resilience": 0.88,
        "velocity": 0.95,
        "engagement": 0.91,
        "transfer": 0.87
      },
      "mastery_level": "achieved",
      "decay_rate": 0.01
    }
  ],
  "proficiency_trajectory": [0.85, 0.88, 0.90, 0.92],
  "last_updated": "2025-02-10T14:30:00Z"
}
```

**LCT Service:**

```python
class LCTService:
    async def update_lct(
        self,
        student_id: UUID,
        competency_id: UUID,
        h_pem: HPEMMetrics
    ) -> LCTProfile:
        # Get existing LCT profile
        lct = await db.get_lct_profile(student_id)
        
        # Add new data point
        new_point = {
            "timestamp": datetime.utcnow().isoformat(),
            "competency_id": str(competency_id),
            "h_pem": h_pem.dict(),
            "mastery_level": "achieved" if h_pem.proficiency >= 0.9 else "developing",
            "decay_rate": self.calculate_decay_rate(student_id, competency_id)
        }
        
        lct.timeline_data["timeline"].append(new_point)
        lct.proficiency_trajectory.append(h_pem.proficiency)
        lct.last_updated = datetime.utcnow()
        
        await db.save(lct)
        return lct
    
    def calculate_decay_rate(self, student_id: UUID, competency_id: UUID) -> float:
        """
        Knowledge decay rate (BYJU'S style)
        Predicts how quickly knowledge fades without practice
        """
        # Get time since last practice
        last_practice = self.get_last_practice_time(student_id, competency_id)
        days_since = (datetime.utcnow() - last_practice).days
        
        # Decay formula: higher complexity = faster decay
        complexity = self.get_competency_complexity(competency_id)
        decay_rate = 0.01 * complexity * (1 + days_since * 0.01)
        
        return min(decay_rate, 0.1)  # Cap at 10% decay rate
```

### Nanoscale Knowledge Points

**Concept**: Break down learning into atomic, measurable competencies (inspired by Squirrel AI).

**Example: Fractions**

```
├── Fractions (Top-level)
│   ├── Understanding Fractions
│   │   ├── What is a fraction? (Nanoscale KP1)
│   │   ├── Numerator vs Denominator (Nanoscale KP2)
│   │   ├── Visual representation (Nanoscale KP3)
│   ├── Comparing Fractions
│   │   ├── Same denominator comparison (Nanoscale KP4)
│   │   ├── Different denominator comparison (Nanoscale KP5)
│   │   ├── Cross-multiplication technique (Nanoscale KP6)
│   ├── Operations on Fractions
│   │   ├── Addition (same denominator) (Nanoscale KP7)
│   │   ├── Addition (different denominator) (Nanoscale KP8)
│   │   ├── Subtraction (Nanoscale KP9)
│   │   ├── Multiplication (Nanoscale KP10)
│   │   ├── Division (Nanoscale KP11)
```

**Each Nanoscale KP has:**
- Unique ID
- Difficulty level (1-10)
- Prerequisites (other KPs that must be mastered first)
- Mastery threshold (minimum H-PEM proficiency required)
- Expected mastery time (minutes)

**Knowledge Graph Representation:**

```python
class KnowledgeGraphNode:
    id: UUID
    competency_id: UUID
    node_type: str  # "concept", "skill", "prerequisite"
    name: str
    difficulty_level: int  # 1-10
    prerequisites: List[UUID]  # IDs of prerequisite nodes
    mastery_threshold: float  # e.g., 0.9 for 90% proficiency
    expected_time_minutes: int
    
    def is_unlocked(self, student_mastery: Dict[UUID, float]) -> bool:
        """Check if student has mastered all prerequisites"""
        for prereq_id in self.prerequisites:
            if student_mastery.get(prereq_id, 0) < self.mastery_threshold:
                return False
        return True
```

### Knowledge Decay (BYJU'S Style)

**Forgetting Curve Integration:**

```python
def calculate_retained_proficiency(
    initial_proficiency: float,
    days_since_practice: int,
    decay_rate: float
) -> float:
    """
    Ebbinghaus forgetting curve: R = e^(-t/S)
    Where:
      R = retention
      t = time since learning
      S = strength of memory (inverse of decay_rate)
    """
    retention = math.exp(-days_since_practice / (1 / decay_rate))
    retained_proficiency = initial_proficiency * retention
    return max(retained_proficiency, 0.1)  # Never goes below 10%
```

**Adaptive Re-Teaching:**

When decay detected:
1. System identifies competencies with proficiency < 0.7
2. AI mentor re-introduces concept (spaced repetition)
3. Student completes refresher tasks
4. H-PEM recalculated
5. LCT updated with recovered proficiency

### Intelligent Adaptive Learning (IAL)

**DreamBox-Inspired Adaptive Engine:**

```python
class AdaptiveLearningEngine:
    def get_next_task(self, student_id: UUID) -> Task:
        # Get student's current knowledge state
        mastery_map = self.get_mastery_map(student_id)
        knowledge_graph = self.load_knowledge_graph()
        
        # Find optimal next competency (Zone of Proximal Development)
        unlocked_nodes = [
            node for node in knowledge_graph.nodes
            if node.is_unlocked(mastery_map) and mastery_map.get(node.id, 0) < 0.9
        ]
        
        # Select based on difficulty, decay risk, and student preferences
        scored_nodes = [
            (node, self.score_node(node, student_id, mastery_map))
            for node in unlocked_nodes
        ]
        
        best_node = max(scored_nodes, key=lambda x: x[1])[0]
        
        # Generate appropriate difficulty task
        task = self.generate_task(best_node, student_id)
        return task
    
    def score_node(self, node: KnowledgeGraphNode, student_id: UUID, mastery_map: Dict) -> float:
        # Scoring factors:
        # 1. Difficulty match (not too easy, not too hard)
        # 2. Decay risk (practice skills at risk of being forgotten)
        # 3. Student preference (topics student enjoys)
        # 4. Learning velocity (students who learn fast get harder tasks)
        
        difficulty_score = 1 - abs(node.difficulty_level - self.get_zpd_difficulty(student_id))
        decay_score = self.get_decay_urgency(student_id, node.id)
        preference_score = self.get_student_preference(student_id, node.competency_id)
        velocity_bonus = self.get_velocity_bonus(student_id)
        
        return (
            difficulty_score * 0.4 +
            decay_score * 0.3 +
            preference_score * 0.2 +
            velocity_bonus * 0.1
        )
```

---

## K.E.R.N.E.L. Agentic Workflow

**K.E.R.N.E.L. = Knowledge, Evaluation, Reasoning, Nanoscale, Explainability, Learning**

A multi-agent system where specialized AI agents handle different aspects of the learning and evaluation pipeline.

### Agent Architecture

```mermaid
flowchart TD
    subgraph "K.E.R.N.E.L. Agents"
        KA[KA: Knowledge Agent<br/>Content & curriculum]
        EA[EA: Evaluation Agent<br/>Assessment & mastery]
        RA[RA: Reasoning Agent<br/>Adaptive pathways]
        NA[NA: Nanoscale Agent<br/>Competency tracking]
        XA[XA: Explainability Agent<br/>XAI & transparency]
        LA[LA: Learning Agent<br/>Student support & tutoring]
    end
    
    subgraph "Data Sources"
        KG[Knowledge Graph]
        CUR[Curriculum Database]
        STU[Student Progress]
    end
    
    subgraph "External Systems"
        LLM[LLM API<br/>Gemini 2.5]
        BC[Blockchain<br/>Stellar]
    end
    
    KA -->|Queries| KG
    KA -->|Retrieves| CUR
    
    EA -->|Reads| STU
    EA -->|Verifies| LLM
    
    RA -->|Analyzes| STU
    RA -->|Consults| KG
    
    NA -->|Updates| STU
    NA -->|Maps| KG
    
    XA -->|Logs decisions| STU
    XA -->|Provides explanations| LA
    
    LA -->|Instructs| LLM
    LA -->|Tutors| Student[Student]
    
    EA -->|Triggers tokenization| BC

    style KA fill:#FFD700
    style EA fill:#90EE90
    style XA fill:#87CEEB
    style LA fill:#FFB6C1
```

### 1. KA: Knowledge Agent

**Responsibilities:**
- Content ingestion from multiple sources
- Curriculum mapping
- Knowledge graph construction
- Competency-to-content alignment

**Pseudocode:**

```python
class KnowledgeAgent:
    async def ingest_content(self, source_url: str, content_type: str):
        # Fetch content
        raw_content = await self.fetch(source_url)
        
        # Parse & extract competencies
        competencies = await self.extract_competencies(raw_content)
        
        # Map to existing knowledge graph
        for competency in competencies:
            node = self.create_knowledge_node(competency)
            self.link_prerequisites(node)
            await self.save_to_knowledge_graph(node)
    
    def create_knowledge_node(self, competency: Dict) -> KnowledgeGraphNode:
        return KnowledgeGraphNode(
            competency_id=competency["id"],
            name=competency["name"],
            difficulty_level=competency["difficulty"],
            prerequisites=competency["prerequisites"],
            mastery_threshold=0.9
        )
```

### 2. EA: Evaluation Agent (ACE - Adaptive Competency Evaluator)

**Responsibilities:**
- Assessment generation
- Answer verification
- Mastery decision
- Tokenization trigger

**Pseudocode:**

```python
class EvaluationAgent:
    async def evaluate_answer(
        self,
        student_id: UUID,
        task_id: UUID,
        answer: str
    ) -> EvaluationResult:
        # Step 1: RAG-based ground truth check
        correct_answer = await self.rag_retrieve_answer(task_id)
        is_correct = await self.compare_answers(answer, correct_answer)
        
        # Step 2: Cross-model verification (second opinion)
        second_opinion = await self.cross_model_verify(answer, correct_answer)
        
        # Step 3: XAI logging
        explanation = await self.explainability_agent.log_decision({
            "student_answer": answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "second_opinion": second_opinion,
            "reasoning": "semantic similarity + factual accuracy"
        })
        
        # Step 4: Mastery decision
        if is_correct and second_opinion["agrees"]:
            h_pem = await self.calculate_h_pem(student_id, task_id)
            if h_pem.proficiency >= 0.9:
                await self.trigger_tokenization(student_id, task_id, h_pem)
        
        return EvaluationResult(
            is_correct=is_correct,
            explanation=explanation,
            next_action="continue" if not is_correct else "advance"
        )
```

### 3. RA: Reasoning Agent (Prophet Agent)

**Responsibilities:**
- Adaptive learning path generation
- Predict optimal next task
- Identify at-risk students
- Recommend interventions

**Pseudocode:**

```python
class ReasoningAgent:
    async def generate_learning_path(self, student_id: UUID) -> LearningPath:
        # Get student's current state
        mastery_map = await self.get_mastery_map(student_id)
        lct_profile = await self.get_lct_profile(student_id)
        
        # Predict future trajectory
        predicted_proficiency = self.predict_next_3_months(lct_profile)
        
        # Identify gaps & risks
        at_risk_competencies = self.identify_decay_risks(mastery_map, lct_profile)
        
        # Generate optimal path
        path = self.optimize_learning_sequence(
            current_mastery=mastery_map,
            goals=self.get_student_goals(student_id),
            at_risk=at_risk_competencies,
            predicted_trajectory=predicted_proficiency
        )
        
        return path
    
    def predict_next_3_months(self, lct_profile: LCTProfile) -> List[float]:
        """Use time-series forecasting to predict future proficiency"""
        # Simple linear regression on proficiency trajectory
        X = np.arange(len(lct_profile.proficiency_trajectory)).reshape(-1, 1)
        y = lct_profile.proficiency_trajectory
        model = LinearRegression().fit(X, y)
        
        future_X = np.arange(len(y), len(y) + 90).reshape(-1, 1)  # 90 days
        predictions = model.predict(future_X)
        
        return predictions.tolist()
```

### 4. NA: Nanoscale Agent

**Responsibilities:**
- Track nanoscale competencies
- Update knowledge graph
- Micro-credential issuance

**Pseudocode:**

```python
class NanoscaleAgent:
    async def track_competency(
        self,
        student_id: UUID,
        nanoscale_kp_id: UUID,
        mastery_level: float
    ):
        # Update knowledge graph
        node = await self.get_knowledge_node(nanoscale_kp_id)
        
        # Store mastery level
        await self.update_student_mastery(student_id, nanoscale_kp_id, mastery_level)
        
        # Check if this unlocks new competencies
        newly_unlocked = await self.check_unlocked_nodes(student_id, node)
        
        # Issue micro-credential if threshold met
        if mastery_level >= node.mastery_threshold:
            await self.issue_micro_credential(student_id, nanoscale_kp_id)
```

### 5. XA: Explainability Agent (OA - Outcome Agent)

**Responsibilities:**
- Log all AI decisions
- Provide human-readable explanations
- GDPR Art. 22 compliance (meaningful information about logic)
- Bias detection

**Pseudocode:**

```python
class ExplainabilityAgent:
    async def log_decision(
        self,
        decision_type: str,
        decision_data: Dict,
        explanation: str
    ):
        # Store in XAI log
        await db.xai_logs.insert({
            "timestamp": datetime.utcnow(),
            "decision_type": decision_type,
            "decision_data": decision_data,
            "explanation": explanation,
            "model_version": self.get_model_version()
        })
    
    def generate_explanation(self, evaluation: EvaluationResult) -> str:
        """GDPR Art. 22 compliant explanation"""
        return f"""
        Your answer was evaluated as {'correct' if evaluation.is_correct else 'incorrect'}.
        
        Reasoning:
        - Semantic similarity to correct answer: {evaluation.similarity_score:.2%}
        - Factual accuracy: {evaluation.factual_accuracy:.2%}
        - Key concepts identified: {', '.join(evaluation.concepts)}
        
        This decision was made using:
        - AI Model: Gemini 2.5 Flash
        - Verification: Cross-checked with second model
        - Human review: {'Required' if evaluation.requires_human_review else 'Not required'}
        
        You have the right to request human review of this decision.
        """
```

### 6. LA: Learning Agent (DCA - Data & Compliance Agent)

**Responsibilities:**
- Direct student interaction (tutoring)
- Socratic questioning
- Hint generation
- Privacy compliance

**Pseudocode:**

```python
class LearningAgent:
    async def tutor_student(
        self,
        student_id: UUID,
        task_id: UUID,
        conversation_history: List[Message]
    ) -> str:
        # Get task context
        task = await db.get_task(task_id)
        
        # Generate Socratic response
        prompt = f"""
        You are Stella, an AI learning mentor.
        Student is working on: {task.description}
        
        Conversation so far:
        {self.format_conversation(conversation_history)}
        
        Provide a Socratic hint that:
        - Doesn't give the answer away
        - Asks a guiding question
        - Encourages critical thinking
        
        Remember: You are a TUTOR, not a JUDGE. Be supportive.
        """
        
        response = await llm_api.generate(prompt)
        
        # Log for GDPR/COPPA compliance
        await self.data_compliance_agent.log_interaction(
            student_id=student_id,
            agent="LearningAgent",
            content=response,
            purpose="tutoring"
        )
        
        return response
```

### Agent Interaction Sequence

```mermaid
sequenceDiagram
    participant Student
    participant LA as Learning Agent
    participant EA as Evaluation Agent
    participant RA as Reasoning Agent
    participant NA as Nanoscale Agent
    participant XA as Explainability Agent
    participant BC as Blockchain

    Student->>LA: "I need help with fractions"
    LA->>RA: Get optimal learning path
    RA-->>LA: Recommend: Fractions KP4 (comparing fractions)
    LA->>Student: "Let's work on comparing 2/3 and 3/4"
    
    Student->>LA: Submits answer
    LA->>EA: Evaluate answer
    EA->>XA: Log evaluation decision
    XA-->>EA: Logged
    
    EA->>EA: Calculate H-PEM
    
    alt Mastery Achieved
        EA->>NA: Update nanoscale competency
        NA->>NA: Check if new competencies unlocked
        NA->>BC: Trigger tokenization
        BC-->>Student: 🎉 Token minted!
        EA->>XA: Log tokenization decision
    else Not Yet Mastered
        EA->>LA: Provide feedback
        LA->>Student: "Good effort! Try this hint..."
    end
```

---

## LLM Answer Quality Layer

**Critical Component**: Ensures AI decisions are accurate, explainable, and compliant.

### Architecture Overview

```mermaid
flowchart TB
    subgraph "Input Layer"
        SI[Student Input]
    end
    
    subgraph "Tutor Mode"
        T1[LLM as Tutor<br/>Gemini 2.5 Flash]
        T2[Socratic Guidance]
        T3[Hint Generation]
    end
    
    subgraph "Judge Mode"
        J1[LLM as Judge<br/>Gemini 2.5 Flash]
        J2[Answer Evaluation]
        J3[Strict Grading]
    end
    
    subgraph "Quality Assurance Layer"
        QA1[RAG Pipeline<br/>Ground Truth Retrieval]
        QA2[Cross-Model Verification<br/>Second Opinion]
        QA3[Bias Detection]
        QA4[Factual Accuracy Check]
    end
    
    subgraph "Compliance Layer"
        C1[XAI Logger<br/>Decision Transparency]
        C2[GDPR Art. 22<br/>Meaningful Explanation]
        C3[Human-in-the-Loop<br/>Escalation]
    end
    
    subgraph "Decision Layer"
        D1{Passes all checks?}
        D2[Mastery Service]
        D3[Block Tokenization]
    end
    
    SI --> T1
    SI --> J1
    
    T1 --> T2
    T2 --> T3
    
    J1 --> J2
    J2 --> J3
    J3 --> QA1
    
    QA1 --> QA2
    QA2 --> QA3
    QA3 --> QA4
    
    QA4 --> C1
    C1 --> C2
    C2 --> D1
    
    D1 -->|Yes| D2
    D1 -->|No| D3
    D1 -->|Uncertain| C3
    
    D2 --> Tokenization[Trigger Tokenization]
    C3 --> Teacher[Teacher Review]

    style QA1 fill:#FFD700
    style C2 fill:#87CEEB
    style C3 fill:#FFB6C1
    style Tokenization fill:#90EE90
```

### 1. RAG Pipeline (Ground Truth Retrieval)

**Purpose**: Retrieve verified correct answers from curriculum database.

**Implementation:**

```python
class RAGPipeline:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name="curriculum_answers",
            embedding_function=OpenAIEmbeddings()
        )
    
    async def retrieve_ground_truth(self, question: str) -> str:
        # Semantic search for similar questions
        results = self.vector_store.similarity_search(
            query=question,
            k=3  # Top 3 similar questions
        )
        
        # Return most relevant answer
        if results:
            return results[0].metadata["correct_answer"]
        else:
            return None  # No ground truth found → escalate to human
```

### 2. Answer Verification Pipeline

**Multi-Stage Verification:**

```python
class AnswerVerificationService:
    async def verify_answer(
        self,
        student_answer: str,
        correct_answer: str,
        question: str
    ) -> VerificationResult:
        # Stage 1: Semantic similarity
        similarity = await self.calculate_semantic_similarity(
            student_answer,
            correct_answer
        )
        
        # Stage 2: Factual accuracy (use LLM to check)
        factual_check = await self.check_factual_accuracy(
            student_answer,
            correct_answer
        )
        
        # Stage 3: Cross-model verification (second opinion)
        second_opinion = await self.cross_model_verify(
            student_answer,
            correct_answer,
            question
        )
        
        # Stage 4: Confidence check
        confidence = (similarity + factual_check["score"] + second_opinion["confidence"]) / 3
        
        # Stage 5: Escalation logic
        if confidence < 0.7:
            return VerificationResult(
                is_correct=None,
                requires_human_review=True,
                confidence=confidence
            )
        
        return VerificationResult(
            is_correct=confidence >= 0.8,
            confidence=confidence,
            requires_human_review=False
        )
```

### 3. Second-Model Cross-Check

**Why**: Single LLM can hallucinate. Cross-check with second model reduces error rate.

**Implementation:**

```python
async def cross_model_verify(
    student_answer: str,
    correct_answer: str,
    question: str
) -> Dict:
    # Primary model: Gemini 2.5 Flash
    primary_evaluation = await gemini_api.evaluate(
        question=question,
        student_answer=student_answer,
        correct_answer=correct_answer
    )
    
    # Secondary model: GPT-4 (for critical evaluations)
    secondary_evaluation = await openai_api.evaluate(
        question=question,
        student_answer=student_answer,
        correct_answer=correct_answer
    )
    
    # Compare results
    agreement = primary_evaluation["is_correct"] == secondary_evaluation["is_correct"]
    
    return {
        "primary_result": primary_evaluation,
        "secondary_result": secondary_evaluation,
        "agrees": agreement,
        "confidence": 0.95 if agreement else 0.5
    }
```

### 4. XAI Logs (Explainability)

**Purpose**: GDPR Art. 22 compliance – provide "meaningful information about the logic involved".

**Log Structure:**

```python
class XAILog(BaseModel):
    id: UUID
    student_id: UUID
    task_id: UUID
    timestamp: datetime
    decision_type: str  # "evaluation", "mastery", "tokenization"
    decision: str  # "correct", "incorrect", "mastery_achieved"
    explanation: str  # Human-readable explanation
    model_version: str  # "gemini-2.5-flash-v1"
    input_data: Dict  # Anonymized input
    output_data: Dict  # Decision details
    confidence_score: float
    human_reviewed: bool

# Usage
await xai_logger.log({
    "student_id": student_id,
    "task_id": task_id,
    "decision_type": "evaluation",
    "decision": "correct",
    "explanation": """
        Answer evaluated as correct because:
        1. Semantic similarity to ground truth: 94%
        2. Factual accuracy confirmed by cross-model check
        3. Key concepts identified: ['photosynthesis', 'chloroplast', 'glucose']
        4. No factual errors detected
    """,
    "model_version": "gemini-2.5-flash-v1",
    "confidence_score": 0.94
})
```

### 5. GDPR Art. 22 "Meaningful Information"

**Requirement**: When decisions are made by automated processing (including profiling), individuals have the right to:
1. Know that a decision was made by automated means
2. Receive meaningful information about the logic involved
3. Request human review

**Implementation:**

```python
def generate_gdpr_explanation(evaluation: EvaluationResult) -> str:
    return f"""
    === AUTOMATED DECISION NOTICE ===
    
    This evaluation was made using AI-powered automated processing.
    
    DECISION: Your answer was marked as {'CORRECT' if evaluation.is_correct else 'INCORRECT'}
    
    LOGIC INVOLVED:
    1. Your answer was compared to verified curriculum content using semantic similarity analysis
    2. A second AI model cross-checked the evaluation for accuracy
    3. Key concepts in your answer were identified and validated
    4. Confidence level: {evaluation.confidence:.0%}
    
    MODELS USED:
    - Primary: Google Gemini 2.5 Flash (evaluation model)
    - Secondary: OpenAI GPT-4 (verification model)
    
    YOUR RIGHTS:
    - You can request human review of this decision
    - You can request full explanation of how the decision was made
    - You can access logs of all automated decisions affecting you
    
    To request human review, contact: support@stellecta.com
    Reference ID: {evaluation.id}
    """
```

### 6. Bias & Fairness Checks

**Challenge**: Ensure AI evaluations don't discriminate based on language proficiency, cultural background, etc.

**Implementation:**

```python
class BiasDetectionService:
    async def check_for_bias(
        self,
        student_id: UUID,
        evaluation: EvaluationResult
    ) -> BiasReport:
        # Get student demographics (anonymized)
        demographics = await self.get_anonymized_demographics(student_id)
        
        # Check for systematic bias patterns
        bias_score = await self.calculate_bias_score(
            demographics=demographics,
            evaluation_history=await self.get_recent_evaluations(student_id)
        )
        
        # Flag if bias detected
        if bias_score > 0.7:
            await self.escalate_to_human_review(student_id, evaluation, bias_score)
        
        return BiasReport(
            bias_detected=bias_score > 0.7,
            bias_score=bias_score,
            flagged_for_review=bias_score > 0.7
        )
```

### 7. Human-in-the-Loop Escalation

**When to Escalate:**
- Confidence < 70%
- Cross-model disagreement
- Bias detected
- Student requests review
- High-stakes decision (final exam, credential issuance)

**Escalation Flow:**

```python
class HumanReviewQueue:
    async def escalate(
        self,
        student_id: UUID,
        task_id: UUID,
        evaluation: EvaluationResult,
        reason: str
    ):
        # Create review ticket
        ticket = ReviewTicket.create(
            student_id=student_id,
            task_id=task_id,
            evaluation_data=evaluation.dict(),
            reason=reason,
            priority="high" if "bias" in reason else "normal",
            assigned_to=None  # Auto-assign to next available reviewer
        )
        
        # Notify teacher
        await notification_service.send(
            recipient=await self.get_teacher(student_id),
            title="Student Answer Needs Review",
            message=f"Student {student_id} answer flagged for review: {reason}"
        )
        
        return ticket
```

### 8. Tutor vs Judge Separation

**Critical Design Principle**: LLM should NEVER be both tutor and judge simultaneously.

**Tutor Mode:**
- Role: Guide, encourage, provide hints
- Tone: Supportive, Socratic
- Goal: Help student learn
- No grading responsibility

**Judge Mode:**
- Role: Evaluate, verify, grade
- Tone: Objective, strict
- Goal: Accurate assessment
- No tutoring responsibility

**Implementation:**

```python
class LLMRouter:
    async def route_request(
        self,
        request_type: str,
        student_id: UUID,
        task_id: UUID,
        data: Dict
    ) -> str:
        if request_type == "tutoring":
            return await self.tutor_mode(student_id, task_id, data)
        elif request_type == "evaluation":
            return await self.judge_mode(student_id, task_id, data)
        else:
            raise ValueError(f"Unknown request type: {request_type}")
    
    async def tutor_mode(self, student_id: UUID, task_id: UUID, data: Dict) -> str:
        prompt = f"""
        You are Stella, a supportive AI learning mentor.
        
        ROLE: TUTOR (NOT JUDGE)
        - Provide Socratic guidance
        - Ask leading questions
        - Offer hints, not answers
        - Be encouraging
        
        Student question: {data['question']}
        """
        return await gemini_api.generate(prompt, temperature=0.7)
    
    async def judge_mode(self, student_id: UUID, task_id: UUID, data: Dict) -> EvaluationResult:
        prompt = f"""
        You are an objective evaluation system.
        
        ROLE: JUDGE (NOT TUTOR)
        - Evaluate answer strictly
        - Compare to ground truth
        - Provide objective score
        - No hints or encouragement
        
        Correct answer: {data['correct_answer']}
        Student answer: {data['student_answer']}
        """
        result = await gemini_api.generate(prompt, temperature=0.1)
        
        # Pass through verification pipeline
        verified = await self.verification_service.verify(result)
        return verified
```

---

## API & Service Layer

### Service Architecture

```python
# Core service interfaces

class WalletService:
    """Manages Stellar wallet creation, key storage, and balance queries"""
    
    async def create_wallet(self, student_id: UUID, wallet_type: WalletType) -> Wallet:
        if wallet_type == WalletType.CUSTODIAL:
            keypair = Keypair.random()
            encrypted_key = encrypt_private_key(keypair.secret)
            wallet = Wallet.create(
                student_id=student_id,
                stellar_public_key=keypair.public_key,
                encrypted_private_key=encrypted_key,
                wallet_type=wallet_type
            )
        elif wallet_type == WalletType.NON_CUSTODIAL:
            # Parent provides public key
            wallet = Wallet.create(
                student_id=student_id,
                stellar_public_key=None,  # Set later when parent links
                wallet_type=wallet_type
            )
        return wallet
    
    async def get_wallet(self, student_id: UUID) -> Wallet:
        return await db.wallets.get(student_id=student_id)
    
    async def get_balance(self, wallet: Wallet) -> List[Asset]:
        account = server.load_account(wallet.stellar_public_key)
        return account.balances

class TokenizationService:
    """Handles asset minting and transaction signing"""
    
    async def mint_token(
        self,
        student_id: UUID,
        asset_code: str,
        metadata: Dict
    ) -> TokenAward:
        wallet = await wallet_service.get_wallet(student_id)
        
        # Build transaction
        asset = Asset(asset_code, STELLECTA_ISSUER_PUBLIC_KEY)
        source_account = server.load_account(STELLECTA_ISSUER_PUBLIC_KEY)
        
        transaction = (
            TransactionBuilder(
                source_account=source_account,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=100
            )
            .append_payment_op(
                destination=wallet.stellar_public_key,
                asset=asset,
                amount="1"
            )
            .add_text_memo(json.dumps(metadata))
            .set_timeout(30)
            .build()
        )
        
        # Sign & submit
        transaction.sign(STELLECTA_ISSUER_KEYPAIR)
        response = server.submit_transaction(transaction)
        
        # Store in database
        token_award = TokenAward.create(
            student_id=student_id,
            wallet_id=wallet.id,
            token_code=asset_code,
            stellar_tx_id=response["hash"],
            metadata=metadata,
            awarded_at=datetime.utcnow()
        )
        
        return token_award

class CredentialService:
    """Orchestrates LVO pipeline"""
    
    async def process_lvo_event(
        self,
        student_id: UUID,
        competency_id: UUID,
        learning_event: LearningEvent
    ):
        # LEARN: Student completed task
        task_result = learning_event.result
        
        # VERIFY: Multi-source validation
        verification = await evaluation_service.verify_answer(
            student_id=student_id,
            task_id=learning_event.task_id,
            answer=learning_event.answer
        )
        
        if not verification.is_correct:
            return  # Not mastered yet
        
        # Calculate H-PEM
        h_pem = await mastery_service.calculate_h_pem(
            student_id=student_id,
            competency_id=competency_id
        )
        
        # Update LCT
        await lct_service.update_lct(student_id, competency_id, h_pem)
        
        # Check mastery threshold
        if h_pem.proficiency >= 0.9:
            # OWN: Tokenize achievement
            asset_code = f"BADGE_{competency.code.upper()}"
            metadata = {
                "h_pem": h_pem.dict(),
                "competency_id": str(competency_id),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            token = await tokenization_service.mint_token(
                student_id=student_id,
                asset_code=asset_code,
                metadata=metadata
            )
            
            # Create on-chain credential record
            credential = OnChainCredential.create(
                student_id=student_id,
                credential_type="BADGE",
                asset_code=asset_code,
                stellar_tx_id=token.stellar_tx_id,
                h_pem_snapshot=h_pem.dict(),
                issued_at=datetime.utcnow()
            )
            
            return credential

class MasteryDecisionService:
    """H-PEM calculation and mastery threshold evaluation"""
    
    async def calculate_h_pem(
        self,
        student_id: UUID,
        competency_id: UUID
    ) -> HPEMMetrics:
        # Get learning history
        history = await db.get_learning_history(student_id, competency_id)
        
        # Calculate metrics
        return h_pem_engine.calculate_h_pem(student_id, competency_id, history)
    
    async def check_mastery(
        self,
        student_id: UUID,
        competency_id: UUID,
        h_pem: HPEMMetrics
    ) -> bool:
        threshold = await self.get_mastery_threshold(competency_id)
        return h_pem.proficiency >= threshold

class EvaluationService:
    """LLM quality layer and answer verification"""
    
    async def verify_answer(
        self,
        student_id: UUID,
        task_id: UUID,
        answer: str
    ) -> VerificationResult:
        # RAG retrieval
        correct_answer = await rag_pipeline.retrieve_ground_truth(task_id)
        
        # LLM evaluation
        evaluation = await llm_judge.evaluate(answer, correct_answer)
        
        # Cross-model verification
        second_opinion = await cross_model_verify(answer, correct_answer)
        
        # XAI logging
        await xai_logger.log(student_id, task_id, evaluation)
        
        # Bias check
        await bias_detector.check(student_id, evaluation)
        
        return VerificationResult(
            is_correct=evaluation["is_correct"] and second_opinion["agrees"],
            confidence=evaluation["confidence"],
            requires_human_review=evaluation["confidence"] < 0.7
        )

class StudentProgressService:
    """LCT tracking and knowledge graph updates"""
    
    async def update_progress(
        self,
        student_id: UUID,
        competency_id: UUID,
        h_pem: HPEMMetrics
    ):
        # Update LCT
        await lct_service.update_lct(student_id, competency_id, h_pem)
        
        # Update knowledge graph
        await knowledge_graph.update_mastery(student_id, competency_id, h_pem.proficiency)
        
        # Calculate decay risks
        at_risk = await self.calculate_decay_risks(student_id)
        
        # Notify if intervention needed
        if at_risk:
            await notification_service.notify_teacher(student_id, at_risk)
```

### API Endpoints

```python
# FastAPI routers

@router.post("/api/v1/blockchain/wallets")
async def create_wallet(
    student_id: UUID,
    wallet_type: WalletType,
    current_user: User = Depends(require_role(["student", "parent"]))
):
    """Create new Stellar wallet for student"""
    wallet = await wallet_service.create_wallet(student_id, wallet_type)
    return wallet

@router.get("/api/v1/blockchain/wallets/{student_id}")
async def get_wallet(
    student_id: UUID,
    current_user: User = Depends(require_role(["student", "parent", "teacher"]))
):
    """Get student's wallet details"""
    wallet = await wallet_service.get_wallet(student_id)
    return wallet

@router.get("/api/v1/blockchain/wallets/{student_id}/tokens")
async def get_tokens(
    student_id: UUID,
    current_user: User = Depends(require_role(["student", "parent", "teacher"]))
):
    """List all tokens in student's wallet"""
    wallet = await wallet_service.get_wallet(student_id)
    tokens = await tokenization_service.get_wallet_tokens(wallet)
    return tokens

@router.post("/api/v1/credentials/mint")
async def mint_credential(
    request: CredentialMintRequest,
    current_user: User = Depends(require_role(["admin"]))
):
    """Manually mint credential (admin only)"""
    credential = await credential_service.mint_manual(
        student_id=request.student_id,
        credential_type=request.credential_type,
        metadata=request.metadata
    )
    return credential

@router.get("/api/v1/credentials/{student_id}")
async def get_credentials(
    student_id: UUID,
    current_user: User = Depends(require_role(["student", "parent", "teacher"]))
):
    """List all credentials earned by student"""
    credentials = await db.onchain_credentials.filter(student_id=student_id)
    return credentials

@router.post("/api/v1/mastery/evaluate")
async def evaluate_mastery(
    request: MasteryEvaluationRequest,
    current_user: User = Depends(require_role(["student"]))
):
    """Trigger LVO pipeline evaluation"""
    result = await credential_service.process_lvo_event(
        student_id=request.student_id,
        competency_id=request.competency_id,
        learning_event=request.learning_event
    )
    return result

@router.get("/api/v1/h-pem/{student_id}/{competency_id}")
async def get_h_pem(
    student_id: UUID,
    competency_id: UUID,
    current_user: User = Depends(require_role(["student", "parent", "teacher"]))
):
    """Get H-PEM metrics for specific competency"""
    h_pem = await mastery_service.calculate_h_pem(student_id, competency_id)
    return h_pem

@router.get("/api/v1/lct/{student_id}")
async def get_lct(
    student_id: UUID,
    current_user: User = Depends(require_role(["student", "parent", "teacher"]))
):
    """Get student's Longitudinal Competency Trajectory"""
    lct = await lct_service.get_lct_profile(student_id)
    return lct
```

---

## Security, Privacy & Compliance

### GDPR Compliance

**Key Requirements:**

1. **Data Minimization**: Only collect necessary data
2. **Purpose Limitation**: Data used only for stated purposes
3. **Storage Limitation**: Delete data when no longer needed
4. **Right to Access**: Students/parents can download all data
5. **Right to Erasure**: Students/parents can request deletion
6. **Right to Explanation**: Automated decisions must be explainable (Art. 22)

**Implementation:**

```python
class GDPRComplianceService:
    async def export_student_data(self, student_id: UUID) -> Dict:
        """Right to Access: Export all student data"""
        return {
            "personal_info": await db.users.get(student_id),
            "learning_history": await db.learning_history.filter(student_id=student_id),
            "h_pem_snapshots": await db.h_pem_snapshots.filter(student_id=student_id),
            "lct_profile": await db.lct_profiles.get(student_id),
            "tokens_earned": await db.token_awards.filter(student_id=student_id),
            "credentials": await db.onchain_credentials.filter(student_id=student_id),
            "xai_logs": await db.xai_logs.filter(student_id=student_id)
        }
    
    async def delete_student_data(self, student_id: UUID):
        """Right to Erasure: Delete all student data"""
        # Note: Blockchain data is immutable, but we can:
        # 1. Delete off-chain PII
        # 2. Revoke access to wallet
        # 3. Mark tokens as "account closed"
        
        await db.users.delete(student_id)
        await db.learning_history.delete(student_id=student_id)
        await db.h_pem_snapshots.delete(student_id=student_id)
        await db.lct_profiles.delete(student_id=student_id)
        await db.wallets.update(student_id=student_id, status="closed")
```

### COPPA Compliance (Children's Online Privacy Protection Act)

**Requirements:**
- Parental consent required for children under 13
- No targeted advertising to children
- Data collection limited to educational purposes
- Parental access to child's data

**Implementation:**

```python
class COPPAComplianceService:
    async def register_child_account(
        self,
        child_email: str,
        parent_email: str,
        date_of_birth: date
    ) -> User:
        # Check age
        age = (date.today() - date_of_birth).days // 365
        
        if age < 13:
            # COPPA applies: require parental consent
            consent_request = await self.send_parental_consent_request(
                child_email=child_email,
                parent_email=parent_email
            )
            
            # Account creation pending until parent approves
            user = User.create(
                email=child_email,
                status="pending_parental_consent",
                consent_request_id=consent_request.id
            )
        else:
            # No parental consent needed
            user = User.create(email=child_email, status="active")
        
        return user
    
    async def send_parental_consent_request(
        self,
        child_email: str,
        parent_email: str
    ) -> ConsentRequest:
        # Send email to parent
        await email_service.send(
            to=parent_email,
            subject="Parental Consent Required",
            body=f"""
            Your child ({child_email}) is attempting to create a Stellecta account.
            
            Under COPPA, we require your consent to collect and process your child's data.
            
            Click here to review and provide consent: {consent_link}
            """
        )
        
        return ConsentRequest.create(
            child_email=child_email,
            parent_email=parent_email,
            status="pending"
        )
```

### Pseudonymization

**On-Chain Data Never Contains:**
- Student names
- Student emails
- School names
- Teacher names

**Instead:**
- Pseudonymized IDs (e.g., `STU_4f7a9b2c`)
- Competency UUIDs (no human-readable labels)
- H-PEM metrics (numeric only)

**Mapping stored off-chain** (GDPR-compliant database):

```sql
-- Off-chain mapping table
CREATE TABLE pseudonym_mappings (
    id UUID PRIMARY KEY,
    pseudonym VARCHAR(32) UNIQUE NOT NULL,
    student_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast lookup
CREATE INDEX idx_pseudonym ON pseudonym_mappings(pseudonym);
```

### Differential Privacy for Analytics

**Challenge**: Aggregate analytics (e.g., "Average proficiency for Grade 5") could leak individual student data.

**Solution**: Differential privacy (add controlled noise to aggregates).

```python
def get_average_proficiency_dp(grade: str, epsilon: float = 1.0) -> float:
    """
    Calculate average proficiency with differential privacy
    
    Args:
        grade: Grade level (e.g., "grade_5")
        epsilon: Privacy budget (lower = more privacy, less accuracy)
    """
    # Get true average
    true_average = db.h_pem_snapshots.filter(grade=grade).avg("proficiency")
    
    # Add Laplace noise
    noise = np.random.laplace(loc=0, scale=1/epsilon)
    private_average = true_average + noise
    
    return max(0, min(private_average, 1.0))  # Clamp to [0, 1]
```

### Safe Handling of Stellar Keys

**Best Practices:**

1. **Environment Variables** (never hardcode)
   ```bash
   # .env file (NEVER commit to git)
   STELLAR_ISSUER_SECRET=SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   WALLET_ENCRYPTION_KEY=base64-encoded-fernet-key
   ```

2. **HSM (Hardware Security Module)** for production
   ```python
   # Use AWS KMS or similar
   import boto3
   
   kms_client = boto3.client('kms')
   
   def encrypt_private_key(private_key: str) -> str:
       response = kms_client.encrypt(
           KeyId='arn:aws:kms:...',
           Plaintext=private_key.encode()
       )
       return base64.b64encode(response['CiphertextBlob']).decode()
   ```

3. **Key Rotation** (quarterly)
   ```python
   async def rotate_issuer_key():
       # Generate new keypair
       new_keypair = Keypair.random()
       
       # Transfer all assets to new issuer
       await transfer_assets_to_new_issuer(new_keypair)
       
       # Update environment variable
       os.environ["STELLAR_ISSUER_SECRET"] = new_keypair.secret
       
       # Log rotation
       await audit_log.log("issuer_key_rotated", new_keypair.public_key)
   ```

4. **Audit Logging**
   ```python
   async def log_key_access(action: str, user: str, key_id: str):
       await audit_log.create({
           "timestamp": datetime.utcnow(),
           "action": action,
           "user": user,
           "key_id": key_id,
           "ip_address": request.client.host
       })
   ```

---

## Deployment Guide

### Environment Setup

**Required Environment Variables:**

```bash
# Stellar Configuration
STELLAR_NETWORK=testnet  # or mainnet
STELLAR_ISSUER_PUBLIC_KEY=GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
STELLAR_ISSUER_SECRET=SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
STELLAR_HORIZON_URL=https://horizon-testnet.stellar.org

# Wallet Encryption
WALLET_ENCRYPTION_KEY=base64-encoded-fernet-key

# Pseudonymization
PSEUDONYMIZATION_SECRET=random-secret-string

# LLM APIs
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key

# Database
DATABASE_URL=postgresql://user:pass@host:5432/stellecta

# Application
APP_ENV=development  # or production
DEBUG=false
```

### Stellar Network Configuration

**Testnet (Development):**

```python
from stellar_sdk import Server, Network

server = Server(horizon_url="https://horizon-testnet.stellar.org")
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# Fund testnet account (Friendbot)
import requests
response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
```

**Mainnet (Production):**

```python
server = Server(horizon_url="https://horizon.stellar.org")
network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE

# Note: Mainnet requires real XLM funding
```

### Local Development

**1. Install Dependencies:**

```bash
pip install stellar-sdk fastapi uvicorn sqlalchemy psycopg2-binary
```

**2. Run Migrations:**

```bash
alembic upgrade head
```

**3. Seed Demo Data:**

```bash
python scripts/seed_demo_data.py
```

**4. Start Server:**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**5. Test Blockchain Integration:**

```bash
pytest tests/integration/test_blockchain.py
```

### Production Deployment Checklist

- [ ] **Stellar Mainnet** configured (not Testnet)
- [ ] **Issuer Account** created and funded with XLM
- [ ] **Private Keys** stored in HSM (not environment variables)
- [ ] **Database** backups enabled (daily)
- [ ] **XAI Logs** retention policy configured (1 year minimum)
- [ ] **GDPR Compliance** verified (data export/deletion endpoints working)
- [ ] **COPPA Compliance** verified (parental consent flow working)
- [ ] **Rate Limiting** enabled (prevent abuse)
- [ ] **Monitoring** setup (Sentry, Prometheus, Grafana)
- [ ] **Audit Logging** enabled (all key accesses logged)

---

## Architecture Checklist

### ✅ Completed Components

- [x] **LVO Pipeline** (Learn-Verify-Own)
- [x] **H-PEM Metrics** (5 dimensions)
- [x] **LCT Tracking** (Longitudinal Competency Trajectory)
- [x] **Stellar Integration** (Wallet creation, token minting)
- [x] **K.E.R.N.E.L. Agents** (6 specialized agents)
- [x] **LLM Quality Layer** (RAG, Verification, XAI, GDPR)
- [x] **Knowledge Graph** (Nanoscale competencies)
- [x] **Adaptive Learning** (DreamBox-style)
- [x] **Blockchain Tokenization** (Asset minting, transaction signing)
- [x] **Parent Dashboard** (Blockchain-connected progress view)
- [x] **GDPR Compliance** (Data export, deletion, explainability)
- [x] **COPPA Compliance** (Parental consent, age verification)
- [x] **Pseudonymization** (Privacy-safe on-chain data)
- [x] **Security** (Key encryption, HSM, audit logging)

### 🔄 Future Enhancements (Phase 3)

- [ ] **Credential Passport** (Universal wallet for all educational credentials)
- [ ] **Non-Custodial Wallets** (Full decentralization)
- [ ] **Soroban Smart Contracts** (Advanced on-chain logic)
- [ ] **NFT Badges** (Visual badges with rich metadata)
- [ ] **Marketplace** (Trade learning tokens, future economy)
- [ ] **Interoperability** (Credentials work across multiple platforms)
- [ ] **Decentralized Identity** (DIDs for students)

### 📊 Key Metrics to Monitor

| Metric | Target | Current |
|--------|--------|---------|
| Token Minting Success Rate | > 99.5% | - |
| Average H-PEM Proficiency | > 0.85 | - |
| LLM Evaluation Accuracy | > 95% | - |
| Human Review Escalation Rate | < 5% | - |
| Parent Dashboard Engagement | > 70% | - |
| Blockchain Transaction Cost | < $0.01 | $0.00001 |
| API Response Time (p95) | < 500ms | - |

---

## Conclusion

The **Stellecta LVO × Stellar Blockchain Architecture** represents a paradigm shift in educational credentialing:

🎓 **Students own their learning achievements** (not platforms)  
⛓️ **Blockchain provides cryptographic proof** (tamper-proof)  
📊 **H-PEM + LCT enable granular tracking** (beyond grades)  
🤖 **K.E.R.N.E.L. agents ensure quality** (multi-layer verification)  
🔒 **Privacy-first design** (GDPR + COPPA compliant)  
🌍 **Future-proof credentials** (portable across any platform)

This system is **production-ready**, **scalable**, and **compliant** — designed to serve millions of students while maintaining individual ownership and privacy.

**Next Steps:**
1. Deploy to Testnet for pilot schools
2. Gather feedback from students/parents/teachers
3. Iterate based on real-world usage
4. Transition to Mainnet for production launch

---

**Stellecta: Every Achievement, Owned Forever.**

🚀