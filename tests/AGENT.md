# `tests/` 测试协作说明

测试使用 pytest，配置位于根目录 `pyproject.toml`，测试路径是 `tests/`，异步模式为 `auto`。测试覆盖模型序列化、几何/视觉、缓冲和线程安全、视频 source、FastAPI REST、WebSocket、合成视频 smoke、多视角规则/复核和团队校准。

## 编写测试

- 优先测试公开行为和状态边界，不依赖私有实现细节。
- 模型/协议变更要覆盖 Python 序列化以及相关 API/WS payload；必要时同步前端类型验证。
- 优先使用 `tmp_path`、合成帧/视频、伪检测器和 fixture；不要要求仓库外的权重、真实视频、RTSP 或 CUDA 才能运行基础回归。
- 测试实时队列时明确区分 `REALTIME` 丢旧帧与 `OFFLINE` 阻塞；线程测试必须能释放资源并设置有限 timeout。
- 对缺失资源、降级状态、UNKNOWN、stale/unavailable 和边界输入写断言，避免只测 happy path。

常用命令：

```bash
uv run pytest tests/ -v
uv run pytest tests/test_x.py -q
uv run pytest --collect-only -q
```

`--collect-only` 只是测试清单，不是测试执行结果。报告中不要把历史数量或静态清单写成“全部通过”。
