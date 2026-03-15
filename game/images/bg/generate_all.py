#!/usr/bin/env python3
# Generate all 7 background images for TimeCastle game

import json
import hashlib
import time
import urllib.request
import os

# Configuration
APP_ID = "100003"
APP_KEY = "38d2391985e2369a5fb8227d8e6cd5e5"
URL = "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image"
TOKEN_URL = "http://127.0.0.1:53699/get_token"
OUTPUT_DIR = "/Users/xurobert/claw_workspace/TimeCastle_1/game/images/bg/"

# Image definitions
images = [
    {
        "filename": "bg_castle_modern.png",
        "prompt": "现代城堡大厅，神秘氛围，蓝色光芒，时间稳定器装置，高清写实风格，1920x1080"
    },
    {
        "filename": "bg_medieval_castle.png",
        "prompt": "中世纪城堡内部，1347 年，石墙，火把照明，阴暗氛围，欧洲中世纪风格，1920x1080"
    },
    {
        "filename": "bg_revolution_paris.png",
        "prompt": "1789 年法国大革命时期的巴黎街头，人群，革命旗帜，历史写实风格，1920x1080"
    },
    {
        "filename": "bg_ww2_battlefield.png",
        "prompt": "1943 年二战欧洲战场，硝烟，战火，军事风格，写实，1920x1080"
    },
    {
        "filename": "bg_time_corridor.png",
        "prompt": "时间走廊，科幻风格，蓝色能量，时空隧道，抽象艺术，1920x1080"
    },
    {
        "filename": "bg_time_vortex.png",
        "prompt": "时间漩涡，宇宙星空，时空扭曲，紫色和蓝色，科幻抽象，1920x1080"
    },
    {
        "filename": "bg_new_timeline.png",
        "prompt": "新时间线，平行宇宙，多重现实，科幻风格，梦幻色彩，1920x1080"
    }
]

def get_token():
    """Get auth token from local service"""
    try:
        with urllib.request.urlopen(TOKEN_URL) as resp:
            token = resp.read().decode("utf-8").strip()
        if not token.lower().startswith("bearer "):
            token = f"Bearer {token}"
        return token
    except Exception as e:
        print(f"ERROR: 无法获取 token: {e}")
        return None

def generate_image(prompt):
    """Generate image from prompt and return image URL"""
    token = get_token()
    if not token:
        return None
    
    timestamp = str(int(time.time()))
    sign_data = f"{APP_ID}&{timestamp}&{APP_KEY}"
    sign = hashlib.md5(sign_data.encode("utf-8")).hexdigest()
    
    payload = json.dumps({"text": prompt}).encode("utf-8")
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "X-Auth-Appid": APP_ID,
        "X-Auth-TimeStamp": timestamp,
        "X-Auth-Sign": sign,
    }
    
    try:
        req = urllib.request.Request(URL, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("code") == 0 and result.get("data", {}).get("image_url"):
                return result["data"]["image_url"]
            else:
                print(f"API error: {result}")
                return None
    except Exception as e:
        print(f"ERROR: 生成图片失败：{e}")
        return None

def download_image(url, filepath):
    """Download image from URL and save to filepath"""
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            image_data = resp.read()
        with open(filepath, 'wb') as f:
            f.write(image_data)
        return True
    except Exception as e:
        print(f"ERROR: 下载图片失败：{e}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for i, img in enumerate(images, 1):
        print(f"\n[{i}/{7}] 生成 {img['filename']}...")
        print(f"  Prompt: {img['prompt']}")
        
        # Generate image
        image_url = generate_image(img['prompt'])
        if not image_url:
            print(f"  ❌ 生成失败，跳过")
            continue
        
        print(f"  ✓ 生成成功：{image_url}")
        
        # Download and save
        filepath = os.path.join(OUTPUT_DIR, img['filename'])
        if download_image(image_url, filepath):
            filesize = os.path.getsize(filepath)
            print(f"  ✓ 已保存：{filepath} ({filesize} bytes)")
        else:
            print(f"  ❌ 保存失败")
        
        # Small delay between requests
        if i < len(images):
            time.sleep(2)
    
    print("\n=== 完成 ===")
    print(f"输出目录：{OUTPUT_DIR}")

if __name__ == "__main__":
    main()
