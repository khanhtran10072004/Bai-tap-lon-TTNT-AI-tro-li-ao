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
        elif i < 2:
            nghe_khong_ro = ["Tôi không nghe rõ. Cậu chủ nói lại được không!",
                             "Xin lỗi bạn, tôi nghe không rõ",
                             "Bạn nói lại nhé, Sojin không nghe rõ"]
            speak(choice(nghe_khong_ro))
            time.sleep(4)
    stop()
    return 0

# Phần chào hỏi của AI
def hello(name):
    hour = int(datetime.datetime.now().hour)
    if 6 <= hour < 10:
        speak(f"Chào buổi sáng {name}. Chúc bạn một ngày thật tuyệt vời.")
    elif 10 <= hour < 12:
        speak(f"Chào buổi trưa {name}. Bạn đã ăn trưa chưa?")
    elif 12 <= hour < 18:
        speak(f"Chào buổi chiều {name}. Bạn có kế hoạch gì chiều nay không?")
    elif 18 <= hour < 21:
        speak(f"Chào buổi tối {name}. Bạn đã ăn tối chưa?")
    else:
        speak(f"Chào buổi tối {name}. Đã khuya rồi, bạn vẫn chưa ngủ sao?")
    time.sleep(2)

# AI trả lời các câu hỏi về thời gian
def get_time():
    now = datetime.datetime.now()
    speak(f"Hiện tại là {now.hour} giờ {now.minute} phút và {now.second} giây.")
    time.sleep(5)

# AI mở website
def open_website(text):
    reg_ex = re.search(r'trang (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1).strip()
        if ' ' in domain:
            speak("Tên miền không hợp lệ. Vui lòng thử lại.")
        else:
            url = 'https://' + domain
            webbrowser.open(url)
            speak(f"Trang web {domain} đã được mở.")
    else:
        speak("Tôi không thể hiểu tên trang web bạn muốn mở.")
    time.sleep(5)

# Dự báo thời tiết
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu?")
    city = get_text()
    if not city:
        return
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        weather_description = data["weather"][0]["description"]
        speak(f"Nhiệt độ là {city_res['temp']} độ C. Trời hôm nay {weather_description}.")
    else:
        speak("Không tìm thấy thông tin thời tiết.")

# Main loop
if __name__ == '__main__':
    speak("Sojin đang khởi động...")
    time.sleep(5)
    speak("Tên của bạn là gì?")
    name = get_text()
    hello(name)

    while True:
        text = get_text()
        if not text:
            continue
        if 'tạm biệt' in text:
            stop()
            break
        elif 'thời gian' in text:
            get_time()
        elif 'trang' in text:
            open_website(text)
        elif 'thời tiết' in text:
            current_weather()
        else:
            speak("Xin lỗi tôi không hiểu yêu cầu của bạn.")