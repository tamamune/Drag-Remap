// Vial 設定
#pragma once

#define VIAL_KEYBOARD_UID {0x4B, 0x57, 0x44, 0x55, 0x4F, 0x21, 0xA6, 0x03}

// ロック解除コンボ: 左手 ESC(行1,列0) と 右手 BSPC(行8,列0) を押しながら Vial で「Unlock」
#define VIAL_UNLOCK_COMBO_ROWS { 1, 8 }
#define VIAL_UNLOCK_COMBO_COLS { 0, 0 }

// 動的エントリ数(必要に応じて増やせます)
#define VIAL_TAP_DANCE_ENTRIES 16
#define VIAL_COMBO_ENTRIES 16
#define VIAL_KEY_OVERRIDE_ENTRIES 8
