
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
# =========================================================
# SCRIPT ENGINE MEMORY
# =========================================================

SCRIPT_VARIABLES = {}
SCRIPT_DISPLAYS = {}
SCRIPT_FUNCTIONS = {}
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
# CIPHER-X CORE

# ENCRYPT / DECRYPT SYSTEM

# REBUILD FROM ORIGINAL PROTOCOL
# =========================================================
# CIPHER-X ENCRYPTION CORE
# ORIGINAL PROTOCOL EDITION
# =========================================================

import string
import re

# =========================================================
# FLAGS
# =========================================================

FLAG_X = r'\0240'
FLAG_Y = r'\0250'
FLAG_END = r'\0000'

# =========================================================
# VALIDATION
# =========================================================

Y_VALID = set("あうおアウオやゆよヤユヨ")
X_VALID = set("あいうえおやゆよつわアイウエオヤユヨツワ")

# =========================================================
# SMALL CHARACTER MAP
# =========================================================

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

# =========================================================
# UTIL
# =========================================================


def is_hiragana(char):
    return 'ぁ' <= char <= 'ゖ'



def is_katakana(char):
    return 'ァ' <= char <= 'ヶ'



def make_code(prefix, row, dan):
    return f"{prefix}{row}{dan}"

# =========================================================
# ROW MAP
# =========================================================

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

# =========================================================
# DAN MAP
# =========================================================

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

# =========================================================
# SPECIAL CHARACTERS
# =========================================================

SPECIAL_ENC = {

    '\n': r'\\0140',

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

# =========================================================
# ALPHABET TABLE
# =========================================================

ALP_ENC = {}

for i, char in enumerate(string.ascii_uppercase, 1):
    ALP_ENC[char] = f"03{i:02d}0"

for i, char in enumerate(string.ascii_lowercase, 1):
    ALP_ENC[char] = f"03{i:02d}1"

ALP_DEC = {
    value: key
    for key, value in ALP_ENC.items()
}

# =========================================================
# AUTO BUILD TABLE
# =========================================================

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

# =========================================================
# FORMAT VALIDATION
# =========================================================


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

# =========================================================
# ENCRYPT
# =========================================================


def encrypt(text):

    if text is None:
        return ""

    text = str(text)

    result = []

    for char in text:

        # =============================================
        # SPACE
        # =============================================

        if char == " ":
            continue

        # =============================================
        # SMALL HIRAGANA
        # =============================================

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

        # =============================================
        # JAPANESE
        # =============================================

        if char in JP_ENC:
            result.append(JP_ENC[char])
            continue

        # =============================================
        # ALPHABET
        # =============================================

        if char in ALP_ENC:
            result.append(ALP_ENC[char])
            continue

        # =============================================
        # UNKNOWN CHARACTER
        # =============================================

        result.append(
            rf'\@<{char}>'
        )

    return " ".join(result)

# =========================================================
# DECRYPT
# =========================================================


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

        # =============================================
        # FLAG START
        # =============================================

        if block in (FLAG_X, FLAG_Y):

            if active_flag:

                return fatal(
                    "FLAG_COLLISION",
                    "Nested operational flags detected.",
                    "04"
                )

            active_flag = block
            continue

        # =============================================
        # FLAG END
        # =============================================

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

        # =============================================
        # CUSTOM SYMBOL
        # =============================================

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

        # =============================================
        # Y FLAG
        # =============================================

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

        # =============================================
        # X FLAG
        # =============================================

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

    # =============================================
    # FLAG EOF CHECK
    # =============================================

    if active_flag:

        return fatal(
            "FLAG_TERMINATION_MISSING",
            "Flag session reached EOF before closure.",
            "09"
        )

    return result

# =========================================================
# SCRIPT ENGINE UI
# =========================================================

def script_banner():

    print(f"{C.BRIGHT_MAGENTA}{C.BOLD}")

    print("╔══════════════════════════════════════════════╗")
    print("║         CIPHER-X  Light Script               ║")
    print("║               PROTOCOL v1.0                  ║")
    print("╚══════════════════════════════════════════════╝")

    print(C.RESET)

# =========================================================
# SCRIPT ENGINE ERROR
# =========================================================

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

# =========================================================
# SAFE VALUE PARSER
# =========================================================

def parse_value(value):

    if value is None:
        return ""

    value = str(value).strip()

    # =============================================
    # INTEGER
    # =============================================

    if re.fullmatch(r'-?\d+', value):

        try:
            return int(value)

        except ValueError:
            return 0

    # =============================================
    # FLOAT
    # =============================================

    if re.fullmatch(r'-?\d+\.\d+', value):

        try:
            return float(value)

        except ValueError:
            return 0.0

    # =============================================
    # STRING
    # =============================================

    if (
        len(value) >= 2 and
        value.startswith('"') and
        value.endswith('"')
    ):

        return value[1:-1]

    # =============================================
    # BOOLEAN
    # =============================================

    lower = value.lower()

    if lower == "true":
        return True

    if lower == "false":
        return False

    # =============================================
    # M.random()
    # =============================================

    if value == "M.random()":

        return random.random()

    # =============================================
    # M.floor()
    # =============================================

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

    # =============================================
    # M.round()
    # =============================================

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

    # =============================================
    # VARIABLE
    # =============================================

    if value in SCRIPT_VARIABLES:

        return SCRIPT_VARIABLES[value]

    # =============================================
    # RAW
    # =============================================

    return value

# =========================================================
# SAFE EXPRESSION EVALUATOR
# =========================================================

def safe_eval(expression):

    expression = str(expression).strip()

    # 不正文字ブロック
    if not SAFE_EXPRESSION_PATTERN.fullmatch(expression):

        raise ValueError(
            "Unsafe expression detected."
        )

    # 危険キーワード遮断
    blocked = [
        "__",
        "import",
        "exec",
        "eval",
        "open",
        "os",
        "sys",
        "subprocess",
        "globals",
        "locals",
        "compile"
    ]

    lower = expression.lower()

    for word in blocked:

        if word in lower:

            raise ValueError(
                f"Blocked keyword: {word}"
            )

    return eval(
        expression,
        {"__builtins__": {}},
        SCRIPT_VARIABLES
    )

# =========================================================
# DISPLAY RENDER
# =========================================================

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

# =========================================================
# OUTPUT SYSTEM
# =========================================================

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

# =========================================================
# VARIABLE SYSTEM
# =========================================================

# =========================================================
# ARRAY SYSTEM
# =========================================================

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

    # =============================================
    # EMPTY ARRAY
    # =============================================

    if raw_items == "":

        SCRIPT_VARIABLES[name] = []

        print(
            f"{C.BRIGHT_GREEN}"
            f"[ ARRAY REGISTERED ] "
            f"{name}"
            f"{C.RESET}"
        )

        return

    # =============================================
    # PARSE ITEMS
    # =============================================

    items = []

    split_items = raw_items.split(",")

    for item in split_items:

        parsed = parse_value(
            item.strip()
        )

        items.append(parsed)

    # =============================================
    # STORE
    # =============================================

    SCRIPT_VARIABLES[name] = items

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ ARRAY REGISTERED ] "
        f"{name}"
        f"{C.RESET}"
    )

