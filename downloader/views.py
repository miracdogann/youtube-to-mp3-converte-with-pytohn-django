from django.shortcuts import render
from pytube import YouTube
import os

def download_view(request):
    context = {}

    if request.method == 'POST':
        url = request.POST.get('url')
        print("url", url)

        # URL boş ise kullanıcıya uyarı göster
        if not url or url.strip() == '':
            context['error_message'] = 'URL boş bırakılamaz.'
        else:
            try:
                youtube_obj = YouTube(url)
                video = youtube_obj.streams.filter(only_audio=True).first()

                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                temp_file = video.download(output_path=desktop_path)
                new_file = os.path.join(desktop_path, f"{youtube_obj.title}.mp3")
                
                # Geçici dosyayı .mp3 olarak yeniden adlandırma
                if not os.path.exists(new_file):
                    os.rename(temp_file, new_file)
                    context['success_message'] = f"{youtube_obj.title} başarıyla indirildi mp3 formatında."
                else:
                    context['error_message'] = f"{youtube_obj.title}.mp3 zaten mevcut, tekrar indirilmedi."

            except Exception as e:
                context['error_message'] = 'URL geçersiz veya tam bir url girmelisiniz.'
                print(f"Hata: {str(e)}")

    return render(request, 'home.html', context)
