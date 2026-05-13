# =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 1 / 6
# SAFE CORE PATCH
# =========================================================
# =========================================================
# IMPORTS
# =========================================================

import re
import sys
import threading
import time
import traceback
import string
import math
import random
import os
import json

# =========================================================
# SCRIPT ENGINE MEMORY
# =========================================================

SCRIPT_VARIABLES = {}
SCRIPT_DISPLAYS = {}
SCRIPT_FUNCTIONS = {}
SCRIPT_GAGES = {}

# =========================================================
# COLOR SYSTEM
# =========================================================

class C:

    RESET = "\033[0m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BOLD = "\033[1m"

# =========================================================
# UI WIDTH
# =========================================================

UI_WIDTH = 56

# =========================================================
# CENTER
# =========================================================

def ui_center(text):

    text = str(text)

    return text.center(UI_WIDTH)

# =========================================================
# LINE
# =========================================================

def ui_line(color=C.BRIGHT_MAGENTA):

    print(
        f"{color}"
        + "═" * UI_WIDTH
        + f"{C.RESET}"
    )

# =========================================================
# BOX TITLE
# =========================================================

def ui_title(title):

    print()

    ui_line(C.BRIGHT_MAGENTA)

    print(
        f"{C.BRIGHT_WHITE}"
        f"{ui_center(title)}"
        f"{C.RESET}"
    )

    ui_line(C.BRIGHT_MAGENTA)

# =========================================================
# BOX MESSAGE
# =========================================================

def ui_message(message, color=C.BRIGHT_WHITE):

    print(
        f"{color}"
        f"{ui_center(message)}"
        f"{C.RESET}"
    )

# =========================================================
# STATUS
# =========================================================

def ui_status(label, value, color=C.BRIGHT_CYAN):

    left = f" {label} "

    dots = "." * max(1, UI_WIDTH - len(left) - len(str(value)) - 2)

    print(
        f"{C.BRIGHT_BLACK}"
        f"{left}{dots} "
        f"{color}{value}"
        f"{C.RESET}"
    )

# =========================================================
# MENU ITEM
# =========================================================

def ui_menu(index, text, color=C.BRIGHT_GREEN):

    line = f" [{index}] {text}"

    print(
        f"{color}"
        f"{line}"
        f"{C.RESET}"
    )

# =========================================================
# INPUT BAR
# =========================================================

def ui_input(label="INPUT"):

    return input(
        f"{C.BRIGHT_MAGENTA}"
        f"┌─[{label}]\n"
        f"└──> "
        f"{C.RESET}"
    )

# =========================================================
# SPLASH SCREEN
# =========================================================

def splash_screen():

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        "██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ "
    )

    print(
        "██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗"
    )

    print(
        "██║     ██║██████╔╝███████║█████╗  ██████╔╝"
    )

    print(
        "██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗"
    )

    print(
        "╚██████╗██║██║     ██║  ██║███████╗██║  ██║"
    )

    print(
        " ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"
        f"{C.RESET}"
    )

    print()

    ui_message(
        "CIPHER-X ENCRYPTION SYSTEM",
        C.BRIGHT_CYAN
    )

    ui_message(
        "LIGHT SCRIPT ENGINE",
        C.BRIGHT_YELLOW
    )

    print()

# =========================================================
# SLOW PRINT
# =========================================================

def slow_print(text, delay=0.01, color=""):

    import time

    text = str(text)

    print(color, end="", flush=True)

    for char in text:

        print(char, end="", flush=True)

        try:
            time.sleep(delay)

        except Exception:
            pass

    print(C.RESET)

# =========================================================
# SAFE CONSTANTS
# =========================================================

SAFE_VAR_PATTERN = re.compile(
    r'^[A-Za-z_][A-Za-z0-9_]*$'
)

SAFE_EXPRESSION_PATTERN = re.compile(
    r'^[0-9A-Za-z_\s+\-*/%()<>!=&|.]+$'
)

# =========================================================
# CIPHER-X ENCRYPTION CORE
# ORIGINAL PROTOCOL EDITION
# =========================================================

FLAG_X = r'\0240'
FLAG_Y = r'\0250'
FLAG_END = r'\0000'

Y_VALID = set("あうおアウオやゆよヤユヨ")
X_VALID = set("あいうえおやゆよつわアイ   エオヤユヨツワ")

SMALL_MAP_X = {

    "あ":"ぁ",
    "い":"ぃ",
    "う":"ぅ",
    "え":"ぇ",
    "お":"ぉ",

    "や":"ゃ",
    "ゆ":"ゅ",
    "よ":"ょ",

    "つ":"っ",
    "わ":"ゎ",

    "ア":"ァ",
    "イ":"ィ",
    "ウ":"ゥ",
    "エ":"ェ",
    "オ":"ォ",

    "ヤ":"ャ",
    "ユ":"ュ",
    "ヨ":"ョ",

    "ツ":"ッ",
    "ワ":"ヮ",
}

SMALL_MAP_Y = {

    "あ":"ぁ",
    "う":"ぅ",
    "お":"ぉ",

    "や":"ゃ",
    "ゆ":"ゅ",
    "よ":"ょ",

    "ア":"ァ",
    "ウ":"ゥ",
    "オ":"ォ",

    "ヤ":"ャ",
    "ユ":"ュ",
    "ヨ":"ョ",
}

def is_hiragana(char):
    return 'ぁ' <= char <= 'ゖ'

def is_katakana(char):
    return 'ァ' <= char <= 'ヶ'

def make_code(prefix, row, dan):
    return f"{prefix}{row}{dan}"

ROW_MAP = {

    **dict.fromkeys("あいうえおアイウエオ", "01"),

    **dict.fromkeys("かきくけこカキクケコ", "11"),
    **dict.fromkeys("がぎぐげごガギグゲゴ", "07"),

    **dict.fromkeys("さしすせそサシスセソ", "19"),
    **dict.fromkeys("ざじずぜぞザジズゼゾ", "26"),

    **dict.fromkeys("たちつてとタチツテト", "20"),
    **dict.fromkeys("だぢづでどダヂヅデド", "04"),

    **dict.fromkeys("なにぬねのナニヌネノ", "14"),

    **dict.fromkeys("はひふへほハヒフヘホ", "08"),
    **dict.fromkeys("ばびぶべぼバビブベボ", "02"),
    **dict.fromkeys("ぱぴぷぺぽパピプペポ", "16"),

    **dict.fromkeys("まみむめもマミムメモ", "13"),

    **dict.fromkeys("やゆよヤユヨ", "25"),

    **dict.fromkeys("らりるれろラリルレロ", "18"),

    **dict.fromkeys("わワ", "23"),
}

DAN_MAP = {

    'あ':'1','い':'2','う':'3','え':'4','お':'5',
    'ア':'1','イ':'2','ウ':'3','エ':'4','オ':'5',

    'か':'1','き':'2','く':'3','け':'4','こ':'5',
    'カ':'1','キ':'2','ク':'3','ケ':'4','コ':'5',

    'が':'1','ぎ':'2','ぐ':'3','げ':'4','ご':'5',
    'ガ':'1','ギ':'2','グ':'3','ゲ':'4','ゴ':'5',

    'さ':'1','し':'2','す':'3','せ':'4','そ':'5',
    'サ':'1','シ':'2','ス':'3','セ':'4','ソ':'5',

    'ざ':'1','じ':'2','ず':'3','ぜ':'4','ぞ':'5',
    'ザ':'1','ジ':'2','ズ':'3','ゼ':'4','ゾ':'5',

    'た':'1','ち':'2','つ':'3','て':'4','と':'5',
    'タ':'1','チ':'2','ツ':'3','テ':'4','ト':'5',

    'だ':'1','ぢ':'2','づ':'3','で':'4','ど':'5',
    'ダ':'1','ヂ':'2','ヅ':'3','デ':'4','ド':'5',

    'な':'1','に':'2','ぬ':'3','ね':'4','の':'5',
    'ナ':'1','ニ':'2','ヌ':'3','ネ':'4','ノ':'5',

    'は':'1','ひ':'2','ふ':'3','へ':'4','ほ':'5',
    'ハ':'1','ヒ':'2','フ':'3','ヘ':'4','ホ':'5',

    'ば':'1','び':'2','ぶ':'3','べ':'4','ぼ':'5',
    'バ':'1','ビ':'2','ブ':'3','ベ':'4','ボ':'5',

    'ぱ':'1','ぴ':'2','ぷ':'3','ぺ':'4','ぽ':'5',
    'パ':'1','ピ':'2','プ':'3','ペ':'4','ポ':'5',

    'ま':'1','み':'2','む':'3','め':'4','も':'5',
    'マ':'1','ミ':'2','ム':'3','メ':'4','モ':'5',

    'や':'1','ゆ':'3','よ':'5',
    'ヤ':'1','ユ':'3','ヨ':'5',

    'ら':'1','り':'2','る':'3','れ':'4','ろ':'5',
    'ラ':'1','リ':'2','ル':'3','レ':'4','ロ':'5',

    'わ':'1',
    'ワ':'1',
}

