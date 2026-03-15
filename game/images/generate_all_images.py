#!/usr/bin/env python3
"""
火山云 Ark - TimeCastle_1 完整图片生成
包含：背景图、角色立绘、CG 图、封面
"""

import os
from openai import OpenAI
import requests
from PIL import Image
import time

# 配置
os.environ["ARK_API_KEY"] = "2c2f285c-a386-4804-9f0d-c1c8bca826c8"

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY")
)

# ==================== 游戏封面 ====================
COVER_IMAGE = [
    ("cover.png", "时之堡游戏封面，神秘古堡在时空漩涡中央，四个时代的人物剪影环绕，1347 年中世纪服饰、1789 年贵族、1943 年军装、2026 年现代服装，科幻与奇幻风格，梦幻色彩，紫色蓝色金色光芒，电影海报质感，1920x1080 高清"),
]

# ==================== 背景图 ====================
BACKGROUND_IMAGES = [
    # 现代场景
    ("bg_lab_modern.png", "2026 年现代量子物理实验室，地下实验室，环形时间纠缠发生器装置，银色金属环悬浮，淡蓝色光芒，科幻风格，写实，1920x1080"),
    ("bg_castle_ruin.png", "2026 年古堡废墟，法国卢瓦尔河谷，破败的中世纪城堡，黄昏，荒凉，废墟美学，写实风格，1920x1080"),
    
    # 中世纪场景
    ("bg_dungeon_1347.png", "1347 年中世纪地牢，石墙，铁链，火把照明，阴暗，压抑，黑死病时期，写实风格，1920x1080"),
    ("bg_castle_corridor.png", "1347 年古堡地下走廊，螺旋石阶，火把，石墙，中世纪建筑，阴暗神秘，1920x1080"),
    ("bg_village_hut.png", "1347 年中世纪村庄，简陋木屋，村庄边缘，黑死病肆虐时期，萧条，写实风格，1920x1080"),
    ("bg_village_cellar.png", "1347 年地窖，陶罐，干粮，简易床铺，昏暗光线，藏身之处，1920x1080"),
    ("bg_castle_tower.png", "1347 年古堡塔楼顶层，螺旋楼梯，石墙，中世纪建筑，神秘氛围，1920x1080"),
    
    # 1789 年场景
    ("bg_rococo_room.png", "1789 年洛可可风格房间，精致油画，华丽家具，蜡烛，书架，科学仪器，启蒙时代，1920x1080"),
    ("bg_study_1789.png", "1789 年书房，橡木桌，泛黄纸张，书籍，科学仪器，蜡烛，贵族书房，1920x1080"),
    ("bg_versailles.png", "1789 年凡尔赛宫，法国大革命前夕，华丽宫殿，金色装饰，历史写实风格，1920x1080"),
    
    # 1943 年场景
    ("bg_ww2_bunker.png", "1943 年二战地堡，德军指挥部，军事地图，无线电设备，战争氛围，写实风格，1920x1080"),
    ("bg_resistance_base.png", "1943 年抵抗组织秘密基地，地下室，简陋设备，武器，二战时期，1920x1080"),
    
    # 科幻/抽象场景
    ("bg_time_vortex.png", "时间漩涡，多色光漩涡，蓝色金色红色绿色，时空扭曲，科幻抽象，1920x1080"),
    ("bg_time_corridor.png", "时间走廊，科幻风格，蓝色能量流动，时空隧道，抽象艺术，1920x1080"),
    ("bg_quantum_chamber.png", "量子密室，时间锚点装置，发光水晶，科幻风格，神秘，1920x1080"),
]

# ==================== 角色立绘（透明背景） ====================
CHARACTER_IMAGES = [
    # 主角
    ("l_mingyuan_normal.png", "陆明远，35 岁，中国量子物理学家，黑色短发，专注眼神，现代实验服，正常表情，正面站立，纯绿色背景用于抠图，1024x1536"),
    ("l_mingyuan_worried.png", "陆明远，35 岁，中国量子物理学家，黑色短发，担忧表情，现代实验服，纯绿色背景，1024x1536"),
    ("l_mingyuan_determined.png", "陆明远，35 岁，中国量子物理学家，黑色短发，坚定表情，现代实验服，纯绿色背景，1024x1536"),
    
    # 1347 年
    ("y_isode_normal.png", "伊索德，25 岁，中世纪草药医生，红棕色长发编辫子，绿色眼睛，亚麻长裙，深色斗篷，正常表情，纯绿色背景，1024x1536"),
    ("y_isode_kind.png", "伊索德，25 岁，中世纪草药医生，红棕色长发，绿色眼睛，亚麻长裙，温暖微笑，纯绿色背景，1024x1536"),
    ("y_isode_serious.png", "伊索德，25 岁，中世纪草药医生，红棕色长发，绿色眼睛，亚麻长裙，严肃表情，纯绿色背景，1024x1536"),
    
    # 1789 年
    ("h_henry_normal.png", "亨利·德·蒙特，45 岁，法国贵族，花白头发，华丽贵族服装，正常表情，纯绿色背景，1024x1536"),
    ("h_henry_tired.png", "亨利·德·蒙特，45 岁，法国贵族，花白头发，华丽贵族服装，疲惫表情，纯绿色背景，1024x1536"),
    ("h_henry_serious.png", "亨利·德·蒙特，45 岁，法国贵族，花白头发，华丽贵族服装，严肃表情，纯绿色背景，1024x1536"),
    
    # 1943 年
    ("g_margaret_normal.png", "玛格丽特，30 岁，法国抵抗组织成员，棕色短发，军装风格服装，坚定表情，纯绿色背景，1024x1536"),
    ("g_margaret_brave.png", "玛格丽特，30 岁，法国抵抗组织成员，棕色短发，军装风格服装，勇敢表情，纯绿色背景，1024x1536"),
    
    # 2026 年
    ("a_aden_normal.png", "艾登，28 岁，历史博主，黑色中长发，现代休闲服装，正常表情，纯绿色背景，1024x1536"),
    ("a_aden_mysterious.png", "艾登，28 岁，历史博主，黑色中长发，现代休闲服装，神秘微笑，纯绿色背景，1024x1536"),
    
    # 林雪（回忆/幻影）
    ("x_linxue_gentle.png", "林雪，30 岁，陆明远的妻子，温柔女性，黑色长发，白色连衣裙，温柔微笑，半透明幻影效果，纯绿色背景，1024x1536"),
]

