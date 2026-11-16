# Drag Remap

Keyball61 / KillerWhale 向けの、ドラッグでキーを移動できるキーマップ編集ツールです。
`index.html` を Chrome / Edge で開くだけで動きます(VIA プロトコル + WebHID)。

## 機能
- キー同士のドラッグで入れ替え / コピー / 移動(Shift でコピー)
- キーコードのパレットからキーへドラッグ、レイヤータブへドラッグでレイヤー切替
- 実機の読込・書込(VIA)、元に戻す/やり直す、レイヤー/全クリア
- JSON の保存・読込、`keymap.c`(`keymaps[]` / `encoder_map[]`)の書出・読込
- VIA 定義 JSON の読込で任意のキーボードに対応

## 使い方
1. プリセット(Keyball61 / KillerWhale DUO)を選び「接続」
2. 「キーボードから読込」→ 編集(橙枠 = 未書込)→「キーボードへ書込」

## 注意
- ファームが `VIA_ENABLE = yes` でビルドされている必要があります
- コンボは VIA で扱えないため編集できません
- KillerWhale のキー配置・エンコーダ番号の対応は推定です。実機で確認してください

## tools/
- `keymap2json.py`: `tools/keymap.c` を読み込み用 JSON(`keymap-test.json`)に変換