SPECIAL_ENC = {

    '\n': r'\0140',

    'ん': '01140',
    'ン': '02140',

    'を': '01235',
    'ヲ': '02235',

    'っ': '01200',
    'ッ': '02200',

    '！': r'\@001',
    '？': r'\@002',
    '、': r'\@003',
    '。': r'\@004',
    'ー': r'\@005',
}

SPECIAL_DEC = {
    value: key
    for key, value in SPECIAL_ENC.items()
}

ALP_ENC = {}

for i, char in enumerate(string.ascii_uppercase, 1):
    ALP_ENC[char] = f"03{i:02d}0"

for i, char in enumerate(string.ascii_lowercase, 1):
    ALP_ENC[char] = f"03{i:02d}1"

ALP_DEC = {
    value: key
    for key, value in ALP_ENC.items()
}

JP_ENC = {}
JP_DEC = {}

for char in ROW_MAP:

    if char not in DAN_MAP:
        continue

    if is_hiragana(char):
        prefix = "01"

    elif is_katakana(char):
        prefix = "02"

    else:
        continue

    code = make_code(
        prefix,
        ROW_MAP[char],
        DAN_MAP[char]
    )

    JP_ENC[char] = code
    JP_DEC[code] = char

JP_ENC.update(SPECIAL_ENC)
JP_DEC.update(SPECIAL_DEC)

def validate_cipher_format(cipher):

    if cipher is None:
        return False

    cipher = str(cipher).strip()

    if cipher == "":
        return False

    if "  " in cipher:
        return False

    blocks = cipher.split(" ")

    for block in blocks:

        if block.startswith(r'\@<') and block.endswith('>'):
            continue

        if len(block) != 5:
            return False

    return True

def encrypt(text):

    if text is None:
        return ""

    text = str(text)

    result = []

    for char in text:

        if char == " ":
            continue

        if char == 'ぁ':
            result.append(r'\0240 01011 \0000')
            continue

        if char == 'ぃ':
            result.append(r'\0240 01012 \0000')
            continue

        if char == 'ぅ':
            result.append(r'\0240 01013 \0000')
            continue

        if char == 'ぇ':
            result.append(r'\0240 01014 \0000')
            continue

        if char == 'ぉ':
            result.append(r'\0240 01015 \0000')
            continue

        if char == 'ゃ':
            result.append(r'\0250 01011 \0000')
            continue

        if char == 'ゅ':
            result.append(r'\0250 01013 \0000')
            continue

        if char == 'ょ':
            result.append(r'\0250 01015 \0000')
            continue

        if char == 'っ':
            result.append(r'\0240 02203 \0000')
            continue

        if char == 'ァ':
            result.append(r'\0240 02011 \0000')
            continue

        if char == 'ィ':
            result.append(r'\0240 02012 \0000')
            continue

        if char == 'ゥ':
            result.append(r'\0240 02013 \0000')
            continue

        if char == 'ェ':
            result.append(r'\0240 02014 \0000')
            continue

        if char == 'ォ':
            result.append(r'\0240 02015 \0000')
            continue

        if char == 'ャ':
            result.append(r'\0250 02011 \0000')
            continue

        if char == 'ュ':
            result.append(r'\0250 02013 \0000')
            continue

        if char == 'ョ':
            result.append(r'\0250 02015 \0000')
            continue

        if char == 'ッ':
            result.append(r'\0240 02203 \0000')
            continue

        if char in JP_ENC:
            result.append(JP_ENC[char])
            continue

        if char in ALP_ENC:
            result.append(ALP_ENC[char])
            continue

        result.append(
            rf'\@<{char}>'
        )

    return " ".join(result)

def decrypt(cipher):

    if not validate_cipher_format(cipher):

        return fatal(
            "FORMAT_VIOLATION",
            "Cipher stream does not match protocol width.",
            "02"
        )

    blocks = cipher.split(" ")

    result = ""
    active_flag = None

    for block in blocks:

        valid_prefixes = (
            "01",
            "02",
            "03",
            r"\@",
            r"\0"
        )

        if not block.startswith(valid_prefixes):

            return fatal(
                "INVALID_PREFIX",
                f"Illegal prefix detected in '{block}'.",
                "03"
            )

        if block in (FLAG_X, FLAG_Y):

            if active_flag:

                return fatal(
                    "FLAG_COLLISION",
                    "Nested operational flags detected.",
                    "04"
                )

            active_flag = block
            continue

        if block == FLAG_END:

            if not active_flag:

                return fatal(
                    "STACK_UNDERFLOW",
                    "Flag end detected without active flag.",
                    "05"
                )

            active_flag = None
            continue

        decoded_char = None

        if block.startswith(r'\@<') and block.endswith('>'):
            decoded_char = block[3:-1]

        elif block in JP_DEC:
            decoded_char = JP_DEC[block]

        elif block in ALP_DEC:
            decoded_char = ALP_DEC[block]

        else:

            return fatal(
                "UNKNOWN_OPCODE",
                f"Opcode '{block}' does not exist.",
                "06"
            )

        if active_flag == FLAG_Y:

            if decoded_char not in Y_VALID:

                return fatal(
                    "INVALID_FLAG_CONTEXT",
                    f"'{block}' rejected by y-flag validator.",
                    "07"
                )

            decoded_char = SMALL_MAP_Y.get(
                decoded_char,
                decoded_char
            )

        elif active_flag == FLAG_X:

            if decoded_char not in X_VALID:

                return fatal(
                    "INVALID_FLAG_CONTEXT",
                    f"'{block}' rejected by x-flag validator.",
                    "08"
                )

            decoded_char = SMALL_MAP_X.get(
                decoded_char,
                decoded_char
            )

        result += decoded_char

    if active_flag:

        return fatal(
            "FLAG_TERMINATION_MISSING",
            "Flag session reached EOF before closure.",
            "09"
        )

    return result

def fatal(code, message, errno):
    return f"[{errno}] {code}: {message}"

def script_banner():

    print(f"{C.BRIGHT_MAGENTA}{C.BOLD}")

    print("╔══════════════════════════════════════════════╗")
    print("║         CIPHER-X  Light Script               ║")
    print("║               PROTOCOL v1.10                 ║")
    print("╚══════════════════════════════════════════════╝")

    print(C.RESET)

def script_error(code, message, errno):

    try:

        return fatal(
            str(code),
            str(message),
            str(errno)
        )

    except Exception:

        return (
            f"[{errno}] "
            f"{code}: {message}"
        )

def parse_value(value):

    if value is None:
        return ""

    value = str(value).strip()

    if re.fullmatch(r'-?\d+', value):

        try:
            return int(value)

        except ValueError:
            return 0

    if re.fullmatch(r'-?\d+\.\d+', value):

        try:
            return float(value)

        except ValueError:
            return 0.0

    if (
        len(value) >= 2 and
        value.startswith('"') and
        value.endswith('"')
    ):

        return value[1:-1]

    lower = value.lower()

    if lower == "true":
        return True

    if lower == "false":
        return False

    if value == "M.random()":

        return random.random()

    floor_match = re.fullmatch(
        r'M\.floor\((.+)\)',
        value
    )

    if floor_match:

        raw = floor_match.group(1).strip()

        parsed = parse_value(raw)

        try:

            return math.floor(
                float(parsed)
            )

        except:

            return 0

    round_match = re.fullmatch(
        r'M\.round\((.+)\)',
        value
    )

    if round_match:

        raw = round_match.group(1).strip()

        parsed = parse_value(raw)

        try:

            return round(
                float(parsed)
            )

        except:

            return 0

    if value in SCRIPT_VARIABLES:

        return SCRIPT_VARIABLES[value]

    return value

def safe_eval(expression):

    safe_globals = {
        "__builtins__": {}
    }

    safe_locals = {

        **SCRIPT_VARIABLES,

        "M": type(
            "MathModule",
            (),
            {
                "random": random.random,
                "floor": math.floor,
                "round": round,
            }
        )()
    }

    return eval(
        expression,
        safe_globals,
        safe_locals
    )

def render_display(name):

    if name not in SCRIPT_DISPLAYS:

        print(
            script_error(
                "DISPLAY_NOT_FOUND",
                f"Display '{name}' does not exist.",
                "S01"
            )
        )
        return

    state = SCRIPT_DISPLAYS.get(name)

    if state == 1:

        print(
            f"{C.BRIGHT_GREEN}〇{C.RESET}"
        )

    elif state == 0:

        print(
            f"{C.BRIGHT_RED}✕{C.RESET}"
        )

    else:

        print(
            script_error(
                "INVALID_DISPLAY_STATE",
                f"Display '{name}' has invalid state.",
                "S02"
            )
        )

def engine_output(value):

    try:

        value = str(value)

    except Exception:

        value = "[OUTPUT_ERROR]"

    value = value.replace(
        r"\ent",
        "\n"
    )

    print(
        f"{C.BRIGHT_WHITE}"
        f"{value}"
        f"{C.RESET}"
    )

