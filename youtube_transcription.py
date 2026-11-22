"""YouTube 動画の音声を Whisper で文字起こしし、タイムスタンプ付きのテキストに保存する。"""

import argparse
import tempfile
from datetime import timedelta
from pathlib import Path

import whisper
from yt_dlp import YoutubeDL

OUTPUT_DIR = Path('text')


def format_time(sec: float) -> str:
    """経過秒数を「分:秒.ミリ秒」（例：03:07.250）の文字列にする。"""
    td = timedelta(seconds=sec)
    m, s = divmod(td.seconds + td.days * 86400, 60)
    ms = td.microseconds // 1000
    return f'{m:02}:{s:02}.{ms:03}'


def download_audio(url: str, work_dir: Path) -> tuple[Path, str]:
    """動画の音声（bestaudio）を work_dir にダウンロードし、ファイルのパスと動画 ID を返す。"""
    ydl_opts = {'outtmpl': str(work_dir / '%(id)s.%(ext)s'), 'format': 'bestaudio'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return Path(ydl.prepare_filename(info)), info['id']


def transcribe(audio_path: Path, model_name: str, language: str) -> str:
    """音声を文字起こしし、セグメントごとに「[開始 --> 終了] テキスト」の行にする。"""
    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_path), verbose=True, language=language)
    lines = [
        f"[{format_time(seg['start'])} --> {format_time(seg['end'])}] {seg['text']}"
        for seg in result['segments']
    ]
    return '\n'.join(lines) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description='YouTube 動画の音声を文字起こしする')
    parser.add_argument('url', nargs='?', help='YouTube の URL（省略すると入力を求める）')
    parser.add_argument('--model', default='medium',
                        help='Whisper のモデル（tiny / base / small / medium / large など。既定は medium）')
    parser.add_argument('--language', default='ja', help='音声の言語（既定は ja）')
    args = parser.parse_args()

    url = args.url or input('YouTube_URL:')

    # 音声は一時フォルダにダウンロードし、終わったら自動で削除する
    with tempfile.TemporaryDirectory() as tmp:
        audio_path, video_id = download_audio(url, Path(tmp))
        text = transcribe(audio_path, args.model, args.language)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f'{video_id}.txt'
    output_path.write_text(text, encoding='utf-8')
    print(f'文字起こしの結果を {output_path} に保存しました')


if __name__ == '__main__':
    main()
