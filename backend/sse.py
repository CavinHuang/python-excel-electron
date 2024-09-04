import asyncio
import logging
from aiohttp import web

# 创建一个日志处理器，直接发送日志消息
class SSEHandler(logging.Handler):
    def __init__(self, sse_response):
        super().__init__()
        self.sse_response = sse_response
        self.loop = asyncio.get_event_loop()

    def emit(self, record):
        if record.name != 'aiohttp.access':  # 排除 HTTP 请求的日志
            log_entry = self.format(record)
            self.loop.create_task(self.send_log(log_entry))

    async def send_log(self, log_entry):
        try:
            await self.sse_response.write(f"data: {log_entry}\n\n".encode('utf-8'))
            await self.sse_response.drain()
        except Exception as e:
            print(f"发送日志时出错: {str(e)}")

# 创建一个日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 设置日志格式
log_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')

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

    # 为每个连接创建一个新的SSEHandler
    sse_handler = SSEHandler(response)
    sse_handler.setFormatter(log_formatter)
    logger.addHandler(sse_handler)

    try:
        while True:
            try:
                # 每30秒发送一次保活消息
                await asyncio.sleep(30)
                await response.write(b': keepalive\n\n')
                await response.drain()
            except asyncio.CancelledError:
                # 客户端断开连接
                break
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
    finally:
        # 移除处理器并关闭连接
        logger.removeHandler(sse_handler)
        await response.write_eof()

    return response