def cmd_inli(command):

    match = re.fullmatch(
        r'inli\((.+?),\[(.*)\]\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_ARRAY_DECLARATION",
                "Invalid inli() syntax.",
                "A01"
            )
        )
        return

    name = match.group(1).strip()

    raw_items = match.group(2).strip()

    if raw_items == "":

        SCRIPT_VARIABLES[name] = []

        print(
            f"{C.BRIGHT_GREEN}"
            f"[ ARRAY REGISTERED ] "
            f"{name}"
            f"{C.RESET}"
        )

        return

    items = []

    split_items = raw_items.split(",")

    for item in split_items:

        parsed = parse_value(
            item.strip()
        )

        items.append(parsed)

    SCRIPT_VARIABLES[name] = items

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ ARRAY REGISTERED ] "
        f"{name}"
        f"{C.RESET}"
    )

def cmd_int(command):

    match = re.fullmatch(
        r'int\((.+?),(.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_INT_DECLARATION",
                "Invalid int() syntax.",
                "S03"
            )
        )
        return

    name = match.group(1).strip()
    raw_value = match.group(2).strip()

    if not SAFE_VAR_PATTERN.fullmatch(name):

        print(
            script_error(
                "INVALID_VARIABLE_NAME",
                f"'{name}' is not a valid variable name.",
                "S03A"
            )
        )
        return

    parsed = parse_value(raw_value)

    if isinstance(parsed, str):

        try:

            if SAFE_EXPRESSION_PATTERN.fullmatch(parsed):

                parsed = safe_eval(parsed)

        except Exception:

            print(
                script_error(
                    "EXPRESSION_EVALUATION_FAILED",
                    f"Failed to evaluate '{parsed}'.",
                    "S03B"
                )
            )
            return

    SCRIPT_VARIABLES[name] = parsed

def cmd_on(command):

    match = re.fullmatch(
        r'on\((.+)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_ON_SYNTAX",
                "Invalid on() syntax.",
                "S04"
            )
        )
        return

    raw = match.group(1).strip()

    value = parse_value(raw)

    engine_output(value)

def cmd_display(command):

    match = re.fullmatch(
        r'display\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_DISPLAY_DECLARATION",
                "Invalid display() syntax.",
                "S05"
            )
        )
        return

    name = match.group(1).strip()

    if not SAFE_VAR_PATTERN.fullmatch(name):

        print(
            script_error(
                "INVALID_DISPLAY_NAME",
                f"'{name}' is not valid.",
                "S05A"
            )
        )
        return

    SCRIPT_DISPLAYS[name] = 0

def cmd_in_dis(command):

    match = re.fullmatch(
        r'in dis \((.+?)\)\s*=\s*(.+)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_DISPLAY_INPUT",
                "Invalid display assignment syntax.",
                "S06"
            )
        )
        return

    name = match.group(1).strip()
    value = match.group(2).strip()

    if name not in SCRIPT_DISPLAYS:

        print(
            script_error(
                "DISPLAY_NOT_FOUND",
                f"Display '{name}' does not exist.",
                "S07"
            )
        )
        return

    try:

        value = int(value)

    except ValueError:

        print(
            script_error(
                "INVALID_DISPLAY_VALUE",
                "Display value must be 0 or 1.",
                "S08"
            )
        )
        return

    if value not in (0, 1):

        print(
            script_error(
                "INVALID_DISPLAY_VALUE",
                "Display value must be 0 or 1.",
                "S09"
            )
        )
        return

    SCRIPT_DISPLAYS[name] = value

    render_display(name)

def cmd_func(command):

    match = re.fullmatch(
        r'func\s+([A-Za-z_][A-Za-z0-9_]*)\(\)\{(.+)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_FUNCTION",
                "Invalid func syntax.",
                "S10"
            )
        )
        return

    name = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_FUNCTION",
                "Function body cannot be empty.",
                "S10A"
            )
        )
        return

    SCRIPT_FUNCTIONS[name] = body

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ FUNCTION REGISTERED ] "
        f"{name}"
        f"{C.RESET}"
    )

FUNC_RETURN_VALUE = None

def cmd_func_run(command):

    global FUNC_RETURN_VALUE

    match = re.fullmatch(
        r'([A-Za-z_][A-Za-z0-9_]*)\.run\((.*?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_FUNCTION_RUN",
                "Invalid function execution syntax.",
                "S11"
            )
        )
        return

    name = match.group(1).strip()

    if name not in SCRIPT_FUNCTIONS:

        print(
            script_error(
                "FUNCTION_NOT_FOUND",
                f"Function '{name}' does not exist.",
                "S12"
            )
        )
        return

    body = SCRIPT_FUNCTIONS.get(name)

    if not body:

        print(
            script_error(
                "EMPTY_FUNCTION_BODY",
                f"Function '{name}' is empty.",
                "S12A"
            )
        )
        return

    FUNC_RETURN_VALUE = None

    try:

        execute_script(body)

    except Exception as e:

        print(
            script_error(
                "FUNCTION_RUNTIME_ERROR",
                str(e),
                "S12B"
            )
        )

class FunctionReturn(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__()

def cmd_func_return(command):

    match = re.fullmatch(
        r'>>\s*(.+)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_RETURN_SYNTAX",
                "Invalid >> syntax.",
                "S12C"
            )
        )
        return

    raw = match.group(1).strip()

    value = parse_value(raw)

    raise FunctionReturn(value)

def execute_script(script):

    script = str(script).strip()

    if script == "":
        return

    commands = split_cipher_commands(script)

    for command in commands:

        command = str(command).strip()

        if command == "":
            continue

        try:

            execute_command(command)

        except FunctionReturn as e:

            global FUNC_RETURN_VALUE
            FUNC_RETURN_VALUE = e.value
            raise
            
def print_gage(name):

    if name not in SCRIPT_GAGES:

        print(
            script_error(
                "UNKNOWN_GAGE",
                f"Gage '{name}' does not exist.",
                "G02"
            )
        )
        return

    data = SCRIPT_GAGES[name]

    visual = "".join(
        "■" if x else "□"
        for x in data
    )

    print(f"[{visual}]")

def cmd_gagecn(command):

    match = re.fullmatch(
        r'(.+?)\.gagecn\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_GAGECN_SYNTAX",
                "Invalid .gagecn() syntax.",
                "G03"
            )
        )
        return

    name = match.group(1).strip()

    value = int(
        parse_value(
            match.group(2).strip()
        )
    )

    if name not in SCRIPT_GAGES:

        print(
            script_error(
                "UNKNOWN_GAGE",
                f"Gage '{name}' does not exist.",
                "G04"
            )
        )
        return

    value = max(0, min(10, value))

    SCRIPT_GAGES[name] = [
        1 if i < value else 0
        for i in range(10)
    ]

    print_gage(name)

def cmd_gagepin(command):

    match = re.fullmatch(
        r'(.+?)\.gagepin\((.+?),(.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_GAGEPIN_SYNTAX",
                "Invalid .gagepin() syntax.",
                "G05"
            )
        )
        return

    name = match.group(1).strip()

    index = int(
        parse_value(
            match.group(2).strip()
        )
    )

    value = int(
        parse_value(
            match.group(3).strip()
        )
    )

    if name not in SCRIPT_GAGES:

        print(
            script_error(
                "UNKNOWN_GAGE",
                f"Gage '{name}' does not exist.",
                "G06"
            )
        )
        return

    if not (1 <= index <= 10):

        print(
            script_error(
                "INVALID_GAGE_INDEX",
                "Gage index must be 1-10.",
                "G07"
            )
        )
        return

    SCRIPT_GAGES[name][index - 1] = 1 if value else 0

    print_gage(name)

def cmd_array_on(command):

    match = re.fullmatch(
        r'(.+?)\.on\((.+?)\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    value = parse_value(
        match.group(2).strip()
    )

    if name not in SCRIPT_VARIABLES:

        print(
            script_error(
                "UNKNOWN_ARRAY",
                f"Array '{name}' does not exist.",
                "A20"
            )
        )
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):

        print(
            script_error(
                "NOT_ARRAY",
                f"'{name}' is not an array.",
                "A21"
            )
        )
        return True

    SCRIPT_VARIABLES[name].append(value)

    return True

def cmd_array_unon(command):

    match = re.fullmatch(
        r'(.+?)\.unon\((.+?)\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    value = parse_value(
        match.group(2).strip()
    )

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    SCRIPT_VARIABLES[name].insert(0, value)

    return True

