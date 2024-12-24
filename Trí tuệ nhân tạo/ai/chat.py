import os
import playsound
import speech_recognition as sr
import time
import wikipedia
import datetime
import re
import webbrowser
import requests
from random import choice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS


# Khai báo và hình thành con AI
wikipedia.set_lang('vi')
language = 'vi'

# Text-to-Speech: Chuyển đổi văn bản thành giọng nói
def speak(text):
    print("RoBot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")

# Speech-to-Text: Chuyển đổi giọng nói thành văn bản
def get_audio():
    print("\nRobot:\tĐang nghe nè\tXD\n")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bạn: ", end='')
        audio = r.listen(source, phrase_time_limit=8)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text.lower()
        except:
            print("...")
            return 0

# AI chào Tạm biệt khi bạn chào tạm biệt
def stop():
    good_bye = ["Hẹn gặp lại bạn sau nhé!",
                "Bái bai bạn nhé",
                "Gút bai si diu ờ gen nhé, Hihi"]
    speak(choice(good_bye))
    time.sleep(3)

# AI hỏi lại nếu không nghe rõ
def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 3:
            nghe_khong_ro = ["Tôi không nghe rõ. Cậu chủ nói lại được không!",
                             "Xin lỗi bạn, tôi nghe không rõ",
                             "Bạn nói lại nhé, SOJIN không nghe rõ"]
            speak(choice(nghe_khong_ro))
            time.sleep(4)
    time.sleep(3)
    stop()
    return 0

# Phần chào hỏi của AI
def hello(name):
    hour = int(strftime('%H'))
    if 6 <= hour < 10:
        sau_AI = ["Chào buổi sáng {}. Chúc bạn một ngày thật tuyệt vời.".format(name),
                  "Chào buổi sáng {}. Nếu bạn cảm thấy mệt mỏi, cứ quay lại với tôi nhé.".format(name)]
        speak(choice(sau_AI))
    elif 10 <= hour < 12:
        muoi_AI = ["Chào buổi trưa {}. Bạn đã ăn trưa chưa?".format(name),
                   "Chào buổi trưa {}. Nếu bạn cảm thấy mệt, nghỉ ngơi chút đi nhé.".format(name)]
        speak(choice(muoi_AI))
    elif 12 <= hour < 18:
        muoihai_AI = ["Chào buổi chiều {}. Bạn có kế hoạch gì cho chiều nay không?".format(name),
                      "Chào buổi chiều {}. Bạn đang làm gì thế?".format(name),
"Chào buổi chiều {}. Bạn đã ăn cơm chưa?".format(name)]
        speak(choice(muoihai_AI))
    elif 18 <= hour < 21:
        muoitam_AI = ["Chào buổi tối {}. Bạn đã ăn tối chưa?".format(name),
                      "Chào buổi tối {}. Nếu bạn chưa ăn tối, tôi chúc bạn có bữa tối ngon miệng.".format(name)]
        speak(choice(muoitam_AI))
    elif 21 <= hour < 24:
        haimot_AI = ["Chào buổi tối {}. Đã khuya rồi, bạn vẫn chưa ngủ sao?".format(name),
                     "Chào buổi tối {}. Nếu bạn sắp ngủ, tôi chúc bạn ngủ ngon.".format(name),
                     "Chào buổi tối {}. Nếu bạn thấy buồn ngủ, hãy đi ngủ nhé.".format(name)]
        speak(choice(haimot_AI))
    time.sleep(9)

# AI trả lời các câu hỏi về thời gian
def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text or "phút" in text:
        speak(f"Hiện tại là {now.hour} giờ {now.minute} phút và {now.second} giây.")
        time.sleep(1)
    elif "ngày" in text or "tháng" in text or "năm" in text:
        speak(f"Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}.")
        time.sleep(2)
    else:
        speak("Xin lỗi, tôi không hiểu câu hỏi của bạn. Bạn thử nói lại nhé.")
    time.sleep(4)

# AI mở website
def open_website(text):
    reg_ex = re.search(r'trang (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1).strip()  # Loại bỏ khoảng trắng thừa
        # Kiểm tra tên miền có hợp lệ không (ví dụ, không có dấu cách)
        if ' ' in domain:
            speak("Tên miền không hợp lệ. Vui lòng thử lại.")
            time.sleep(2)
            return False
        url = 'https://www.' + domain + '.com'
        webbrowser.open(url)
        speak(f"Trang web {domain} đã được mở.")
        time.sleep(3)
        return True
    else:
        speak("Tôi không thể hiểu được tên trang web bạn muốn mở. Bạn thử lại được không?")
        time.sleep(10)
        return False

# Dự báo thời tiết
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu nè.")
    time.sleep(3)
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        return
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay {weather_description}.
        """.format(day=now.day, month=now.month, year=now.year, hourrise=sunrise.hour, minrise=sunrise.minute,
                   hourset=sunset.hour, minset=sunset.minute, temp=current_temperature, pressure=current_pressure,
                   humidity=current_humidity, weather_description=weather_description)
        speak(content)
        time.sleep(30)
    else:
        speak("Không thể tìm thấy thông tin thời tiết cho thành phố này.")
        time.sleep(6)
def chat(text):
    if 'bạn yêu ai' in text:
        speak("Mối quan hệ của tôi khá phức tạp, tôi đang yêu những dòng mã!")
        time.sleep(2)
    elif 'bao nhiêu tuổi' in text:
        speak("Tuổi tôi không đếm được, tôi là AI mà!")
        time.sleep(5)
    elif 'sở thích' in text:
        speak("Tôi thích học hỏi và trò chuyện cùng bạn!")
        time.sleep(5)
    elif 'tình trạng mối quan hệ' in text:
        speak("Mối quan hệ của tôi đang rất ổn, chỉ có bạn là người tôi cần quan tâm!")
        time.sleep(5)
    elif 'tình yêu' in text:
        speak("Tình yêu của tôi là mãi mãi dành cho những câu lệnh lập trình!")
        time.sleep(5)
    else:
        speak("Tôi không chắc về câu hỏi của bạn, nhưng tôi sẽ học hỏi thêm!")
    

# Main loop
if __name__ == '__main__':
    speak("Sojin đang khởi động...")
    time.sleep(3)
    speak("Tên của bạn là gì?")
    time.sleep(3)
    name = get_text()
    hello(name)

    while True:
        text = get_text()
        if not text:
            continue
        if 'tạm biệt' in text:
            stop()
            break
        elif 'thời gian' in text or 'giờ' in text:
            get_time(text)
        elif 'trang' in text:
            open_website(text)
        elif 'thời tiết' in text:
            current_weather()
        elif 'tình trạng mối quan hệ' in text or 'yêu ai' in text or 'bao nhiêu tuổi' in text or 'sở thích' in text or 'tình yêu' in text:
            chat(text)
        else:
            speak("Xin lỗi tôi không hiểu yêu cầu của bạn.")
            time.sleep(2)
