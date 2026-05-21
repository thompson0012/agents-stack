# Goal-QA-Driven Development Methodology

## Core Idea

人類專注於決策、邊界條件與驗收標準；AI 負責架構展開與編碼實作。

## The Pipeline

spec → plan → tasks → implement → qa → release

### spec
產出：spec.md
內容：Core Goal, User Stories, Edge Cases, BDD Acceptance Criteria (Given-When-Then), Out of Scope
核心問題：我們要做什麼？怎麼驗收？

### plan
產出：plan.md
內容：Architecture Decisions, API Design, DB Schema, Impact Analysis, Test Strategy, Risks
核心問題：系統層面怎麼做？影響哪些模組？

### tasks
產出：tasks.md
內容：Task checklist，每個 task 附 5 維驗收元資料
核心問題：如何拆解成可獨立執行的小步驟？

### implement
產出：程式碼 + handoff.md
方法：TDD — 每個 task 先寫測試再實作，通過後才進行下一個
核心原則：實作 ≠ 驗收

### qa
產出：qa-report.md
方法：獨立 worker 重現實作，逐條驗證 SPEC 的 Acceptance Criteria
核心原則：Generator ≠ Auditor

### release
產出：changelog.md + archive
動作：記錄變更、更新 reference、封存工作流

## 5-Dimension Task Verification

每個 task 嵌入 5 個維度的驗收資訊：

1. Align Spec — 對應到 SPEC.md 哪個章節
2. Coverage Checklist — 涵蓋哪些需求/edge case
3. Deliverables — 產出哪些檔案
4. Verification Checkpoints — 可測試的通過條件
5. Definition of Done — 品質底線

## Three-Layer Rework

QA 發現問題時 root cause 追蹤：

L1 (code) → implement phase 返工
L2 (architecture) → plan phase 返工
L3 (requirement) → spec phase 返工

越早發現，成本越低。
