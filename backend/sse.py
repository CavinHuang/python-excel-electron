import asyncio
import logging
from aiohttp import web

# 创建一个队列来存储日志消息
log_queue = asyncio.Queue()

# 创建一个日志处理器，将日志消息添加到队列中
class QueueHandler(logging.Handler):
    def emit(self, record):
        if record.name != 'aiohttp.access':  # 排除 HTTP 请求的日志
            log_entry = self.format(record)
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # 如果当前线程没有事件循环，创建一个新的
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                loop.call_soon_threadsafe(asyncio.create_task, self.send_log(log_entry))
            else:
                loop.run_until_complete(self.send_log(log_entry))

    async def send_log(self, log_entry):
        await log_queue.put(log_entry)

# 创建一个日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建一个日志处理器，将日志消息添加到队列中
queue_handler = QueueHandler()
# 设置日志格式 返回 时分秒 即可，例如：14:22:21。
queue_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(queue_handler)

async def sse_handler(request):
    response = web.StreamResponse(
        status=200,
        reason='OK',
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )
    await response.prepare(request)

    try:
        while True:
            try:
                message = await asyncio.wait_for(log_queue.get(), timeout=30)
                # message包含complate，表示任务完成
                if 'complate' in message:
                    print("==========complate")
                    await response.write(f"data: {message}\n\n".encode('utf-8'))
                    # 发送完成消息后，关闭连接
                    await response.write_eof()
                    break
                await response.write(f"data: {message}\n\n".encode('utf-8'))
                await response.drain()
            except asyncio.TimeoutError:
                # 发送保持连接的消息
                await response.write(b': keepalive\n\n')
                await response.drain()
            except asyncio.CancelledError:
                # 客户端断开连接
                break
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
    finally:
        await response.write_eof()

    return response
