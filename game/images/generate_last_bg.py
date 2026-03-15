#!/usr/bin/env python3
"""
使用 AutoGLM 生成最后一张背景图：bg_new_timeline.png
"""

import requests
import json
import os

# 获取 token
def get_token():
    try:
        response = requests.get("http://127.0.0.1:53699/get_token", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    return None

def generate_new_timeline():
    token = get_token()
    if not token:
        print("无法获取 token，尝试直接调用...")
        token = ""
    
    url = "http://127.0.0.1:53699/api/autoglm/generate-image"
    
    prompt = "新时间线，平行宇宙，多重现实叠加效果，科幻风格，梦幻色彩，紫色蓝色粉色渐变，抽象艺术，1920x1080 游戏背景图"
    
    payload = {
        "prompt": prompt,
        "size": "1920x1080",
        "output_path": "/Users/xurobert/claw_workspace/TimeCastle_1/game/images/bg/bg_new_timeline.png"
    }
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        result = response.json()
        
        if result.get("success") or result.get("status") == "success":
            print("✓ bg_new_timeline.png 生成成功")
            return True
        else:
            print(f"✗ 生成失败：{result}")
            return False
    except Exception as e:
        print(f"✗ 错误：{e}")
        return False

if __name__ == "__main__":
    generate_new_timeline()
