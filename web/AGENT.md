# `web/` 前端协作说明

## 技术与结构

这是 React 18 + TypeScript + Vite + Zustand 仪表盘。`src/components/` 放通用面板，`src/pages/` 放页面级视图，`src/hooks/useWebSocket.ts` 管理实时连接，`src/store/` 管理 UI 状态，`src/types/` 镜像后端 Pydantic 契约，`src/api/` 封装 REST 请求。开发服务器默认 `5173`，将 `/api`、`/ws`、`/video` 代理到 FastAPI `8000`。

## 数据与交互约束

- WebSocket 只消费结构化 `frame_state`、`metrics`、`team_calibration` 消息；视频使用 MJPEG `<img>`，不要在浏览器端运行 YOLO 或传输 Base64 视频。
- 后端模型字段、枚举、nullability 或默认值变更时，先同步 `src/types/`，再检查 store、组件和请求代码。
- 连接断开应保持可见状态并按现有策略重连；不要创建重复定时器或在 unmount 后更新状态。
- 控制面板发送的命令必须与后端允许的 command/config 字段一致；错误和不完整状态应可见，不要静默显示“正常”。

## 验证

```bash
npm run lint
npm run build
```

UI 行为变更还应结合后端运行状态做浏览器检查；仅 TypeScript 编译通过不等于视频、WebSocket 或接口交互已验证。
