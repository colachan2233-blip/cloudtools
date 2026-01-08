# my-backend/code/index.py
import json
import time
import secrets  # 密码学安全随机库
import string
from urllib.parse import parse_qs


def handler(environ, start_response):
    try:
        # 1. 解析请求参数 (例如 ?action=pwd&len=16)
        query_string = environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)

        # 获取动作指令，默认为 'probe'
        action = params.get('action', ['probe'])[0]

        result_data = {}

        # === 功能 1: 系统探针 (保留原有功能) ===
        if action == 'probe':
            client_ip = environ.get('HTTP_X_FORWARDED_FOR') or environ.get('REMOTE_ADDR')
            result_data = {
                "message": "System Probe OK",
                "client_ip": client_ip,
                "server_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "request_id": environ.get('fc.request_id', 'unknown'),
                "runtime": "Python 3.9 (Upgraded)"
            }


        # === 功能 3: 设备指纹分析 (新增) ===
        elif action == 'ua':
            ua_string = environ.get('HTTP_USER_AGENT', 'Unknown')

            # 简单的关键词分析
            os_name = "Unknown OS"
            if "Windows" in ua_string:
                os_name = "Windows"
            elif "Macintosh" in ua_string:
                os_name = "macOS"
            elif "Android" in ua_string:
                os_name = "Android"
            elif "iPhone" in ua_string:
                os_name = "iOS"
            elif "Linux" in ua_string:
                os_name = "Linux"

            result_data = {
                "user_agent": ua_string,
                "os_guess": os_name,
                "browser_guess": "Chrome/Edge" if "Chrome" in ua_string else "Other"
            }

        else:
            result_data = {"error": "Unknown Action"}

        # 2. 返回响应
        status = '200 OK'
        response_headers = [
            ('Content-type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),  # 允许跨域
            ('Access-Control-Allow-Methods', 'GET,POST')
        ]
        start_response(status, response_headers)
        return [json.dumps(result_data).encode('utf-8')]

    except Exception as e:
        status = '500 Internal Server Error'
        start_response(status, [('Content-type', 'text/plain')])
        return [str(e).encode('utf-8')]