# =========================================================
# SAFE PATTERNS
# =========================================================

SAFE_VAR_PATTERN = re.compile(
    r'^[A-Za-z_][A-Za-z0-9_]*$'
)

SAFE_EXPRESSION_PATTERN = re.compile(
    r'^[0-9A-Za-z_+\-*/%().,\s]+$'
)

# =========================================================
# SAFE EVAL
# =========================================================

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

# =========================================================
# VARIABLE SYSTEM
# =========================================================

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

    # =============================================
    # VARIABLE NAME CHECK
    # =============================================

    if not SAFE_VAR_PATTERN.fullmatch(name):

        print(
            script_error(
                "INVALID_VARIABLE_NAME",
                f"'{name}' is not a valid variable name.",
                "S03A"
            )
        )
        return

    # =============================================
    # PARSE VALUE
    # =============================================

    parsed = parse_value(raw_value)

    # =============================================
    # EXPRESSION SUPPORT
    # =============================================

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

    # =============================================
    # STORE VARIABLE
    # =============================================

    SCRIPT_VARIABLES[name] = parsed
# =========================================================
# OUTPUT COMMAND
# =========================================================

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

# =========================================================
# DISPLAY DECLARATION
# =========================================================

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

    # =============================================
    # VARIABLE NAME CHECK
    # =============================================

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

# =========================================================
# DISPLAY INPUT
# =========================================================

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

# =========================================================
# FUNCTION STORAGE
# =========================================================

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

    # 空関数防止
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
# =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 2 / 6
# SAFE EXECUTION PATCH
# =========================================================

# =========================================================
# FUNCTION EXECUTION
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

    # =============================================
    # FUNCTION EXISTS
    # =============================================

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

    # =============================================
    # EMPTY BODY CHECK
    # =============================================

    if not body:

        print(
            script_error(
                "EMPTY_FUNCTION_BODY",
                f"Function '{name}' is empty.",
                "S12A"
            )
        )
        return

    # =============================================
    # EXECUTE
    # =============================================

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

# =========================================================
# TOUCH SYSTEM MEMORY
# =========================================================

TOUCH_BINDINGS = {
    "w": None,
    "a": None,
    "s": None,
    "d": None,
}

# =========================================================
# TOUCH BIND
# =========================================================

