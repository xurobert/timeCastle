#!/bin/bash

# 火山云 Doubao-Seedream-5.0-lite API
API_KEY="api-key-20260314003919 2c2f285c-a386-4804-9f0d-c1c8bca826c8"
ENDPOINT="https://visual.volcengine.com/api/v1/models/doubao-seedream-5-0-lite/generation"

generate_image() {
    local prompt="$1"
    local output="$2"
    
    echo "生成：$output"
    
    curl -X POST "$ENDPOINT" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "{
            \"model\": \"doubao-seedream-5-0-lite\",
            \"prompt\": \"$prompt\",
            \"size\": \"1920x1080\",
            \"num_inferences\": 1
        }" | jq -r '.data.images[0].url' | xargs curl -o "$output"
    
    echo "完成：$output"
}

# 生成 7 张背景图
generate_image "现代城堡大厅内部，神秘氛围，蓝色光芒，时间稳定器装置中央，高清写实风格，1920x1080" "bg_castle_modern.png"
generate_image "中世纪城堡内部，1347 年欧洲，石墙，火把照明，阴暗氛围，高清写实" "bg_medieval_castle.png"
generate_image "1789 年法国大革命时期巴黎街头，人群聚集，革命旗帜，历史建筑，写实风格" "bg_revolution_paris.png"
generate_image "1943 年二战欧洲战场，硝烟弥漫，战火，军事场景，写实风格" "bg_ww2_battlefield.png"
generate_image "时间走廊，科幻风格，蓝色能量流动，时空隧道，抽象艺术" "bg_time_corridor.png"
generate_image "时间漩涡，宇宙星空背景，时空扭曲效果，紫色和蓝色调，科幻抽象" "bg_time_vortex.png"
generate_image "新时间线，平行宇宙，多重现实叠加，科幻风格，梦幻色彩" "bg_new_timeline.png"

echo "所有背景图生成完成！"
