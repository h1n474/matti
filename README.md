# matti

## `--set-raw-extention`
探す対象のRAWデータの拡張子を指定する。デフォルト設定では`.CR2`

## `--set-moved-dir`
マッチしたファイルの移動先。デフォルト設定は`../SELECT`

## サブコマンド
なにから参照するか、サブコマンドから選択する。
1. ra -- アドビのレーティングから
1. pb -- ペーストボードから
1. fi -- 指定ファイルから

## - rating command
### `args`
見つけたいrawファイルの入っているフォルダ
### `--input`
参照元のファイルを指定する。    


## - pb command
### `args`
見つけたいrawファイルの入っているフォルダ

## - file command
### `args`
見つけたいrawファイルの入っているフォルダ

## example
カレントディレクトリのJPGフォルダ内の`*.JPG` についているAdobeRatingを参照して  
RAWフォルダの`*.CR2` から同じ名前のファイルを抽出する。

```bash
matti ra RAW --input JPG
```