def cmd_touch_bind(command):

    match = re.fullmatch(
        r'touch\.([wasd])=\{(.+)\}',
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

    # =============================================
    # EMPTY BODY CHECK
    # =============================================

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

# =========================================================
# TOUCH LISTENER
# =========================================================

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

        # =============================================
        # EXIT
        # =============================================

        if key == "exit":

            print()

            slow_print(
                "[ TOUCH SESSION CLOSED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        # =============================================
        # INVALID KEY
        # =============================================

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

        # =============================================
        # UNBOUND
        # =============================================

        if body is None:

            print(
                script_error(
                    "UNBOUND_TOUCH_KEY",
                    f"'{key}' has no binding.",
                    "S15"
                )
            )
            continue

        # =============================================
        # EXECUTE
        # =============================================

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

# =========================================================
# TIMER SYSTEM
# =========================================================

ACTIVE_INTERVALS = {}
INTERVAL_COUNTER = 0

MIN_INTERVAL_MS = 10
MAX_INTERVAL_MS = 3600000

# =========================================================
# TIMER VALIDATION
# =========================================================

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

# =========================================================
# SETTIME
# =========================================================

def cmd_settime(command):

    match = re.fullmatch(
        r'settime\((\d+)\)\{(.+)\}',
        command
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

# =========================================================
# SETINTER
# =========================================================

def cmd_setinter(command):

    global INTERVAL_COUNTER

    match = re.fullmatch(
        r'setInter\((\d+)\)\{(.+)\}',
        command
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

# =========================================================
# CLEARINTER
# =========================================================

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
# IF SYSTEM
# =========================================================

def cmd_if(command):

    match = re.fullmatch(
        r'if\((.+?)\)\{(.+)\}',
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

    # =============================================
    # EMPTY BODY
    # =============================================

    if body == "":

        print(
            script_error(
                "EMPTY_IF_BODY",
                "if() body cannot be empty.",
                "S19A"
            )
        )
        return

    # =============================================
    # SAFE EVAL
    # =============================================

    try:

        result = safe_eval(condition)

    except Exception as e:

        print(
            script_error(
                "IF_EVALUATION_FAILED",
                str(e),
                "S20"
            )
        )
        return

    # =============================================
    # EXECUTE
    # =============================================

    if bool(result):

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "IF_RUNTIME_ERROR",
                    str(e),
                    "S20A"
                )
            )

# =========================================================
# WHILE SYSTEM
# =========================================================

def cmd_while(command):

    match = re.fullmatch(
        r'while\((.+?)\)\{(.+)\}',
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

    # =============================================
    # EMPTY BODY
    # =============================================

    if body == "":

        print(
            script_error(
                "EMPTY_WHILE_BODY",
                "while() body cannot be empty.",
                "S21A"
            )
        )
        return

    # =============================================
    # SAFETY LIMIT
    # =============================================

    safety = 0
    max_loops = 10000

    while True:

        safety += 1

        # =============================================
        # LOOP OVERFLOW
        # =============================================

        if safety > max_loops:

            print(
                script_error(
                    "WHILE_OVERFLOW",
                    "Loop exceeded safe limit.",
                    "S22"
                )
            )
            return

        # =============================================
        # CONDITION EVAL
        # =============================================

        try:

            result = safe_eval(condition)

        except Exception as e:

            print(
                script_error(
                    "WHILE_EVALUATION_FAILED",
                    str(e),
                    "S23"
                )
            )
            return

        # =============================================
        # BREAK
        # =============================================

        if not bool(result):
            break

        # =============================================
        # EXECUTE
        # =============================================

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "WHILE_RUNTIME_ERROR",
                    str(e),
                    "S23A"
                )
            )
            return

# =========================================================
# SCRIPT COMMAND EXECUTOR
# =========================================================

def execute_command(command):

    if command is None:
        return

    command = str(command).strip()

    if command == "":
        return

    # =============================================
    # int()
    # =============================================

    if command.startswith("int("):

        cmd_int(command)
        return

    # =============================================
    # inli()
    # =============================================

    if command.startswith("inli("):

        cmd_inli(command)
        return
    
    # =============================================
    # on()
    # =============================================

    if command.startswith("on("):

        cmd_on(command)
        return

    # =============================================
    # display()
    # =============================================

    if command.startswith("display("):

        cmd_display(command)
        return

    # =============================================
    # in dis ()
    # =============================================

    if command.startswith("in dis"):

        cmd_in_dis(command)
        return

    # =============================================
    # func
    # =============================================

    if command.startswith("func "):

        cmd_func(command)
        return

    # =============================================
    # function.run()
    # =============================================

    if re.fullmatch(
        r'[A-Za-z_][A-Za-z0-9_]*\.run\((.*?)\)',
        command
    ):

        cmd_func_run(command)
        return

    # =============================================
    # if()
    # =============================================

    if command.startswith("if("):

        cmd_if(command)
        return

    # =============================================
    # while()
    # =============================================

    if command.startswith("while("):

        cmd_while(command)
        return

    # =============================================
    # touch bind
    # =============================================

    if command.startswith("touch."):

        cmd_touch_bind(command)
        return
    # =============================================
    # settime()
    # =============================================
   
    if command.startswith("settime("):
    
        cmd_settime(command)
        return

    # =============================================
    # setInter()
    # =============================================
    
    if command.startswith("setInter("):
    
        cmd_setinter(command)
        return

    # =============================================
    # clearInter()
    # =============================================
    
    if command.startswith("clearInter("):
    
        cmd_clearinter(command)
        return

    # =============================================
    # touch()
    # =============================================

    if command == "touch()":

        touch_session()
        return

    # =============================================
    # UNKNOWN
    # =============================================

    print(
        script_error(
            "UNKNOWN_COMMAND",
            f"Unknown command '{command}'",
            "S16"
        )
    )

# =========================================================
# SCRIPT EXECUTOR
# =========================================================

# =========================================================
# SCRIPT EXECUTOR
# =========================================================

def execute_script(script):

    commands = []

    current = ""

    brace_depth = 0
    in_string = False

    i = 0

    while i < len(script):

        char = script[i]

        # =============================================
        # STRING TOGGLE
        # =============================================

        if char == '"':

            in_string = not in_string

            current += char
            i += 1
            continue

        # =============================================
        # BRACE TRACK
        # =============================================

        if not in_string:

            if char == "{":
                brace_depth += 1

            elif char == "}":
                brace_depth -= 1

        # =============================================
        # COMMAND SPLIT
        # =============================================

        if (
            char == ";" and
            brace_depth == 0 and
            not in_string
        ):

            if current.strip():
                commands.append(current.strip())

            current = ""

            i += 1
            continue

        current += char

        i += 1

    # =============================================
    # FINAL COMMAND
    # =============================================

    if current.strip():
        commands.append(current.strip())

    # =============================================
    # EXECUTION
    # =============================================

    for command in commands:

        execute_command(command)
# =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 3 / 6
# CONSOLE & MENU STABILITY PATCH
# =========================================================

# =========================================================
# SCRIPT ENGINE CONSOLE
# =========================================================

def script_console():

    while True:

        print()

        print(
            f"{C.BRIGHT_MAGENTA}[SCRIPT]{C.WHITE} "
            f"Enter Script Command"
        )

        print(
            f"{C.BRIGHT_BLACK}"
            "Use ';' to separate commands"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_BLACK}"
            "Type 'exit' to return"
            f"{C.RESET}"
        )

        print()

        # =============================================
        # INPUT
        # =============================================

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
                    "S17A"
                )
            )

            break

        raw = raw.strip()

        # =============================================
        # EXIT
        # =============================================

        if raw.lower() == "exit":

            print()

            slow_print(
                "[ LIGHT SCRIPT CLOSED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        # =============================================
        # EMPTY
        # =============================================

        if raw == "":
            continue

        # =============================================
        # EXECUTE
        # =============================================

        print()

        slow_print(
            "[ EXECUTING SCRIPT ]",
            0.003,
            C.BRIGHT_CYAN
        )

        print()

        try:

            execute_script(raw)

        except KeyboardInterrupt:

            print()

            slow_print(
                "[ SCRIPT EXECUTION INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

        except Exception as e:

            print(
                script_error(
                    "SCRIPT_RUNTIME_EXCEPTION",
                    str(e),
                    "S17"
                )
            )

# =========================================================
# HELP SYSTEM
# =========================================================

def script_help():

    print()

    print(
        f"{C.BRIGHT_CYAN}{C.BOLD}"
        "=============== SCRIPT HELP ==============="
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # int()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}int(name,value)"
        f"{C.WHITE} -> Variable declaration"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: int(hp,100)"
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # inli()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}inli(name,[...])"
        f"{C.WHITE} -> Create array"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: inli(items,["A","B","C"])'
        f"{C.RESET}"
    )

    print()
    # =====================================================
    # on()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}on(value)"
        f"{C.WHITE} -> Output text or variable"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: on("HELLO")'
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: on(hp)"
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # display()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}display(name)"
        f"{C.WHITE} -> Create display"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: display(power)"
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # in dis ()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}in dis (name)=0/1"
        f"{C.WHITE} -> Change display state"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "0 = ✕ / 1 = 〇"
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # func
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}func name()"
        f"{C.WHITE} -> Create function"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: func heal(){on("HEAL")}'
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # function.run()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}name.run()"
        f"{C.WHITE} -> Execute function"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: heal.run()"
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # if()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}if(condition)"
        f"{C.WHITE} -> Conditional execution"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: if(hp>0){on("ALIVE")}'
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # while()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}while(condition)"
        f"{C.WHITE} -> Loop execution"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: while(x<5){on(x)}'
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # touch bind
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}touch.w={{...}}"
        f"{C.WHITE} -> Bind touch key"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: touch.w={on("UP")}'
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # touch()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}touch()"
        f"{C.WHITE} -> Start touch session"
    )

    print()

    # =====================================================
    # settime()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}settime(ms){{...}}"
        f"{C.WHITE} -> Execute once after delay"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: settime(1000){on("READY")}'
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # setInter()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}setInter(ms){{...}}"
        f"{C.WHITE} -> Execute repeatedly"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: setInter(500){on("tick")}'
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # clearInter()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}clearInter(id)"
        f"{C.WHITE} -> Stop interval timer"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: clearInter(1)"
        f"{C.RESET}"
    )

    print()
    # =====================================================
    # M.random()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}M.random()"
        f"{C.WHITE} -> Random float (0.0 ~ 1.0)"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: int(r,M.random())"
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # M.floor()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}M.floor(value)"
        f"{C.WHITE} -> Round down"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: int(x,M.floor(4.9))"
        f"{C.RESET}"
    )

    print()

    # =====================================================
    # M.round()
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}M.round(value)"
        f"{C.WHITE} -> Round number"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "Example: int(x,M.round(4.6))"
        f"{C.RESET}"
    )

    print()
    # =====================================================
    # \ent
    # =====================================================

    print(
        f"{C.BRIGHT_GREEN}\\ent"
        f"{C.WHITE} -> New line"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        'Example: on("HELLO\\entWORLD")'
        f"{C.RESET}"
    )

    print()

    print(
        f"{C.BRIGHT_CYAN}"
        "==========================================="
        f"{C.RESET}"
    )

