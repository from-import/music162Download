import os
import requests
from pyncm.apis import track, cloudsearch
from pyncm import GetCurrentSession

def music_download(song_name):
    # 创建名为 "music" 的文件夹
    folder_name = "music"
    os.makedirs(folder_name, exist_ok=True)

    # 搜索歌曲
    search_result = cloudsearch.GetSearchResult(song_name, stype=1, limit=1)
    if not search_result['result']['songs']:
        print(f"未找到歌曲：{song_name}")
        return

    # 获取歌曲 ID 和名称
    song = search_result['result']['songs'][0]
    song_id = song['id']
    song_name = song['name']
    artist_name = song['ar'][0]['name'] if song['ar'] else 'unknown'

    # 获取歌曲下载链接
    session = GetCurrentSession()
    audio_info = track.GetTrackAudio([song_id], bitrate=320000)
    if not audio_info['data'] or not audio_info['data'][0]['url']:
        print(f"无法获取歌曲下载链接：{song_name}")
        return

    # 下载歌曲
    mp3_url = audio_info['data'][0]['url']
    response = requests.get(mp3_url)
    if response.status_code == 200:
        # 构建文件路径，替换文件名中的非法字符
        valid_song_name = "".join(c for c in song_name if c.isalnum() or c in [' ', '-', '_'])
        valid_artist_name = "".join(c for c in artist_name if c.isalnum() or c in [' ', '-', '_'])
        file_path = os.path.join(folder_name, f"{valid_song_name} - {valid_artist_name}.mp3")
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"歌曲下载完成，保存为文件：{file_path}")
    else:
        print(f"歌曲下载失败：{song_name}")



# 示例调用
music_download("春日影 CRYCHIC")
