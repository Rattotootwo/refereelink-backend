# `docs/` 文档与验证 Artifact 说明

架构和路线图文档描述系统边界；性能 JSON、诊断 JSON/JPG 是带时间/环境上下文的证据 Artifact，不应被当作当前实时状态或完整质量证明。

更新文档时以代码和实际执行结果为准，标明“已执行”“静态清单”“历史结果”“需要真实模型/CUDA/视频”等状态。涉及 `FrameState`、接口、运行参数、阶段验收或降级行为的改动，应同时检查 README、SETUP_GUIDE、`ARCHITECTURE.md` 和 `ROADMAP.md` 是否仍一致。
