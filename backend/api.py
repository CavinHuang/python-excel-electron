import json
import traceback
import os
from aiohttp import web
import aiohttp_cors
import aiofiles
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
import controller
from sse import sse_handler, logger
from excel.data_processor import process_excel

current_path = os.path.dirname(os.path.abspath(__file__))
tmp_file_path = os.path.join(current_path, 'tmpFiles')

# 确保上传目录存在
os.makedirs(tmp_file_path, exist_ok=True)

async def write_file(file_path, part):
  async with aiofiles.open(file_path, 'wb') as f:
    while True:
      chunk = await part.read_chunk()  # 默认大小为8192
      if not chunk:
        break
      await f.write(chunk)

## 上传文件 formData
async def add_task(request):
    print('add_task')

    try:
        tmp_file_path = 'uploads'
        os.makedirs(tmp_file_path, exist_ok=True)

        reader = await request.multipart()
        response_data = {}
        file_write_tasks = []
        excel_files = []

        while True:
            part = await reader.next()
            if part is None:
                break

            if part.filename:
                filename = part.filename
                file_path = os.path.join(tmp_file_path, filename)

                await write_file(file_path, part)

                response_data[part.name] = f"File '{filename}' uploaded successfully"

                if filename.endswith(('.xls', '.xlsx')):
                    excel_files.append(file_path)
            else:
                value = await part.text()
                response_data[part.name] = value

        print("All files have been written successfully.")

        isPrice = response_data.get('isPrice', '0') == '1'
        isFetchImg = response_data.get('isFetchImg', '0') == '1'
        # 启动数据处理的工作线程
        def process_data():
          process_excel(excel_files[0], isPrice, isFetchImg)
          print("Excel processing tasks have been completed.")

        processing_thread = threading.Thread(target=process_data)
        processing_thread.start()

        print(response_data)
        return web.json_response({"status": "success", "data": response_data})

    except Exception as e:
        print(f"Error in add_task: {str(e)}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)

app = web.Application()
app.add_routes([
  # web.get('/', handle),
  web.get('/controlApi', controller.controlApi),
  web.get('/t', controller.test),
  web.get('/logs', sse_handler),
  web.post('/add_task', add_task)
])

if __name__ == '__main__':
  cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
  for route in list(app.router.routes()):
    if route.method != "GET" or route.handler != sse_handler:
      try:
        cors.add(route)
      except ValueError as e:
        error_message = f"错误: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        # 将错误信息发送到前端
  web.run_app(app, port=1134)