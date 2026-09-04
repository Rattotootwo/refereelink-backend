# `app/server/` 服务端协作说明

## 结构

- `main.py`：FastAPI 应用组装、启动参数和共享状态初始化。
- `api/`：health、status、events、pipeline、team-calibration、multiview REST 路由。
- `ws/state.py`：`/ws/state` WebSocket 路由；具体广播与命令处理在 `app/services/publisher.py`。

## 协议边界

- `/health` 是存活检查；`/api/status`、`/api/config`、`/api/events` 提供结构化 JSON。
- `/api/pipeline/start` 和 `/api/pipeline/stop` 控制推理生命周期；配置更新必须经过 `PipelineConfig` 校验。
- `/ws/state` 服务端推送 `FrameState`、`MetricsSnapshot` 和校准状态，客户端发送 `start`、`stop`、`update_config` 命令。
- `/video/stream` 是独立的 `multipart/x-mixed-replace` MJPEG 流；不要通过 WebSocket 发送图像或在路由中重复执行模型推理。

保持路由薄：业务状态放在 store/service/pipeline，避免把长时间运行的同步工作直接放入 async 路由。连接断开、重复启动、缺少模型/视频和无可用帧都应有可预测的降级行为。

## 修改后的检查

```bash
uv run pytest tests/test_api.py tests/test_websocket.py tests/test_frame_encoder.py tests/test_team_calibration_clip_api.py tests/test_multiview_api.py -q
```

涉及 JSON 字段时，同时更新 `web/src/types/messages.ts` 或 `web/src/types/multiview.ts`，并验证 REST 与 WebSocket 的序列化结果。