# =========================================================
# CLEAR SCRIPT MEMORY
# =========================================================

def clear_script_memory():

    SCRIPT_VARIABLES.clear()
    SCRIPT_DISPLAYS.clear()
    SCRIPT_FUNCTIONS.clear()

    # TOUCH RESET
    for key in TOUCH_BINDINGS.keys():

        TOUCH_BINDINGS[key] = None

# =========================================================
# SCRIPT MENU
# =========================================================

def script_menu():

    while True:

        print()

        print(
            f"{C.BRIGHT_GREEN}[1]{C.WHITE} Run Script"
        )

        print(
            f"{C.BRIGHT_CYAN}[2]{C.WHITE} Help"
        )

        print(
            f"{C.BRIGHT_YELLOW}[3]{C.WHITE} Clear Memory"
        )

        print(
            f"{C.BRIGHT_RED}[4]{C.WHITE} Exit LIGHT SCRIPT"
        )

        print()

        # =============================================
        # INPUT
        # =============================================

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
                    "S18A"
                )
            )

            break

        choice = choice.strip()

        # =============================================
        # RUN SCRIPT
        # =============================================

        if choice == "1":

            print()

            script_console()

        # =============================================
        # HELP
        # =============================================

        elif choice == "2":

            print()

            script_help()

        # =============================================
        # CLEAR MEMORY
        # =============================================

        elif choice == "3":

            try:

                clear_script_memory()

                print()

                slow_print(
                    "[ SCRIPT MEMORY CLEARED ]",
                    0.005,
                    C.BRIGHT_YELLOW
                )

            except Exception as e:

                print(
                    script_error(
                        "MEMORY_CLEAR_FAILED",
                        str(e),
                        "S18B"
                    )
                )

        # =============================================
        # EXIT
        # =============================================

        elif choice == "4":

            print()

            slow_print(
                "[ EXITING LIGHT SCRIPT ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        # =============================================
        # EMPTY INPUT
        # =============================================

        elif choice == "":

            continue

        # =============================================
        # INVALID
        # =============================================

        else:

            print(
                script_error(
                    "INVALID_SCRIPT_MENU",
                    "Unknown script menu index.",
                    "S18"
                )
            )
            # =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 4 / 6
# MAIN SYSTEM STABILITY PATCH
# =========================================================

# =========================================================
# SAFE RESULT BOX
# =========================================================

def safe_result_box(title, content, color):

    try:

        result_box(
            title,
            content,
            color
        )

    except Exception:

        print()

        print(
            f"{color}"
            f"[ {title} ]"
            f"{C.RESET}"
        )

        print(content)

# =========================================================
# SAFE FATAL
# =========================================================

def safe_fatal(code, message, errno):

    try:

        return fatal(
            code,
            message,
            errno
        )

    except Exception:

        return (
            f"[{errno}] "
            f"{code}: {message}"
        )

# =========================================================
# SAFE INPUT
# =========================================================

def safe_input(prompt=""):

    try:

        return input(prompt)

    except KeyboardInterrupt:
        raise

    except EOFError:

        print(
            script_error(
                "INPUT_STREAM_CLOSED",
                "Input stream closed.",
                "M01"
            )
        )

        return None

# =========================================================
# MENU
# =========================================================

def menu():

    print(
        f"{C.BRIGHT_GREEN}[1]{C.WHITE} Encrypt"
    )

    print(
        f"{C.BRIGHT_CYAN}[2]{C.WHITE} Decrypt"
    )

    print(
        f"{C.BRIGHT_MAGENTA}[3]{C.WHITE} LIGHT SCRIPT"
    )

    print(
        f"{C.BRIGHT_RED}[4]{C.WHITE} Exit"
    )

# =========================================================
# ENCRYPT FLOW
# =========================================================

def process_encrypt():

    print()

    raw = safe_input(
        f"{C.BRIGHT_CYAN}"
        f"Input Text"
        f"{C.WHITE} : "
        f"{C.RESET}"
    )

    if raw is None:
        return

    print()

    slow_print(
        "[ PROCESSING ENCRYPTION ]",
        0.005,
        C.BRIGHT_MAGENTA
    )

    try:

        result = encrypt(raw)

    except Exception as e:

        print(
            safe_fatal(
                "ENCRYPTION_FAILED",
                str(e),
                "M02"
            )
        )

        return

    safe_result_box(
        "ENCRYPTED OUTPUT",
        result,
        C.BRIGHT_GREEN
    )

# =========================================================
# DECRYPT FLOW
# =========================================================

def process_decrypt():

    print()

    raw = safe_input(
        f"{C.BRIGHT_CYAN}"
        f"Input Code"
        f"{C.WHITE} : "
        f"{C.RESET}"
    )

    if raw is None:
        return

    print()

    slow_print(
        "[ PROCESSING DECRYPTION ]",
        0.005,
        C.BRIGHT_BLUE
    )

    try:

        result = decrypt(raw)

    except Exception as e:

        print(
            safe_fatal(
                "DECRYPTION_FAILED",
                str(e),
                "M03"
            )
        )

        return

    safe_result_box(
        "DECRYPTED OUTPUT",
        result,
        C.BRIGHT_CYAN
    )

# =========================================================
# SCRIPT ENGINE FLOW
# =========================================================

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

        print(
            "[ LIGHT SCRIPT ONLINE ]"
        )

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
            safe_fatal(
                "SCRIPT_ENGINE_FAILURE",
                str(e),
                "M04"
            )
        )

