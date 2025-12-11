from deep_translator import GoogleTranslator

def translate_text(text, target_language='vi'):
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translation
    except Exception as e:
        return f"Translation error: {text}"

def translate_instruction(maneuver_type, modifier):
    instructions = {
        "turn": {
            "left": "🔄 Rẽ trái",
            "right": "🔄 Rẽ phải",
            "slight left": "↖️ Rẽ nhẹ bên trái",
            "slight right": "↗️ Rẽ nhẹ bên phải",
            "sharp left": "↩️ Rẽ gắt bên trái",
            "sharp right": "↪️ Rẽ gắt bên phải",
            "uturn": "🔃 Quay đầu"
        },
        "depart": "🚀 Bắt đầu hành trình",
        "arrive": "🏁 Đến đích",
        "merge": {
            "left": "↖️ Nhập làn bên trái",
            "right": "↗️ Nhập làn bên phải",
            "slight left": "↖️ Nhập làn nhẹ bên trái",
            "slight right": "↗️ Nhập làn nhẹ bên phải"
        },
        "on ramp": {
            "left": "↖️ Vào đường cao tốc bên trái",
            "right": "↗️ Vào đường cao tốc bên phải"
        },
        "off ramp": {
            "left": "↙️ Rời đường cao tốc bên trái",
            "right": "↘️ Rời đường cao tốc bên phải"
        },
        "fork": {
            "left": "↖️ Đi theo nhánh trái",
            "right": "↗️ Đi theo nhánh phải"
        },
        "roundabout": "🔄 Vào vòng xuyến",
        "continue": "➡️ Tiếp tục đi thẳng"
    }
    
    if maneuver_type in ["depart", "arrive", "continue", "roundabout"]:
        return instructions.get(maneuver_type, "➡️ Tiếp tục")
    
    if maneuver_type in instructions and isinstance(instructions[maneuver_type], dict):
        return instructions[maneuver_type].get(modifier, f"➡️ {maneuver_type}")
    
    return "➡️ Tiếp tục"