# ==================== CG 场景图 ====================
CG_IMAGES = [
    ("cg_lab_explosion.png", "时间纠缠发生器爆炸，刺目白光，实验室仪器扭曲，主角被光芒吞噬，科幻灾难场景，戏剧性光影，1920x1080"),
    ("cg_time_portal.png", "时间窗口开启，石墙荡漾如水波，另一个时代房间显现，科幻奇幻风格，1920x1080"),
    ("cg_vortex_tower.png", "塔楼中央悬浮多色光漩涡，蓝色金色红色绿色，四个人物剪影在漩涡中，科幻史诗场景，1920x1080"),
    ("cg_four_eras.png", "四个时代同时展现，1347 年伊索德、1789 年亨利、1943 年玛格丽特、2026 年艾登，四人绿色眼睛，时空交错，1920x1080"),
    ("cg_final_choice.png", "最终抉择场景，时间锚点装置发光，四个时间线汇聚，主角站在中央，史诗感，1920x1080"),
]

def remove_background(image_path, output_path, tolerance=100):
    """去除绿色背景，转换为透明 PNG"""
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        
        for item in datas:
            if (item[0] < tolerance and 
                item[1] > 255 - tolerance and 
                item[2] < tolerance):
                newData.append((item[0], item[1], item[2], 0))
            else:
                newData.append(item)
        
        img.putdata(newData)
        img.save(output_path, "PNG")
        return True
    except Exception as e:
        print(f"  ✗ 去背失败：{e}")
        return False

def generate_image(prompt, output_path, size="2560x1440"):
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
            
            img_response = requests.get(image_url, timeout=60)
            img_response.raise_for_status()
            
            temp_path = output_path.replace('.png', '_temp.jpg')
            with open(temp_path, 'wb') as f:
                f.write(img_response.content)
            
            # 如果是角色立绘，去除背景
            if size == "1024x1536":
                if remove_background(temp_path, output_path):
                    os.remove(temp_path)
                    print(f"✓ 完成：{output_path}")
                    return True
            else:
                os.rename(temp_path, output_path)
                print(f"✓ 完成：{output_path}")
                return True
        else:
            print(f"✗ 失败：API 返回空数据")
            return False
            
    except Exception as e:
        print(f"✗ 错误：{str(e)}")
        return False

def main():
    base_dir = "/Users/xurobert/claw_workspace/TimeCastle_1/game/images"
    
    bg_dir = os.path.join(base_dir, "bg")
    char_dir = os.path.join(base_dir, "characters")
    cg_dir = os.path.join(base_dir, "cg")
    
    os.makedirs(bg_dir, exist_ok=True)
    os.makedirs(char_dir, exist_ok=True)
    os.makedirs(cg_dir, exist_ok=True)
    
    print("=" * 70)
    print("火山云 Ark - TimeCastle_1 完整图片生成")
    print("=" * 70)
    
    # 生成封面
    print("\n【游戏封面】")
    print("-" * 70)
    for filename, prompt in COVER_IMAGE:
        output_path = os.path.join(base_dir, filename)
        generate_image(prompt, output_path, "1920x1080")
        time.sleep(2)
    
    # 生成背景图
    print("\n【背景图】")
    print("-" * 70)
    for filename, prompt in BACKGROUND_IMAGES:
        output_path = os.path.join(bg_dir, filename)
        generate_image(prompt, output_path, "1920x1080")
        time.sleep(2)
    
    # 生成角色立绘
    print("\n【角色立绘】（透明背景）")
    print("-" * 70)
    for filename, prompt in CHARACTER_IMAGES:
        output_path = os.path.join(char_dir, filename)
        generate_image(prompt, output_path, "1536x2560")
        time.sleep(2)
    
    # 生成 CG 图
    print("\n【CG 场景图】")
    print("-" * 70)
    for filename, prompt in CG_IMAGES:
        output_path = os.path.join(cg_dir, filename)
        generate_image(prompt, output_path, "1920x1080")
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print("所有图片生成完成！")
    print("=" * 70)

if __name__ == "__main__":
    main()
