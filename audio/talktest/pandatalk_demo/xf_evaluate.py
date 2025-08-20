import hashlib
import base64
import hmac
import json
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket

class XFClient:
    def __init__(self, app_id, api_key, api_secret):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.url = "wss://ise-api.xfyun.cn/v2/open-ise"

    def _assemble_auth_url(self):
        """生成认证URL，用于WebSocket连接"""
        url = 'wss://ise-api.xfyun.cn/v2/open-ise'
        host = 'ise-api.xfyun.cn'
        path = '/v2/open-ise'

        now = format_date_time(mktime(datetime.now().timetuple()))
        signature_origin = f"host: {host}\ndate: {now}\nGET {path} HTTP/1.1"
        signature_sha = base64.b64encode(
            hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest())
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha.decode()}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": now,
            "host": host
        }
        auth_url = url + '?' + urlencode(v)
        return auth_url

    def evaluate(self, audio_path, text):
        """执行评测的主要方法"""
        auth_url = self._assemble_auth_url()
        ws = websocket.WebSocketApp(auth_url,
                                   on_open=lambda ws: self.on_open(ws, audio_path, text),
                                   on_message=self.on_message,
                                   on_error=self.on_error,
                                   on_close=self.on_close)
        ws.run_forever()
        def on_open(self, ws, audio_path, text):
            """WebSocket连接成功时调用，发送开始帧和音频数据"""
        print("WebSocket连接已打开")

        # 1. 读取整个音频文件
        try:
            with open(audio_path, 'rb') as f:
                self.audio_data = f.read()
        except FileNotFoundError:
            print(f"错误：找不到音频文件 {audio_path}")
            ws.close()
            return

        # 2. 计算需要分多少帧 (每帧1280字节)
        self.frame_size = 1280  # 每帧音频大小
        self.interval = 40  # 发送音频间隔(毫秒)
        self.cur_pos = 0  # 当前处理位置
        
        # 3. 发送起始参数帧 (不包含音频数据)
        start_params = {
            "common": {
                "app_id": self.app_id
            },
            "business": {
                "category": "read_sentence",
                "ent": "cn_vip",  # 使用中文精品引擎
                "cmd": "ssb",
                "auf": "audio/L16;rate=16000",
                "aue": "raw",
                "text": base64.b64encode(text.encode('utf-8')).decode('utf-8'),
                "ttp_skip": True,
                "aus": 1
            },
            "data": {
                "status": 0,  # 0 表示开始
                "data": "",   # 起始参数帧不含音频数据
                "format": "audio/L16;rate=16000",
                "encoding": "raw"
            }
        }
        ws.send(json.dumps(start_params))
        print("起始参数帧已发送")

        # 4. 开始发送音频数据帧
        self._send_audio_frames(ws)

    def _send_audio_frames(self, ws):
        """分帧发送音频数据"""
        import threading
        import time
        
        # 计算总帧数
        total_frames = (len(self.audio_data) + self.frame_size - 1) // self.frame_size
        
        # 发送音频数据帧
        while self.cur_pos < len(self.audio_data):
            # 获取当前帧数据
            end_pos = min(self.cur_pos + self.frame_size, len(self.audio_data))
            frame_data = self.audio_data[self.cur_pos:end_pos]
            
            # Base64编码
            frame_base64 = base64.b64encode(frame_data).decode('utf-8')
            
            # 构建数据帧
            data_frame = {
                "data": {
                    "status": 1,  # 1 表示中间数据帧
                    "data": frame_base64,
                    "format": "audio/L16;rate=16000",
                    "encoding": "raw"
                }
            }
            
            # 发送数据帧
            ws.send(json.dumps(data_frame))
            
            # 更新位置
            self.cur_pos = end_pos
            
            # 添加延迟以模拟实时发送
            time.sleep(self.interval / 1000.0)
        
        # 发送结束帧
        end_frame = {
            "data": {
                "status": 2,  # 2 表示结束
                "data": "",   # 结束帧数据为空
                "format": "audio/L16;rate=16000",
                "encoding": "raw"
            }
        }
        ws.send(json.dumps(end_frame))
        print(f"所有音频帧已发送完毕，共{total_frames}帧")

    def on_message(self, ws, message):
        """收到服务器消息时调用"""
        response = json.loads(message)
        print("收到响应:", json.dumps(response, indent=4, ensure_ascii=False))
        # 这里可以解析响应，提取评分信息

    def on_error(self, ws, error):
        """发生错误时调用"""
        print("发生错误:", error)

    def on_close(self, ws, close_status_code, close_msg):
        """连接关闭时调用"""
        print("WebSocket连接已关闭")

    def _read_audio(self, audio_path, frame_size):
        """读取音频文件（模拟函数，需要您根据实际音频格式完善）"""
        # 这是一个示例，您需要根据您的音频文件格式来读取数据
        # 讯飞要求: 16k采样率、16bit、单声道、pcm编码的wav文件
        try:
            with open(audio_path, 'rb') as f:
                data = f.read()
            # 简单模拟：只返回前frame_size字节
            return data[:frame_size]
        except FileNotFoundError:
            print(f"错误：找不到音频文件 {audio_path}")
            return b''

# --- 主程序执行部分 ---
if __name__ == '__main__':
    APP_ID = "7927cbac"
    API_SECRET = "YjhhNWY5NDJhNzJkMGUzNTVlNGE2Yzg4"
    API_KEY = "bf0042eb279642bbecd457d9eee607d0"
    

    # 初始化客户端
    client = XFClient(APP_ID, API_KEY, API_SECRET)

    # 指定音频文件和对应的文本
    audio_file = "test2.wav"  # 请确保这个文件存在
    text_to_evaluate = "三山撑四水，四水绕三山。三山四水春常在，四水三山四时春。"  # 音频文件所说的内容

    # 开始评测
    print("开始语音评测...")
    client.evaluate(audio_file, text_to_evaluate)