# `app/multiview/` 多视角犯规复核说明

## 模块职责

- `models.py`：案例、视角、证据、事实、规则评估、判定和复核记录模型。
- `repository.py`：从 `assets/multiview/cases.json` 解析案例并解析受控媒体路径。
- `inference.py`：可选 SoccerNet VARS/MViT 推理；代码与权重是外部运行时资产。
- `localization.py`：时空 Grad-CAM、attention gate、光流 fallback 和证据框。
- `rules.py`、`geometry.py`：确定性规则、Law 12 相关结构化结果和场地几何。
- `review_store.py`：SQLite 复核记录、版本冲突和历史；默认运行时库位于 `var/`。
- `service.py`、`explanation.py`：服务编排和受保护的本地解释文案路径。

## 证据链约束

模型动作/严重度是 evidence，不是 ground truth；规则引擎的 canonical assessment 与人工确认事实决定可复核的结论。事实被修改后，过期的判定/解释必须失效或重新生成。解释器只能复述已确认事实和确定性规则，不能补造球员身份、动作、牌级或重启方式。

缺少外部模型、权重、真实视频或 CUDA 时可以使用案例中的 scripted fallback；必须把模式、前置条件和 fallback 状态呈现清楚，不能把 fallback 当作真实模型验证。

```bash
uv run pytest tests/test_multiview_*.py tests/test_events.py -q
```
