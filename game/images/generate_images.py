#!/usr/bin/env python3
"""
火山云 Doubao-Seedream-5.0-lite 图片生成脚本
"""

import requests
import time
import os

API_KEY = "api-key-20260314003919 2c2f285c-a386-4804-9f0d-c1c8bca826c8"
ENDPOINT = "https://visual.volcengine.com/api/v1/models/doubao-seedream-5-0-lite/generation"

# 背景图列表 (1920x1080)
BACKGROUND_IMAGES = [
    ("bg_castle_modern.png", "现代城堡大厅内部，神秘氛围，蓝色光芒，时间稳定器装置在中央，高清写实风格，游戏背景图"),
    ("bg_medieval_castle.png", "中世纪城堡内部大厅，1347 年欧洲，石墙，火把照明，阴暗氛围，高清写实，游戏背景"),
    ("bg_revolution_paris.png", "1789 年法国大革命时期巴黎街头场景，人群聚集，革命旗帜，历史建筑，写实风格，游戏背景"),
    ("bg_ww2_battlefield.png", "1943 年二战欧洲战场，硝烟弥漫，战火纷飞，军事场景，写实风格，游戏背景图"),
    ("bg_time_corridor.png", "时间走廊，科幻风格，蓝色能量流动，时空隧道效果，抽象艺术，游戏背景"),
    ("bg_time_vortex.png", "时间漩涡，宇宙星空背景，时空扭曲特效，紫色和蓝色调，科幻抽象风格，游戏背景"),
    ("bg_new_timeline.png", "新时间线，平行宇宙，多重现实叠加效果，科幻风格，梦幻色彩，游戏背景图"),
]

# 角色立绘列表 (512x768 透明背景)
CHARACTER_IMAGES = [
    ("eileen_normal.png", "艾登，神秘男性守护者，银色长发，蓝色眼睛，穿着中世纪风格长袍，正常表情，正面站立，透明背景，角色立绘"),
    ("eileen_happy.png", "艾登，神秘男性守护者，银色长发，蓝色眼睛，中世纪长袍，微笑表情，温暖友好，透明背景，游戏角色立绘"),
    ("eileen_surprised.png", "艾登，神秘男性守护者，银色长发，蓝色眼睛，中世纪长袍，惊讶表情，眼睛睁大，透明背景，角色立绘"),
    ("eileen_serious.png", "艾登，神秘男性守护者，银色长发，蓝色眼睛，中世纪长袍，严肃表情，眉头微皱，透明背景，游戏角色"),
    ("eileen_worried.png", "艾登，神秘男性守护者，银色长发，蓝色眼睛，中世纪长袍，担忧表情，眉头紧锁，透明背景，角色立绘"),
]

def generate_image(prompt, output_path, size="1024x1024"):
    """调用火山云 API 生成图片"""
    print(f"生成：{output_path}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "doubao-seedream-5-0-lite",
        "prompt": prompt,
        "size": size,
        "num_inferences": 1
    }
    
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and "images" in result["data"] and len(result["data"]["images"]) > 0:
            image_url = result["data"]["images"][0]["url"]
            
            # 下载图片
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✓ 完成：{output_path}")
            return True
        else:
            print(f"✗ 失败：{output_path} - API 返回格式错误")
            print(f"响应：{result}")
            return False
            
    except Exception as e:
        print(f"✗ 错误：{output_path} - {str(e)}")
        return False

def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    bg_dir = os.path.join(output_dir, "bg")
    char_dir = os.path.join(output_dir, "characters")
    
    os.makedirs(bg_dir, exist_ok=True)
    os.makedirs(char_dir, exist_ok=True)
    
    print("=" * 50)
    print("火山云 Doubao-Seedream-5.0-lite 图片生成")
    print("=" * 50)
    
    # 生成背景图
    print("\n【背景图】(1920x1080)")
    print("-" * 50)
    for filename, prompt in BACKGROUND_IMAGES:
        output_path = os.path.join(bg_dir, filename)
        generate_image(prompt, output_path, "1920x1080")
        time.sleep(2)  # 避免请求过快
    
    # 生成角色立绘
    print("\n【角色立绘】(512x768)")
    print("-" * 50)
    for filename, prompt in CHARACTER_IMAGES:
        output_path = os.path.join(char_dir, filename)
        generate_image(prompt, output_path, "512x768")
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("所有图片生成完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
