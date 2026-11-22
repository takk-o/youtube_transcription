# youtube_transcription

YouTube 動画の音声をダウンロードし、OpenAI の [Whisper](https://github.com/openai/whisper) で文字起こしして、タイムスタンプ付きのテキストファイルに保存するツール。

```
[00:00.000 --> 00:04.320] 皆さんこんにちは、今日は〇〇についてお話しします。
[00:04.320 --> 00:09.880] まず最初に…
```

## 特徴

- URL を渡すだけで、音声のダウンロードから文字起こしまでを自動で行う
- Whisper はローカルで動くため、音声を外部の API に送らない
- セグメントごとに開始・終了時刻を付けて出力する（`分:秒.ミリ秒`）
- ダウンロードした音声は一時フォルダに置き、終わったら自動で削除する

## 必要なもの

- [uv](https://docs.astral.sh/uv/)（Python とライブラリの管理）
- ffmpeg（Whisper が音声の読み込みに使う）：macOS は `brew install ffmpeg`
- deno（推奨。yt-dlp が YouTube から情報を取得するときに使う）：macOS は `brew install deno`

## セットアップ

```bash
git clone https://github.com/takk-o/youtube_transcription.git
cd youtube_transcription
uv sync
```

## 使い方

```bash
uv run youtube_transcription.py "https://www.youtube.com/watch?v=動画ID"
```

- URL を省略すると、実行後に入力を求められる。
- 結果は `text/<動画ID>.txt` に保存される（UTF-8）。

### オプション

| オプション | 既定値 | 説明 |
|---|---|---|
| `--model` | `medium` | Whisper のモデル。`tiny` / `base` / `small` / `medium` / `large` など。大きいほど精度が上がるが、時間とメモリを使う |
| `--language` | `ja` | 音声の言語 |

```bash
uv run youtube_transcription.py "https://youtu.be/動画ID" --model small
```

初回は Whisper のモデル（`medium` で約 1.5GB）がダウンロードされる。`tiny` は速いが日本語の精度が低いため、実際に使うときは `medium` 以上がおすすめ。

## 注意

- 動画のダウンロードと文字起こしは、YouTube の利用規約や著作権の範囲で、自分が利用してよい動画に対して行うこと。
- 文字起こしの精度は、音質やモデルの大きさで変わる。固有名詞などは誤認識することがある。

## 技術メモ

- 音声の取得：[yt-dlp](https://github.com/yt-dlp/yt-dlp)（`bestaudio` 形式）。YouTube 側の JavaScript による変換は、deno と yt-dlp-ejs（`yt-dlp[default]` に含まれる）で解く（[説明](https://github.com/yt-dlp/yt-dlp/wiki/EJS)）
- 文字起こし：openai-whisper の `transcribe()` が返すセグメント（`start` / `end` / `text`）を整形

## 経緯

2024 年 1 月に作成し、2026 年 11 月に公開用に整理した。動作確認環境：macOS（Apple シリコン）、Python 3.12。

## ライセンス

[MIT License](LICENSE)
