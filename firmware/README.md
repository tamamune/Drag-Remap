# KillerWhale DUO を Vial 化する(ファーム側)

目的: コンボ・タップダンスを **再ビルドなしで** 実機から編集できるようにする。

> ⚠ このフォルダの内容は **ビルド未確認** です(作成環境に ARM ツールチェーンがなかったため)。
> 必ず、いまの VIA 版ファームを残したまま試してください(UF2 でいつでも書き戻せます)。

## 構成
`firmware/vial-port/keyboards/tarohayashi/killerwhale/duo/` に、vial-qmk へ上書きコピーするファイルが入っています。

| ファイル | 内容 |
|---|---|
| `keyboard.json` `config.h` `rules.mk` `lib/` など | あなたの fork(`tarohayashi` ブランチ)の duo をそのままコピー |
| `keymaps/vial/keymap.c` | `keymaps/test/keymap.c` から自動生成。静的な `tap_dance_actions[]` とコンボ定義を削除、`MC_CAD`/`MC_TASK` を `QK_KB_32/33` に移動 |
| `keymaps/vial/rules.mk` | `VIA_ENABLE` `VIAL_ENABLE` ほか |
| `keymaps/vial/config.h` | `VIAL_KEYBOARD_UID`、ロック解除キー(左 ESC + 右 BSPC)、動的エントリ数 |
| `keymaps/vial/vial.json` | Vial 画面の配置(`tools/gen_vial_json.py` で生成)。エンコーダ8個、独自キーコード34個を含む |

作り直すとき:
```bash
python tools/make_vial_port.py <fork の qmk_firmware のパス>
python tools/gen_vial_json.py
```

## 手順(あなたの手元で)
1. QMK のビルド環境を用意する(QMK MSYS など)
2. vial-qmk を取得する
   ```bash
   git clone --recurse-submodules -b vial https://github.com/vial-kb/vial-qmk.git
   ```
3. `firmware/vial-port/keyboards/` を vial-qmk の `keyboards/` に上書きコピーする
4. ビルドする
   ```bash
   cd vial-qmk
   qmk compile -kb tarohayashi/killerwhale/duo -km vial
   ```
5. 左右とも UF2 で書き込む(BOOTSEL)。分割キーボードなので **左右同じファーム** を書くこと
6. [Vial](https://get.vial.today/) を開き、キーボードを選ぶ。編集前に「Unlock」(左 ESC と右 BSPC を押しながら)
7. タップダンス(13個)とコンボ(`J+K`=Enter、`D+F`=Space)を Vial の画面で再設定する

## 知っておくこと・リスク
- **土台の QMK が古い**: vial-qmk は 2025年5月相当、あなたの fork は 2025年11月相当です。`lib/` が呼ぶ QMK の関数は vial-qmk に全部あることを確認しましたが、ビルド自体は未確認です。コンパイルエラーが出たら、エラー文を送ってください。
- **タップダンス/コンボは再設定が必要**: 静的な定義は Vial の動的エントリに置き換わるため、キーボード上は最初空です。
- **Vial を使うと、標準 VIA 版とは別のファーム**です。Remap(公式ツール)では開けなくなります。
- **SOLO は未対応**(DUO のみ)。
- `MC_CAD` / `MC_TASK` のコードが `0x7E40` 系から `QK_KB_32/33`(`0x7E20/21`)に変わります。
- **ロック解除キー**を変えたい場合は `keymaps/vial/config.h` の `VIAL_UNLOCK_COMBO_*` を編集します。
