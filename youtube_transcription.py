from pathlib import Path
from datetime import timedelta
from yt_dlp import YoutubeDL
import whisper

# 経過時間を分・秒・マイクロ秒の文字列に編集
def get_msls(sec):
    td = timedelta(seconds=sec)
    m, s = divmod(td.seconds, 60)
    ls = int(td.microseconds / 1000)
    return f'{m:02}:{s:02}.{ls:03}'

# 対象とするYouTubeのURLを入力(Copy & Paste)
url = input('YouTube_URL:')

# 'bestaudio'フォーマットで、'audio'フォルダにサウンドデータ'dl_sound.tmp'をダウンロード
ydl_opts = {'outtmpl': 'audio/dl_sound.tmp', 'format': 'bestaudio'}
with YoutubeDL(ydl_opts) as ydl:
    ydl.download(url)

# Whisperのモデルサイズを'medium'に設定
model = whisper.load_model('medium')

txt_audio = ''
# 言語を日本語、メッセージ表示をTrueに設定して、音声ファイルより文字起こし
tmp_audio = model.transcribe('audio/dl_sound.tmp', verbose=True, language='ja')

# セグメント毎に開始時間、終了時間、テキストをtxt_audioに出力（追記）
for segment in tmp_audio['segments']:
    st = get_msls(segment['start'])
    ed = get_msls(segment['end'])
    tx = segment['text']
    txt_audio += f"[{st} --> {ed}] {tx}\n"

# textフォルダーを作成
text_fd = Path('text')
text_fd.mkdir(exist_ok=True)

# txt_audioの内容を'text/dl_sound.txt'に出力
with open('text/dl_sound.txt', mode='w') as f:
    f.write(txt_audio)

# audioファイル・フォルダを削除
audio_fl = Path('./audio/dl_sound.tmp')
audio_fl.unlink()
audio_fd = Path('./audio')
audio_fd.rmdir()
