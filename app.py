import time
import subprocess
from flask import Flask, redirect

app = Flask(__name__)

# --- إعدادات البث ---
# رابط قناة beIN الإخبارية
YOUTUBE_URL = "https://www.youtube.com/watch?v=2lJZPT6OljI"
# مدة التحديث: 3 ساعات (بالثواني: 3 * 60 * 60 = 10800)
CACHE_DURATION = 10800 

# --- متغيرات التخزين المؤقت (لخدمة 100 مستخدم بدون حظر) ---
cached_m3u8 = None
last_update_time = 0

def get_cached_stream():
    global cached_m3u8, last_update_time
    
    current_time = time.time()
    
    # الشرط: إذا كان الرابط فارغاً أو مر عليه أكثر من 3 ساعات
    if cached_m3u8 is None or (current_time - last_update_time > CACHE_DURATION):
        print("جاري تحديث الرابط من يوتيوب...")
        try:
            # استخدام yt-dlp لاستخراج الرابط المباشر
            # الأمر -g يجلب الرابط، و -f 96 يختار جودة متوسطة/جيدة لضمان الثبات (أو احذفه لأفضل جودة)
            command = ["yt-dlp", "-g", YOUTUBE_URL]
            
            # تنفيذ الأمر
            new_url = subprocess.check_output(command).decode('utf-8').strip()
            
            # التأكد من أن الرابط صالح
            if "http" in new_url:
                cached_m3u8 = new_url
                last_update_time = current_time
                print("تم تحديث الرابط بنجاح!")
            else:
                print("فشل الاستخراج، سنستخدم الرابط القديم إن وجد")
                
        except Exception as e:
            print(f"حدث خطأ أثناء التحديث: {e}")
            
    return cached_m3u8

@app.route('/')
def home():
    return "BEIN SERVER IS RUNNING (Use /bein to watch)"

@app.route('/bein')
def redirect_to_stream():
    stream_url = get_cached_stream()
    
    if stream_url:
        # توجيه المستخدم للرابط المباشر
        return redirect(stream_url, code=302)
    else:
        return "جاري تهيئة البث، حاول مرة أخرى بعد ثوانٍ...", 503

if __name__ == '__main__':
    # تشغيل السيرفر
    app.run(host='0.0.0.0', port=10000)