def cmd_array_off(command):

    match = re.fullmatch(
        r'(.+?)\.off\(\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    if SCRIPT_VARIABLES[name]:

        SCRIPT_VARIABLES[name].pop()

    return True

def cmd_array_unoff(command):

    match = re.fullmatch(
        r'(.+?)\.unoff\(\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    if SCRIPT_VARIABLES[name]:

        SCRIPT_VARIABLES[name].pop(0)

    return True

def cmd_array_pointer(command):

    match = re.fullmatch(
        r'(.+?)\.pointer\((.+?),(.+?)\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    index = int(
        parse_value(
            match.group(2).strip()
        )
    )

    value = parse_value(
        match.group(3).strip()
    )

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    if not (
        0 <= index < len(SCRIPT_VARIABLES[name])
    ):

        print(
            script_error(
                "ARRAY_INDEX_ERROR",
                "Index out of range.",
                "A22"
            )
        )

        return True

    SCRIPT_VARIABLES[name][index] = value

    return True

LAST_IF_RESULT = False

def cmd_if(command):

    global LAST_IF_RESULT

    match = re.fullmatch(
        r'if\((.*?)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_IF_SYNTAX",
                "Invalid if() syntax.",
                "S19"
            )
        )
        return

    condition = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_IF_BODY",
                "if() body cannot be empty.",
                "S19A"
            )
        )
        return

    try:

        result = safe_eval(condition)

    except NameError as e:

        print(
            script_error(
                "IF_VARIABLE_NOT_FOUND",
                str(e),
                "S20A"
            )
        )
        return

    except SyntaxError as e:

        print(
            script_error(
                "IF_SYNTAX_ERROR",
                str(e),
                "S20B"
            )
        )
        return

    except Exception as e:

        print(
            script_error(
                "IF_EVALUATION_FAILED",
                str(e),
                "S20"
            )
        )
        return

    if bool(result):

        LAST_IF_RESULT = True

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "IF_RUNTIME_ERROR",
                    str(e),
                    "S20C"
                )
            )

    else:

        LAST_IF_RESULT = False

def cmd_ifel(command):

    global LAST_IF_RESULT

    match = re.fullmatch(
        r'ifel\((.+?)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_IFEL_SYNTAX",
                "Invalid ifel() syntax.",
                "S20D"
            )
        )
        return

    if LAST_IF_RESULT:
        return

    condition = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_IFEL_BODY",
                "ifel() body cannot be empty.",
                "S20E"
            )
        )
        return

    try:

        result = safe_eval(condition)

    except Exception as e:

        print(
            script_error(
                "IFEL_EVALUATION_FAILED",
                str(e),
                "S20F"
            )
        )
        return

    if bool(result):

        LAST_IF_RESULT = True

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "IFEL_RUNTIME_ERROR",
                    str(e),
                    "S20G"
                )
            )

    else:

        LAST_IF_RESULT = False

def cmd_else(command):

    global LAST_IF_RESULT

    match = re.fullmatch(
        r'else\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_ELSE_SYNTAX",
                "Invalid else syntax.",
                "S20H"
            )
        )
        return

    body = match.group(1).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_ELSE_BODY",
                "else body cannot be empty.",
                "S20I"
            )
        )
        return

    if not LAST_IF_RESULT:

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "ELSE_RUNTIME_ERROR",
                    str(e),
                    "S20J"
                )
            )

    LAST_IF_RESULT = False

def cmd_while(command):

    match = re.fullmatch(
        r'while\s*\((.*?)\)\s*\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_WHILE_SYNTAX",
                "Invalid while() syntax.",
                "S21"
            )
        )

        return

    condition = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_WHILE_BODY",
                "while() body cannot be empty.",
                "S21A"
            )
        )
        return

    loop_count = 0
    max_loops = 10000

    while True:

        loop_count += 1

        if loop_count > max_loops:

            print(
                script_error(
                    "WHILE_LIMIT_EXCEEDED",
                    "Loop exceeded safety limit.",
                    "S22"
                )
            )

            return

        try:

            result = safe_eval(condition)

        except NameError as e:

            print(
                script_error(
                    "WHILE_VARIABLE_NOT_FOUND",
                    str(e),
                    "S23A"
                )
            )

            return

        except SyntaxError as e:

            print(
                script_error(
                    "WHILE_CONDITION_SYNTAX_ERROR",
                    str(e),
                    "S23B"
                )
            )

            return

        except Exception as e:

            print(
                script_error(
                    "WHILE_CONDITION_FAILURE",
                    str(e),
                    "S23"
                )
            )

            return

        if not result:
            break

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "WHILE_RUNTIME_FAILURE",
                    str(e),
                    "S24"
                )
            )

            return

def split_cipher_commands(script):

    commands = []
    current = []
    brace_depth = 0
    paren_depth = 0
    bracket_depth = 0
    in_string = False
    escape = False

    for i, char in enumerate(script):
        if escape:
            current.append(char)
            escape = False
            continue

        if char == "\\":
            current.append(char)
            escape = True
            continue

        if char == '"':
            in_string = not in_string
            current.append(char)
            continue

        if in_string:
            current.append(char)
            continue

        if char == "{":
            brace_depth += 1
            current.append(char)
            continue

        if char == "}":
            brace_depth -= 1
            current.append(char)
            continue

        if char == "(":
            paren_depth += 1
            current.append(char)
            continue

        if char == ")":
            paren_depth -= 1
            current.append(char)
            continue

        if char == "[":
            bracket_depth += 1
            current.append(char)
            continue

        if char == "]":
            bracket_depth -= 1
            current.append(char)
            continue

        if (
            char == ";"
            and brace_depth == 0
            and paren_depth == 0
            and bracket_depth == 0
            and not in_string
        ):
            command = "".join(current).strip()
            if command:
                commands.append(command)
            current = []
            continue

        current.append(char)

    final_command = "".join(current).strip()
    if final_command:

        if final_command and not final_command.endswith("}"):
            print(
                script_error(
                    "MISSING_COMMAND_SEPARATOR",
                    f"Command must end with ';' or '}}': {final_command}",
                    "PARSE01"
                )
            )
            return []

        commands.append(final_command)

    return commands

# =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 2 / 6
# SAFE EXECUTION PATCH
# =========================================================

def cmd_func_run(command):

    match = re.fullmatch(
        r'([A-Za-z_][A-Za-z0-9_]*)\.run\((.*?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_FUNCTION_RUN",
                "Invalid function execution syntax.",
                "S11"
            )
        )
        return

    name = match.group(1).strip()

    if name not in SCRIPT_FUNCTIONS:

        print(
            script_error(
                "FUNCTION_NOT_FOUND",
                f"Function '{name}' does not exist.",
                "S12"
            )
        )
        return

    body = SCRIPT_FUNCTIONS.get(name)

    if not body:

        print(
            script_error(
                "EMPTY_FUNCTION_BODY",
                f"Function '{name}' is empty.",
                "S12A"
            )
        )
        return

    try:

        execute_script(body)

    except Exception as e:

        print(
            script_error(
                "FUNCTION_RUNTIME_ERROR",
                str(e),
                "S12B"
            )
        )

TOUCH_BINDINGS = {
    "w": None,
    "a": None,
    "s": None,
    "d": None,
}

def cmd_touch_bind(command):

    match = re.fullmatch(
        r'touch\.([wasd])=\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_TOUCH_BIND",
                "Invalid touch binding syntax.",
                "S13"
            )
        )
        return

    key = match.group(1).strip().lower()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_TOUCH_BIND",
                "Touch bind body cannot be empty.",
                "S13A"
            )
        )
        return

    TOUCH_BINDINGS[key] = body

    print(
        f"{C.BRIGHT_CYAN}"
        f"[ TOUCH BIND SET ] "
        f"{key.upper()}"
        f"{C.RESET}"
    )

def touch_session():

    print()

    slow_print(
        "[ TOUCH SESSION STARTED ]",
        0.005,
        C.BRIGHT_MAGENTA
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "PRESS W/A/S/D"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "TYPE 'exit' TO LEAVE"
        f"{C.RESET}"
    )

    while True:

        print()

        try:

            key = input(
                f"{C.BRIGHT_YELLOW}touch >> {C.RESET}"
            ).strip().lower()

        except KeyboardInterrupt:

            print()

            slow_print(
                "[ TOUCH SESSION INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        except EOFError:

            print(
                script_error(
                    "TOUCH_INPUT_ERROR",
                    "Input stream closed.",
                    "S14A"
                )
            )
            break

        if key == "exit":

            print()

            slow_print(
                "[ TOUCH SESSION CLOSED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        if key not in TOUCH_BINDINGS:

            print(
                script_error(
                    "INVALID_TOUCH_KEY",
                    f"'{key}' is not supported.",
                    "S14"
                )
            )
            continue

        body = TOUCH_BINDINGS.get(key)

        if body is None:

            print(
                script_error(
                    "UNBOUND_TOUCH_KEY",
                    f"'{key}' has no binding.",
                    "S15"
                )
            )
            continue

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "TOUCH_RUNTIME_ERROR",
                    str(e),
                    "S15A"
                )
            )

ACTIVE_INTERVALS = {}
INTERVAL_COUNTER = 0

MIN_INTERVAL_MS = 10
MAX_INTERVAL_MS = 3600000

def validate_timer_value(value):

    try:

        value = int(value)

    except:

        return None

    if value < MIN_INTERVAL_MS:
        return None

    if value > MAX_INTERVAL_MS:
        return None

    return value