# =========================================================
# MAIN LOOP
# =========================================================

def main():

    # =============================================
    # TERMINAL TITLE
    # =============================================

    try:

        print(
            "\033]0;CIPHER-X TERMINAL SYSTEM\a",
            end=""
        )

    except:
        pass

    # =============================================
    # BANNER
    # =============================================

    try:

        print()

        print(
            f"{C.BRIGHT_MAGENTA}{C.BOLD}"
            "===================================================="
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}{C.BOLD}"
            "                 CIPHER-X TERMINAL                 "
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_BLACK}"
            "             ENCRYPTION CORE SYSTEM                "
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_CYAN}"
            "              installed : Light Script             "
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_CYAN}"
            "                    ver 1.1.0                      "
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}{C.BOLD}"
            "===================================================="
            f"{C.RESET}"
        )

        print()

    except Exception:

        print(
            f"{C.BRIGHT_GREEN}"
            "CIPHER-X"
            f"{C.RESET}"
        )

    # =============================================
    # BOOT
    # =============================================

    try:

        slow_print(
            "[ SYSTEM BOOT COMPLETE ]",
            0.01,
            C.BRIGHT_GREEN
        )

        slow_print(
            "[ ENCRYPTION MATRIX ONLINE ]",
            0.005,
            C.BRIGHT_CYAN
        )

        slow_print(
            "[ LIGHT SCRIPT RUNTIME READY ]",
            0.005,
            C.BRIGHT_MAGENTA
        )

        print()

    except Exception:

        print("SYSTEM BOOT COMPLETE")
    # =============================================
    # MAIN LOOP
    # =============================================

    while True:

        print()

        try:

            menu()

        except Exception as e:

            print(
                safe_fatal(
                    "MENU_RENDER_FAILED",
                    str(e),
                    "M05"
                )
            )

            return

        print()

        # =============================================
        # INPUT
        # =============================================

        try:

            choice = safe_input(
                f"{C.BRIGHT_YELLOW}>> {C.RESET}"
            )

        except KeyboardInterrupt:

            print()

            slow_print(
                "SYSTEM INTERRUPT...",
                0.01,
                C.BRIGHT_RED
            )

            break

        if choice is None:
            break

        choice = choice.strip()

        # =============================================
        # EMPTY
        # =============================================

        if choice == "":
            continue

        # =============================================
        # ENCRYPT
        # =============================================

        if choice == "1":

            process_encrypt()

        # =============================================
        # DECRYPT
        # =============================================

        elif choice == "2":

            process_decrypt()

        # =============================================
        # SCRIPT ENGINE
        # =============================================

        elif choice == "3":

            process_script_engine()

        # =============================================
        # EXIT
        # =============================================

        elif choice == "4":

            print()

            try:

                slow_print(
                    "SYSTEM EXIT...",
                    0.01,
                    C.BRIGHT_RED
                )

            except Exception:

                print("SYSTEM EXIT...")

            break

        # =============================================
        # INVALID
        # =============================================

        else:

            print(
                safe_fatal(
                    "INVALID_MENU",
                    "Unknown menu index selected.",
                    "10"
                )
            )
            # =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 5 / 6
# ADVANCED SCRIPT PARSER PATCH
# =========================================================

# =========================================================
# SMART SCRIPT SPLITTER
# =========================================================

# =========================================================
# SMART SCRIPT SPLITTER
# =========================================================

