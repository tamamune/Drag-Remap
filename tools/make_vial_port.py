"""KillerWhale DUO を vial-qmk へ移植するための一式を firmware/vial-port/ に作る。

使い方:
  python tools/make_vial_port.py <qmk_firmware(tarohayashi)のパス>
  python tools/gen_vial_json.py
できたフォルダ firmware/vial-port/keyboards を vial-qmk の keyboards に上書きコピーして、
  qmk compile -kb tarohayashi/killerwhale/duo -km vial
"""
import os, re, shutil, sys

fork = sys.argv[1]
src = os.path.join(fork, "keyboards", "tarohayashi", "killerwhale", "duo")
dst = os.path.join("firmware", "vial-port", "keyboards", "tarohayashi", "killerwhale", "duo")
if os.path.isdir(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("keymaps", ".vscode"))

# ---- keymap.c (test) から Vial 用 keymap.c を作る ----
km = open(os.path.join(src, "keymaps", "test", "keymap.c"), encoding="utf-8").read()

# タップダンス定義(tap_dance_actions[])は Vial の動的エントリに置き換わるので削除
km = re.sub(r"tap_dance_action_t tap_dance_actions\[\] = \{.*?\n\};\n", "", km, flags=re.S)
# コンボ定義(静的)も Vial の動的コンボに置き換わるので削除
km = re.sub(r"// 3\. コンボの設定.*?combo_t key_combos\[\] = \{.*?\n\};\n", "", km, flags=re.S)
# 独自キーコードは Vial の customKeycodes に載せるため QK_KB_32 以降に置く
km = km.replace("MC_CAD = SAFE_RANGE, // Ctrl + Alt + Del 用", "MC_CAD = QK_KB_32,   // Ctrl + Alt + Del 用 (vial.json の customKeycodes 33番目)")
km = km.replace("MC_TASK              // タスクマネージャーを直接起動", "MC_TASK = QK_KB_33   // タスクマネージャーを直接起動 (同 34番目)")
header = (
    "// Vial 用 keymap(test キーマップから自動生成)\n"
    "// - タップダンス TD(n) とコンボは Vial の画面で設定します(静的定義は削除済み)\n"
    "// - TD_* の enum は TD(n) の番号の目印として残しています\n"
)
os.makedirs(os.path.join(dst, "keymaps", "vial"), exist_ok=True)
open(os.path.join(dst, "keymaps", "vial", "keymap.c"), "w", encoding="utf-8", newline="\n").write(header + km)

open(os.path.join(dst, "keymaps", "vial", "rules.mk"), "w", encoding="utf-8", newline="\n").write(
    "VIA_ENABLE = yes\nVIAL_ENABLE = yes\n"
    "ENCODER_MAP_ENABLE = yes\n"
    "COMBO_ENABLE = yes\n"
    "TAP_DANCE_ENABLE = yes\n"
    "POINTING_DEVICE_AUTO_MOUSE_ENABLE = yes\n"
    "# ビルドが容量不足になった場合のみ有効化\n"
    "# LTO_ENABLE = yes\n"
)

# VIAL_KEYBOARD_UID はキーボード固有の8バイト。下は生成した値(変更しないこと。変えるとVial側の保存データと紐づかなくなる)
uid = [0x4B, 0x57, 0x44, 0x55, 0x4F, 0x21, 0xA6, 0x03]
open(os.path.join(dst, "keymaps", "vial", "config.h"), "w", encoding="utf-8", newline="\n").write(
    "// Vial 設定\n#pragma once\n\n"
    "#define VIAL_KEYBOARD_UID {" + ", ".join("0x%02X" % b for b in uid) + "}\n\n"
    "// ロック解除コンボ: 左手 ESC(行1,列0) と 右手 BSPC(行8,列0) を押しながら Vial で「Unlock」\n"
    "#define VIAL_UNLOCK_COMBO_ROWS { 1, 8 }\n"
    "#define VIAL_UNLOCK_COMBO_COLS { 0, 0 }\n\n"
    "// 動的エントリ数(必要に応じて増やせます)\n"
    "#define VIAL_TAP_DANCE_ENTRIES 16\n"
    "#define VIAL_COMBO_ENTRIES 16\n"
    "#define VIAL_KEY_OVERRIDE_ENTRIES 8\n"
)
print("done ->", dst)
