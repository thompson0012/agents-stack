# Constitution — agents-stack v3

這份文件是 agents-stack 的技術章程，定義所有工作流必須遵守的不變量與規則。

## 核心不變量

1. **文件即狀態** — 所有 durable state 存放在 `.agents-stack/`，對話記錄不是狀態
2. **單一活躍工作流** — 同一時間最多只有一個 non-parked workstream
3. **實作者 ≠ 驗收者** — implement 和 qa 必須分派給不同的 worker instance
4. **Cold start 必須可用** — 全新 agent 從檔案即可恢復完整狀態，不需對話歷史
5. **迭代 ≠ 重試** — retry 修正執行，iteration 質疑前提。重試不改變 contract；iteration 回到 spec/plan

## 檔案優先級

`.agents-stack/<id>/` 內檔案發生衝突時，依以下優先級判定：

qa-report.md > handoff.md > tasks.md > plan.md > spec.md > status.json > .agents-stack/tracked-work.json

## 檔案組織

.agents-stack/
├── <workstream-id>/     # 進行中的工作流 artifacts
│   ├── spec.md          # SPEC phase 產出
│   ├── plan.md          # PLAN phase 產出
│   ├── tasks.md         # TASKS phase 產出
│   ├── handoff.md       # IMPLEMENT phase 產出
│   ├── qa-report.md     # QA phase 產出
│   ├── changelog.md     # RELEASE phase 產出
│   └── status.json      # 當前 phase / layer / depth / attempt
├── tracked-work.json    # Workstream registry
├── reference/           # 穩定的專案知識（read-optimized）
│   ├── methodology.md   # 方法論說明
│   ├── architecture.md  # 專案架構
│   └── design.md        # 設計語言
├── insights/            # Session 回顧
├── archive/             # 已封存工作流
└── scripts/             # 工具腳本

## 工作流規則

- spec phase 必須產出 BDD 格式的 Acceptance Criteria（Given-When-Then）
- tasks phase 的每個 task 必須包含 5 維驗收元資料（Align Spec, Coverage, Deliverables, Checkpoints, DoD）
- implement phase 必須按照 tasks.md 順序執行 TDD，每個 task 通過才能進入下一個
- qa phase 必須獨立重現實作並逐條驗證 SPEC 的 AC
- 修改需求必須先更新 spec.md，不可直接改 code
- 發現架構問題必須先更新 plan.md，不可繞過 plan 直接改 tasks

## Reference 更新規則

- reference/ 是 read-optimized，AI 在工作流中不得直接修改
- 只有 release phase 結束時或開發者執行 /update-reference 命令才能更新
- release worker 比對 changelog 與 reference，提出更新建議

## 三層返工

qa-report.md 中的 FAIL 必須 trace 到 root cause layer：

| Layer | 範圍 | 觸發 | 回到 phase |
|-------|------|------|-----------|
| L1 | 程式碼實作 | 實作錯誤、edge case 漏掉 | implement（該 task 標記 [↩]）|
| L2 | 架構設計 | API/DB 設計不足 | plan（更新 plan.md → 重拆 tasks）|
| L3 | 需求規格 | Edge case 未定義、AC 遺漏 | spec（更新 spec.md → 重 plan）|

## 預算限制

- max_depth: 5（超過 → escalated_to_human）
- max_attempts: 3（超過 → escalated_to_human）
