# Foul Candidate Detection Trade-offs

## 防噪机制（已实现，已通过单元测试）
原始 MVFoul 逐帧推理会在 10 秒片段（约 300 帧）内产生数百个原始预测。引入两个过滤器：
1. **置信度阈值**（默认由 `InferencePipeline.foul_confidence_threshold` 提供，默认 0.48）：
   丢弃弱预测。
2. **冷却帧数**（默认由 `InferencePipeline.foul_cooldown_frames` 提供，默认 25 帧）：
   同一个动作不会连续触发。

**测试证据**：
- `test_drops_noise_on_ten_second_clip`：300 帧推理后候选数 < 15。
- `test_avoids_zero_detections_on_foul_clip`：犯规片段至少输出 1 个候选。
- `test_weak_inference_output_is_filtered`：推理生成的低置信度预测被过滤。

## MVFoul 降级预留（静态设计，尚未实现真实降级）
当前仍使用 MVFoul 作为后端模型。`cooldown_frames` 和 `confidence_threshold` 由
`InferencePipeline` 的 `foul_cooldown_frames` 和 `foul_confidence_threshold` 参数控制。
**当前 CLI 尚未暴露这两个参数。** 未来轻量级降级方案（替换 `predict_foul_from_frames`
或提前返回 None）尚未实现，也未在真实 CUDA 环境做对比 benchmark。

**状态说明**：
- #69 中“避免 10 秒片段产生数百个检测”与“犯规片段不产生 0 检测”这两个验收目标
  已通过单元测试验证。
- #69 中“比较 MVFoul 替代方案并在过重时降级”这一验收目标 **未完成**，需要在后续 PR
  中补充 benchmark 和降级实现。

## 已知局限性（需真实模型/视频验证）
- 无法区分“合理冲撞”和“恶意犯规”，仅输出可疑候选。
- 远距离视角（>40m）准确率下降。
- 本模块只输出候选，最终判罚由规则引擎和人工复核决定（见 `app/multiview/` 和
  `app/events/engine.py` 的 `FoulEventAdapter`）。
**状态**：上述结论基于代码逻辑和现有文档，未执行真实场景 benchmark。