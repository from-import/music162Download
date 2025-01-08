import requests
import json
import time
import random
import os

def get_playlist_details(playlist_id):
    """
    根据歌单 ID 获取歌单详细信息。

    :param playlist_id: 歌单 ID
    :return: 歌单详细信息，包括歌曲列表。
    """
    url = f"https://music.163.com/api/playlist/detail?id={playlist_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = data.get("result", {})
            tracks = result.get("tracks", [])

            # 构建歌曲列表
            song_list = [
                {
                    "id": track.get("id"),
                    "src": f"https://music.163.com/song/media/outer/url?id={track.get('id')}.mp3",
                    "name": track.get("name"),
                    "singer": track.get("artists", [{}])[0].get("name", ""),
                    "time": track.get("duration")
                }
                for track in tracks
            ]

            return {
                "coverImgUrl": result.get("coverImgUrl", "").replace("http:", ""),
                "tracks": song_list,
                "name": result.get("name"),
                "createTime": result.get("createTime"),
                "description": result.get("description")
            }
        else:
            print(f"HTTP 错误: {response.status_code}")
    except requests.RequestException as e:
        print(f"请求异常: {e}")

    return {}

def get_lyric(song_id):
    """
    根据歌曲 ID 获取歌词。

    :param song_id: 歌曲 ID
    :return: 歌词文本
    """
    url = f"https://music.163.com/api/song/media?id={song_id}"
    headers = {
        "Referer": "https://music.163.com",
        "Cookie": "appver=1.5.2",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": random_user_agent()
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("lyric", "")
    except requests.RequestException as e:
        print(f"请求异常: {e}")

    return ""

def random_user_agent():
    """
    生成随机的 User-Agent。

    :return: 随机 User-Agent 字符串
    """
    user_agent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1"
    ]
    return random.choice(user_agent_list)

def save_json(filepath, data):
    """
    保存数据到 JSON 文件。

    :param filepath: 文件路径
    :param data: 要保存的数据
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    playlist_id = "2161739123"  # 替换为目标歌单 ID

    # 获取歌单详情
    playlist_data = get_playlist_details(playlist_id)

    if playlist_data:
        print("成功获取歌单信息")
        save_json("musicList.json", playlist_data)

        # 获取歌词列表
        lyrics = {}
        for index, track in enumerate(playlist_data["tracks"]):
            song_id = track["id"]
            try:
                lyric = get_lyric(song_id)
                lyrics[song_id] = lyric
                print(f"成功获取第 {index + 1} 首歌曲的歌词")
                time.sleep(random.uniform(0.3, 0.6))  # 防止请求过快
            except Exception as e:
                print(f"获取歌词失败: {e}")

        # 保存歌词到 JSON 文件
        save_json("musicLyric.json", lyrics)
        print("歌词已保存到 musicLyric.json")
    else:
        print("未能获取歌单信息")

if __name__ == "__main__":
    main()