def cmd_settime(command):

    match = re.fullmatch(
        r'settime\((\d+)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_SETTIME",
                "Invalid settime syntax.",
                "T01"
            )
        )
        return

    delay = validate_timer_value(
        match.group(1)
    )

    if delay is None:

        print(
            script_error(
                "INVALID_SETTIME_VALUE",
                (
                    f"Timer must be between "
                    f"{MIN_INTERVAL_MS}ms and "
                    f"{MAX_INTERVAL_MS}ms."
                ),
                "T02"
            )
        )
        return

    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_SETTIME_BODY",
                "settime body cannot be empty.",
                "T03"
            )
        )
        return

    def runner():

        try:

            time.sleep(delay / 1000)

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "SETTIME_RUNTIME",
                    str(e),
                    "T04"
                )
            )

    thread = threading.Thread(
        target=runner,
        daemon=True
    )

    thread.start()

    print(
        f"{C.BRIGHT_CYAN}"
        f"[ SETTIME REGISTERED ] "
        f"{delay}ms"
        f"{C.RESET}"
    )

def cmd_setinter(command):

    global INTERVAL_COUNTER

    match = re.fullmatch(
        r'setInter\((\d+)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_SETINTER",
                "Invalid setInter syntax.",
                "T05"
            )
        )
        return

    interval = validate_timer_value(
        match.group(1)
    )

    if interval is None:

        print(
            script_error(
                "INVALID_SETINTER_VALUE",
                (
                    f"Interval must be between "
                    f"{MIN_INTERVAL_MS}ms and "
                    f"{MAX_INTERVAL_MS}ms."
                ),
                "T06"
            )
        )
        return

    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_SETINTER_BODY",
                "setInter body cannot be empty.",
                "T07"
            )
        )
        return

    INTERVAL_COUNTER += 1

    interval_id = INTERVAL_COUNTER

    ACTIVE_INTERVALS[interval_id] = True

    def runner():

        while ACTIVE_INTERVALS.get(interval_id):

            try:

                execute_script(body)

            except Exception as e:

                print(
                    script_error(
                        "SETINTER_RUNTIME",
                        str(e),
                        "T08"
                    )
                )

            time.sleep(interval / 1000)

    thread = threading.Thread(
        target=runner,
        daemon=True
    )

    thread.start()

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ SETINTER STARTED ] "
        f"ID={interval_id} "
        f"{interval}ms"
        f"{C.RESET}"
    )

def cmd_clearinter(command):

    match = re.fullmatch(
        r'clearInter\((\d+)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_CLEARINTER",
                "Invalid clearInter syntax.",
                "T09"
            )
        )
        return

    interval_id = int(
        match.group(1)
    )

    if interval_id not in ACTIVE_INTERVALS:

        print(
            script_error(
                "INTERVAL_NOT_FOUND",
                f"Interval ID '{interval_id}' does not exist.",
                "T10"
            )
        )
        return

    ACTIVE_INTERVALS[interval_id] = False

    print(
        f"{C.BRIGHT_RED}"
        f"[ SETINTER STOPPED ] "
        f"ID={interval_id}"
        f"{C.RESET}"
    )

# =========================================================
# COMMAND EXECUTOR
# =========================================================

def execute_command(command):

    command = str(command).strip()

    if command == "":
        return

    if command.startswith(">>"):

        cmd_func_return(command)
        return

    if command.startswith("inli("):

        cmd_inli(command)
        return

    if command.startswith("int("):

        cmd_int(command)
        return

    if command.startswith("on("):

        cmd_on(command)
        return

    if command.startswith("display("):

        cmd_display(command)
        return

    if command.startswith("in dis"):

        cmd_in_dis(command)
        return

    if command.startswith("func "):

        cmd_func(command)
        return

    if re.fullmatch(
        r'[A-Za-z_][A-Za-z0-9_]*\.run\((.*?)\)',
        command
    ):

        cmd_func_run(command)
        return

    if command.startswith("if("):

        cmd_if(command)
        return

    if command.startswith("ifel("):

        cmd_ifel(command)
        return

    if command.startswith("else{"):

        cmd_else(command)
        return

    if command.startswith("while("):

        cmd_while(command)
        return

    if command.startswith("touch."):

        cmd_touch_bind(command)
        return

    if command.startswith("settime("):

        cmd_settime(command)
        return

    if command.startswith("setInter("):

        cmd_setinter(command)
        return

    if command.startswith("clearInter("):

        cmd_clearinter(command)
        return

    if command == "touch()":

        touch_session()
        return

    if command.startswith("gage("):

        cmd_gage(command)
        return

    if ".gagecn(" in command:

        cmd_gagecn(command)
        return

    if ".gagepin(" in command:

        cmd_gagepin(command)
        return

    if ".on(" in command:
        if cmd_array_on(command):
            return

    if ".unon(" in command:
        if cmd_array_unon(command):
            return

    if ".off()" in command:
        if cmd_array_off(command):
            return

    if ".unoff()" in command:
        if cmd_array_unoff(command):
            return

    if ".pointer(" in command:
        if cmd_array_pointer(command):
            return

    if command.startswith("input("):

        cmd_input(command)
        return

    if command == "clear()":

        cmd_clear(command)
        return

    if command.startswith("wait("):

        cmd_wait(command)
        return

    if command == "exit()":

        cmd_exit(command)
        return

    if command.startswith("encrypt("):

        cmd_encrypt(command)
        return

    if command.startswith("decrypt("):

        cmd_decrypt(command)
        return

    if command.startswith("save("):

        cmd_save(command)
        return

    if command.startswith("load("):

        cmd_load(command)
        return

    if command == "reset()":

        cmd_reset(command)
        return

    if command.startswith("del("):

        cmd_del(command)
        return

    if command == "memory()":

        cmd_memory(command)
        return

    if command == "help()":

        cmd_help(command)
        return

    print(
        script_error(
            "UNKNOWN_COMMAND",
            f"Unknown command '{command}'",
            "S16"
        )
    )

def execute_script(script):

    script = str(script).strip()

    if script == "":
        return

    commands = split_cipher_commands(script)

    for command in commands:

        command = str(command).strip()

        if command == "":
            continue

        execute_command(command)

# =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 3 / 6
# FILE / INPUT / TERMINAL PATCH
# =========================================================

def cmd_input(command):

    match = re.fullmatch(
        r'input\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_INPUT_SYNTAX",
                "Invalid input() syntax.",
                "I01"
            )
        )

        return

    variable_name = match.group(1).strip()

    if not SAFE_VAR_PATTERN.fullmatch(variable_name):

        print(
            script_error(
                "INVALID_INPUT_VARIABLE",
                f"'{variable_name}' is not valid.",
                "I02"
            )
        )

        return

    try:

        value = input(
            f"{C.BRIGHT_CYAN}"
            f"{variable_name} >> "
            f"{C.RESET}"
        )

    except KeyboardInterrupt:

        print()

        print(
            script_error(
                "INPUT_INTERRUPTED",
                "Input interrupted.",
                "I03"
            )
        )

        return

    except EOFError:

        print(
            script_error(
                "INPUT_STREAM_CLOSED",
                "Input stream closed.",
                "I04"
            )
        )

        return

    SCRIPT_VARIABLES[variable_name] = value

def cmd_clear(command):

    if command != "clear()":

        print(
            script_error(
                "INVALID_CLEAR_SYNTAX",
                "Invalid clear() syntax.",
                "C01"
            )
        )

        return

    try:

        if os.name == "nt":
            os.system("cls")

        else:
            os.system("clear")

    except Exception as e:

        print(
            script_error(
                "CLEAR_FAILED",
                str(e),
                "C02"
            )
        )

def cmd_wait(command):

    match = re.fullmatch(
        r'wait\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_WAIT_SYNTAX",
                "Invalid wait() syntax.",
                "W01"
            )
        )

        return

    raw = match.group(1).strip()

    value = parse_value(raw)

    try:

        value = float(value)

    except:

        print(
            script_error(
                "WAIT_NOT_NUMBER",
                "wait() value must be numeric.",
                "W02"
            )
        )

        return

    if value < 0:

        print(
            script_error(
                "NEGATIVE_WAIT",
                "wait() cannot be negative.",
                "W03"
            )
        )

        return

    if value > 3600:

        print(
            script_error(
                "WAIT_TOO_LARGE",
                "wait() exceeded safety limit.",
                "W04"
            )
        )

        return

    try:

        time.sleep(value)

    except Exception as e:

        print(
            script_error(
                "WAIT_RUNTIME_ERROR",
                str(e),
                "W05"
            )
        )

def cmd_exit(command):

    if command != "exit()":

        print(
            script_error(
                "INVALID_EXIT_SYNTAX",
                "Invalid exit() syntax.",
                "E01"
            )
        )

        return

    slow_print(
        "[ ENGINE TERMINATED ]",
        0.005,
        C.BRIGHT_RED
    )

    sys.exit(0)

