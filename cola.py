import requests
import datetime

API_URL = "https://api.gvapi.cc/api/matches"
OUTPUT_FILE = "cola.m3u"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://giovang.co/"
}

response = requests.get(API_URL, headers=headers, timeout=10)
matches = response.json().get("data", {})

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for key, match in matches.items():
        home = match.get("homeTeamName")
        away = match.get("awayTeamName")
        home_logo = match.get("homeTeamLogo")
        away_logo = match.get("awayTeamLogo")
        match_time = match.get("matchTime")

        # giờ Việt Nam (UTC+7)
        dt = datetime.datetime.utcfromtimestamp(match_time) + datetime.timedelta(hours=7)
        date_str = dt.strftime("%Y-%m-%d %H:%M")

        title = f"{home} vs {away}"

        video_url = match.get("videoUrl") or match.get("video_url")
        blv_name = ""
        if not video_url and match.get("anchorAppointmentVoList"):
            anchor = match["anchorAppointmentVoList"][0]
            video_url = anchor.get("playStreamAddress2")
            blv_name = anchor.get("nickName", "")

        # chọn logo: ghép URL home + away nếu muốn, hoặc chỉ lấy home
        logo_url = home_logo or away_logo or ""

        if video_url:
            f.write(f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="Football",{date_str} | {title} | BLV {blv_name}\n')
            f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
            f.write("#EXTVLCOPT:http-referrer=https://giovang.co/\n")
            f.write(f"{video_url}\n")

print("🎉 Đã tạo file cola.m3u với logo từ API, giờ VN, tên trận và BLV.")
