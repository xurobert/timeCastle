#!/usr/bin/env python3
"""
火山云 Ark - Doubao-Seedream-5.0-260128 图片生成脚本
使用 OpenAI 兼容 SDK
"""

import os
from openai import OpenAI
import requests
import time

# 配置
os.environ["ARK_API_KEY"] = "2c2f285c-a386-4804-9f0d-c1c8bca826c8"

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY")
)

# 背景图列表 (2K)
BACKGROUND_IMAGES = [
    ("bg_castle_modern.png", "现代城堡大厅内部，神秘氛围，蓝色光芒，时间稳定器装置在中央，高清写实风格，游戏背景图，1920x1080"),
    ("bg_medieval_castle.png", "中世纪城堡内部大厅，1347 年欧洲，石墙，火把照明，阴暗氛围，高清写实，游戏背景，1920x1080"),
    ("bg_revolution_paris.png", "1789 年法国大革命时期巴黎街头场景，人群聚集，革命旗帜，历史建筑，写实风格，游戏背景，1920x1080"),
    ("bg_ww2_battlefield.png", "1943 年二战欧洲战场，硝烟弥漫，战火纷飞，军事场景，写实风格，游戏背景图，1920x1080"),
    ("bg_time_corridor.png", "时间走廊，科幻风格，蓝色能量流动，时空隧道效果，抽象艺术，游戏背景，1920x1080"),
    ("bg_time_vortex.png", "时间漩涡，宇宙星空背景，时空扭曲特效，紫色和蓝色调，科幻抽象风格，游戏背景，1920x1080"),
    ("bg_new_timeline.png", "新时间线，平行宇宙，多重现实叠加效果，科幻风格，梦幻色彩，游戏背景图，1920x1080"),
]

# 角色立绘列表 (Ren'Py 标准 512x768 全身立绘)
CHARACTER_IMAGES = [
    ("eileen_normal.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，穿着深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，正常平静表情，正面站立，双臂自然下垂，透明背景 PNG，Ren'Py 游戏角色 sprite，512x768 比例"),
    ("eileen_happy.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，温暖微笑表情，友好，正面站立，透明背景 PNG，Ren'Py 游戏角色，512x768"),
    ("eileen_surprised.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛睁大，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，惊讶表情，嘴巴微张，正面站立，透明背景 PNG，Ren'Py sprite，512x768 比例"),
    ("eileen_serious.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，严肃表情，眉头微皱，正面站立，透明背景 PNG，Ren'Py 游戏角色，512x768"),
    ("eileen_worried.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，担忧表情，眉头紧锁，正面站立，透明背景 PNG，Ren'Py sprite，512x768 比例"),
]

def download_image(url, output_path):
    """下载图片到指定路径"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"下载失败：{e}")
        return False

def generate_image(prompt, output_path, size="1024x1024"):
    """调用火山云 Ark API 生成图片"""
    print(f"生成：{output_path}")
    
    try:
        response = client.images.generate(
            model="doubao-seedream-5-0-260128",
            prompt=prompt,
            size=size,
            response_format="url"
        )
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            print(f"  → URL: {image_url[:50]}...")
            
            if download_image(image_url, output_path):
                print(f"✓ 完成：{output_path}")
                return True
            else:
                return False
        else:
            print(f"✗ 失败：API 返回空数据")
            return False
            
    except Exception as e:
        print(f"✗ 错误：{str(e)}")
        return False

def main():
    import sys
    
    # 确定输出目录
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    bg_dir = os.path.join(base_dir, "bg")
    char_dir = os.path.join(base_dir, "characters")
    
    os.makedirs(bg_dir, exist_ok=True)
    os.makedirs(char_dir, exist_ok=True)
    
    print("=" * 60)
    print("火山云 Ark - Doubao-Seedream-5.0-260128 图片生成")
    print("=" * 60)
    
    # 生成背景图
    print("\n【背景图】(2K)")
    print("-" * 60)
    for filename, prompt in BACKGROUND_IMAGES:
        output_path = os.path.join(bg_dir, filename)
        generate_image(prompt, output_path, "2K")
        time.sleep(2)
    
    # 生成角色立绘 (512x768 Ren'Py 标准比例 2:3)
    print("\n【角色立绘】(512x768 Ren'Py 标准)")
    print("-" * 60)
    for filename, prompt in CHARACTER_IMAGES:
        output_path = os.path.join(char_dir, filename)
        # 火山云使用 1024x1536 保持 2:3 比例，适合 Ren'Py 角色立绘
        generate_image(prompt, output_path, "1024x1536")
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("所有图片生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
