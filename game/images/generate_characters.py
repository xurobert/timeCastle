#!/usr/bin/env python3
"""
火山云 Ark - 生成 Ren'Py 角色立绘（透明背景 PNG）
"""

import os
from openai import OpenAI
import requests
from PIL import Image
import io

# 配置
os.environ["ARK_API_KEY"] = "api-key-20260314003919 2c2f285c-a386-4804-9f0d-c1c8bca826c8"

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY")
)

# 角色立绘 - 生成时要求纯色背景便于后期去除
CHARACTER_IMAGES = [
    ("eileen_normal.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，穿着深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，正常平静表情，正面站立，双臂自然下垂，纯绿色背景 #00FF00，用于抠图"),
    ("eileen_happy.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，温暖微笑表情，友好，正面站立，纯绿色背景 #00FF00，用于抠图"),
    ("eileen_surprised.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛睁大，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，惊讶表情，嘴巴微张，正面站立，纯绿色背景 #00FF00，用于抠图"),
    ("eileen_serious.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，严肃表情，眉头微皱，正面站立，纯绿色背景 #00FF00，用于抠图"),
    ("eileen_worried.png", "艾登，神秘男性守护者，银色长发及腰，蓝色眼睛，深蓝色中世纪魔法师长袍，全身立绘，从头顶到脚完整可见，担忧表情，眉头紧锁，正面站立，纯绿色背景 #00FF00，用于抠图"),
]

def remove_background(image_path, output_path, bg_color=(0, 255, 0), tolerance=100):
    """去除绿色背景，转换为透明 PNG"""
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        
        datas = img.getdata()
        newData = []
        
        for item in datas:
            # 如果接近绿色背景，设为透明
            if (item[0] < tolerance and 
                item[1] > 255 - tolerance and 
                item[2] < tolerance):
                newData.append((item[0], item[1], item[2], 0))
            else:
                newData.append(item)
        
        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"  ✓ 背景已去除：{output_path}")
        return True
    except Exception as e:
        print(f"  ✗ 去背失败：{e}")
        return False

def generate_image(prompt, output_path):
    """调用火山云 Ark API 生成图片"""
    print(f"生成：{output_path}")
    
    try:
        response = client.images.generate(
            model="doubao-seedream-5-0-260128",
            prompt=prompt,
            size="1024x1536",
            response_format="url"
        )
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            print(f"  → URL: {image_url[:50]}...")
            
            # 下载图片
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            # 保存为临时 JPEG
            temp_path = output_path.replace('.png', '_temp.jpg')
            with open(temp_path, 'wb') as f:
                f.write(img_response.content)
            
            # 去除背景
            if remove_background(temp_path, output_path):
                # 删除临时文件
                os.remove(temp_path)
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
    char_dir = "/Users/xurobert/claw_workspace/TimeCastle_1/game/images/characters"
    os.makedirs(char_dir, exist_ok=True)
    
    print("=" * 60)
    print("火山云 Ark - Ren'Py 角色立绘生成（透明背景）")
    print("=" * 60)
    
    for filename, prompt in CHARACTER_IMAGES:
        output_path = os.path.join(char_dir, filename)
        generate_image(prompt, output_path)
        print()
    
    print("=" * 60)
    print("所有立绘生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
