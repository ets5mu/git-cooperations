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

    # def _assemble_auth_url(self):
    #     """生成认证URL（使用讯飞更常见的格式）"""
    #     from urllib.parse import urlparse
    #     import _thread as thread
    #     from time import sleep
    #     from datetime import datetime
    #     from hashlib import sha256
    #     import hmac

    #     url = 'wss://ise-api.xfyun.cn/v2/open-ise'
    #     host = 'ise-api.xfyun.cn'
    #     path = '/v2/open-ise'
    #     date = format_date_time(mktime(datetime.now().timetuple()))

    #     signature_origin = "host: {}\ndate: {}\nGET {} HTTP/1.1".format(host, date, path)
    #     signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=sha256).digest()
    #     signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

    #     authorization_origin = 'api_key="{}", algorithm="{}", headers="{}", signature="{}"'.format(
    #         self.api_key, "hmac-sha256", "host date request-line", signature_sha)
    #     authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

    #     v = {
    #         "authorization": authorization,
    #         "date": date,
    #         "host": host
    #     }
    #     auth_url = url + '?' + urlencode(v)
    #     return auth_url

    def evaluate(self, audio_path, text):
        """执行评测的主要方法"""
        auth_url = self._assemble_auth_url()
        ws = websocket.WebSocketApp(auth_url,
                                   on_open=lambda ws: self.on_open(ws, audio_path, text),
                                   on_message=self.on_message,
                                   on_error=self.on_error,
                                   on_close=self.on_close)
        ws.run_forever()

    # def on_open(self, ws, audio_path, text):
    #     """WebSocket连接成功时调用，发送开始帧和音频数据"""
    #     print("WebSocket连接已打开")
    #     # 1. 发送开始参数帧
    #     frame_size = 1280  # 每帧音频大小
    #     interval = 40  # 发送音频间隔(毫秒)
    #     sample_rate = 16000 # 音频采样率16k
    #     format = 1 # 音频格式，1为pcm
    #     channel = 1 # 声道数，1是单声道
    #     bits = 16 # 采样位数

    #     start_frame = {
    #         "common": {"app_id": self.app_id},
    #         "business": {
    #             "category": "read_sentence",
    #             "sub_category": "default",
    #             "ent": "en_vip",
    #             "cmd": "ssb",
    #             "auf": f"audio/L16;rate={sample_rate}",
    #             "aue": "raw",
    #             "text": base64.b64encode(text.encode('utf-8')).decode('utf-8'),
    #             "ttp_skip": True,
    #             "aus": 1
    #         },
    #         "data": {
    #             "status": 0,
    #             "format": f"audio/L16;rate={sample_rate}",
    #             "encoding": "raw",
    #             "audio": base64.b64encode(self._read_audio(audio_path, frame_size)).decode('utf-8')
    #         }
    #     }
    #     ws.send(json.dumps(start_frame))

    #     # 2. 模拟发送后续音频帧... (为简化Demo，我们一次性发送完所有数据)
    #     # 在实际应用中，这里应该是一个循环，读取音频文件并分帧发送
    #     end_frame = {
    #         "business": {
    #             "cmd": "auw",
    #             "aus": 2,
    #             "aue": "raw"
    #         },
    #         "data": {
    #             "status": 2,
    #             "format": f"audio/L16;rate={sample_rate}",
    #             "encoding": "raw",
    #             "audio": ""
    #         }
    #     }
    #     ws.send(json.dumps(end_frame))
    def on_open(self, ws, audio_path, text):
        """WebSocket连接成功时调用，发送开始帧和音频数据"""
        print("WebSocket连接已打开")

        # 1. 读取整个音频文件并进行Base64编码
        try:
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        except FileNotFoundError:
            print(f"错误：找不到音频文件 {audio_path}")
            ws.close()
            return

        # 2. 构建并发送起始帧 (status = 0)
        # 注意：根据错误信息，我们去掉了无效的 'sub_category' 字段，并将 'audio' 改为了 'data'
        start_frame = {
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
                "data": audio_base64,  # 关键修正：字段名从 'audio' 改为 'data'
                "format": "audio/L16;rate=16000",
                "encoding": "raw"
            }
        }
        ws.send(json.dumps(start_frame))

        # 3. 构建并发送结束帧 (status = 2)
        end_frame = {
            "data": {
                "status": 2,  # 2 表示结束
                "data": "",   # 结束帧数据为空
                "format": "audio/L16;rate=16000",
                "encoding": "raw"
            }
        }
        ws.send(json.dumps(end_frame))
        print("起始帧和结束帧已发送")

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