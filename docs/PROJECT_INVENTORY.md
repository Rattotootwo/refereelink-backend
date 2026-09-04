# SC 当前项目清单

更新时间：2026-09-04

本文是当前代码与分支的整理清单，不是长期路线图。分支原始提交保持独立，产品完成度只按当前 `main` 的代码、测试和现有文档判断。

## 完成基线

### 已完成

- 赛前片段标注与 Track 标注。
- 角色/球队分队逻辑、质量评估、校验、bundle 和运行时分配。
- 多视角犯规案例、证据定位、规则评估、人工复核、SQLite 历史和受保护解释文案。

主要代码位于 `app/classification/team_calibration/`、`app/multiview/`、`app/server/` 和 `web/src/`，对应测试位于 `tests/test_team_calibration*.py`、`tests/test_role_calibration.py`、`tests/test_multiview_*.py`。

### 已实现但尚待真实部署验收

固定广角实时检测/跟踪、球场投影、足球状态、事件候选、REST、WebSocket、MJPEG 和 Dashboard 已有实现与测试，但仍需在目标设备、真实模型、真实视频和实际视频源条件下单独验收。

## 分支归位

| 分支 | 当前内容 | 归类 |
|---|---|---|
| `main` `0a7443b` | 完成基线与实时基础管线 | 产品主线 |
| `feature/live-foul-progress` `2515dac` | 几何犯规候选、异步 MVFoul worker、实时犯规 UI | 实时犯规进展 |
| `research/pitch-field` `396ae65` | broadcast camera、field registration、离线评估、训练和专项测试 | pitch/field 研究 |
| `demo/web-showcase` `8ed8d12` | 独立 Demo 入口、展示数据和页面 | Demo 展示 |
| `origin/weekly-report` `c4a3f36` | 周报、会话归档和周报工具 | 已删除分支/范围 |
| `dev-3d-cad` `13e06ca` | CAD/3D 源文件、导出模型和设计研究 | 已删除分支/范围 |

已删除临时分支：`agents/greeting-in-chinese`（`0a7443b`，与 `main` 同点）。

## 易混淆与累赘内容

- `app/classification/team.py` 和 `app/classification/online.py` 是旧 `TeamClassifier` 兼容层；生产基线是 `team_calibration`，本轮不删除旧接口。
- `app/foul_detection/detector.py` 是旧 `fouls_far` 适配器；`app/multiview/` 是多视角复核；`feature/live-foul-progress` 是实时犯规候选与异步 worker，三者不应混称为同一条链路。
- 当前 `app/geometry/`/`VisionCore` 面向固定广角；`research/pitch-field` 的 `app/field_registration/` 是另一套研究架构，不直接并入主线。
- `app.server.main` 是产品入口；`app/modes/` 的 radar/PySide6/QML 属于 legacy；`demo/web-showcase` 的根目录 `main.py` 不属于产品主线。
- `debug/`、`docs/remote_*`、`docs/test1_*` 和 benchmark JSON 是历史验证证据，不代表当前实时状态。

## 已确认删除清单

- CAD/3D：`cad/parts/`、`designs/3d/`、`docs/main_camera_dimension_study.md` 及 `dev-3d-cad` 分支。
- 周报：`docs/weekly_reports/`、`tools/generate_weekly_report.py`、`tools/codex_conversations/`（仅周报分支中的内容）及 `origin/weekly-report` 分支。
- 分支整理：删除 `agents/greeting-in-chinese`；将三个保留分支统一为 `feature/live-foul-progress`、`research/pitch-field`、`demo/web-showcase`。
- `.workbuddy/` 和已创建的 `AGENT.md` 不属于删除范围；`cad/AGENT.md` 仅保留为历史边界说明。

## 当前验证边界

本次整理不宣称测试已通过。执行整理后应运行：

```bash
uv run pytest tests/ -q
uv run ruff check app tests tools experiments
cd web && npm run lint && npm run build
```
