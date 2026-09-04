# `app/pipeline/` 管线与生命周期说明

- `source.py`：`LocalFileSource` 与 `RTSPSource`。构造函数应保持非阻塞；首次读取才建立实际采集，RTSP 读取失败时按既定次数重连并更新 `StateStore` source 状态。
- `buffer.py`：`REALTIME` 满队列丢最旧帧，`OFFLINE` 满队列阻塞生产者；关闭时必须解除等待中的生产者/消费者。
- `engine.py`：推理线程协调去畸变、视觉核心、实体语义、事件和指标，并把结构化结果写入 store；停止、异常和 source 结束都要释放 source、buffer 和 recorder。
- `recorder.py`：可选地写最终标注帧到 MP4 调试产物，不应改变主推理结果。

时间戳要区分 source 交付帧的 capture time、处理完成时间和模型 forward latency。不要让浏览器连接、MJPEG 客户端、磁盘写入或无限重试阻塞实时推理；所有线程、队列、重连和后台任务都必须有明确退出路径。

修改管线时优先覆盖 source factory、reconnect、buffer drop/block/close、pipeline stop/error 和合成视频 smoke；真实模型/RTSP/CUDA 验证需单列环境条件。

```bash
uv run pytest tests/test_video_source.py tests/test_buffer.py tests/test_recorder.py tests/test_smoke_integration.py -q
```