def split_script_commands(script):

    commands = []

    current = []

    brace_depth = 0
    in_string = False

    escape = False

    for char in script:

        # =============================================
        # ESCAPE
        # =============================================

        if escape:

            current.append(char)
            escape = False
            continue

        if char == "\\":

            current.append(char)
            escape = True
            continue

        # =============================================
        # STRING TOGGLE
        # =============================================

        if char == '"':

            in_string = not in_string

            current.append(char)
            continue

        # =============================================
        # INSIDE STRING
        # =============================================

        if in_string:

            current.append(char)
            continue

        # =============================================
        # BRACE DEPTH
        # =============================================

        if char == "{":

            brace_depth += 1

            current.append(char)
            continue

        if char == "}":

            brace_depth -= 1

            # =========================================
            # INVALID CLOSE
            # =========================================

            if brace_depth < 0:

                raise Exception(
                    "[S30] UNEXPECTED_BRACE_CLOSE"
                )

            current.append(char)
            continue

        # =============================================
        # COMMAND SPLIT
        # =============================================

        if char == ";" and brace_depth == 0:

            command = "".join(current).strip()

            # 空命令防止
            if command != "":

                commands.append(command)

            current = []

            continue

        # =============================================
        # NORMAL CHAR
        # =============================================

        current.append(char)

    # =====================================================
    # STRING NOT CLOSED
    # =====================================================

    if in_string:

        raise Exception(
            "[S31] STRING_NOT_TERMINATED"
        )

    # =====================================================
    # BRACE NOT CLOSED
    # =====================================================

    if brace_depth != 0:

        raise Exception(
            "[S32] BRACE_NOT_TERMINATED"
        )

    # =====================================================
    # LAST COMMAND
    # =====================================================

    final_command = "".join(current).strip()

    if final_command != "":

        commands.append(final_command)

    return commands
# =========================================================
# COMMAND VALIDATOR
# =========================================================

def validate_command_structure(command):

    if not command:
        return False

    # =============================================
    # BRACE CHECK
    # =============================================

    brace = 0
    in_string = False
    escape = False

    for char in command:

        if escape:
            escape = False
            continue

        if char == "\\":
            escape = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            brace += 1

        elif char == "}":
            brace -= 1

            if brace < 0:
                return False

    # =============================================
    # UNCLOSED
    # =============================================

    if brace != 0:
        return False

    if in_string:
        return False

    return True

# =========================================================
# COMMAND NORMALIZER
# =========================================================

def normalize_command(command):

    if command is None:
        return ""

    command = str(command)

    # 改行整理
    command = command.replace("\n", " ")
    command = command.replace("\r", " ")

    # 連続空白圧縮
    command = re.sub(
        r'\s+',
        ' ',
        command
    )

    return command.strip()

# =========================================================
# EXECUTION STACK GUARD
# =========================================================

SCRIPT_EXECUTION_DEPTH = 0
MAX_SCRIPT_DEPTH = 100

# =========================================================
# SAFE EXECUTE COMMAND
# =========================================================

def safe_execute_command(command):

    global SCRIPT_EXECUTION_DEPTH

    # =============================================
    # DEPTH LIMIT
    # =============================================

    if SCRIPT_EXECUTION_DEPTH >= MAX_SCRIPT_DEPTH:

        print(
            script_error(
                "EXECUTION_DEPTH_LIMIT",
                "Maximum execution depth exceeded.",
                "P01"
            )
        )

        return

    SCRIPT_EXECUTION_DEPTH += 1

    try:

        execute_command(command)

    except KeyboardInterrupt:
        raise

    except Exception as e:

        print(
            script_error(
                "COMMAND_EXECUTION_FAILED",
                str(e),
                "P02"
            )
        )

    finally:

        SCRIPT_EXECUTION_DEPTH -= 1

# =========================================================
# PATCHED SCRIPT EXECUTOR
# =========================================================

# =========================================================
# SCRIPT EXECUTOR
# =========================================================

def execute_script(script):

    commands = split_commands(script)

    for command in commands:

        command = command.strip()

        if command == "":
            continue

        execute_command(command)
# =========================================================
# DEBUG MEMORY VIEWER
# =========================================================

def debug_script_memory():

    print()

    print(
        f"{C.BRIGHT_CYAN}"
        "=========== SCRIPT MEMORY ==========="
        f"{C.RESET}"
    )

    print()

    # =============================================
    # VARIABLES
    # =============================================

    print(
        f"{C.BRIGHT_GREEN}[ VARIABLES ]{C.RESET}"
    )

    if SCRIPT_VARIABLES:

        for key, value in SCRIPT_VARIABLES.items():

            print(
                f"{C.WHITE}"
                f"{key}"
                f"{C.BRIGHT_BLACK} = "
                f"{C.BRIGHT_YELLOW}{value}"
                f"{C.RESET}"
            )

    else:

        print(
            f"{C.BRIGHT_BLACK}EMPTY{C.RESET}"
        )

    print()

    # =============================================
    # DISPLAYS
    # =============================================

    print(
        f"{C.BRIGHT_MAGENTA}[ DISPLAYS ]{C.RESET}"
    )

    if SCRIPT_DISPLAYS:

        for key, value in SCRIPT_DISPLAYS.items():

            state = "〇" if value == 1 else "✕"

            print(
                f"{C.WHITE}"
                f"{key}"
                f"{C.BRIGHT_BLACK} = "
                f"{state}"
                f"{C.RESET}"
            )

    else:

        print(
            f"{C.BRIGHT_BLACK}EMPTY{C.RESET}"
        )

    print()

    # =============================================
    # FUNCTIONS
    # =============================================

    print(
        f"{C.BRIGHT_CYAN}[ FUNCTIONS ]{C.RESET}"
    )

    if SCRIPT_FUNCTIONS:

        for key in SCRIPT_FUNCTIONS.keys():

            print(
                f"{C.BRIGHT_WHITE}"
                f"{key}()"
                f"{C.RESET}"
            )

    else:

        print(
            f"{C.BRIGHT_BLACK}EMPTY{C.RESET}"
        )

    print()

    # =============================================
    # TOUCH BINDS
    # =============================================

    print(
        f"{C.BRIGHT_YELLOW}[ TOUCH BINDS ]{C.RESET}"
    )

    for key, value in TOUCH_BINDINGS.items():

        state = "BOUND" if value else "EMPTY"

        print(
            f"{C.WHITE}"
            f"{key.upper()}"
            f"{C.BRIGHT_BLACK} : "
            f"{state}"
            f"{C.RESET}"
        )

    print()

    print(
        f"{C.BRIGHT_CYAN}"
        "====================================="
        f"{C.RESET}"
    )
    # =========================================================
# CIPHER-X SCRIPT ENGINE
# PART 6 / 6
# FINAL STABILITY & RECOVERY PATCH
# =========================================================

# =========================================================
# ENGINE STATUS
# =========================================================

ENGINE_STATE = {
    "boot_time": time.time(),
    "executed_commands": 0,
    "runtime_errors": 0,
    "last_error": None,
}