def cmd_encrypt(command):

    match = re.fullmatch(
        r'encrypt\((.+)\)',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_ENCRYPT_SYNTAX",
                "Invalid encrypt() syntax.",
                "CR01"
            )
        )

        return

    raw = match.group(1).strip()

    value = parse_value(raw)

    try:

        result = encrypt(
            str(value)
        )

    except Exception as e:

        print(
            script_error(
                "ENCRYPT_RUNTIME_ERROR",
                str(e),
                "CR02"
            )
        )

        return

    engine_output(result)

def cmd_decrypt(command):

    match = re.fullmatch(
        r'decrypt\((.+)\)',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_DECRYPT_SYNTAX",
                "Invalid decrypt() syntax.",
                "CR03"
            )
        )

        return

    raw = match.group(1).strip()

    value = parse_value(raw)

    try:

        result = decrypt(
            str(value)
        )

    except Exception as e:

        print(
            script_error(
                "DECRYPT_RUNTIME_ERROR",
                str(e),
                "CR04"
            )
        )

        return

    engine_output(result)

SAVE_DIRECTORY = "cipherx_saves"

def init_save_directory():

    try:

        if not os.path.exists(SAVE_DIRECTORY):

            os.makedirs(SAVE_DIRECTORY)

    except Exception as e:

        print(
            script_error(
                "SAVE_DIRECTORY_ERROR",
                str(e),
                "F01"
            )
        )

def cmd_save(command):

    match = re.fullmatch(
        r'save\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_SAVE_SYNTAX",
                "Invalid save() syntax.",
                "F02"
            )
        )

        return

    filename = match.group(1).strip()

    if (
        filename.startswith('"')
        and filename.endswith('"')
    ):

        filename = filename[1:-1]

    filename = filename.strip()

    if filename == "":

        print(
            script_error(
                "EMPTY_SAVE_FILENAME",
                "Filename cannot be empty.",
                "F03"
            )
        )

        return

    invalid_chars = r'<>:"/\|?*'

    for char in invalid_chars:

        if char in filename:

            print(
                script_error(
                    "INVALID_SAVE_FILENAME",
                    f"Illegal filename character '{char}'.",
                    "F04"
                )
            )

            return

    if not filename.endswith(".json"):

        filename += ".json"

    init_save_directory()

    path = os.path.join(
        SAVE_DIRECTORY,
        filename
    )

    data = {

        "variables": SCRIPT_VARIABLES,
        "displays": SCRIPT_DISPLAYS,
        "functions": SCRIPT_FUNCTIONS,
        "gages": SCRIPT_GAGES,
    }

    try:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception as e:

        print(
            script_error(
                "SAVE_WRITE_ERROR",
                str(e),
                "F05"
            )
        )

        return

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ SAVE COMPLETE ] "
        f"{filename}"
        f"{C.RESET}"
    )

def cmd_load(command):

    match = re.fullmatch(
        r'load\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_LOAD_SYNTAX",
                "Invalid load() syntax.",
                "F06"
            )
        )

        return

    filename = match.group(1).strip()

    if (
        filename.startswith('"')
        and filename.endswith('"')
    ):

        filename = filename[1:-1]

    filename = filename.strip()

    if filename == "":

        print(
            script_error(
                "EMPTY_LOAD_FILENAME",
                "Filename cannot be empty.",
                "F07"
            )
        )

        return

    if not filename.endswith(".json"):

        filename += ".json"

    path = os.path.join(
        SAVE_DIRECTORY,
        filename
    )

    if not os.path.exists(path):

        print(
            script_error(
                "SAVE_FILE_NOT_FOUND",
                f"'{filename}' does not exist.",
                "F08"
            )
        )

        return

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as e:

        print(
            script_error(
                "SAVE_FILE_CORRUPTED",
                str(e),
                "F09"
            )
        )

        return

    except Exception as e:

        print(
            script_error(
                "SAVE_FILE_READ_ERROR",
                str(e),
                "F10"
            )
        )

        return

    if not isinstance(data, dict):

        print(
            script_error(
                "INVALID_SAVE_STRUCTURE",
                "Save data must be object.",
                "F11"
            )
        )

        return

    try:

        SCRIPT_VARIABLES.clear()
        SCRIPT_DISPLAYS.clear()
        SCRIPT_FUNCTIONS.clear()
        SCRIPT_GAGES.clear()

        SCRIPT_VARIABLES.update(
            data.get("variables", {})
        )

        SCRIPT_DISPLAYS.update(
            data.get("displays", {})
        )

        SCRIPT_FUNCTIONS.update(
            data.get("functions", {})
        )

        SCRIPT_GAGES.update(
            data.get("gages", {})
        )

    except Exception as e:

        print(
            script_error(
                "SAVE_APPLY_ERROR",
                str(e),
                "F12"
            )
        )

        return

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ LOAD COMPLETE ] "
        f"{filename}"
        f"{C.RESET}"
    )

def cmd_reset(command):

    if command != "reset()":

        print(
            script_error(
                "INVALID_RESET_SYNTAX",
                "Invalid reset() syntax.",
                "R01"
            )
        )

        return

    SCRIPT_VARIABLES.clear()
    SCRIPT_DISPLAYS.clear()
    SCRIPT_FUNCTIONS.clear()
    SCRIPT_GAGES.clear()

    ACTIVE_INTERVALS.clear()

    print(
        f"{C.BRIGHT_RED}"
        f"[ MEMORY RESET COMPLETE ]"
        f"{C.RESET}"
    )

def cmd_del(command):

    match = re.fullmatch(
        r'del\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_DEL_SYNTAX",
                "Invalid del() syntax.",
                "D01"
            )
        )

        return

    name = match.group(1).strip()

    if name not in SCRIPT_VARIABLES:

        print(
            script_error(
                "VARIABLE_NOT_FOUND",
                f"Variable '{name}' does not exist.",
                "D02"
            )
        )

        return

    del SCRIPT_VARIABLES[name]

    print(
        f"{C.BRIGHT_RED}"
        f"[ VARIABLE DELETED ] "
        f"{name}"
        f"{C.RESET}"
    )

def cmd_memory(command):

    if command != "memory()":

        print(
            script_error(
                "INVALID_MEMORY_SYNTAX",
                "Invalid memory() syntax.",
                "M01"
            )
        )

        return

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== VARIABLES =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_VARIABLES) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key, value in SCRIPT_VARIABLES.items():

            print(
                f"{C.BRIGHT_CYAN}"
                f"{key}"
                f"{C.RESET}"
                f" = "
                f"{C.BRIGHT_WHITE}"
                f"{repr(value)}"
                f"{C.RESET}"
            )

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== DISPLAYS =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_DISPLAYS) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key, value in SCRIPT_DISPLAYS.items():

            print(
                f"{C.BRIGHT_YELLOW}"
                f"{key}"
                f"{C.RESET}"
                f" = "
                f"{C.BRIGHT_WHITE}"
                f"{value}"
                f"{C.RESET}"
            )

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== FUNCTIONS =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_FUNCTIONS) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key in SCRIPT_FUNCTIONS.keys():

            print(
                f"{C.BRIGHT_GREEN}"
                f"{key}"
                f"{C.RESET}"
            )

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== GAGES =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_GAGES) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key in SCRIPT_GAGES.keys():

            print(
                f"{C.BRIGHT_MAGENTA}"
                f"{key}"
                f"{C.RESET}"
            )

