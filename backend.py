from flask import Flask, send_file, jsonify, render_template_string
import os
import sys

app = Flask(__name__)

# Port ayarı - Render için önemli
port = int(os.environ.get('PORT', 5000))

# Not metni - TEMİZ VE DÜZENLİ
ROJDA_NOTU = """Seyhan’ım…

Bu siteyi sana özel yaptım. Belki kusurları vardır, belki eksik kalmıştır… ama içindeki her şeyde sen varsın. Çünkü daha ilk günden, nasıl oldu anlamadım ama kalbime dokundun.

Sanki hayatıma gönderilmiş en güzel hediye gibisin. Öyle dış görünüş, fizik falan… inan hiçbiri umrumda değil. Benim tek istediğim bir şey var: o da sensin. Sadece sen…

İstiyorum ki herkes gibi olmayalım. Geçici değil, gerçek olalım. Herkes gelip geçerken, biz kalalım. İnsanlar çorap değiştirir gibi sevgili değiştirirken, biz birbirimize ait olalım… sağlam, gerçek, tertemiz bir şekilde.

Ben bu yolda seninle yürümek istiyorum. Ne olursa olsun, ne yaşarsak yaşayalım, elini bırakmadan… sonuna kadar.

Peki sen… benimle birlikte bu yolda yürümeye var mısın, ömrüm? 🤍"""

