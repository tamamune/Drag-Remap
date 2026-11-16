"""KillerWhale DUO 用の vial.json を生成する(index.html の配置と同じ座標を使う)。
使い方: python tools/gen_vial_json.py  ->  firmware/vial-port/.../keymaps/vial/vial.json
"""
import json, os

U = 56.0           # 1U = 56px
P = 56
topsL = [123, 110, 68, 45, 58, 80]
topsR = [112, 110, 60, 52, 68, 80]
lc = [[(1, 0), (2, 1), (3, 2)],
      [(0, 5), (2, 0), (3, 1), (4, 2)],
      [(0, 4), (1, 5), (3, 0), (4, 1), (4, 5)],
      [(0, 3), (1, 4), (2, 5), (4, 0)],
      [(0, 2), (1, 3), (2, 4), (3, 5)],
      [(0, 1), (1, 2), (2, 3), (3, 4)]]
rc = [[(8, 0), (9, 1), (10, 2)],
      [(7, 5), (9, 0), (10, 1), (11, 2)],
      [(7, 4), (8, 5), (10, 0), (11, 1), (11, 5)],
      [(7, 3), (8, 4), (9, 5), (11, 0)],
      [(7, 2), (8, 3), (9, 4), (10, 5)],
      [(7, 1), (8, 2), (9, 3), (10, 4)]]

keys = []  # (cx, cy, w_px, h_px, legend)


def add(cx, cy, row, col, w=54):
    keys.append((cx, cy, w, 54, f"{row},{col}"))


for i, col in enumerate(lc):
    for j, (r, c) in enumerate(col):
        add(72 + 56 * i, topsL[i] + P * j, r, c)
for i, col in enumerate(rc):
    for j, (r, c) in enumerate(col):
        add(990 - 56 * i, topsR[i] + P * j, r, c)
for x, y, u, d, lf, rt, j in [(101, 421, 3, 1, 2, 4, 0), (968, 421, 11, 9, 10, 8, 7)]:
    add(x, y - 56, u, 6); add(x - 56, y, lf, 6); add(x, y, j, 6); add(x + 56, y, rt, 6); add(x, y + 56, d, 6)
add(296, 395, 6, 5); add(296, 449, 5, 6)        # 左 側面
add(775, 395, 13, 5); add(775, 449, 12, 6)      # 右 側面
add(437, 350, 5, 4); add(493, 350, 5, 3); add(464, 210, 4, 3, 82)   # 左 追加/トグル
add(577, 350, 12, 3); add(633, 350, 12, 4); add(604, 210, 11, 3, 82)  # 右 追加/トグル

# エンコーダ8個(左半分 e0-e3 / 右半分 e4-e7)。各ノブは 左回し/右回し の半円2つ
knobs = [(45, 50), (115, 40), (465, 282), (227, 405), (1020, 50), (950, 40), (605, 282), (843, 420)]
for e, (cx, cy) in enumerate(knobs):
    keys.append((cx - 15, cy, 30, 56, f"{e},0" + "\n" * 9 + "e"))
    keys.append((cx + 15, cy, 30, 56, f"{e},1" + "\n" * 9 + "e"))

# KLE: 1キー1行。行頭の x は 0 起点、y は「前行の y+1」からの差分で絶対座標へ
rows = []
cur_y = 0.0  # 次の行が始まる y
for cx, cy, w, h, legend in sorted(keys, key=lambda k: (k[1], k[0])):
    x = (cx - w / 2) / U
    y = (cy - h / 2) / U
    props = {}
    if abs(x) > 1e-6: props["x"] = round(x, 3)
    if abs(y - cur_y) > 1e-6: props["y"] = round(y - cur_y, 3)
    if abs(w - 54) > 1e-6: props["w"] = round(w / U, 3)
    if abs(h - 54) > 1e-6: props["h"] = round(h / U, 3)
    rows.append(([props] if props else []) + [legend])
    cur_y = y + 1

out = {
    "name": "KillerWhale DUO",
    "lighting": "none",
    "matrix": {"rows": 14, "cols": 7},
    "customKeycodes": [{"name": n, "title": n, "shortName": n} for n in (
        "CMD_CTL UNDO REDO COPY CUT PASTE SC_UP SC_DOWN SC_RESET CAPTCHA SAVE SAVEAS NEXTTAB PREVTAB CLOSETAB RSTRTAB "
        "L_SPD_I L_SPD_D R_SPD_I R_SPD_D L_ANG_I L_ANG_D L_INV L_CHMOD R_ANG_I R_ANG_D R_INV R_CHMOD INV_SCRL MOD_SCRL "
        "AUTO_MOUSE OLED_MOD MC_CAD MC_TASK").split()],
    "layouts": {"keymap": rows},
}
dst = os.path.join("firmware", "vial-port", "keyboards", "tarohayashi", "killerwhale", "duo", "keymaps", "vial")
os.makedirs(dst, exist_ok=True)
with open(os.path.join(dst, "vial.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("keys:", len(keys), "->", dst)