HELP_CATEGORIES = {

    "1": {
        "title": "VARIABLES / OUTPUT",
        "content": """
============================================================
VARIABLES / OUTPUT
============================================================

int(name,value)
------------------------------------------------------------
Create or overwrite a variable.

The value can be:
- numbers
- text
- expressions
- variable calculations

Examples:
int(hp,100)
int(power,8+9)
int(total,hp+50)

------------------------------------------------------------

on(value)
------------------------------------------------------------
Display values to the terminal.

Supports:
- text
- variables
- expressions
- calculations

Examples:
on("HELLO")
on(hp)
on(8+9)
on(hp+power)

------------------------------------------------------------

input(name)
------------------------------------------------------------
Store keyboard input into a variable.

Example:
input(username)

============================================================
"""
    },

    "2": {
        "title": "DISPLAY SYSTEM",
        "content": """
============================================================
DISPLAY SYSTEM
============================================================

display(name)
------------------------------------------------------------
Create a display object.

Displays are lightweight UI elements
that can be turned ON or OFF.

Example:
display(power)

------------------------------------------------------------

in dis (name)=0/1
------------------------------------------------------------
Control display visibility.

0 = hidden
1 = visible

Example:
in dis (power)=1

============================================================
"""
    },

    "3": {
        "title": "FUNCTION SYSTEM",
        "content": """
============================================================
FUNCTION SYSTEM
============================================================

func name(){...}
------------------------------------------------------------
Create a reusable function.

Example:
func heal(){
    on("HEAL")
}

------------------------------------------------------------

name.run()
------------------------------------------------------------
Execute a function.

Example:
heal.run()

------------------------------------------------------------

>> value
------------------------------------------------------------
Return value from function.

The return value is stored in FUNC_RETURN_VALUE.

Example:
func getValue(){
    int(x,100)
    >> x
}

getValue.run()
on(FUNC_RETURN_VALUE)

============================================================
"""
    },

    "4": {
        "title": "CONTROL FLOW",
        "content": """
============================================================
CONTROL FLOW
============================================================

if(condition){...}
------------------------------------------------------------
Execute code if condition is true.

Example:
if(hp>0){
    on("ALIVE")
}

------------------------------------------------------------

ifel(condition){...}
------------------------------------------------------------
Execute code if previous if failed.

Works like "else if".

Example:
ifel(hp<=0){
    on("DEAD")
}

------------------------------------------------------------

else{...}
------------------------------------------------------------
Execute code if all previous conditions failed.

Example:
else{
    on("UNKNOWN")
}

------------------------------------------------------------

while(condition){...}
------------------------------------------------------------
Loop while condition remains true.

Example:
while(x>0){
    on(x)
    int(x,x-1)
}

============================================================
"""
    },

    "5": {
        "title": "ARRAY SYSTEM",
        "content": """
============================================================
ARRAY SYSTEM
============================================================

inli(name,[...])
------------------------------------------------------------
Create an array.

Example:
inli(nums,[1,2,3])

------------------------------------------------------------

array[index]
------------------------------------------------------------
Read a value from an array.

Example:
on(nums[0])

------------------------------------------------------------

array.on(value)
------------------------------------------------------------
Add element to end of array.

Example:
nums.on(4)

------------------------------------------------------------

array.unon(value)
------------------------------------------------------------
Add element to beginning of array.

Example:
nums.unon(0)

------------------------------------------------------------

array.off()
------------------------------------------------------------
Remove last element from array.

Example:
nums.off()

------------------------------------------------------------

array.unoff()
------------------------------------------------------------
Remove first element from array.

Example:
nums.unoff()

------------------------------------------------------------

array.pointer(index,value)
------------------------------------------------------------
Replace value at index.

Example:
nums.pointer(0,99)

============================================================
"""
    },

    "6": {
        "title": "GAGE SYSTEM",
        "content": """
============================================================
GAGE SYSTEM
============================================================

gage(name)
------------------------------------------------------------
Create a 10-slot gage bar.
The results will not be displayed until a value is entered.

Example:
gage(health)

Result:
[□□□□□□□□□□]

------------------------------------------------------------

name.gagecn(value)
------------------------------------------------------------
Fill gage from left side.

Range:
0 - 10

Example:
health.gagecn(7)

Result:
[■■■■■■■□□□]

------------------------------------------------------------

name.gagepin(index,value)
------------------------------------------------------------
Modify a specific slot.

1 = filled
0 = empty

Example:
health.gagepin(5,1)

============================================================
"""
    },

    "7": {
        "title": "MATH SYSTEM",
        "content": """
============================================================
MATH SYSTEM
============================================================

M.random()
------------------------------------------------------------
Generate random float value.

Range:
0.0 - 1.0

Example:
int(x,M.random())

------------------------------------------------------------

M.floor(value)
------------------------------------------------------------
Round number downward.

Example:
int(x,M.floor(3.9))

Result:
3

------------------------------------------------------------

M.round(value)
------------------------------------------------------------
Round number normally.

Example:
int(x,M.round(3.5))

Result:
4

============================================================
"""
    },

    "8": {
        "title": "TIMER SYSTEM",
        "content": """
============================================================
TIMER SYSTEM
============================================================

settime(ms){...}
------------------------------------------------------------
Execute code once after delay.

Time unit:
milliseconds

Example:
settime(1000){
    on("READY")
}

------------------------------------------------------------

setInter(ms){...}
------------------------------------------------------------
Execute code repeatedly.

Example:
setInter(500){
    on("tick")
}

------------------------------------------------------------

clearInter(id)
------------------------------------------------------------
Stop interval execution.

Example:
clearInter(1)

============================================================
"""
    },

    "9": {
        "title": "TOUCH SYSTEM",
        "content": """
============================================================
TOUCH SYSTEM
============================================================

touch.w={...}
touch.a={...}
touch.s={...}
touch.d={...}

------------------------------------------------------------
Bind commands to movement keys.

w = up
a = left
s = down
d = right

Example:
touch.w={
    on("UP")
}

------------------------------------------------------------

touch()
------------------------------------------------------------
Start touch input mode.

============================================================
"""
    },

    "10": {
        "title": "CRYPTO SYSTEM",
        "content": """
============================================================
CRYPTO SYSTEM
============================================================

encrypt(value)
------------------------------------------------------------
Encrypt text using Cipher-X encoding.

Example:
encrypt("HELLO")

------------------------------------------------------------

decrypt(value)
------------------------------------------------------------
Decode Cipher-X encrypted text.

Example:
decrypt(code)

============================================================
"""
    },

    "11": {
        "title": "FILE SYSTEM",
        "content": """
============================================================
FILE SYSTEM
============================================================

save(filename)
------------------------------------------------------------
Save current memory state.

Example:
save("game1")

------------------------------------------------------------

load(filename)
------------------------------------------------------------
Load saved memory state.

Example:
load("game1")

------------------------------------------------------------

reset()
------------------------------------------------------------
Clear all engine memory.

============================================================
"""
    },

    "12": {
        "title": "SYSTEM COMMANDS",
        "content": """
============================================================
SYSTEM COMMANDS
============================================================

clear()
------------------------------------------------------------
Clear terminal screen.

------------------------------------------------------------

del(name)
------------------------------------------------------------
Delete a variable or object.

Example:
del(hp)

------------------------------------------------------------

memory()
------------------------------------------------------------
Display current engine memory.

------------------------------------------------------------

wait(sec)
------------------------------------------------------------
Pause execution temporarily.

Example:
wait(1)

------------------------------------------------------------

exit()
------------------------------------------------------------
Shutdown Light Script.

============================================================
"""
    }

}

def script_help():

    while True:

        print()

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╔════════════════════════════════════════════════╗"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "║             HELP MENU                         ║"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╚════════════════════════════════════════════════╝"
            f"{C.RESET}"
        )

        print()

        for key, value in HELP_CATEGORIES.items():

            print(
                f"{C.BRIGHT_GREEN}"
                f"  [{key:>2}] "
                f"{value['title']}"
                f"{C.RESET}"
            )

        print()

        print(
            f"{C.BRIGHT_RED}"
            "  [ 0] EXIT HELP"
            f"{C.RESET}"
        )

        print()

        choice = input(
            f"{C.BRIGHT_CYAN}HELP >> {C.RESET}"
        ).strip()

        if choice == "0":

            break

        if choice in HELP_CATEGORIES:

            print()

            print(
                f"{C.BRIGHT_WHITE}"
                f"{HELP_CATEGORIES[choice]['content']}"
                f"{C.RESET}"
            )

            input(
                f"{C.BRIGHT_BLACK}"
                "Press Enter to continue..."
                f"{C.RESET}"
            )

            continue

        print(
            script_error(
                "INVALID_HELP_MENU",
                "Unknown help category selected.",
                "H01"
            )
        )

def cmd_help(command):

    if command != "help()":

        print(
            script_error(
                "INVALID_HELP_SYNTAX",
                "Invalid help() syntax.",
                "H02"
            )
        )

        return

    script_help()

ENGINE_STATE = {

    "boot_time": time.time(),

    "executed_commands": 0,
    "scripts_executed": 0,

    "runtime_errors": 0,

    "last_error": None,
}