# =========================================================
# SAFE MEMORY VALIDATION
# =========================================================

def validate_engine_memory():

    global SCRIPT_VARIABLES
    global SCRIPT_DISPLAYS
    global SCRIPT_FUNCTIONS
    global TOUCH_BINDINGS

    repaired = False

    # =============================================
    # VARIABLES
    # =============================================

    if not isinstance(SCRIPT_VARIABLES, dict):

        SCRIPT_VARIABLES = {}
        repaired = True

    # =============================================
    # DISPLAYS
    # =============================================

    if not isinstance(SCRIPT_DISPLAYS, dict):

        SCRIPT_DISPLAYS = {}
        repaired = True

    # =============================================
    # FUNCTIONS
    # =============================================

    if not isinstance(SCRIPT_FUNCTIONS, dict):

        SCRIPT_FUNCTIONS = {}
        repaired = True

    # =============================================
    # TOUCH
    # =============================================

    if not isinstance(TOUCH_BINDINGS, dict):

        TOUCH_BINDINGS = {
            "w": None,
            "a": None,
            "s": None,
            "d": None,
        }

        repaired = True

    # =============================================
    # TOUCH KEY REPAIR
    # =============================================

    for key in ["w", "a", "s", "d"]:

        if key not in TOUCH_BINDINGS:

            TOUCH_BINDINGS[key] = None
            repaired = True

    return repaired

# =========================================================
# ENGINE DIAGNOSTIC
# =========================================================

def engine_diagnostic():

    print()

    print(
        f"{C.BRIGHT_CYAN}"
        "=========== ENGINE DIAGNOSTIC ==========="
        f"{C.RESET}"
    )

    print()

    repaired = validate_engine_memory()

    # =============================================
    # STATUS
    # =============================================

    status = "STABLE"

    if ENGINE_STATE["runtime_errors"] > 0:
        status = "WARNING"

    print(
        f"{C.BRIGHT_GREEN}STATUS{C.WHITE} : "
        f"{status}"
        f"{C.RESET}"
    )

    # =============================================
    # MEMORY
    # =============================================

    print(
        f"{C.BRIGHT_GREEN}VARIABLES{C.WHITE} : "
        f"{len(SCRIPT_VARIABLES)}"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_MAGENTA}DISPLAYS{C.WHITE} : "
        f"{len(SCRIPT_DISPLAYS)}"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_CYAN}FUNCTIONS{C.WHITE} : "
        f"{len(SCRIPT_FUNCTIONS)}"
        f"{C.RESET}"
    )

    # =============================================
    # EXECUTION
    # =============================================

    print(
        f"{C.BRIGHT_YELLOW}EXECUTED{C.WHITE} : "
        f"{ENGINE_STATE['executed_commands']}"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_RED}ERRORS{C.WHITE} : "
        f"{ENGINE_STATE['runtime_errors']}"
        f"{C.RESET}"
    )

    # =============================================
    # REPAIR
    # =============================================

    if repaired:

        print()

        print(
            f"{C.BRIGHT_YELLOW}"
            "[ MEMORY AUTO-REPAIRED ]"
            f"{C.RESET}"
        )

    print()

    print(
        f"{C.BRIGHT_CYAN}"
        "========================================="
        f"{C.RESET}"
    )

# =========================================================
# COMMAND EXECUTION TRACKER
# =========================================================

_ORIGINAL_EXECUTE_COMMAND = execute_command

# =========================================================
# EXECUTE COMMAND WRAPPER
# =========================================================

def execute_command(command):

    # =============================================
    # ENGINE STATE
    # =============================================

    ENGINE_STATE["executed_commands"] += 1

    # =============================================
    # NORMALIZE
    # =============================================

    if command is None:

        ENGINE_STATE["runtime_errors"] += 1

        print(
            script_error(
                "NULL_COMMAND",
                "Command does not exist.",
                "F00"
            )
        )
        return

    command = str(command).strip()

    # =============================================
    # EMPTY
    # =============================================

    if command == "":
        return

    # =============================================
    # INVALID GLOBAL ESCAPE
    # =============================================

    in_string = False

    for i in range(len(command)):

        char = command[i]

        # STRING TOGGLE
        if char == '"':

            in_string = not in_string

        # GLOBAL \ent
        if (
            not in_string and
            command[i:i+4] == r'\ent'
        ):

            ENGINE_STATE["runtime_errors"] += 1

            print(
                script_error(
                    "INVALID_ESCAPE_SEQUENCE",
                    r"\ent must be inside a string.",
                    "F01"
                )
            )
            return

    # =============================================
    # UNMATCHED QUOTES
    # =============================================

    if command.count('"') % 2 != 0:

        ENGINE_STATE["runtime_errors"] += 1

        print(
            script_error(
                "UNMATCHED_QUOTES",
                "String literal is not closed.",
                "F02"
            )
        )
        return

    # =============================================
    # BRACKET VALIDATION
    # =============================================

    if command.count("(") != command.count(")"):

        ENGINE_STATE["runtime_errors"] += 1

        print(
            script_error(
                "UNMATCHED_PARENTHESES",
                "Parentheses count mismatch.",
                "F03"
            )
        )
        return

    if command.count("{") != command.count("}"):

        ENGINE_STATE["runtime_errors"] += 1

        print(
            script_error(
                "UNMATCHED_BRACES",
                "Brace count mismatch.",
                "F04"
            )
        )
        return

    if command.count("[") != command.count("]"):

        ENGINE_STATE["runtime_errors"] += 1

        print(
            script_error(
                "UNMATCHED_BRACKETS",
                "Bracket count mismatch.",
                "F05"
            )
        )
        return

    # =============================================
    # COMMAND SIZE LIMIT
    # =============================================

    if len(command) > 10000:

        ENGINE_STATE["runtime_errors"] += 1

        print(
            script_error(
                "COMMAND_OVERFLOW",
                "Command length exceeded safe limit.",
                "F06"
            )
        )
        return

    # =============================================
    # EXECUTION
    # =============================================

    try:

        _ORIGINAL_EXECUTE_COMMAND(command)

    # =============================================
    # CTRL+C
    # =============================================

    except KeyboardInterrupt:

        raise

    # =============================================
    # RECURSION
    # =============================================

    except RecursionError:

        ENGINE_STATE["runtime_errors"] += 1

        ENGINE_STATE["last_error"] = "RecursionError"

        print(
            script_error(
                "STACK_OVERFLOW",
                "Maximum recursion depth exceeded.",
                "F07"
            )
        )

    # =============================================
    # MEMORY
    # =============================================

    except MemoryError:

        ENGINE_STATE["runtime_errors"] += 1

        ENGINE_STATE["last_error"] = "MemoryError"

        print(
            script_error(
                "MEMORY_OVERFLOW",
                "Engine memory allocation failed.",
                "F08"
            )
        )

    # =============================================
    # VALUE ERROR
    # =============================================

    except ValueError as e:

        ENGINE_STATE["runtime_errors"] += 1

        ENGINE_STATE["last_error"] = str(e)

        print(
            script_error(
                "INVALID_VALUE",
                str(e),
                "F09"
            )
        )

    # =============================================
    # TYPE ERROR
    # =============================================

    except TypeError as e:

        ENGINE_STATE["runtime_errors"] += 1

        ENGINE_STATE["last_error"] = str(e)

        print(
            script_error(
                "TYPE_MISMATCH",
                str(e),
                "F10"
            )
        )

    # =============================================
    # NAME ERROR
    # =============================================

    except NameError as e:

        ENGINE_STATE["runtime_errors"] += 1

        ENGINE_STATE["last_error"] = str(e)

        print(
            script_error(
                "UNKNOWN_IDENTIFIER",
                str(e),
                "F11"
            )
        )

    # =============================================
    # INDEX ERROR
    # =============================================

    except IndexError as e:

        ENGINE_STATE["runtime_errors"] += 1

        ENGINE_STATE["last_error"] = str(e)

        print(
            script_error(
                "INDEX_OUT_OF_RANGE",
                str(e),
                "F12"
            )
        )

    # =============================================
    # GENERIC
    # =============================================

    except Exception as e:

        ENGINE_STATE["runtime_errors"] += 1

        ENGINE_STATE["last_error"] = str(e)

        print(
            script_error(
                "ENGINE_COMMAND_FAILURE",
                str(e),
                "F99"
            )
        )
