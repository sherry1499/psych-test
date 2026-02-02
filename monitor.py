"""
网站拨测脚本
用法：python monitor.py
可配合 Windows 任务计划程序或 Linux cron 定时执行
"""

import requests
import time
from datetime import datetime


def check_website(url, timeout=30):
    """检测网站可用性"""
    result = {
        "url": url,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "unknown",
        "status_code": None,
        "response_time": None,
        "error": None
    }
    
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        result["response_time"] = round(time.time() - start, 2)
        result["status_code"] = response.status_code
        
        if response.status_code == 200:
            # 检查页面内容
            if "心理测试" in response.text:
                result["status"] = "正常"
            else:
                result["status"] = "内容异常"
                result["error"] = "页面未包含关键字"
        else:
            result["status"] = "异常"
            result["error"] = f"状态码: {response.status_code}"
            
    except requests.exceptions.Timeout:
        result["status"] = "超时"
        result["error"] = f"请求超过 {timeout} 秒"
    except requests.exceptions.ConnectionError:
        result["status"] = "连接失败"
        result["error"] = "无法连接到服务器"
    except Exception as e:
        result["status"] = "错误"
        result["error"] = str(e)
    
    return result


def send_alert(result):
    """发送告警（可扩展为邮件、钉钉、微信等）"""
    print(f"⚠️ 告警：网站 {result['url']} 状态异常！")
    print(f"   错误：{result['error']}")
    
    # 扩展示例：发送钉钉告警
    # webhook = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
    # requests.post(webhook, json={"msgtype": "text", "text": {"content": f"网站异常: {result}"}})


def main():
    # 要监控的网站
    urls = [
        "https://sherry1499.github.io/psych-test/",
        # 可以添加更多网站
    ]
    
    print("=" * 50)
    print(f"拨测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    for url in urls:
        result = check_website(url)
        
        # 打印结果
        status_icon = "✅" if result["status"] == "正常" else "❌"
        print(f"\n{status_icon} {result['url']}")
        print(f"   状态: {result['status']}")
        print(f"   状态码: {result['status_code']}")
        print(f"   响应时间: {result['response_time']}s")
        
        if result["error"]:
            print(f"   错误: {result['error']}")
            send_alert(result)
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
