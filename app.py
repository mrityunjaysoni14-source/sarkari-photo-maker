import io, base64
from datetime import date
from flask import Flask, render_template_string, request, jsonify
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

HTML = r'''<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sarkari Exam Photo & Signature Maker — Free Name/Date Stamp + KB Compressor</title>
<meta name="description" content="Free online Sarkari Exam Passport Photo and Signature maker with name & date stamp, aspect ratio crop, and KB file size compressor for SSC, UPSC, Railway, Bank, IBPS exams. No signup required.">
<meta name="keywords" content="sarkari exam photo maker, passport photo online, signature compressor, SSC photo size, UPSC photo maker, bank exam photo, KB compressor, photo stamp">
<meta name="author" content="Sarkari Photo Tool">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#2563eb">
<link rel="canonical" href="/">
<meta property="og:title" content="Sarkari Exam Photo & Signature Maker">
<meta property="og:description" content="Free passport photo maker with name/date stamp and KB compressor for all government exams.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📸</text></svg>">

<!-- Tailwind CSS (Bina defer ke) -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Critical CSS inlined for FCP -->
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:linear-gradient(135deg,#eff6ff,#e0e7ff);min-height:100vh}
.loader{width:2.5rem;height:2.5rem;border:4px solid #93c5fd;border-top-color:#2563eb;border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.tab-on{background:#2563eb;color:#fff;box-shadow:0 2px 8px rgba(37,99,235,.3)}
.tab-off{background:#e5e7eb;color:#374151}
.kb-on{background:#2563eb;color:#fff}.kb-off{background:#f3f4f6;color:#374151}
.ratio-on{background:#2563eb;color:#fff}.ratio-off{background:#f3f4f6;color:#374151}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
</style>

<!-- Structured Data for SEO -->
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"Sarkari Exam Photo & Signature Maker","description":"Free online passport photo and signature maker with name/date stamp and KB compressor for SSC, UPSC, Railway, Bank exams.","applicationCategory":"UtilityApplication","operatingSystem":"All","offers":{"@type":"Offer","price":"0","priceCurrency":"INR"},"browserRequirements":"Requires JavaScript"}
</script>
</head>


<body>
<!-- Skip Navigation for Accessibility -->
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:bg-blue-600 focus:text-white focus:px-4 focus:py-2 focus:rounded-lg focus:z-50">Skip to main content</a>

<header class="bg-white/90 backdrop-blur shadow-sm sticky top-0 z-10" role="banner">
<div class="max-w-2xl mx-auto px-4 py-3 flex items-center gap-3">
<span class="text-3xl" role="img" aria-label="Camera">📸</span>
<div>
<h1 class="text-lg md:text-xl font-bold text-blue-700 leading-tight">Sarkari Exam Photo & Signature Maker</h1>
<p class="text-xs text-gray-500">Free Name/Date Stamp + KB Compressor — SSC, UPSC, Railway, Bank</p>
</div>
</div>
</header>

<main id="main-content" class="max-w-2xl mx-auto px-4 py-5" role="main">

<!-- Tab Navigation -->
<nav aria-label="Tool selection" class="flex gap-2 mb-5">
<button id="tab0" onclick="setTab(0)" class="flex-1 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 tab-on" role="tab" aria-selected="true" aria-controls="panel-photo">🪪 Passport Photo</button>
<button id="tab1" onclick="setTab(1)" class="flex-1 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 tab-off" role="tab" aria-selected="false" aria-controls="panel-sig">✍️ Signature</button>
</nav>

<form id="frm" class="bg-white rounded-2xl shadow-lg p-5 md:p-6 space-y-5" onsubmit="return false" aria-label="Image processing form">

<!-- Upload -->
<div>
<label for="fileIn" class="block text-sm font-semibold mb-1.5 text-gray-700" id="upLabel">Upload Photo</label>
<input type="file" accept="image/jpeg,image/png,image/webp" id="fileIn" required
  class="block w-full text-sm file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-blue-600 file:text-white file:font-semibold file:cursor-pointer hover:file:bg-blue-700 transition"
  aria-describedby="fileHelp">
<p id="fileHelp" class="text-xs text-gray-400 mt-1">JPG, PNG or WebP — max 10MB recommended</p>
</div>

<!-- Photo Options Panel -->
<fieldset id="photoOpts" class="space-y-4 border-0 p-0 m-0">
<legend class="sr-only">Photo stamp and crop options</legend>

<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
<div>
<label for="cname" class="text-xs font-semibold text-gray-600 block mb-1">Candidate Name</label>
<input id="cname" placeholder="e.g. Rahul Kumar" autocomplete="name"
  class="border border-gray-300 rounded-xl px-3 py-2.5 text-sm w-full focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none transition">
</div>
<div>
<label for="dop" class="text-xs font-semibold text-gray-600 block mb-1">Date of Photo (DOP)</label>
<div class="flex gap-1">
<input id="dop" type="date" class="border border-gray-300 rounded-xl px-3 py-2.5 text-sm flex-1 focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none transition">
<button type="button" onclick="document.getElementById('dop').value='{{today}}';go()" class="bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-xl px-3 text-xs font-bold whitespace-nowrap transition border border-blue-200" aria-label="Fill today's date">📅 Today</button>
</div>
</div>
</div>

<label class="flex items-center gap-2.5 text-sm cursor-pointer select-none group">
<input type="checkbox" id="showStrip" checked class="w-4 h-4 rounded text-blue-600 focus:ring-2 focus:ring-blue-400" aria-describedby="stripDesc">
<span>Show Name & Date strip on photo</span>
</label>
<p id="stripDesc" class="sr-only">Adds a white bar at the bottom of the photo with candidate name and date</p>

<div role="group" aria-labelledby="ratioLabel">
<span id="ratioLabel" class="text-xs font-semibold text-gray-600">Aspect Ratio</span>
<div class="flex flex-wrap gap-2 mt-1.5">
<button type="button" onclick="setRatio('3.5x4.5',this)" class="ratio-btn ratio-on px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm" aria-pressed="true">3.5×4.5 (SSC/Passport)</button>
<button type="button" onclick="setRatio('2x2.5',this)" class="ratio-btn ratio-off px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm" aria-pressed="false">2×2.5 (IBPS/Bank)</button>
<button type="button" onclick="setRatio('1x1',this)" class="ratio-btn ratio-off px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm" aria-pressed="false">Square</button>
<button type="button" onclick="setRatio('orig',this)" class="ratio-btn ratio-off px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm" aria-pressed="false">Original</button>
</div>
</div>
</fieldset>

<!-- KB Target -->
<div role="group" aria-labelledby="kbLabel">
<span id="kbLabel" class="text-xs font-semibold text-gray-600">Target File Size (KB)</span>
<div class="flex flex-wrap gap-2 mt-1.5 items-center">
<button type="button" onclick="setKB(10,this)" class="kb-btn kb-off px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm">10 KB</button>
<button type="button" onclick="setKB(20,this)" class="kb-btn kb-off px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm">20 KB</button>
<button type="button" onclick="setKB(50,this)" class="kb-btn kb-on px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm">50 KB</button>
<button type="button" onclick="setKB(100,this)" class="kb-btn kb-off px-3 py-1.5 rounded-xl text-xs font-semibold transition shadow-sm">100 KB</button>
<label for="customKB" class="sr-only">Custom target size in KB</label>
<input id="customKB" type="number" min="5" max="2000" placeholder="Custom KB"
  class="border border-gray-300 rounded-xl px-3 py-1.5 text-sm w-24 focus:ring-2 focus:ring-blue-400 outline-none transition"
  oninput="targetKB=+this.value||50;document.querySelectorAll('.kb-btn').forEach(b=>{b.classList.remove('kb-on');b.classList.add('kb-off')});go()">
</div>
</div>

<!-- Preview Area -->
<div class="text-center space-y-3" aria-live="polite">
<div id="placeholder" class="border-2 border-dashed border-gray-300 rounded-xl p-10 text-gray-400">
<p class="text-4xl mb-2">🖼️</p>
<p class="text-sm">Upload an image to see preview</p>
</div>
<div id="spinner" class="hidden py-6"><div class="loader mx-auto"></div><p class="text-sm text-gray-500 mt-2">Processing image...</p></div>
<img id="preview" alt="Processed photo preview" class="mx-auto rounded-xl border shadow-md max-w-full hidden" style="max-height:420px">
<div id="info" class="text-sm text-gray-600 font-medium" role="status"></div>
<div id="sizeBar" class="hidden mx-auto max-w-xs">
<div class="bg-gray-200 rounded-full h-2.5 overflow-hidden"><div id="sizeProgress" class="h-full rounded-full transition-all duration-500" style="width:0"></div></div>
<p id="sizeLabel" class="text-xs text-gray-500 mt-1"></p>
</div>
</div>

<!-- Download -->
<button type="button" onclick="dl()" id="dlBtn"
  class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold py-3.5 rounded-xl text-sm shadow-lg transition-all duration-200 hidden focus:ring-4 focus:ring-green-300"
  aria-label="Download processed image as JPG">
  ⬇️ Download JPG
</button>
</form>

<!-- Instructions / FAQ for SEO -->
<section class="mt-8 bg-white rounded-2xl shadow p-5 md:p-6" aria-labelledby="howto">
<h2 id="howto" class="text-base font-bold text-gray-800 mb-3">📋 How to Use — Step by Step</h2>
<ol class="text-sm text-gray-600 space-y-2 list-decimal list-inside">
<li><strong>Choose tab</strong> — Passport Photo (with name/date stamp) or Signature compressor.</li>
<li><strong>Upload image</strong> — JPG, PNG or WebP format.</li>
<li><strong>Set details</strong> — Enter candidate name, date, choose aspect ratio (3.5×4.5 for SSC/Passport, 2×2.5 for IBPS/Bank).</li>
<li><strong>Set target KB</strong> — Select 10, 20, 50, 100 KB or enter custom size.</li>
<li><strong>Download</strong> — Click the green button to save your perfectly sized photo!</li>
</ol>
</section>

<section class="mt-4 bg-white rounded-2xl shadow p-5 md:p-6" aria-labelledby="faq">
<h2 id="faq" class="text-base font-bold text-gray-800 mb-3">❓ Frequently Asked Questions</h2>
<details class="mb-2"><summary class="text-sm font-semibold text-gray-700 cursor-pointer">SSC exam ke liye photo size kya honi chahiye?</summary><p class="text-sm text-gray-600 mt-1 ml-4">SSC exams ke liye 3.5×4.5 cm aspect ratio mein 10-20 KB JPEG photo chahiye hoti hai.</p></details>
<details class="mb-2"><summary class="text-sm font-semibold text-gray-700 cursor-pointer">Kya signature bhi compress ho sakti hai?</summary><p class="text-sm text-gray-600 mt-1 ml-4">Haan! Signature tab use karke aap signature ko exact KB size mein compress kar sakte hain.</p></details>
<details class="mb-2"><summary class="text-sm font-semibold text-gray-700 cursor-pointer">Kya ye tool free hai?</summary><p class="text-sm text-gray-600 mt-1 ml-4">Bilkul free hai! Koi signup ya payment nahi chahiye.</p></details>
<details><summary class="text-sm font-semibold text-gray-700 cursor-pointer">Photo quality kharab to nahi hogi?</summary><p class="text-sm text-gray-600 mt-1 ml-4">Humara smart compression system sabse best quality maintain karta hai aapke target KB ke andar.</p></details>
</section>
</main>

<footer class="text-center text-xs text-gray-400 py-6" role="contentinfo">
<p>© 2026 Sarkari Exam Photo Tool — Free for SSC, UPSC, Railway, Bank & all government exam candidates.</p>
</footer>

<script>
let tab=0,targetKB=50,ratio='3.5x4.5',lastB64='',fileData=null;
const $=id=>document.getElementById(id);

function setTab(t){
  tab=t;
  ['tab0','tab1'].forEach((id,i)=>{
    const el=$(id);
    el.className='flex-1 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 '+(i===t?'tab-on':'tab-off');
    el.setAttribute('aria-selected',i===t);
  });
  $('photoOpts').classList.toggle('hidden',t===1);
  $('upLabel').textContent=t===0?'Upload Photo':'Upload Signature';
  go();
}

function setKB(kb,btn){
  targetKB=kb;$('customKB').value='';
  document.querySelectorAll('.kb-btn').forEach(b=>{b.classList.remove('kb-on');b.classList.add('kb-off');b.setAttribute('aria-pressed','false')});
  btn.classList.remove('kb-off');btn.classList.add('kb-on');btn.setAttribute('aria-pressed','true');
  go();
}

function setRatio(r,btn){
  ratio=r;
  document.querySelectorAll('.ratio-btn').forEach(b=>{b.classList.remove('ratio-on');b.classList.add('ratio-off');b.setAttribute('aria-pressed','false')});
  btn.classList.remove('ratio-off');btn.classList.add('ratio-on');btn.setAttribute('aria-pressed','true');
  go();
}

$('fileIn').onchange=e=>{
  const f=e.target.files[0];if(!f)return;
  if(f.size>10*1024*1024){alert('File too large! Please use an image under 10MB.');return}
  const r=new FileReader();
  r.onload=ev=>{fileData=ev.target.result;$('placeholder').classList.add('hidden');go()};
  r.readAsDataURL(f);
};
$('cname').oninput=debounce(go,400);
$('dop').oninput=()=>go();
$('showStrip').onchange=()=>go();

function debounce(fn,ms){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),ms)}}

let pending=0;
async function go(){
  if(!fileData)return;
  pending++;const my=pending;
  $('spinner').classList.remove('hidden');
  $('preview').classList.add('hidden');$('dlBtn').classList.add('hidden');
  $('info').textContent='';$('sizeBar').classList.add('hidden');

  const body={image:fileData,tab,ratio,target_kb:targetKB,name:$('cname').value,dop:$('dop').value,strip:$('showStrip').checked};
  try{
    const res=await fetch('/process',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(my!==pending)return;
    if(!res.ok)throw new Error('Server error '+res.status);
    const j=await res.json();
    lastB64='data:image/jpeg;base64,'+j.b64;
    $('preview').src=lastB64;$('preview').classList.remove('hidden');
    $('info').innerHTML=`<span class="inline-block bg-gray-100 rounded-lg px-3 py-1">${j.w}×${j.h}px</span> <span class="inline-block bg-blue-50 text-blue-700 rounded-lg px-3 py-1 font-bold">${j.kb} KB</span> <span class="text-gray-400">target ≤${targetKB} KB • Quality ${j.q}%</span>`;

    // Size progress bar
    const pct=Math.min(100,Math.round(j.kb/targetKB*100));
    $('sizeBar').classList.remove('hidden');
    $('sizeProgress').style.width=pct+'%';
    $('sizeProgress').className='h-full rounded-full transition-all duration-500 '+(pct>90?'bg-orange-400':pct>70?'bg-yellow-400':'bg-green-400');
    $('sizeLabel').textContent=pct+'% of target used';

    $('dlBtn').classList.remove('hidden');
  }catch(e){$('info').textContent='❌ Error: '+e.message}
  finally{if(my===pending)$('spinner').classList.add('hidden')}
}

function dl(){
  if(!lastB64)return;
  const a=document.createElement('a');a.href=lastB64;
  a.download=(tab===0?'photo':'signature')+'_'+targetKB+'kb.jpg';
  a.click();
}
</script>
</body>
</html>'''


