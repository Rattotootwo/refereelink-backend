# Foul Candidate Detection Trade-offs

## 防噪机制（已实现，已通过单元测试）
原始 MVFoul 逐帧推理会在 10 秒片段（约 300 帧）内产生数百个原始预测。引入两个过滤器：
1. **置信度阈值**（默认 0.5）：丢弃弱预测。
2. **冷却帧数**（默认 25 帧，约 1 秒）：同一个动作不会连续触发。

**测试证据**：`test_drops_noise_on_ten_second_clip` 验证 300 帧推理后候选数 < 15；
`test_avoids_zero_detections_on_foul_clip` 验证犯规片段至少输出 1 个候选。

## MVFoul 降级预留（静态设计，尚未在真实部署中验证）
当前仍使用 MVFoul 作为后端模型，但 `cooldown_frames` 和 `confidence_threshold` 参数由调用方
（`InferencePipeline` 和 CLI）控制，为未来轻量级降级预留接口。若部署环境无法运行 MVFoul，
可在 `FoulDetector.__init__` 中提前返回 `None`，或替换 `predict_foul_from_frames` 的实现。
**状态**：代码已预留接口，未在真实 CUDA 环境执行降级对比。

## 已知局限性（需真实模型/视频验证）
- 无法区分“合理冲撞”和“恶意犯规”，仅输出可疑候选。
- 远距离视角（>40m）准确率下降。
- 本模块只输出候选，最终判罚由规则引擎和人工复核决定（见 `app/multiview/` 和 `app/events/engine.py`
  的 `FoulEventAdapter`）。
**状态**：上述结论基于代码逻辑和现有文档，未执行真实场景 benchmark。