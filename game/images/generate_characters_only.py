#!/usr/bin/env python3
"""
生成 TimeCastle_1 角色立绘（仅角色部分）
使用火山云 Ark API
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from the main script
from generate_volcano import CHARACTER_IMAGES, generate_image

def main():
    base_dir = "/Users/xurobert/claw_workspace/TimeCastle_1/game/images"
    char_dir = os.path.join(base_dir, "characters")
    
    os.makedirs(char_dir, exist_ok=True)
    
    print("=" * 60)
    print("生成 TimeCastle_1 角色立绘 - 艾登")
    print("=" * 60)
    print(f"输出目录：{char_dir}")
    print(f"尺寸：2K (约 2048x2880, 2:3 比例)")
    print("-" * 60)
    
    import time
    for filename, prompt in CHARACTER_IMAGES:
        output_path = os.path.join(char_dir, filename)
        # 火山云要求最小 3686400 像素，使用 2K 尺寸 (约 2048x2880)
        generate_image(prompt, output_path, "2K")
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("所有角色立绘生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