def script_console():

    while True:

        print()

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╔════════════════════════════════════════════════╗"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "║          LIGHT SCRIPT CONSOLE                ║"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╚════════════════════════════════════════════════╝"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_BLACK}"
            "  Use ';' to separate commands"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_BLACK}"
            "  Type 'exit' to return"
            f"{C.RESET}"
        )

        print()

        try:

            raw = input(
                f"{C.BRIGHT_YELLOW}SCRIPT >> {C.RESET}"
            )

        except KeyboardInterrupt:

            print()

            slow_print(
                "[ LIGHT SCRIPT INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        except EOFError:

            print(
                script_error(
                    "SCRIPT_INPUT_ERROR",
                    "Input stream closed.",
                    "P12"
                )
            )

            break

        raw = raw.strip()

        if raw.lower() == "exit":

            print()

            slow_print(
                "[ LIGHT SCRIPT CLOSED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        if raw == "":
            continue

        print()

        slow_print(
            "[ EXECUTING SCRIPT ]",
            0.003,
            C.BRIGHT_MAGENTA
        )

        try:

            execute_script(raw)

        except KeyboardInterrupt:

            print()

            slow_print(
                "[ SCRIPT INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

        except Exception as e:

            print(
                script_error(
                    "SCRIPT_RUNTIME_FAILURE",
                    str(e),
                    "P13"
                )
            )

def script_menu():

    while True:

        print()

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╔════════════════════════════════════════════════╗"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "║          LIGHT SCRIPT MENU                   ║"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╚════════════════════════════════════════════════╝"
            f"{C.RESET}"
        )

        print()

        print(
            f"{C.BRIGHT_GREEN}  [1]{C.WHITE} Run Script"
        )

        print(
            f"{C.BRIGHT_CYAN}  [2]{C.WHITE} Help"
        )

        print(
            f"{C.BRIGHT_YELLOW}  [3]{C.WHITE} Clear Memory"
        )

        print(
            f"{C.BRIGHT_BLUE}  [4]{C.WHITE} Debug Memory"
        )

        print(
            f"{C.BRIGHT_RED}  [5]{C.WHITE} Exit LIGHT SCRIPT"
        )

        print()

        try:

            choice = input(
                f"{C.BRIGHT_MAGENTA}SCRIPT >> {C.RESET}"
            )

        except KeyboardInterrupt:

            print()

            slow_print(
                "[ SCRIPT MENU INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        except EOFError:

            print(
                script_error(
                    "SCRIPT_MENU_INPUT_ERROR",
                    "Input stream closed.",
                    "P14"
                )
            )

            break

        choice = choice.strip()

        if choice == "1":

            script_console()

        elif choice == "2":

            script_help()

        elif choice == "3":

            SCRIPT_VARIABLES.clear()
            SCRIPT_DISPLAYS.clear()
            SCRIPT_FUNCTIONS.clear()
            SCRIPT_GAGES.clear()
            ACTIVE_INTERVALS.clear()

            print()

            slow_print(
                "[ SCRIPT MEMORY CLEARED ]",
                0.005,
                C.BRIGHT_YELLOW
            )

        elif choice == "4":

            print()

            print(
                f"{C.BRIGHT_MAGENTA}"
                "╔════════════════════════════════════════════════╗"
            )

            print(
                f"{C.BRIGHT_MAGENTA}"
                "║           SCRIPT MEMORY STATE                ║"
                f"{C.RESET}"
            )

            print(
                f"{C.BRIGHT_MAGENTA}"
                "╚════════════════════════════════════════════════╝"
                f"{C.RESET}"
            )

            print()

            print(
                f"{C.BRIGHT_GREEN}[ VARIABLES ]{C.RESET}"
            )

            if SCRIPT_VARIABLES:

                for key, value in SCRIPT_VARIABLES.items():

                    print(
                        f"{C.BRIGHT_CYAN}"
                        f"  {key}"
                        f"{C.BRIGHT_BLACK} = "
                        f"{C.BRIGHT_YELLOW}{repr(value)}"
                        f"{C.RESET}"
                    )

            else:

                print(
                    f"{C.BRIGHT_BLACK}  [ EMPTY ]{C.RESET}"
                )

            print()

            print(
                f"{C.BRIGHT_CYAN}[ FUNCTIONS ]{C.RESET}"
            )

            if SCRIPT_FUNCTIONS:

                for key in SCRIPT_FUNCTIONS.keys():

                    print(
                        f"{C.BRIGHT_WHITE}"
                        f"  {key}()"
                        f"{C.RESET}"
                    )

            else:

                print(
                    f"{C.BRIGHT_BLACK}  [ EMPTY ]{C.RESET}"
                )

            print()

        elif choice == "5":

            print()

            slow_print(
                "[ EXITING LIGHT SCRIPT ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        elif choice == "":

            continue

        else:

            print(
                script_error(
                    "INVALID_SCRIPT_MENU",
                    "Unknown script menu index.",
                    "P15"
                )
            )

def process_script_engine():

    print()

    try:

        script_banner()

    except Exception:

        print(
            f"{C.BRIGHT_MAGENTA}"
            "[ LIGHT SCRIPT ]"
            f"{C.RESET}"
        )

    try:

        slow_print(
            "[ LIGHT SCRIPT ONLINE ]",
            0.005,
            C.BRIGHT_MAGENTA
        )

    except Exception:

        print("[ LIGHT SCRIPT ONLINE ]")

    try:

        script_menu()

    except KeyboardInterrupt:

        print()

        slow_print(
            "[ LIGHT SCRIPT INTERRUPTED ]",
            0.005,
            C.BRIGHT_RED
        )

    except Exception as e:

        print(
            script_error(
                "SCRIPT_ENGINE_FAILURE",
                str(e),
                "P16"
            )
        )

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def ui_fancy_box(title, subtitle=""):

    print(
        f"{C.BRIGHT_MAGENTA}"
        "╔════════════════════════════════════════════════╗"
    )

    print(
        "║"
        f" {title:^44} "
        "║"
    )

    if subtitle != "":

        print(
            "║"
            f" {subtitle:^44} "
            "║"
        )

    print(
        "╚════════════════════════════════════════════════╝"
        f"{C.RESET}"
    )

def ui_fancy_menu(index, text, color):

    print(
        f"{color}"
        f"  ▸ [{index}] {text}"
        f"{C.RESET}"
    )

def main():

    while True:

        clear_screen()

        print()

        ui_fancy_box(
            "CIPHER-X",
            "ENCRYPTION PROTOCOL v1.10"
        )

        print()

        print(
            f"{C.BRIGHT_BLACK}"
            "  ═══════════════════════════════════════════"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}  Select Function"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_BLACK}"
            "  ═══════════════════════════════════════════"
            f"{C.RESET}"
        )

        print()

        ui_fancy_menu(
            "1",
            "ENCRYPT TEXT",
            C.BRIGHT_CYAN
        )

        ui_fancy_menu(
            "2",
            "DECRYPT TEXT",
            C.BRIGHT_GREEN
        )

        ui_fancy_menu(
            "3",
            "LIGHT SCRIPT",
            C.BRIGHT_YELLOW
        )

        ui_fancy_menu(
            "4",
            "EXIT",
            C.BRIGHT_RED
        )

        print()

        try:

            choice = input(
                f"{C.BRIGHT_MAGENTA}"
                "  ➜ SYSTEM > "
                f"{C.RESET}"
            ).strip()

        except KeyboardInterrupt:

            print()
            break

        except EOFError:

            print(
                script_error(
                    "MAIN_INPUT_ERROR",
                    "Input stream closed.",
                    "SYS01"
                )
            )

            break

        if choice == "1":

            clear_screen()

            print()

            ui_fancy_box(
                "ENCRYPT MODE",
                "INPUT → CIPHER"
            )

            print()

            text = input(
                f"{C.BRIGHT_CYAN}"
                "  ➜ TEXT > "
                f"{C.RESET}"
            )

            print()

            try:

                result = encrypt(text)

                print(
                    f"{C.BRIGHT_CYAN}"
                    "╔════════════════════════════════════════════════╗"
                )

                print(
                    "║            ENCRYPT RESULT                    ║"
                )

                print(
                    "╚════════════════════════════════════════════════╝"
                    f"{C.RESET}"
                )

                print()

                print(
                    f"{C.BRIGHT_WHITE}"
                    f"  {result}"
                    f"{C.RESET}"
                )

            except Exception as e:

                print(
                    script_error(
                        "ENCRYPTION_FAILURE",
                        str(e),
                        "ENCX"
                    )
                )

            print()

            input(
                f"{C.BRIGHT_BLACK}"
                "  Press ENTER to return..."
                f"{C.RESET}"
            )

        elif choice == "2":

            clear_screen()

            print()

            ui_fancy_box(
                "DECRYPT MODE",
                "CIPHER → TEXT"
            )

            print()

            print(
                f"{C.BRIGHT_BLACK}"
                "  Format: 5 chars per space (XXXXX XXXXX ...)"
                f"{C.RESET}"
            )

            print()

            text = input(
                f"{C.BRIGHT_GREEN}"
                "  ➜ CIPHER > "
                f"{C.RESET}"
            )

            print()

            try:

                result = decrypt(text)

                print(
                    f"{C.BRIGHT_GREEN}"
                    "╔════════════════════════════════════════════════╗"
                )

                print(
                    "║            DECRYPT RESULT                    ║"
                )

                print(
                    "╚════════════════════════════════════════════════╝"
                    f"{C.RESET}"
                )

                print()

                print(
                    f"{C.BRIGHT_WHITE}"
                    f"  {result}"
                    f"{C.RESET}"
                )

            except Exception as e:

                print(
                    script_error(
                        "DECRYPTION_FAILURE",
                        str(e),
                        "DECX"
                    )
                )

            print()

            input(
                f"{C.BRIGHT_BLACK}"
                "  Press ENTER to return..."
                f"{C.RESET}"
            )

        elif choice == "3":

            process_script_engine()

        elif choice == "4":

            clear_screen()

            print()

            ui_fancy_box(
                "SYSTEM CLOSED"
            )

            print()

            break

        else:

            print()

            print(
                script_error(
                    "INVALID_MAIN_MENU",
                    "Unknown menu index.",
                    "SYS02"
                )
            )

            time.sleep(1)

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()

        try:

            slow_print(
                "[ SYSTEM INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

        except:

            print("[ SYSTEM INTERRUPTED ]")

    except Exception as e:

        print(
            script_error(
                "FATAL_SYSTEM_ERROR",
                str(e),
                "P17"
            )
        )
