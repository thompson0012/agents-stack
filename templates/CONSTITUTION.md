# Constitution

這份文件是專案的技術章程，定義所有工作流必須遵守的不變量與規則。

## 核心不變量

1. **文件即狀態** — 所有 durable state 存放在 `.agents-stack/`
2. **單一活躍工作流** — 同一時間最多一個 non-parked workstream
3. **實作者 ≠ 驗收者** — implement 和 qa 必須分派給不同 worker
4. **Cold start 必須可用** — 從檔案即可恢復完整狀態
5. **迭代 ≠ 重試** — retry 修正執行，iteration 質疑前提

## 工作流規則

- spec phase 必須產出 BDD 格式的 Acceptance Criteria
- tasks phase 每個 task 必須包含 5 維驗收元資料
- implement 必須按 tasks.md 順序執行 TDD
- qa 必須獨立重現並逐條驗證 SPEC 的 AC
- 修改需求→先更新 spec，修改架構→先更新 plan

<!-- 在此添加專案特定的技術棧、編碼規範、架構約束 -->