# =========================================================
# EMERGENCY MEMORY RESET
# =========================================================

def emergency_reset():

    global SCRIPT_VARIABLES
    global SCRIPT_DISPLAYS
    global SCRIPT_FUNCTIONS
    global TOUCH_BINDINGS

    SCRIPT_VARIABLES = {}
    SCRIPT_DISPLAYS = {}
    SCRIPT_FUNCTIONS = {}

    TOUCH_BINDINGS = {
        "w": None,
        "a": None,
        "s": None,
        "d": None,
    }

    print()

    print(
        f"{C.BRIGHT_RED}"
        "[ EMERGENCY MEMORY RESET COMPLETE ]"
        f"{C.RESET}"
    )

# =========================================================
# SAFE BOOT CHECK
# =========================================================

def engine_boot_check():

    validate_engine_memory()

    required_functions = [
        "execute_script",
        "execute_command",
        "script_menu",
        "script_console",
    ]

    missing = []

    for name in required_functions:

        if name not in globals():

            missing.append(name)

    if missing:

        print(
            script_error(
                "BOOT_CHECK_FAILED",
                f"Missing functions: {', '.join(missing)}",
                "F02"
            )
        )

        return False

    return True

# =========================================================
# SHUTDOWN HANDLER
# =========================================================

def graceful_shutdown():

    print()

    try:

        uptime = int(
            time.time() - ENGINE_STATE["boot_time"]
        )

    except Exception:

        uptime = 0

    print(
        f"{C.BRIGHT_BLACK}"
        f"UPTIME : {uptime}s"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        f"EXECUTED : "
        f"{ENGINE_STATE['executed_commands']}"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        f"ERRORS : "
        f"{ENGINE_STATE['runtime_errors']}"
        f"{C.RESET}"
    )

    print()

    print(
        f"{C.BRIGHT_RED}"
        "SYSTEM SHUTDOWN COMPLETE"
        f"{C.RESET}"
    )

# =========================================================
# PATCHED MAIN ENTRY
# =========================================================

if __name__ == "__main__":

    try:

        # =============================================
        # BOOT CHECK
        # =============================================

        if not engine_boot_check():

            input(
                f"{C.BRIGHT_RED}"
                f"\nBoot failed. Press Enter..."
                f"{C.RESET}"
            )

            sys.exit(1)

        # =============================================
        # START
        # =============================================

        main()

    except KeyboardInterrupt:

        print()

        print(
            f"{C.BRIGHT_YELLOW}"
            "INTERRUPT DETECTED"
            f"{C.RESET}"
        )

    except MemoryError:

        print(
            script_error(
                "MEMORY_OVERFLOW",
                "System ran out of memory.",
                "F03"
            )
        )

        emergency_reset()

    except Exception as e:

        ENGINE_STATE["runtime_errors"] += 1
        ENGINE_STATE["last_error"] = str(e)

        print()

        print(
            script_error(
                "RUNTIME_EXCEPTION",
                str(e),
                "99"
            )
        )

        # =============================================
        # TRACEBACK
        # =============================================

        try:

            print()

            print(
                f"{C.BRIGHT_BLACK}"
                "TRACEBACK:"
                f"{C.RESET}"
            )

            traceback.print_exc()

        except Exception:
            pass

    finally:

        # =============================================
        # DIAGNOSTIC
        # =============================================

        try:

            print()

            engine_diagnostic()

        except Exception:
            pass

        # =============================================
        # SHUTDOWN
        # =============================================

        try:

            graceful_shutdown()

        except Exception:
            pass

        # =============================================
        # EXIT WAIT
        # =============================================

        try:

            input(
                f"{C.BRIGHT_BLACK}"
                f"\nPress Enter to exit..."
                f"{C.RESET}"
            )

        except Exception:
            pass