# İlk sayfa HTML'i - GERÇEKÇİ MEKTUP KUTUSU (RENDER UYUMLU)
INDEX_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seyhan'ıma Özel</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            width: 100%;
            text-align: center;
        }

        /* BAŞLIK */
        .baslik {
            margin-bottom: 40px;
            font-size: 2rem;
            color: #d44e8c;
            font-weight: 500;
            letter-spacing: 2px;
            text-shadow: 0 0 5px rgba(212, 78, 140, 0.2);
        }

        /* GERÇEKÇİ MEKTUP KUTUSU */
        .mektup-kutusu {
            cursor: pointer;
            position: relative;
            width: 500px;
            height: 350px;
            margin: 0 auto 40px;
            perspective: 1500px;
            transition: transform 0.3s;
        }

        .mektup-kutusu:hover {
            transform: translateY(-5px);
        }

        /* Zarf */
        .zarf {
            position: relative;
            width: 100%;
            height: 100%;
            background: #f9f1e0;
            border-radius: 15px 15px 8px 8px;
            box-shadow: 0 20px 30px -10px rgba(0,0,0,0.2);
            border: 2px solid #e6d5b8;
        }

        /* Zarfın Alt Kısmı (sabit) */
        .zarf-alt {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #f9f1e0;
            border-radius: 15px 15px 8px 8px;
            z-index: 1;
        }

        /* Zarf Deseni */
        .zarf-alt::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: repeating-linear-gradient(45deg, rgba(210, 180, 140, 0.1) 0px, rgba(210, 180, 140, 0.1) 2px, transparent 2px, transparent 8px);
            border-radius: 15px 15px 8px 8px;
            pointer-events: none;
        }

        /* Zarf Kapağı (Üçgen) */
        .zarf-kapak {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #f9f1e0;
            clip-path: polygon(0% 0%, 50% 40%, 100% 0%);
            transform-origin: top;
            transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            border-bottom: 2px solid #d4b68a;
            z-index: 4;
            border-radius: 15px 15px 0 0;
        }

        .zarf-kapak::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(255,255,240,0.8) 0%, rgba(230,215,180,0.2) 100%);
            clip-path: polygon(0% 0%, 50% 40%, 100% 0%);
        }

        /* Mektup Kağıdı */
        .mektup-ici {
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            bottom: 20px;
            background: #fff9f0;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(0);
            transition: transform 0.8s ease-out;
            z-index: 2;
            border: 1px solid #e6d5b8;
            overflow-y: auto;
            font-family: 'Georgia', serif;
            line-height: 1.8;
            color: #2c3e50;
            font-size: 1.1rem;
            text-align: left;
            opacity: 0;
            pointer-events: none;
        }

        /* Mektup Açılınca */
        .mektup-kutusu.acik .zarf-kapak {
            transform: rotateX(180deg);
            z-index: 1;
        }

        .mektup-kutusu.acik .mektup-ici {
            transform: translateY(-60px);
            opacity: 1;
            pointer-events: all;
            box-shadow: 0 20px 30px -5px rgba(0,0,0,0.3);
            z-index: 3;
        }

        /* Mühür */
        .muhur {
            position: absolute;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            background: #c0a080;
            border-radius: 50%;
            border: 3px solid #8b6b4d;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 5;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 30px;
            color: #ff6b6b;
            transition: all 0.3s;
        }

        /* Butonlar */
        .butonlar {
            margin-top: 80px;
            display: flex;
            gap: 30px;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.5s;
        }

        .butonlar.goster {
            opacity: 1;
        }

        .evet-btn, .hayir-btn {
            padding: 15px 50px;
            font-size: 1.5rem;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
            letter-spacing: 1px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .evet-btn {
            background: #4CAF50;
            color: white;
            border-bottom: 4px solid #2e7d32;
        }

        .evet-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(76, 175, 80, 0.4);
        }

        .hayir-btn {
            background: #f44336;
            color: white;
            border-bottom: 4px solid #b71c1c;
        }

        .hayir-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(244, 67, 54, 0.4);
        }

        /* Not İçeriği */
        .not-icerik {
            white-space: pre-line;
            font-size: 1.1rem;
            line-height: 1.8;
            height: 100%;
            overflow-y: auto;
            font-family: 'Georgia', serif;
            color: #2c3e50;
        }

        .not-icerik::-webkit-scrollbar {
            width: 6px;
        }

        .not-icerik::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        .not-icerik::-webkit-scrollbar-thumb {
            background: #d44e8c;
            border-radius: 10px;
        }

        /* Responsive */
        @media (max-width: 600px) {
            .mektup-kutusu {
                width: 320px;
                height: 240px;
            }
            
            .baslik {
                font-size: 1.5rem;
            }
            
            .evet-btn, .hayir-btn {
                padding: 12px 30px;
                font-size: 1.2rem;
            }
            
            .muhur {
                width: 40px;
                height: 40px;
                font-size: 20px;
                bottom: 15px;
                right: 15px;
            }
            
            .mektup-ici {
                padding: 15px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="baslik">💌 Sana Özel Bir Mektup Var 💌</h1>
        
        <div class="mektup-kutusu" id="mektupKutusu" onclick="mektupAc()">
            <div class="zarf">
                <div class="zarf-alt"></div>
                <div class="zarf-kapak"></div>
                
                <!-- Mektup içeriği -->
                <div class="mektup-ici" id="mektupIci">
                    <div class="not-icerik" id="notIcerik"></div>
                </div>
                
                <!-- Mühür -->
                <div class="muhur">❤️</div>
            </div>
        </div>
        
        <div class="butonlar" id="butonlar">
            <button class="evet-btn" onclick="evetClick()">Evet ❤️</button>
            <button class="hayir-btn" onclick="hayirClick()">Hayır 💔</button>
        </div>
    </div>

    <script>
        let mektupAcildi = false;

        function mektupAc() {
            if (!mektupAcildi) {
                document.getElementById('mektupKutusu').classList.add('acik');
                
                // Backend'den notu al
                fetch('/get-not')
                    .then(response => response.json())
                    .then(data => {
                        const notMetni = data.not || '';
                        document.getElementById('notIcerik').innerHTML = notMetni.replace(/\\n/g, '<br>');
                        
                        setTimeout(() => {
                            document.getElementById('butonlar').classList.add('goster');
                        }, 800);
                    })
                    .catch(() => {
                        document.getElementById('notIcerik').innerText = 'Not yüklenemedi.';
                        document.getElementById('butonlar').classList.add('goster');
                    });
                
                mektupAcildi = true;
            }
        }

        function evetClick() {
            window.location.href = '/evet';
        }

        function hayirClick() {
            if (confirm('Emin misin? Bir daha düşün istersen 💕')) {
                alert('Üzgünüm... Belki başka zaman? 😔');
            }
        }
    </script>
</body>
</html>"""

# İkinci sayfa HTML'i
EVET_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seni Seviyorum SeyhanımN ❤️</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .container {
            text-align: center;
            color: white;
            animation: fadeIn 2s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        .gif-container {
            margin: 30px auto;
            max-width: 500px;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        .gif-container img {
            width: 100%;
            height: auto;
            display: block;
        }

        .mesaj {
            font-size: 3rem;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            animation: kalpAtisi 1.5s ease-in-out infinite;
        }

        @keyframes kalpAtisi {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .alt-mesaj {
            font-size: 1.5rem;
            opacity: 0.9;
            margin-top: 20px;
            font-style: italic;
        }

        .kalpler {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }

        .kalp {
            position: absolute;
            color: rgba(255, 255, 255, 0.5);
            font-size: 20px;
            animation: yukari 10s linear infinite;
        }

        @keyframes yukari {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) rotate(720deg);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="kalpler" id="kalpler"></div>
    <div class="container">
        <div class="mesaj">
            SENİ SEVİYORUM HATUNUM 🤍
        </div>
        <div class="gif-container">
            <img src="/manita.gif" alt="Manita GIF" onerror="this.src='https://media.giphy.com/media/3o7abB06u9bNzA8LC8/giphy.gif'">
        </div>
        <div class="alt-mesaj">
            Sonsuza kadar benimle olur musun? 💕
        </div>
    </div>

    <script>
        function kalpOlustur() {
            const kalpler = document.getElementById('kalpler');
            const kalp = document.createElement('div');
            kalp.classList.add('kalp');
            kalp.innerHTML = '❤️';
            kalp.style.left = Math.random() * 100 + '%';
            kalp.style.animationDuration = (Math.random() * 5 + 5) + 's';
            kalp.style.fontSize = (Math.random() * 20 + 10) + 'px';
            kalpler.appendChild(kalp);

            setTimeout(() => {
                kalp.remove();
            }, 10000);
        }

        setInterval(kalpOlustur, 500);
    </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/evet')
def evet():
    return render_template_string(EVET_HTML)

@app.route('/get-not')
def get_not():
    return jsonify({'not': ROJDA_NOTU})

@app.route('/manita.gif')
def manita_gif():
    try:
        return send_file('manita.gif', mimetype='image/gif')
    except:
        # GIF bulunamazsa yedek GIF gönder
        return '', 404

# Render.com için health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

# Render.com için ana çalıştırma
if __name__ == '__main__':
    print(f"🚀 Site başlatılıyor... Port: {port}")
    print(f"📍 Adres: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