RATIO_MAP = {
    '3.5x4.5': (3.5, 4.5),
    '2x2.5': (2, 2.5),
    '1x1': (1, 1),
}


@app.route('/')
def index():
    return render_template_string(HTML, today=date.today().isoformat())


@app.route('/process', methods=['POST'])
def process():
    try:
        d = request.json
        header, b64data = d['image'].split(',', 1)
        img = Image.open(io.BytesIO(base64.b64decode(b64data))).convert('RGB')

        # Crop to aspect ratio
        if d['tab'] == 0 and d['ratio'] in RATIO_MAP:
            rw, rh = RATIO_MAP[d['ratio']]
            target_r = rw / rh
            iw, ih = img.size
            if iw / ih > target_r:
                new_w = int(ih * target_r)
                img = img.crop(((iw - new_w) // 2, 0, (iw + new_w) // 2, ih))
            else:
                new_h = int(iw / target_r)
                img = img.crop((0, (ih - new_h) // 2, iw, (ih + new_h) // 2))

        # Name/Date strip
        if d['tab'] == 0 and d.get('strip'):
            iw, ih = img.size
            strip_h = max(28, int(ih * 0.08))
            new_img = Image.new('RGB', (iw, ih + strip_h), (255, 255, 255))
            new_img.paste(img, (0, 0))
            draw = ImageDraw.Draw(new_img)
            parts = []
            if d.get('name', '').strip():
                parts.append(d['name'].strip().upper())
            if d.get('dop', '').strip():
                parts.append('DOP: ' + d['dop'].strip())
            text = '  |  '.join(parts)
            if text:
                fs = max(14, strip_h * 45 // 100)
                try:
                    font = ImageFont.truetype("arialbd.ttf", fs)
                except Exception:
                    try:
                        font = ImageFont.truetype("arial.ttf", fs)
                    except Exception:
                        try:
                            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fs)
                        except Exception:
                            font = ImageFont.load_default()
                bbox = draw.textbbox((0, 0), text, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(((iw - tw) // 2, ih + (strip_h - th) // 2), text, fill=(0, 0, 0), font=font)
            img = new_img

        # Binary search JPEG compression
        target_bytes = max(1024, d.get('target_kb', 50) * 1024)
        lo, hi, best_buf, best_q = 3, 97, None, 50

        for _ in range(16):
            if lo > hi:
                break
            mid = (lo + hi) // 2
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=mid, optimize=True, subsampling=2)
            if buf.tell() <= target_bytes:
                best_buf, best_q = buf, mid
                lo = mid + 1
            else:
                hi = mid - 1

        # If still too big at lowest quality, resize down
        if best_buf is None:
            for scale in [0.75, 0.5, 0.35, 0.25, 0.15]:
                resized = img.resize((max(10, int(img.width * scale)), max(10, int(img.height * scale))), Image.LANCZOS)
                buf = io.BytesIO()
                resized.save(buf, format='JPEG', quality=5, optimize=True, subsampling=2)
                if buf.tell() <= target_bytes:
                    best_buf, best_q, img = buf, 5, resized
                    break
            if best_buf is None:
                buf = io.BytesIO()
                tiny = img.resize((max(10, img.width // 6), max(10, img.height // 6)), Image.LANCZOS)
                tiny.save(buf, format='JPEG', quality=3, optimize=True)
                best_buf, best_q, img = buf, 3, tiny

        b64out = base64.b64encode(best_buf.getvalue()).decode()
        kb = round(best_buf.tell() / 1024, 1)
        return jsonify(b64=b64out, w=img.width, h=img.height, kb=kb, q=best_q)

    except Exception as e:
        return jsonify(error=str(e)), 400


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
