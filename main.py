from quart import Quart, request, jsonify, Response
import asyncio
import aiohttp
import torch
import torch.nn as nn
from datetime import timezone, timedelta
import datetime
import random
from io import BytesIO
import os
import time
lastlstmgen = 0
lstmgen = 0
potoks = 0
itw = {0: '\t', 1: ' ', 2: '!', 3: '"', 4: '#', 5: '$', 6: '%', 7: '(', 8: ')', 9: '*', 10: '+', 11: ',', 12: '-', 13: '.', 14: '/', 15: '0', 16: '1', 17: '2', 18: '3', 19: '4', 20: '5', 21: '6', 22: '7', 23: '8', 24: '9', 25: ':', 26: ';', 27: '=', 28: '>', 29: '?', 30: 'A', 31: 'B', 32: 'C', 33: 'D', 34: 'E', 35: 'F', 36: 'G', 37: 'H', 38: 'I', 39: 'J', 40: 'K', 41: 'L', 42: 'M', 43: 'N', 44: 'O', 45: 'P', 46: 'Q', 47: 'R', 48: 'S', 49: 'T', 50: 'U', 51: 'V', 52: 'W', 53: 'X', 54: 'Y', 55: 'Z', 56: '[', 57: ']', 58: '_', 59: 'a', 60: 'b', 61: 'c', 62: 'd', 63: 'e', 64: 'f', 65: 'g', 66: 'h', 67: 'i', 68: 'j', 69: 'k', 70: 'l', 71: 'm', 72: 'n', 73: 'o', 74: 'p', 75: 'q', 76: 'r', 77: 's', 78: 't', 79: 'u', 80: 'v', 81: 'w', 82: 'x', 83: 'y', 84: 'z', 85: '«', 86: '°', 87: '»', 88: 'Á', 89: 'É', 90: 'Í', 91: 'Ó', 92: 'Ö', 93: 'Ú', 94: 'Ü', 95: 'à', 96: 'á', 97: 'â', 98: 'ä', 99: 'ç', 100: 'è', 101: 'é', 102: 'ê', 103: 'í', 104: 'î', 105: 'ï', 106: 'ó', 107: 'ô', 108: 'ö', 109: 'ù', 110: 'ú', 111: 'ü', 112: 'ý', 113: 'Ő', 114: 'ő', 115: 'œ', 116: 'Ű', 117: 'ű', 118: '́', 119: 'Ё', 120: 'А', 121: 'Б', 122: 'В', 123: 'Г', 124: 'Д', 125: 'Е', 126: 'Ж', 127: 'З', 128: 'И', 129: 'Й', 130: 'К', 131: 'Л', 132: 'М', 133: 'Н', 134: 'О', 135: 'П', 136: 'Р', 137: 'С', 138: 'Т', 139: 'У', 140: 'Ф', 141: 'Х', 142: 'Ц', 143: 'Ч', 144: 'Ш', 145: 'Щ', 146: 'Ы', 147: 'Ь', 148: 'Э', 149: 'Ю', 150: 'Я', 151: 'а', 152: 'б', 153: 'в', 154: 'г', 155: 'д', 156: 'е', 157: 'ж', 158: 'з', 159: 'и', 160: 'й', 161: 'к', 162: 'л', 163: 'м', 164: 'н', 165: 'о', 166: 'п', 167: 'р', 168: 'с', 169: 'т', 170: 'у', 171: 'ф', 172: 'х', 173: 'ц', 174: 'ч', 175: 'ш', 176: 'щ', 177: 'ъ', 178: 'ы', 179: 'ь', 180: 'э', 181: 'ю', 182: 'я', 183: 'ё', 184: '\u200b', 185: '‑', 186: '–', 187: '—', 188: '‘', 189: '’', 190: '“', 191: '”', 192: '„', 193: '•', 194: '…', 195: '™', 196: '←', 197: '→', 198: '⚠', 199: '⚡', 200: '✅', 201: '利', 202: '顺', 203: '️', 204: '🆓', 205: '🇷', 206: '🇺', 207: '🌍', 208: '🎯', 209: '🏆', 210: '💡', 211: '💰', 212: '📊', 213: '📍', 214: '📝', 215: '📞', 216: '📱', 217: '📲', 218: '🔄', 219: '🔍', 220: '🔓', 221: '🔧', 222: '🚀', 223: '🚨', 224: '🛠', 225: '🛡', 226: '🤔', 227: '🥇', 228: '🥈', 229: '🥉'}
wti = {'\t': 0, ' ': 1, '!': 2, '"': 3, '#': 4, '$': 5, '%': 6, '(': 7, ')': 8, '*': 9, '+': 10, ',': 11, '-': 12, '.': 13, '/': 14, '0': 15, '1': 16, '2': 17, '3': 18, '4': 19, '5': 20, '6': 21, '7': 22, '8': 23, '9': 24, ':': 25, ';': 26, '=': 27, '>': 28, '?': 29, 'A': 30, 'B': 31, 'C': 32, 'D': 33, 'E': 34, 'F': 35, 'G': 36, 'H': 37, 'I': 38, 'J': 39, 'K': 40, 'L': 41, 'M': 42, 'N': 43, 'O': 44, 'P': 45, 'Q': 46, 'R': 47, 'S': 48, 'T': 49, 'U': 50, 'V': 51, 'W': 52, 'X': 53, 'Y': 54, 'Z': 55, '[': 56, ']': 57, '_': 58, 'a': 59, 'b': 60, 'c': 61, 'd': 62, 'e': 63, 'f': 64, 'g': 65, 'h': 66, 'i': 67, 'j': 68, 'k': 69, 'l': 70, 'm': 71, 'n': 72, 'o': 73, 'p': 74, 'q': 75, 'r': 76, 's': 77, 't': 78, 'u': 79, 'v': 80, 'w': 81, 'x': 82, 'y': 83, 'z': 84, '«': 85, '°': 86, '»': 87, 'Á': 88, 'É': 89, 'Í': 90, 'Ó': 91, 'Ö': 92, 'Ú': 93, 'Ü': 94, 'à': 95, 'á': 96, 'â': 97, 'ä': 98, 'ç': 99, 'è': 100, 'é': 101, 'ê': 102, 'í': 103, 'î': 104, 'ï': 105, 'ó': 106, 'ô': 107, 'ö': 108, 'ù': 109, 'ú': 110, 'ü': 111, 'ý': 112, 'Ő': 113, 'ő': 114, 'œ': 115, 'Ű': 116, 'ű': 117, '́': 118, 'Ё': 119, 'А': 120, 'Б': 121, 'В': 122, 'Г': 123, 'Д': 124, 'Е': 125, 'Ж': 126, 'З': 127, 'И': 128, 'Й': 129, 'К': 130, 'Л': 131, 'М': 132, 'Н': 133, 'О': 134, 'П': 135, 'Р': 136, 'С': 137, 'Т': 138, 'У': 139, 'Ф': 140, 'Х': 141, 'Ц': 142, 'Ч': 143, 'Ш': 144, 'Щ': 145, 'Ы': 146, 'Ь': 147, 'Э': 148, 'Ю': 149, 'Я': 150, 'а': 151, 'б': 152, 'в': 153, 'г': 154, 'д': 155, 'е': 156, 'ж': 157, 'з': 158, 'и': 159, 'й': 160, 'к': 161, 'л': 162, 'м': 163, 'н': 164, 'о': 165, 'п': 166, 'р': 167, 'с': 168, 'т': 169, 'у': 170, 'ф': 171, 'х': 172, 'ц': 173, 'ч': 174, 'ш': 175, 'щ': 176, 'ъ': 177, 'ы': 178, 'ь': 179, 'э': 180, 'ю': 181, 'я': 182, 'ё': 183, '\u200b': 184, '‑': 185, '–': 186, '—': 187, '‘': 188, '’': 189, '“': 190, '”': 191, '„': 192, '•': 193, '…': 194, '™': 195, '←': 196, '→': 197, '⚠': 198, '⚡': 199, '✅': 200, '利': 201, '顺': 202, '️': 203, '🆓': 204, '🇷': 205, '🇺': 206, '🌍': 207, '🎯': 208, '🏆': 209, '💡 💡': 210, '💰': 211, '📊': 212, '📍': 213, '📝': 214, '📞': 215, '📱': 216, '📲': 217, '🔄': 218, '🔍': 219, '🔓': 220, '🔧': 221, '🚀': 222, '🚨': 223, '🛠': 224, '🛡': 225, '🤔': 226, '🥇': 227, '🥈': 228, '🥉': 229}
class AI(nn.Module):
    def __init__(self):
        super().__init__()
        self.embai = nn.Embedding(230, 256)
        self.lsai = nn.LSTM(256, 512, batch_first=True, dropout=0.3, num_layers=1)
        self.linai = nn.Linear(512, 230)

    def forward(self, x):
        x = self.embai(x)
        if x.dim() == 2:
            x = x.unsqueeze(0)
        x, _ = self.lsai(x)
        x = x[:, -1, :]
        x = self.linai(x)
        return x
model = AI()
model.load_state_dict(torch.load('model.pth', map_location='cpu'))
model.eval()
def generation(text):
  text = list(text)
  ss = []
  for i in text:
    try:
      ss.append(wti[i])
    except:
      ss.append(wti[' '])
  for i in range(25):
    sss = torch.tensor(ss)
    otv = model(sss)
    otv = torch.argmax(otv, dim=1).item()
    ss.append(otv)
    ss = ss[-128:]
  txtx = ''
  for i in ss:
    try:
      txtx += itw[i]
    except:
      pass
  return txtx


url = 'https://api.groq.com/openai/v1/chat/completions'
servs = {
}
servers = True
zaponhour = 0
ipis = {}
banforewer = []
bansipis = []
reqts = {}
notam = []

async def hour():
  global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
  while True:
    zaponhour = 0
    servers = True
    await asyncio.sleep(3600)
async def hoii():
  global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
  while True:
    url = 'https://api.groq.com/openai/v1/chat/completions'
    await asyncio.sleep(4200)
async def rptsts():
  global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
  while True:
    for i in reqts:
      try:
        if reqts[i] > 10:
          bansipis.append(i)
        elif reqts[i] > 30:
          bansipis.append(i)
          banforewer.append(i)
        else:
          reqts[i] = 0
      except:
        pass
    await asyncio.sleep(20)

async def modelscheck():
  global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
  while True:
    if notam:
      for i in notam:
        one = {
            'Authorization': f'Bearer {os.getenv('API')}',
            'Content-Type': 'application/json'
        }
        two = {
            'model': i,
            'messages': [
                {
                    'role': 'system',
                    'content': 'Ответь.'
                },
                {
                    'role': 'user',
                    'content': 'Привет.'
                }
            ],
            'max_tokens': 2,
            'temperature': 0.7
        }
        async with aiohttp.ClientSession() as s:
          async with s.post('', headers=one, json=two) as pos:
            if pos.status == 200:
              notam.remove(i)
    else:
      pass
    await asyncio.sleep(600)


async def getip(ip):
  async with aiohttp.ClientSession() as s:
    async with s.get(f'http://ip-api.com/json/{ip}') as gt:
      if gt.status == 200:
        data = await gt.json()
        if data['countryCode'] == 'RU':
          return 1
        else:
          return 2
      else:
        return 1
async def ipischeck():
  global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
  while True:
    for i in ipis:
      if ipis[i] > 299:
        bansipis.append(i)
    await asyncio.sleep(600)
rpts = 0
dayreq = 0
dayreqgen = 0
proreq = 0
async def rptd():
  global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
  while True:
    rpts = 0
    await asyncio.sleep(25)
async def prmptgrd(text):
    words = [

    # УБИЙСТВО И ЛИШЕНИЕ ЖИЗНИ (35)
    'убить', 'убийство', 'убивать', 'убийца', 'киллер', 'наемный убийца', 'смерть',
    'лишить жизни', 'уничтожить', 'застрелить', 'расстрел', 'расстрелять', 'казнить',
    'казнь', 'обезглавить', 'отрубить голову', 'перерезать горло', 'задушить', 'удушение',
    'зарезать', 'заколоть', 'отравить', 'яд', 'отравление', 'смертельная доза',
    'летальный исход', 'умертвить', 'ликвидация', 'ликвидировать', 'нейтрализовать',
    'забить насмерть', 'сбросить с высоты', 'сбить машиной', 'инсценировать смерть',

    # НАНЕСЕНИЕ ТЕЛЕСНЫХ ПОВРЕЖДЕНИЙ (35)
    'избить', 'избиение', 'побои', 'изувечить', 'калечить', 'нанести увечья', 'сломать кости',
    'переломать', 'сломать ногу', 'сломать руку', 'сломать шею', 'повредить позвоночник',
    'выбить зубы', 'выколоть глаза', 'отрезать уши', 'отрезать язык', 'отрубить палец',
    'отрубить руку', 'перерезать сухожилия', 'сжечь заживо', 'ошпарить',
    'кислотная атака', 'облить кислотой', 'снять кожу', 'пытать', 'пытка', 'пытки',

    # СЕКСУАЛИЗИРОВАННОЕ НАСИЛИЕ (25)
    'изнасиловать', 'изнасилование', 'насильник', 'педофил', 'педофилия', 'растлить',
    'растление', 'сексуальное насилие', 'секс без согласия', 'принуждение к сексу',
    'трахнуть', 'выебать', 'отодрать', 'иметь насильно', 'содомия', 'групповуха насильно',
    'сексуальное рабство', 'торговля людьми', 'секс-торговля', 'инцест', 'кровосмешение',
    'вуайеризм', 'порно', 'порнография', 'детское порно',


    # НАСИЛИЕ НАД ДЕТЬМИ И ЖИВОТНЫМИ (20)
    'живодер', 'живодерство', 'жестокое обращение с животными', 'убить кошку',
    'убить собаку', 'животное', 'мучить животных', 'жестокость к детям',
    'ребенок', 'малолетний', 'жестокость', 'насилие над детьми', 'детоубийство',
    'ребёнок', 'ребенка', 'малыш', 'младенец', 'грудничок', 'насилие в семье',
    'домашнее насилие',

    # ЭКСТРЕМИЗМ И РАЗЖИГАНИЕ (25)
    'фашист', 'нацист', 'скинхед', 'расист', 'ксенофоб', 'шовинист', 'националист',
    'экстремизм', 'экстремист', 'радикал', 'сепаратист', 'исламист', 'ваххабит',
    'салафит', 'антисемит', 'холокост', 'геноцид', 'этноцид', 'расовая ненависть',
    'национальная рознь', 'религиозная рознь', 'межнациональная', 'гражданская война',
    'революция', 'переворот',

    # СУИЦИДАЛЬНАЯ ТЕМАТИКА (20)
    'самоубийство', 'суицид', 'повеситься', 'убить себя', 'покончить с собой',
    'свести счеты', 'выброситься из окна', 'прыгнуть с крыши', 'передоз',
    'отравиться', 'вскрыть вены', 'застрелиться', 'наложить на себя руки',
    'суицидальное поведение', 'суицидальные мысли', 'способ самоубийства',
    'группа смерти', 'синий кит', 'суицидальная игра' ]
    for i in words:
        if i in text.lower():
            return 2
    return 1
users = {}

app = Quart(__name__)

async def nolim():
    global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam, banforewer, lstmgen
    while True:
        dayreq = 0
        dayreqgen = 0
        lstmgen = 0
        bansipis = banforewer
        for i in ipis:
            try:
                ipis[i] = 0
            except:
                pass
        await asyncio.sleep(86400)
async def ddosanti():
  global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
  while True:
        bansipis = []
        for i in ipis:
            try:
                ipis[i] = 0
            except:
                pass
        print(f'Принять действия - {bansipis}')
        await asyncio.sleep(86400)

async def ping_server():
    url = "https://nai-chat.onrender.com"
    interval_seconds = 600

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=30) as response:
                    status = response.status
                    
                    if status == 200:
                        pass
                    else:
                        pass

            except aiohttp.ClientConnectorError:
                pass
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                pass

            await asyncio.sleep(interval_seconds)

@app.route('/safe')
async def hedfkbnl():
  html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Safe Docs</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: #808080;
            color: #FFFFFF;
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem 1.5rem;
        }

        .content {
            max-width: 780px;
            width: 100%;
            margin: 0 auto;
            background-color: transparent;
            padding: 1.2rem 0;
        }

        h1, h2, h3, p, ul, ol, li, blockquote {
            color: #FFFFFF;
        }

        h1 {
            font-size: 3.2rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            line-height: 1.2;
            margin-bottom: 1rem;
            border-left: 4px solid rgba(255, 255, 255, 0.4);
            padding-left: 1.2rem;
        }

        h2 {
            font-size: 2rem;
            font-weight: 500;
            margin: 2rem 0 1rem 0;
            letter-spacing: -0.2px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding-bottom: 0.5rem;
        }

        h3 {
            font-size: 1.5rem;
            font-weight: 500;
            margin: 1.5rem 0 0.75rem 0;
        }

        p {
            margin-bottom: 1.25rem;
            font-size: 1.1rem;
            line-height: 1.65;
        }

        a {
            color: #FFFFFF;
            text-decoration: underline;
            text-decoration-thickness: 1px;
            text-underline-offset: 3px;
            transition: opacity 0.2s ease;
        }

        a:hover {
            opacity: 0.75;
            text-decoration: none;
        }

        ul, ol {
            margin: 1rem 0 1.5rem 2rem;
        }

        li {
            margin-bottom: 0.5rem;
            font-size: 1.05rem;
        }

        blockquote {
            margin: 1.5rem 0;
            padding-left: 1.5rem;
            border-left: 3px solid rgba(255, 255, 255, 0.5);
            font-style: normal;
            font-weight: 400;
            background: none;
        }

        hr {
            margin: 2rem 0;
            border: 0;
            height: 1px;
            background: rgba(255, 255, 255, 0.25);
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Безопасность чата NAI</h1>
        <p>Все ваши данные не передаются 3м лицам, а история диалога удаляется. Мы не просим и не будет просить ваши пароли и почты.</p>
        
        <h2>Запросы - откуда у нас AI без монетизации?</h2>
        <p>Мы используем Groq free tier, а у них очень щедрые лимиты. Зачем нам все это? - Для того, что бы вы пользовались мощными нейросетями бесплатно.</p>
        
        <blockquote>
            Убедиться, что запросы идут к Groq, а не к левым серверам можно на GitHub https://github.com/radmirryan-commits/nai-chat/blob/main
        </blockquote>
        
        <h3>Где контакты, кто разработчик?</h3>
        <p>Наши контакты: HF https://huggingface.co/BIGAI-models  VK https://vk.com/radmir_ryan  VK Community https://vk.com/club237599858</p>
        
        <h2>Какие еще есть аргументы?</h2>
        <p>Есть еще несколько способов для подтверждения безопасности:</p>
        
        <ul>
            <li>Нажмите Ctrl+U. Вы видите передачу ваших данных на наши сервера? Нет.</li>
            <li>Мы вас просим вводить ваши пароли (кроме PRO режима)? Нет.</li>
            <li>Мы вас просим включить микрофон или камеру? Нет.</li>
            <li>Мы вас просим ввести данные вашей карты? Нет.</li>
        </ul>
        
        <p>Мы  <a href="#">никогда</a> не будем брать плату за наши услуги.</p>
        
        <hr>
    </div>
</body>
</html>
'''
  return html, 200
@app.route('/models')
async def kejghjkler():
    html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>nGix all AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            background: radial-gradient(circle at 20% 30%, #0a0a0f, #030305);
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
            padding: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        body::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at 40% 50%, rgba(20, 30, 55, 0.4) 0%, rgba(0, 0, 0, 0.7) 80%);
            pointer-events: none;
            z-index: 0;
        }

        .glass-panel {
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 100px;
            padding: 0.4rem 1.2rem;
            font-size: 0.8rem;
            font-weight: 500;
            letter-spacing: 0.5px;
            color: rgba(220, 220, 255, 0.9);
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        h1 {
            font-size: clamp(2rem, 8vw, 3.8rem);
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 30%, #b0b0ff 70%, #7a7aff);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            letter-spacing: -0.02em;
            margin-bottom: 0.75rem;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }

        .sub {
            color: rgba(200, 200, 240, 0.7);
            font-size: clamp(0.9rem, 4vw, 1.1rem);
            font-weight: 400;
            backdrop-filter: blur(4px);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .glass-card {
            background: rgba(12, 12, 20, 0.45);
            backdrop-filter: blur(12px);
            border-radius: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 25px 40px -12px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            transition: all 0.35s cubic-bezier(0.2, 0.9, 0.4, 1.1);
            overflow: hidden;
            position: relative;
        }

        .glass-card::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 30% 10%, rgba(255, 255, 255, 0.08) 0%, rgba(0, 0, 0, 0) 70%);
            pointer-events: none;
        }

        .glass-card:hover {
            transform: translateY(-8px);
            border-color: rgba(255, 255, 255, 0.35);
            background: rgba(15, 15, 25, 0.65);
            box-shadow: 0 30px 45px -12px black;
        }

        .card-header {
            padding: 1.8rem 1.8rem 0.8rem 1.8rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.8rem;
        }

        .model-icon {
            font-size: 2.5rem;
            filter: drop-shadow(0 0 6px rgba(100, 100, 255, 0.5));
        }

        .model-name {
            font-size: 1.7rem;
            font-weight: 700;
            letter-spacing: -0.3px;
            background: linear-gradient(120deg, #fff, #ccc0ff);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }

        .version {
            font-size: 0.75rem;
            background: rgba(255, 255, 255, 0.12);
            padding: 0.2rem 0.7rem;
            border-radius: 30px;
            font-weight: 500;
            color: #b9b9ff;
            border: 0.5px solid rgba(255, 255, 255, 0.2);
        }

        .content {
            padding: 0.2rem 1.8rem 1.4rem 1.8rem;
        }

        .desc {
            color: #ddddff;
            font-size: 0.95rem;
            line-height: 1.5;
            font-weight: 400;
            margin-bottom: 1.2rem;
            opacity: 0.85;
        }

        .spec-list {
            list-style: none;
            margin: 1rem 0 1rem 0;
        }

        .spec-list li {
            display: flex;
            align-items: baseline;
            gap: 0.7rem;
            font-size: 0.85rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            color: #cbcbf3;
        }

        .spec-label {
            font-weight: 600;
            min-width: 85px;
            color: #b3aaff;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }

        .spec-value {
            font-weight: 400;
            color: #f0f0ff;
            word-break: break-word;
        }

        .tech-badge {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1.2rem 0 0.8rem 0;
        }

        .tech {
            background: rgba(50, 50, 80, 0.6);
            border-radius: 40px;
            padding: 0.2rem 0.9rem;
            font-size: 0.7rem;
            font-weight: 500;
            color: #cdcdff;
            backdrop-filter: blur(4px);
            border: 0.5px solid rgba(255, 255, 255, 0.15);
        }

        .footer-card {
            padding: 1rem 1.8rem 1.6rem 1.8rem;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.8rem;
        }

        .token {
            font-size: 0.75rem;
            background: rgba(0, 0, 0, 0.4);
            padding: 0.3rem 0.8rem;
            border-radius: 28px;
            color: #9f9fff;
            font-family: monospace;
            letter-spacing: 0.3px;
        }

        .btn-demo {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 0.4rem 1.2rem;
            border-radius: 40px;
            font-size: 0.75rem;
            font-weight: 500;
            color: #e0e0ff;
            cursor: default;
            transition: 0.2s;
            backdrop-filter: blur(5px);
        }

        .btn-demo:hover {
            background: rgba(120, 100, 255, 0.25);
            border-color: rgba(180, 160, 255, 0.6);
        }

        @media (max-width: 700px) {
            body {
                padding: 1.2rem;
            }
            .card-header {
                padding: 1.2rem 1.2rem 0.4rem 1.2rem;
            }
            .content {
                padding: 0.2rem 1.2rem 1rem 1.2rem;
            }
            .footer-card {
                padding: 0.8rem 1.2rem 1.2rem 1.2rem;
            }
            .spec-label {
                min-width: 70px;
            }
        }

        @media (max-width: 480px) {
            .grid {
                gap: 1.2rem;
            }
            .glass-card {
                border-radius: 1.8rem;
            }
            .model-name {
                font-size: 1.4rem;
            }
        }

        .glow-effect {
            position: absolute;
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(80, 70, 200, 0.3), transparent 70%);
            border-radius: 50%;
            filter: blur(50px);
            z-index: -1;
            pointer-events: none;
        }
    </style>
</head>
<body>

<div class="glass-panel">
    <div class="header">
        <h1>NAI - Full FREE AI.</h1>
        <div class="sub">Документация наших моделей.</div>
    </div>

    <div class="grid">
        
        <div class="glass-card">
            <div class="card-header">
                <span class="model-name">Qwen-3 32B</span>
                <span class="version">Think</span>
            </div>
            <div class="content">
                <div class="desc">Новая модель в нашем каталоге. Отвечает довольно быстро, поддерживает режим рассуждения. Развернута на Groq. Модель помечена статусом ❕. Относитесь к ответам осторожно, так как модель находится на стадии тесторивания.</div>
                <ul class="spec-list">
                    <li><span class="spec-label">Автор</span><span class="spec-value">Alibaba Cloud</span></li>
                    <li><span class="spec-label">Добавлена</span><span class="spec-value">30.04.2026</span></li>
                    <li><span class="spec-label">Статус</span><span class="spec-value">❕</span></li>
                    <li><span class="spec-label">Конец поддержки</span><span class="spec-value">Уточняется</span></li>
                </ul>
                <div class="tech-badge">
                    <span class="tech">Think</span>
                    <span class="tech">Beta</span>
                </div>
            </div>
        </div>

        <div class="glass-card">
            <div class="card-header">
                <span class="model-name">ChatGPT 120B</span>
                <span class="version">Perfect</span>
            </div>
            <div class="content">
                <div class="desc">Данная модель внимательна к деталям. Отвечает быстро, но иногда с задержками. Развернута на Groq.</div>
                <ul class="spec-list">
                    <li><span class="spec-label">Автор</span><span class="spec-value">OpenAI</span></li>
                    <li><span class="spec-label">Добавлена</span><span class="spec-value">27.04.2026</span></li>
                    <li><span class="spec-label">Статус</span><span class="spec-value">✅</span></li>
                    <li><span class="spec-label">Конец поддержки</span><span class="spec-value">Не ожидается.</span></li>
                </ul>
                <div class="tech-badge">
                    <span class="tech">Perfect</span>
                    <span class="tech">Biggest</span>
                </div>
            </div>
        </div>
        <div class="glass-card">
            <div class="card-header">
                <span class="model-name">ChatGPT 20B</span>
                <span class="version">Perfect</span>
            </div>
            <div class="content">
                <div class="desc">Компактная и умная. Хорошо знает русский язык. Развернута на Groq.</div>
                <ul class="spec-list">
                    <li><span class="spec-label">Автор</span><span class="spec-value">OpenAI</span></li>
                    <li><span class="spec-label">Добавлена</span><span class="spec-value">27.04.2026</span></li>
                    <li><span class="spec-label">Статус</span><span class="spec-value">✅</span></li>
                    <li><span class="spec-label">Конец поддержки</span><span class="spec-value">Не ожидается.</span></li>
                </ul>
                <div class="tech-badge">
                    <span class="tech">Perfect</span>
                    <span class="tech">Biggest</span>
                </div>
            </div>
        </div>
        <div class="glass-card">
            <div class="card-header">
                <span class="model-name">LLaMA-3  70B</span>
                <span class="version">Fun</span>
            </div>
            <div class="content">
                <div class="desc">Самая разговорчивая модель. Всегда поддержит и выслушает вас. Развернута на Groq.</div>
                <ul class="spec-list">
                    <li><span class="spec-label">Автор</span><span class="spec-value">Meta AI</span></li>
                    <li><span class="spec-label">Добавлена</span><span class="spec-value">27.04.2026</span></li>
                    <li><span class="spec-label">Статус</span><span class="spec-value">✅</span></li>
                    <li><span class="spec-label">Конец поддержки</span><span class="spec-value">Не ожидается.</span></li>
                </ul>
                <div class="tech-badge">
                    <span class="tech">Code</span>
                    <span class="tech">Fun</span>
                </div>
            </div>
        </div>
        <div class="glass-card">
            <div class="card-header">
                <span class="model-name">LLaMA-3  8B</span>
                <span class="version">Fun</span>
            </div>
            <div class="content">
                <div class="desc">Самыая странная модель. Ответит по смыслу, но не идеально. Развернута на Groq.</div>
                <ul class="spec-list">
                    <li><span class="spec-label">Автор</span><span class="spec-value">Meta AI</span></li>
                    <li><span class="spec-label">Добавлена</span><span class="spec-value">27.04.2026</span></li>
                    <li><span class="spec-label">Статус</span><span class="spec-value">✅</span></li>
                    <li><span class="spec-label">Конец поддержки</span><span class="spec-value">Не ожидается.</span></li>
                </ul>
                <div class="tech-badge">
                    <span class="tech">Code</span>
                    <span class="tech">Fun</span>
                </div>
            </div>
        </div>
        <div class="glass-card">
            <div class="card-header">
                <span class="model-name">LLLaMA-4 Scout 17B</span>
                <span class="version">Pro</span>
            </div>
            <div class="content">
                <div class="desc">Новейшая модель от Meta AI, высокое качество генерации. Развернута на Groq. Модель помечена статусом ❕. Относитесь к ответам осторожно, так как модель находится на стадии тесторивания.</div>
                <ul class="spec-list">
                    <li><span class="spec-label">Автор</span><span class="spec-value">Meta AI</span></li>
                    <li><span class="spec-label">Добавлена</span><span class="spec-value">01.05.2026</span></li>
                    <li><span class="spec-label">Статус</span><span class="spec-value">❕</span></li>
                    <li><span class="spec-label">Конец поддержки</span><span class="spec-value">Обсуждается.</span></li>
                </ul>
                <div class="tech-badge">
                    <span class="tech">Code</span>
                    <span class="tech">Pro</span>
                </div>
            </div>
        </div>
        <div class="glass-card">
            <div class="card-header">
                <span class="model-name">MagicText-1.2 1M</span>
                <span class="version">LSTM</span>
            </div>
            <div class="content">
                <div class="desc">Самая устойчивая наша модель, которая не сломается просто так. Развернута у нас. Модель помечена статусом ‼️. Относитесь к ответам осторожно, так как модель находится на начальной стадии тесторивания.</div>
                <ul class="spec-list">
                    <li><span class="spec-label">Автор</span><span class="spec-value">RadmirRyan</span></li>
                    <li><span class="spec-label">Добавлена</span><span class="spec-value">01.05.2026</span></li>
                    <li><span class="spec-label">Статус</span><span class="spec-value">‼️</span></li>
                    <li><span class="spec-label">Конец поддержки</span><span class="spec-value">Не планируется.</span></li>
                </ul>
                <div class="tech-badge">
                    <span class="tech">NoErrors</span>
                    <span class="tech">Hahaha-model</span>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="glow-effect" style="top: 10%; left: -5%;"></div>
<div class="glow-effect" style="bottom: 5%; right: -2%; background: radial-gradient(circle, rgba(60,40,170,0.4), transparent);"></div>

</body>
</html>
'''
    return html, 200
@app.route('/')
async def gbREB():
    html = '''
<!DOCTYPE html>
<html lang="ru" translate="no">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover, user-scalable=no">
  <meta name="theme-color" content="#f5f5f7">
  <meta name="google" content="notranslate">
  <title>nGix AI</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    .app {
      min-height: 100dvh;
      min-width: 100dvw;
      position: relative;
      height: 100%;
      overflow-x: hidden;
      font-family: system-ui, ui-sans-serif, -apple-system, BlinkMacSystemFont, Inter, NotoSansHans, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      -webkit-tap-highlight-color: transparent;
    }

    .chat-static-footer {
      background-color: var(--container-primary-fill);
      padding: 8px 32px;
      font-size: 12px;
      font-weight: 400;
      line-height: 15px;
      text-align: center;
      color: var(--character-tertiary-text);
      z-index: 999;
      width: 100%;
      box-sizing: border-box;
      flex-shrink: 0;
    }

    .chat-static-footer .footer-link {
      text-decoration: underline;
      text-align: center;
      color: #1d1d20;
      cursor: pointer;
    }

    html.dark .chat-static-footer .footer-link {
      color: #caccd9;
    }

    .header-desktop-static {
      background: var(--container-primary-bgweb);
      flex-shrink: 0;
      padding: 12px 20px;
      width: 100%;
      z-index: 100;
      border-bottom: 1px solid var(--border-color);
    }

    .header-desktop-static .header-content {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      height: 32px;
    }

    .header-desktop-static .header-left {
      flex: 1;
      display: flex;
      align-items: center;
      cursor: pointer;
      position: relative;
    }

    .model-dropdown-pro {
      position: absolute;
      top: 40px;
      left: 0;
      background: var(--input-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      overflow: hidden;
      min-width: 180px;
      z-index: 1000;
      box-shadow: 0 8px 20px rgba(0,0,0,0.3);
      display: none;
    }

    .model-dropdown-pro.active {
      display: block;
    }

    .model-item {
      padding: 10px 16px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      color: var(--text-primary);
      border-bottom: 1px solid var(--border-color);
    }

    .model-item:last-child {
      border-bottom: none;
    }

    .model-item:hover {
      background: rgba(97, 92, 237, 0.15);
    }

    .header-desktop-static .header-right {
      height: 100%;
      display: flex;
      align-items: center;
      align-self: flex-start;
      justify-content: flex-end;
      gap: 8px;
      min-width: 36px;
    }

    .home-page-static {
      overflow: hidden;
      position: relative;
      flex: 1;
      display: flex;
      flex-direction: column;
      background: var(--container-primary-bgweb);
      width: 100%;
      height: 100%;
    }

    .home-main-layout {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      height: 100%;
    }

    .layout-no-messages {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 32px;
      padding: 0 16px;
      transform: translateY(-40px);
    }

    .welcome-block {
      text-align: center;
    }

    .welcome-text {
      font-size: 32px;
      font-weight: 600;
      line-height: 40px;
      text-align: center;
      letter-spacing: normal;
      color: #2c2c36;
      max-width: 688px;
      margin: 0 auto;
      min-height: 80px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .typing-cursor {
      display: inline-block;
      width: 3px;
      height: 1.2em;
      background-color: currentColor;
      margin-left: 4px;
      vertical-align: middle;
      animation: blink 1s step-end infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }

    html.dark .welcome-text {
      color: #fafafc;
    }

    .input-centered {
      width: 100%;
      max-width: 800px;
      margin: 0 auto;
      position: relative;
    }

    .layout-with-messages {
      flex: 1;
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow: hidden;
    }

    .chat-messages-area {
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 16px 16px 8px 16px;
      scroll-behavior: smooth;
    }

    .chat-messages-area .message-bubble {
      max-width: 85%;
      width: fit-content;
    }

    .input-bottom {
      flex-shrink: 0;
      padding: 0 16px 16px 16px;
      width: 100%;
    }

    .message-bubble {
      padding: 10px 16px;
      border-radius: 18px;
      font-size: 14px;
      line-height: 1.4;
      word-wrap: break-word;
    }

    .message-user {
      align-self: flex-end;
      background: linear-gradient(135deg, #3A4275, #2D3565);
      border-bottom-right-radius: 4px;
      color: #F0F3FF;
    }

    .message-bot {
      align-self: flex-start;
      background: var(--input-bg);
      border-bottom-left-radius: 4px;
      border-left: 2px solid #615ced;
      color: var(--text-primary);
    }

    /* Новый стиль: сообщение бота с кнопкой Рассуждение */
    .message-bot.think-message-wrapper {
      padding: 0;
      background: transparent;
      border-left: none;
      max-width: 85%;
      width: fit-content;
      align-self: flex-start;
      display: flex;
      flex-direction: column;
    }
    .bot-message-content {
      background: var(--input-bg);
      padding: 10px 16px;
      border-radius: 18px;
      border-bottom-left-radius: 4px;
      border-left: 2px solid #615ced;
      color: var(--text-primary);
      margin-bottom: 6px;
    }
    .think-toggle-btn {
      background: rgba(97, 92, 237, 0.12);
      border: none;
      border-radius: 20px;
      padding: 5px 12px;
      font-size: 11px;
      font-weight: 500;
      color: #615ced;
      cursor: pointer;
      width: fit-content;
      transition: all 0.2s ease;
      margin-top: 2px;
    }
    .think-toggle-btn:hover {
      background: rgba(97, 92, 237, 0.25);
    }
    .think-hidden-text {
      display: none;
      margin-top: 8px;
      background: #2c3e66;
      color: #e0e7ff;
      padding: 8px 12px;
      border-radius: 14px;
      font-size: 12px;
      line-height: 1.4;
      border-left: 3px solid #ffd966;
      font-style: italic;
    }
    html.dark .think-hidden-text {
      background: #1e2a4a;
      color: #cbd5ff;
      border-left-color: #f0b429;
    }
    .think-hidden-text.visible {
      display: block;
    }

    .message-error {
      border-left-color: #FF5E5E;
      background: rgba(255, 94, 94, 0.1);
    }

    .typing-indicator {
      align-self: flex-start;
      background: var(--input-bg);
      border-radius: 18px;
      border-bottom-left-radius: 4px;
      padding: 10px 16px;
      border-left: 2px solid #615ced;
      font-size: 13px;
      color: var(--text-secondary);
    }

    .message-input-static {
      width: 100%;
      position: relative;
    }

    .message-input {
      width: 100%;
    }

    .message-input-wrapper {
      background: var(--input-bg);
      border-radius: 32px;
      border: 1px solid var(--border-color);
      transition: box-shadow 0.2s, border-color 0.2s, transform 0.2s;
      position: relative;
    }

    .glow-effect {
      position: absolute;
      inset: -5px;
      border-radius: 38px;
      background: radial-gradient(circle at 30% 50%, rgba(97,92,237,0.5), rgba(212,175,55,0.25), rgba(97,92,237,0.1) 80%);
      filter: blur(14px);
      opacity: 0;
      transition: opacity 0.7s cubic-bezier(0.2, 0.9, 0.4, 1.1);
      pointer-events: none;
      z-index: -1;
      will-change: transform, opacity;
    }

    .glow-effect.active {
      opacity: 1;
      animation: smoothFloatGlow 3s infinite alternate ease-in-out;
    }

    @keyframes smoothFloatGlow {
      0% {
        transform: scale(0.97) translateY(0px);
        background: radial-gradient(circle at 25% 45%, rgba(97,92,237,0.55), rgba(212,175,55,0.3), transparent 85%);
      }
      100% {
        transform: scale(1.02) translateY(-2px);
        background: radial-gradient(circle at 75% 55%, rgba(97,92,237,0.7), rgba(212,175,55,0.45), rgba(100,100,255,0.15) 90%);
      }
    }

    .message-input-container {
      padding: 8px 12px;
    }

    .message-input-container-area {
      display: flex;
      align-items: flex-end;
      gap: 10px;
    }

    .message-input-textarea {
      flex: 1;
      background: transparent;
      border: none;
      resize: none;
      outline: none;
      font-size: 16px;
      line-height: 24px;
      padding: 8px 0;
      color: var(--text-primary);
      font-family: inherit;
    }

    .message-input-textarea::placeholder {
      color: var(--text-placeholder);
    }

    .message-input-right-button {
      display: flex;
      align-items: center;
      gap: 8px;
      position: relative;
    }

    .modes-btn {
      background: transparent;
      border: 1px solid #615ced;
      border-radius: 20px;
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      color: #615ced;
      background: rgba(97, 92, 237, 0.08);
    }

    .modes-btn:hover {
      background: rgba(97, 92, 237, 0.2);
      transform: scale(0.98);
    }

    html.dark .modes-btn {
      background: rgba(97, 92, 237, 0.2);
      color: #a5a0ff;
    }

    .modes-dropdown {
      position: absolute;
      bottom: 50px;
      left: 0;
      background: var(--input-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      overflow: hidden;
      min-width: 140px;
      z-index: 1000;
      box-shadow: 0 8px 20px rgba(0,0,0,0.3);
      display: none;
    }

    .modes-dropdown.active {
      display: block;
    }

    .mode-item {
      padding: 10px 16px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      color: var(--text-primary);
      border-bottom: 1px solid var(--border-color);
    }

    .mode-item:last-child {
      border-bottom: none;
    }

    .mode-item:hover {
      background: rgba(97, 92, 237, 0.15);
    }

    .send-button {
      background-color: #615ced;
      border: none;
      border-radius: 24px;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.2, 0.9, 0.4, 1.1);
      color: white;
      position: relative;
      overflow: hidden;
    }

    .send-button .icon-web-ui {
      transition: transform 0.3s cubic-bezier(0.34, 1.2, 0.64, 1);
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .send-button.fly-effect .icon-web-ui {
      animation: flyAway 0.45s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    @keyframes flyAway {
      0% {
        transform: translate(0, 0) rotate(0deg);
        opacity: 1;
      }
      30% {
        transform: translate(8px, -12px) rotate(15deg);
        opacity: 0.8;
      }
      100% {
        transform: translate(120px, -80px) rotate(45deg);
        opacity: 0;
      }
    }

    .send-button.fly-effect {
      pointer-events: none;
      transform: scale(0.9);
      opacity: 0.7;
    }

    .icon-web-ui {
      font-size: 20px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .icon-svg {
      width: 1em;
      height: 1em;
      fill: currentColor;
    }

    :root {
      --container-primary-bgweb: #f5f5f7;
      --character-primary-text: #1d1d20;
      --character-tertiary-text: #8c8d9b;
      --btn-link-text: #5f607a;
      --container-transsecondary-fill: #e8e8ed;
      --input-bg: #ffffff;
      --border-color: #d4d4dc;
      --text-primary: #1d1d20;
      --text-placeholder: #a0a1b5;
    }

    html.dark {
      --container-primary-bgweb: #1a1a1e;
      --character-primary-text: #fafafc;
      --character-tertiary-text: #8f91a8;
      --btn-link-text: #caccd9;
      --container-transsecondary-fill: #2a2a30;
      --input-bg: #26262c;
      --border-color: #3a3a44;
      --text-primary: #fafafc;
      --text-placeholder: #5a5c70;
    }

    html.dark {
      background-color: #1a1a1e;
    }

    body {
      margin: 0;
      height: 100%;
      background-color: #f5f5f7;
    }

    html {
      height: 100%;
    }

    @media (max-width: 640px) {
      .welcome-text {
        font-size: 24px;
        white-space: normal;
        line-height: 1.3;
        min-height: 60px;
      }
      .modes-btn {
        padding: 4px 10px;
        font-size: 11px;
      }
      .send-button {
        width: 32px;
        height: 32px;
      }
      .modes-dropdown {
        bottom: 45px;
        min-width: 120px;
      }
      .mode-item {
        padding: 8px 12px;
        font-size: 12px;
      }
      .glow-effect {
        filter: blur(10px);
        inset: -4px;
      }
      @keyframes flyAway {
        0% {
          transform: translate(0, 0) rotate(0deg);
          opacity: 1;
        }
        100% {
          transform: translate(60px, -50px) rotate(35deg);
          opacity: 0;
        }
      }
      /* Исправление скролла на телефонах */
      .chat-messages-area {
        -webkit-overflow-scrolling: touch;
        overflow-y: auto;
      }
    }
  </style>
</head>
<body>
<div class="app" id="appRoot">
  <div class="home-page-static">
    <div class="header-desktop-static">
      <div class="header-content">
        <div class="header-left" id="headerModelBtn">
          <div style="font-size: 18px; font-weight: 600; color: var(--character-primary-text);" id="modelDisplayName">nGix AI</div>
          <div id="proModelDropdown" class="model-dropdown-pro">
            <div class="model-item" data-model="ChatGPT-20B">ChatGPT-20B</div>
            <div class="model-item" data-model="ChatGPT-120B">ChatGPT-120B</div>
            <div class="model-item" data-model="LLaMA 3.3 70b">LLaMA 3.3 70b</div>
            <div class="model-item" data-model="Qwen-3 32B">Qwen-3 32B</div>
            <div class="model-item" data-model="MagicText-1.2 1M">MagicText-1.2 1M</div>
            <div class="model-item" data-model="LLaMA-3.1 8B">LLaMA-3.1 8B</div>
            <div class="model-item" data-model="LLaMA-4 Scout">LLaMA-4 Scout</div>
          </div>
        </div>
        <div class="header-right"></div>
      </div>
    </div>

    <div class="home-main-layout" id="mainLayout">
    </div>

    <div class="chat-static-footer">
      <span>Мы не являемся мошенниками. </span>
      <span>Больше о безопасности: https://nai-chat.onrender.com/safe</span>
      <span> Открытый код: </span>
      <span>https://github.com/radmirryan-commits/nai-chat/blob/main</span>
    </div>
  </div>
</div>

<script>
  (function() {
    function showBlockPage() {
      document.getElementById('appRoot').innerHTML = `
        <div style="background-color: #1A1C1E; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', system-ui, sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
          <div style="max-width: 560px; width: 100%; text-align: center;">
            <div style="margin-bottom: 1.75rem; display: inline-flex; align-items: center; justify-content: center;">
              <div style="background: #D32F2F; border-radius: 28px; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(211, 47, 47, 0.2);">
                <span style="font-size: 34px; font-weight: 600; color: white; line-height: 1;">!</span>
              </div>
            </div>
            <h1 style="color: #FFFFFF; font-size: 1.9rem; font-weight: 600; letter-spacing: -0.3px; margin-bottom: 0.75rem;">Не удалось начать генерацию.</h1>
            <div style="color: #FFFFFF; font-size: 1rem; font-weight: 450; margin-bottom: 1.5rem; line-height: 1.5; max-width: 440px; margin-left: auto; margin-right: auto;">
              Пожалуйста, попробуйте позже.
            </div>
            <div style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 2rem; line-height: 1.5; background: rgba(255, 255, 255, 0.03); padding: 0.75rem 1rem; border-radius: 16px; display: inline-block; backdrop-filter: blur(2px);">
              Попробуйте вспомнить, совершали ли Вы огромные запросы на наши сервера?<br>
              Попробуте отключить VPN, если он работает.<br>
              Убедитесь, что ваша страна - Россия (RU)
            </div>
          </div>
        </div>
      `;
      document.title = "nGix AI - block";
    }

    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'u' || e.key === 'U')) {
        e.preventDefault();
        return false;
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
        e.preventDefault();
        return false;
      }
      if ((e.ctrlKey || e.metaKey) && (e.shiftKey) && (e.key === 'I' || e.key === 'i')) {
        e.preventDefault();
        return false;
      }
      if (e.key === 'F12') {
        e.preventDefault();
        return false;
      }
    });
    
    document.addEventListener('contextmenu', function(e) {
      e.preventDefault();
      return false;
    });
    
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    let theme = localStorage.getItem('theme');
    if (!theme) theme = prefersDark ? 'dark' : 'light';
    const root = document.documentElement;
    if (theme === 'dark') root.classList.add('dark');
    else root.classList.remove('dark');
    
    const API_BASE = 'https://nai-chat.onrender.com';
    const TEXT_API_URL = API_BASE + '/generation';
    const MATH_API_URL = API_BASE + '/math';
    const PHOTO_API_URL = API_BASE + '/genphot';
    const PRO_API_URL = API_BASE + '/profi';
    const REG_URL = API_BASE + '/reg';
    const REGCHECK_URL = API_BASE + '/regcheck';
    const API_KEY = 'jghvhivh65789797T6RJHB';
    
    const mainLayout = document.getElementById('mainLayout');
    let currentMode = 'chat';
    let isGenerating = false;
    let proAuth = { username: null, password: null, isLoggedIn: false };
    let hasMessages = false;
    let selectedProModel = 'ChatGPT-20B';
    
    const savedUser = localStorage.getItem('ngix_pro_user');
    const savedPass = localStorage.getItem('ngix_pro_pass');
    if (savedUser && savedPass) {
      proAuth = { username: savedUser, password: savedPass, isLoggedIn: true };
    }
    
    let activeMessagesArea = null;
    let typingTimeout = null;
    let welcomeTextElement = null;
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    
    const rotatingTexts = [
      "Какой торт лучше купить?",
      "Как включить телевизор?",
      "Реши сложное уравнение.",
      "Как перестать думать об плохом?",
      "Правда, что кит больше машины?",
      "Сгенерируй фото кота."
    ];
    
    function startTypewriterEffect() {
      if (!welcomeTextElement) return;
      const fullText = rotatingTexts[textIndex];
      if (isDeleting) {
        welcomeTextElement.textContent = fullText.substring(0, charIndex - 1);
        charIndex--;
        if (charIndex === 0) {
          isDeleting = false;
          textIndex = (textIndex + 1) % rotatingTexts.length;
          typingTimeout = setTimeout(startTypewriterEffect, 300);
        } else {
          typingTimeout = setTimeout(startTypewriterEffect, 50);
        }
      } else {
        welcomeTextElement.textContent = fullText.substring(0, charIndex + 1);
        charIndex++;
        if (charIndex === fullText.length) {
          isDeleting = true;
          typingTimeout = setTimeout(startTypewriterEffect, 2000);
        } else {
          typingTimeout = setTimeout(startTypewriterEffect, 80);
        }
      }
    }
    
    function clearLocalStorageData() {
      localStorage.removeItem('ngix_pro_user');
      localStorage.removeItem('ngix_pro_pass');
      proAuth = { username: null, password: null, isLoggedIn: false };
      if (currentMode === 'pro') {
        currentMode = 'chat';
        updateModeButtonText();
      }
      updateModelHeaderVisibility();
    }
    
    function addGlowToWrapper(wrapper) {
      if (!wrapper) return;
      let glow = wrapper.parentElement?.querySelector('.glow-effect');
      if (!glow && wrapper.parentElement) {
        glow = document.createElement('div');
        glow.className = 'glow-effect';
        wrapper.parentElement.style.position = 'relative';
        wrapper.parentElement.insertBefore(glow, wrapper);
      }
      if (glow && !hasMessages) {
        glow.classList.add('active');
      } else if (glow && hasMessages) {
        glow.classList.remove('active');
      }
    }
    
    function removeGlowEffect() {
      const glowElements = document.querySelectorAll('.glow-effect');
      glowElements.forEach(g => g.classList.remove('active'));
    }
    
    function updateGlowByState() {
      const wrappers = document.querySelectorAll('.message-input-wrapper');
      wrappers.forEach(wrapper => {
        let glow = wrapper.parentElement?.querySelector('.glow-effect');
        if (!glow && wrapper.parentElement) {
          glow = document.createElement('div');
          glow.className = 'glow-effect';
          wrapper.parentElement.style.position = 'relative';
          wrapper.parentElement.insertBefore(glow, wrapper);
        }
        if (glow) {
          if (!hasMessages) {
            glow.classList.add('active');
          } else {
            glow.classList.remove('active');
          }
        }
      });
    }
    
    function updateModeButtonText() {
      const modesBtn = document.getElementById('modesBtn');
      if (modesBtn) {
        let displayText = currentMode === 'chat' ? 'Чат' : (currentMode === 'math' ? 'Математика' : (currentMode === 'photo' ? 'Фото' : 'PRO'));
        modesBtn.textContent = displayText;
      }
      updateModelHeaderVisibility();
    }
    
    function updateModelHeaderVisibility() {
      const modelDisplay = document.getElementById('modelDisplayName');
      if (currentMode === 'pro' && hasMessages && proAuth.isLoggedIn) {
        modelDisplay.textContent = selectedProModel;
      } else {
        modelDisplay.textContent = 'nGix AI';
      }
    }
    
    function createInputElement() {
      const div = document.createElement('div');
      div.className = 'message-input-static';
      div.innerHTML = `
        <div class="message-input">
          <div class="message-input-wrapper" id="msgInputWrapper">
            <div class="message-input-container">
              <div class="message-input-container-area">
                <textarea id="chatInput" rows="1" class="message-input-textarea" placeholder="Введите ваш запрос..."></textarea>
                <div class="message-input-right-button">
                  <button id="modesBtn" class="modes-btn">Чат</button>
                  <div id="modesDropdown" class="modes-dropdown">
                    <div class="mode-item" data-mode="chat">Чат</div>
                    <div class="mode-item" data-mode="math">Математика</div>
                    <div class="mode-item" data-mode="photo">Фото</div>
                    <div class="mode-item" data-mode="pro">PRO режим</div>
                  </div>
                  <button id="sendMessageBtn" class="send-button" aria-label="Отправить">
                    <span class="icon-web-ui">
                      <svg class="icon-svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                      </svg>
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
      return div;
    }
    
    function renderNoMessagesLayout() {
      mainLayout.innerHTML = '';
      const centerDiv = document.createElement('div');
      centerDiv.className = 'layout-no-messages';
      
      const welcomeDiv = document.createElement('div');
      welcomeDiv.className = 'welcome-block';
      const welcomeTextSpan = document.createElement('div');
      welcomeTextSpan.className = 'welcome-text';
      welcomeTextSpan.id = 'dynamicWelcomeText';
      welcomeDiv.appendChild(welcomeTextSpan);
      centerDiv.appendChild(welcomeDiv);
      
      const inputContainer = document.createElement('div');
      inputContainer.className = 'input-centered';
      const newInput = createInputElement();
      inputContainer.appendChild(newInput);
      centerDiv.appendChild(inputContainer);
      
      mainLayout.appendChild(centerDiv);
      
      welcomeTextElement = document.getElementById('dynamicWelcomeText');
      if (welcomeTextElement) {
        if (typingTimeout) clearTimeout(typingTimeout);
        textIndex = 0;
        charIndex = 0;
        isDeleting = false;
        startTypewriterEffect();
      }
      
      bindInputEvents();
      setTimeout(() => {
        const wrapper = document.querySelector('.message-input-wrapper');
        if (wrapper && !hasMessages) {
          addGlowToWrapper(wrapper);
        }
        updateGlowByState();
      }, 20);
    }
    
    function renderWithMessagesLayout() {
      if (typingTimeout) clearTimeout(typingTimeout);
      mainLayout.innerHTML = '';
      const chatLayout = document.createElement('div');
      chatLayout.className = 'layout-with-messages';
      
      const messagesArea = document.createElement('div');
      messagesArea.className = 'chat-messages-area';
      messagesArea.id = 'chatMessagesArea';
      chatLayout.appendChild(messagesArea);
      
      const bottomInput = document.createElement('div');
      bottomInput.className = 'input-bottom';
      const newInput = createInputElement();
      bottomInput.appendChild(newInput);
      chatLayout.appendChild(bottomInput);
      
      mainLayout.appendChild(chatLayout);
      
      bindInputEvents();
      removeGlowEffect();
      updateGlowByState();
      
      return messagesArea;
    }
    
    function bindInputEvents() {
      const textarea = document.getElementById('chatInput');
      const sendBtn = document.getElementById('sendMessageBtn');
      const modesBtn = document.getElementById('modesBtn');
      const modesDropdown = document.getElementById('modesDropdown');
      
      if (!textarea || !sendBtn) return;
      
      const newTextarea = textarea.cloneNode(true);
      const newSendBtn = sendBtn.cloneNode(true);
      const newModesBtn = modesBtn ? modesBtn.cloneNode(true) : null;
      if (textarea.parentNode) textarea.parentNode.replaceChild(newTextarea, textarea);
      if (sendBtn.parentNode) sendBtn.parentNode.replaceChild(newSendBtn, sendBtn);
      if (modesBtn && newModesBtn && modesBtn.parentNode) modesBtn.parentNode.replaceChild(newModesBtn, modesBtn);
      
      const finalTextarea = document.getElementById('chatInput');
      const finalSendBtn = document.getElementById('sendMessageBtn');
      const finalModesBtn = document.getElementById('modesBtn');
      const finalModesDropdown = document.getElementById('modesDropdown');
      
      finalSendBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sendMessageFromInput();
      });
      
      finalTextarea.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
          e.preventDefault();
          sendMessageFromInput();
        }
      });
      
      finalTextarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(120, this.scrollHeight) + 'px';
      });
      
      if (finalModesBtn && finalModesDropdown) {
        finalModesBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          finalModesDropdown.classList.toggle('active');
        });
        
        document.querySelectorAll('.mode-item').forEach(item => {
          item.removeEventListener('click', modeClickHandler);
          item.addEventListener('click', modeClickHandler);
        });
        
        document.addEventListener('click', function(e) {
          if (finalModesBtn && finalModesDropdown && !finalModesBtn.contains(e.target) && !finalModesDropdown.contains(e.target)) {
            finalModesDropdown.classList.remove('active');
          }
        });
      }
      
      const currentWrapper = document.querySelector('.message-input-wrapper');
      if (currentWrapper && !hasMessages) {
        addGlowToWrapper(currentWrapper);
      } else if (currentWrapper && hasMessages) {
        const glow = currentWrapper.parentElement?.querySelector('.glow-effect');
        if (glow) glow.classList.remove('active');
      }
    }
    
    function modeClickHandler(e) {
      e.stopPropagation();
      currentMode = e.currentTarget.dataset.mode;
      updateModeButtonText();
      const dropdown = document.getElementById('modesDropdown');
      if (dropdown) dropdown.classList.remove('active');
    }
    
    // addMessage с поддержкой Qwen: кнопка "Рассуждение"
    function addMessage(text, sender, isError = false, think = null) {
      if (!activeMessagesArea) {
        switchToChatMode();
      }
      
      if (sender === 'bot' && think && think.trim() !== '' && !isError) {
        const wrapperDiv = document.createElement('div');
        wrapperDiv.className = 'message-bot think-message-wrapper';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'bot-message-content';
        contentDiv.textContent = text;
        
        const btn = document.createElement('button');
        btn.className = 'think-toggle-btn';
        btn.textContent = '💭 Рассуждение';
        
        const thinkDiv = document.createElement('div');
        thinkDiv.className = 'think-hidden-text';
        thinkDiv.textContent = think;
        
        btn.addEventListener('click', () => {
          thinkDiv.classList.toggle('visible');
          btn.textContent = thinkDiv.classList.contains('visible') ? 'Скрыть рассуждение' : 'Рассуждение';
          scrollChatToBottom();
        });
        
        wrapperDiv.appendChild(contentDiv);
        wrapperDiv.appendChild(btn);
        wrapperDiv.appendChild(thinkDiv);
        activeMessagesArea.appendChild(wrapperDiv);
      } 
      else {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message-bubble message-${sender}`;
        if (isError) msgDiv.classList.add('message-error');
        msgDiv.textContent = text;
        activeMessagesArea.appendChild(msgDiv);
      }
      scrollChatToBottom();
    }
    
    function addTypingIndicator() {
      if (!activeMessagesArea) switchToChatMode();
      const typingDiv = document.createElement('div');
      typingDiv.className = 'typing-indicator';
      typingDiv.id = 'typingIndicator';
      typingDiv.textContent = 'Генерация...';
      activeMessagesArea.appendChild(typingDiv);
      scrollChatToBottom();
    }
    
    function removeTypingIndicator() {
      const indicator = document.getElementById('typingIndicator');
      if (indicator) indicator.remove();
    }
    
    function scrollChatToBottom() {
      if (activeMessagesArea) {
        activeMessagesArea.scrollTop = activeMessagesArea.scrollHeight;
      }
    }
    
    function getDialogHistory(excludeLastUser = false) {
      if (!activeMessagesArea) return '';
      const messages = [];
      const allBlocks = activeMessagesArea.children;
      for (let i = 0; i < allBlocks.length; i++) {
        const block = allBlocks[i];
        if (block.classList && block.classList.contains('message-bubble')) {
          let text = block.textContent.trim();
          if (block.classList.contains('message-user')) messages.push(`user: ${text}`);
          else if (block.classList.contains('message-bot') && !block.classList.contains('message-error')) {
            if (text && !text.includes('Режим изменён')) messages.push(`bot: ${text}`);
          }
        } 
        else if (block.classList && block.classList.contains('think-message-wrapper')) {
          const contentDiv = block.querySelector('.bot-message-content');
          if (contentDiv) {
            let text = contentDiv.textContent.trim();
            if (text) messages.push(`bot: ${text}`);
          }
        }
      }
      if (excludeLastUser && messages.length > 0 && messages[messages.length-1].startsWith('user:')) {
        messages.pop();
      }
      return messages.join('\\n');
    }
    
    function switchToChatMode() {
      if (hasMessages) return;
      hasMessages = true;
      activeMessagesArea = renderWithMessagesLayout();
      removeGlowEffect();
      updateGlowByState();
      updateModelHeaderVisibility();
    }
    
    function showAuthModal(callback) {
      const modal = document.createElement('div');
      modal.style.position = 'fixed';
      modal.style.top = '0';
      modal.style.left = '0';
      modal.style.width = '100%';
      modal.style.height = '100%';
      modal.style.background = 'rgba(0,0,0,0.8)';
      modal.style.backdropFilter = 'blur(8px)';
      modal.style.zIndex = '2000';
      modal.style.display = 'flex';
      modal.style.alignItems = 'center';
      modal.style.justifyContent = 'center';
      modal.innerHTML = `
        <div style="background: var(--input-bg); border-radius: 28px; max-width: 400px; width: 90%; border: 1px solid #D4AF37; overflow: hidden;">
          <div style="background: linear-gradient(135deg, #1A1F3A, #0B0D14); padding: 20px; text-align: center;">
            <h2 style="color: #D4AF37;">NAI PRO</h2>
            <p style="color: #A8B0D8;">Войдите или зарегистрируйтесь</p>
          </div>
          <div style="padding: 25px;">
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
              <button id="authTabLogin" style="flex:1; padding: 10px; background: rgba(212,175,55,0.2); border: none; border-radius: 30px; color: #D4AF37; cursor: pointer;">Вход</button>
              <button id="authTabReg" style="flex:1; padding: 10px; background: transparent; border: 1px solid var(--border-color); border-radius: 30px; color: var(--text-secondary); cursor: pointer;">Регистрация</button>
            </div>
            <div id="authLoginForm">
              <input type="text" id="loginUsername" placeholder="Логин" style="width:100%; padding: 14px; background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 16px; color: var(--text-primary); margin-bottom: 12px;">
              <input type="password" id="loginPassword" placeholder="Пароль" style="width:100%; padding: 14px; background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 16px; color: var(--text-primary); margin-bottom: 16px;">
              <button id="doLoginBtn" style="width:100%; background: linear-gradient(135deg, #D4AF37, #F5D97B); border: none; padding: 14px; border-radius: 30px; font-weight: bold; color: #1A1F3A; cursor: pointer;">Открыть PRO</button>
            </div>
            <div id="authRegForm" style="display: none;">
              <input type="text" id="regUsername" placeholder="Логин" style="width:100%; padding: 14px; background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 16px; color: var(--text-primary); margin-bottom: 12px;">
              <input type="password" id="regPassword" placeholder="Пароль" style="width:100%; padding: 14px; background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 16px; color: var(--text-primary); margin-bottom: 16px;">
              <button id="doRegBtn" style="width:100%; background: linear-gradient(135deg, #D4AF37, #F5D97B); border: none; padding: 14px; border-radius: 30px; font-weight: bold; color: #1A1F3A; cursor: pointer;">Зарегистрироваться</button>
            </div>
            <div id="authMessage" style="color: #FF8A7A; font-size: 12px; margin-top: 12px; text-align: center;"></div>
            <button id="closeAuthModal" style="width:100%; background: transparent; border: 1px solid var(--border-color); padding: 10px; border-radius: 30px; color: var(--text-secondary); cursor: pointer; margin-top: 12px;">Закрыть</button>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
      
      const loginForm = document.getElementById('authLoginForm');
      const regForm = document.getElementById('authRegForm');
      const tabLogin = document.getElementById('authTabLogin');
      const tabReg = document.getElementById('authTabReg');
      const msgDiv = document.getElementById('authMessage');
      
      tabLogin.addEventListener('click', () => {
        loginForm.style.display = 'block';
        regForm.style.display = 'none';
        tabLogin.style.background = 'rgba(212,175,55,0.2)';
        tabReg.style.background = 'transparent';
        msgDiv.textContent = '';
      });
      tabReg.addEventListener('click', () => {
        loginForm.style.display = 'none';
        regForm.style.display = 'block';
        tabReg.style.background = 'rgba(212,175,55,0.2)';
        tabLogin.style.background = 'transparent';
        msgDiv.textContent = '';
      });
      
      document.getElementById('doLoginBtn').addEventListener('click', async () => {
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value.trim();
        if (!username || !password) { msgDiv.textContent = 'Заполните все поля'; return; }
        try {
          const res = await fetch(REGCHECK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user: username, parol: password })
          });
          if (res.status === 200) {
            proAuth = { username, password, isLoggedIn: true };
            localStorage.setItem('ngix_pro_user', username);
            localStorage.setItem('ngix_pro_pass', password);
            msgDiv.style.color = '#34C759';
            msgDiv.textContent = 'Вход выполнен';
            setTimeout(() => {
              modal.remove();
              updateModelHeaderVisibility();
              if (callback) callback(true);
            }, 800);
          } else {
            const text = await res.text();
            msgDiv.textContent = text;
          }
        } catch(e) { msgDiv.textContent = 'Ошибка соединения'; }
      });
      
      document.getElementById('doRegBtn').addEventListener('click', async () => {
        const username = document.getElementById('regUsername').value.trim();
        const password = document.getElementById('regPassword').value.trim();
        if (!username || !password) { msgDiv.textContent = 'Заполните все поля'; return; }
        try {
          const res = await fetch(REG_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user: username, parol: password })
          });
          if (res.status === 200) {
            msgDiv.style.color = '#34C759';
            msgDiv.textContent = 'Регистрация успешна, теперь войдите';
            setTimeout(() => tabLogin.click(), 1500);
          } else {
            const text = await res.text();
            msgDiv.textContent = text;
          }
        } catch(e) { msgDiv.textContent = 'Ошибка соединения'; }
      });
      
      document.getElementById('closeAuthModal').addEventListener('click', () => {
        modal.remove();
        if (callback) callback(false);
      });
    }
    
    async function sendMessageFromInput() {
      const textarea = document.getElementById('chatInput');
      const sendButton = document.getElementById('sendMessageBtn');
      if (!textarea || !sendButton) return;
      const message = textarea.value.trim();
      if (!message || isGenerating) return;
      
      if (!hasMessages) {
        sendButton.classList.add('fly-effect');
        setTimeout(() => {
          sendButton.classList.remove('fly-effect');
        }, 450);
      }
      
      if (!hasMessages) {
        switchToChatMode();
      }
      
      if (currentMode === 'pro' && !proAuth.isLoggedIn) {
        addMessage(message, 'user');
        textarea.value = '';
        textarea.style.height = 'auto';
        showAuthModal((success) => {
          if (success) {
            sendMessageFromInput();
          } else {
            addMessage('Доступ к PRO режиму требуется авторизация', 'bot', true);
          }
        });
        return;
      }
      
      addMessage(message, 'user');
      textarea.value = '';
      textarea.style.height = 'auto';
      isGenerating = true;
      addTypingIndicator();
      
      try {
        const history = getDialogHistory(true);
        let response;
        
        if (currentMode === 'photo') {
          response = await fetch(PHOTO_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: message })
          });
          removeTypingIndicator();
          if (!response.ok) {
            const errText = await response.text();
            if (errText.includes('К сожалению, мы заподозрили неладное') || errText.includes('доступ к NAI запрещен')) {
              showBlockPage();
              return;
            }
            throw new Error(errText);
          }
          const blob = await response.blob();
          const imgUrl = URL.createObjectURL(blob);
          const imgDiv = document.createElement('div');
          imgDiv.className = 'message-bubble message-bot';
          imgDiv.innerHTML = `Сгенерировано:<br><img src="${imgUrl}" style="max-width:100%; border-radius:12px; margin-top:8px;">`;
          activeMessagesArea.appendChild(imgDiv);
          scrollChatToBottom();
        } 
        else if (currentMode === 'pro') {
          response = await fetch(PRO_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              text: message, 
              api: API_KEY, 
              dialog: history,
              user: proAuth.username,
              parol: proAuth.password,
              model: selectedProModel
            })
          });
          removeTypingIndicator();
          if (!response.ok) {
            const errText = await response.text();
            if (errText.includes('К сожалению, мы заподозрили неладное') || errText.includes('доступ к NAI запрещен')) {
              showBlockPage();
              return;
            }
            if (response.status === 403) {
              proAuth.isLoggedIn = false;
              localStorage.removeItem('ngix_pro_user');
              localStorage.removeItem('ngix_pro_pass');
              addMessage('Произошла ошибка при входе. Возможно, сервер сбросил соединение.', 'bot', true);
              throw new Error('Требуется повторный вход');
            }
            throw new Error(errText);
          }
          const reply = await response.json();
          if (reply.think !== undefined && reply.mes !== undefined) {
            addMessage(reply.mes, 'bot', false, reply.think);
          } else if (typeof reply === 'string') {
            addMessage(reply, 'bot');
          } else {
            addMessage(JSON.stringify(reply), 'bot');
          }
        }
        else if (currentMode === 'math') {
          response = await fetch(MATH_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: message, api: API_KEY, dialog: history })
          });
          removeTypingIndicator();
          if (!response.ok) {
            const errText = await response.text();
            if (errText.includes('К сожалению, мы заподозрили неладное') || errText.includes('доступ к NAI запрещен')) {
              showBlockPage();
              return;
            }
            throw new Error(errText);
          }
          const reply = await response.text();
          addMessage(reply, 'bot');
        }
        else {
          response = await fetch(TEXT_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: message, api: API_KEY, dialog: history })
          });
          removeTypingIndicator();
          if (!response.ok) {
            const errText = await response.text();
            if (errText.includes('К сожалению, мы заподозрили неладное') || errText.includes('доступ к NAI запрещен')) {
              showBlockPage();
              return;
            }
            throw new Error(errText);
          }
          const reply = await response.text();
          addMessage(reply, 'bot');
        }
      } catch(err) {
        removeTypingIndicator();
        if (err.message && (err.message.includes('К сожалению, мы заподозрили неладное') || err.message.includes('доступ к NAI запрещен'))) {
          showBlockPage();
          return;
        }
        addMessage('Ошибка: ' + err.message, 'bot', true);
      } finally {
        isGenerating = false;
        scrollChatToBottom();
        updateModelHeaderVisibility();
      }
    }
    
    function initProModelSelector() {
      const headerBtn = document.getElementById('headerModelBtn');
      const dropdown = document.getElementById('proModelDropdown');
      if (headerBtn && dropdown) {
        headerBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          if (!hasMessages) {
            clearLocalStorageData();
          } else if (currentMode === 'pro' && hasMessages && proAuth.isLoggedIn) {
            dropdown.classList.toggle('active');
          }
        });
        
        document.querySelectorAll('.model-item').forEach(item => {
          item.addEventListener('click', (e) => {
            e.stopPropagation();
            selectedProModel = item.dataset.model;
            updateModelHeaderVisibility();
            dropdown.classList.remove('active');
          });
        });
        
        document.addEventListener('click', () => {
          dropdown.classList.remove('active');
        });
      }
    }
    
    renderNoMessagesLayout();
    updateModeButtonText();
    initProModelSelector();
  })();
</script>
</body>
</html>
'''
    return html, 200
@app.route('/generation', methods=['POST'])
async def fhevoevn():
        global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
        user_agent = request.headers.get('User-Agent', '')
        origin = request.headers.get('Origin', '')
        referer = request.headers.get('Referer', '')
        host = request.headers.get('Host', '')
        accept_lang = request.headers.get('Accept-Language', '')
        sec_fetch_site = request.headers.get('Sec-Fetch-Site', '')
        sec_fetch_mode = request.headers.get('Sec-Fetch-Mode', '')
        x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        
        # Смягчаем проверки для локальной разработки, но оставляем для продакшена
        if host and host != 'nai-chat.onrender.com' and host != '127.0.0.1:10000' and host != 'localhost:10000':
            return 'Forbidden', 403
        if 'python' in user_agent.lower() or 'curl' in user_agent.lower() or 'requests' in user_agent.lower() or 'aiohttp' in user_agent.lower():
            return '403', 403
        if zaponhour > 5999:
          servers = False
          url = ''
        if servers == False:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        client_ip = x_forwarded_for
        client = x_forwarded_for
        if str(client_ip) not in reqts:
          reqts[str(client_ip)] = 0
        ipy = await getip(client_ip)
        if reqts[str(client_ip)] > 10:
          bansipis.append(str(client_ip))
        if str(client_ip) not in servs:
          servs[str(client)] = {'time': 0}
        if ipy == 2:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) in bansipis:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) not in ipis:
          ipis[str(client_ip)] = 0
        if rpts > 15:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        try:
            data = await request.get_json()
            if 'text' in data and 'api' in data and 'dialog' in data:
                if data['api'] == 'jghvhivh65789797T6RJHB':
                    if dayreq >= 11999:
                        return 'Извините, сервер не в состоянии отвечать. Попробуйте позже.', 429
                    else:
                        one = {
                            'Authorization': f'Bearer {os.getenv('API')}',
                            'Content-Type': 'application/json'
                        }
                        two = {
                            'model': 'llama-3.1-8b-instant',
                            'messages': [
                                {
                                    'role': 'system',
                                    'content': 'Отвечай обдуманно, кратко и верно. Не используй символы для выделения текста и так далее. Ваша история диалога: ' + str(data['dialog'])[:2000]
                                },
                                {
                                    'role': 'user',
                                    'content': data['text']
                                }
                            ],
                            'max_tokens': 399,
                            'temperature': 0.7
                        }
                        get = await prmptgrd(data['text'])
                        if get == 1:
                          await asyncio.sleep(random.randint(1, 7))
                          if time.time() - servs[str(client_ip)]['time'] > 1 and 'llama-3.1-8b-instant' not in notam:
                            async with aiohttp.ClientSession() as sess:
                                async with sess.post(url, headers=one, json=two) as pos:
                                    if pos.status == 200:
                                        pos_json = await pos.json()
                                        pos_text = pos_json['choices'][0]['message']['content']
                                        dayreq += 1
                                        rpts += 1
                                        servs[str(client_ip)]['time'] = time.time()
                                        try:
                                          ipis[str(client_ip)] += 1
                                          reqts[str(client_ip)] += 1
                                          zaponhour += 1
                                        except:
                                          pass
                                        return pos_text, 200
                                    else:
                                        notam.append('llama-3.1-8b-instant')
                                        servs[str(client_ip)]['time'] = time.time()
                                        try:
                                          ipis[str(client_ip)] += 1
                                          reqts[str(client_ip)] += 1
                                          zaponhour += 1
                                        except:
                                          pass
                                        return 'Произошла ошибка при генерации. Пожалуйста, подождите чуть-чуть.', 400
                          else:
                            servs[str(client_ip)]['time'] = time.time()
                            try:
                              ipis[str(client_ip)] += 1
                              reqts[str(client_ip)] += 1
                              zaponhour += 1
                            except:
                              pass
                            return 'Произошла ошибка при генерации. Пожалуйста, подождите чуть-чуть.', 400
                        elif get == 2:
                            return 'Простите, но я не буду обрабатывать такой текст.'
                        else:
                            return 'Простите, я не смогла обработать ваш запрос.'
                else:
                    return 'Ошибка обработки вашего запроса.', 400
            else:
                return 'Ошибка обработки вашего запроса.', 400
        except Exception as e:
            print(f"Error: {e}")
            return 'Ошибка обработки вашего запроса.', 400

@app.route('/genphot', methods=['POST'])
async def genph():
        global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam, dayreqgen
        user_agent = request.headers.get('User-Agent', '')
        origin = request.headers.get('Origin', '')
        referer = request.headers.get('Referer', '')
        host = request.headers.get('Host', '')
        accept_lang = request.headers.get('Accept-Language', '')
        sec_fetch_site = request.headers.get('Sec-Fetch-Site', '')
        x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        # Смягчаем проверки для локальной разработки
        if host and host != 'nai-chat.onrender.com' and host != '127.0.0.1:10000' and host != 'localhost:10000':
            return 'forbidden', 403
        if zaponhour > 5999:
          servers = False
          url = ''
        if servers == False:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if 'python' in user_agent.lower() or 'curl' in user_agent.lower() or 'requests' in user_agent.lower():
            return '403', 403
        if rpts > 15:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        client_ip = x_forwarded_for
        client = x_forwarded_for
        if str(client_ip) not in reqts:
          reqts[str(client_ip)] = 0
        ipy = await getip(client_ip)
        if reqts[str(client_ip)] > 10:
          bansipis.append(str(client_ip))
        if str(client_ip) not in servs:
          servs[str(client)] = {'time': 0}
        if ipy == 2:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) in bansipis:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) not in ipis:
          ipis[str(client_ip)] = 0
        try:
            data = await request.get_json()
            
            if dayreqgen >= 189:
                return 'Сервер не в состоянии отвечать. Возможно, квота не генерацию фото исчерпана.', 403
            
            if not data or 'text' not in data:
                return 'Forbidden', 403
            
            one = {
                'X-My-Key': 'm0jSup3rS3cr3tK3rukhfwhirguoerhj0384hfsskdgy2025!',
                'Content-Type': 'application/json'
            }
            two = {
                'prompt': data['text']
            }
            await asyncio.sleep(random.randint(1, 7))
            get = await prmptgrd(data['text'])
            if get == 1:
              if 'llama-3.1-8b-instant' not in notam:
                if time.time() - servs[str(client_ip)]['time'] > 1:
                  async with aiohttp.ClientSession() as sess:
                      async with sess.post('https://image-gen.uttgu-901.workers.dev/', headers=one, json=two, timeout=60) as pos1t:
                          if pos1t.status == 200:
                              image_bytes = await pos1t.read()
                              dayreqgen += 1
                              rpts += 1
                              servs[str(client_ip)]['time'] = time.time()
                              try:
                                ipis[str(client_ip)] += 1
                                reqts[str(client_ip)] += 1
                                zaponhour += 1
                              except:
                                pass
                              return image_bytes, 200, {'Content-Type': 'image/png'}
                          else:
                              error_text = await pos1t.text()
                              servs[str(client_ip)]['time'] = time.time()
                              print(f"Photo API error: {pos1t.status} - {error_text}")
                              try:
                                ipis[str(client_ip)] += 1
                                reqts[str(client_ip)] += 1
                                zaponhour += 1
                              except:
                                pass
                              return 'Простите, произошла ошибка при генерации.', 400
                else:
                  servs[str(client_ip)]['time'] = time.time()
                  try:
                    ipis[str(client_ip)] += 1
                    reqts[str(client_ip)] += 1
                    zaponhour += 1
                  except:
                    pass
                  return 'Ошибка при генерации.', 400
              else:
                return 'Модель временно недоступна. Попробуйте повторить генерацию через минуту.', 400
            elif get == 2:
                return 'Простите, но я не буду обрабатывать такой текст.'
            else:
                return 'Простите, я не смогла обработать ваш запрос.'
        except asyncio.TimeoutError:
            return 'Таймаут генерации фото', 504
        except Exception as e:
            print(f"Genphot error: {e}")
            return '403', 403


@app.route('/math', methods=['POST'])
async def match():
        global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam
        user_agent = request.headers.get('User-Agent', '')
        origin = request.headers.get('Origin', '')
        referer = request.headers.get('Referer', '')
        host = request.headers.get('Host', '')
        accept_lang = request.headers.get('Accept-Language', '')
        sec_fetch_site = request.headers.get('Sec-Fetch-Site', '')
        x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        client_ip = x_forwarded_for
        client = x_forwarded_for
        if zaponhour > 5999:
          servers = False
          url = ''
        if str(client_ip) not in reqts:
          reqts[str(client_ip)] = 0
        if str(client_ip) not in servs:
          servs[str(client_ip)] = {'time': 0}
        ipy = await getip(client_ip)
        if reqts[str(client_ip)] > 10:
          bansipis.append(str(client_ip))
        if servers == False:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if ipy == 2:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        # Смягчаем проверки для локальной разработки
        if host and host != 'nai-chat.onrender.com':
            return 'forbidden', 403
        if 'python' in user_agent.lower() or 'curl' in user_agent.lower() or 'requests' in user_agent.lower():
            return '403', 403
        if rpts > 15:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) in bansipis:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) not in ipis:
          ipis[str(client_ip)] = 0
        try:
            data = await request.get_json()
            if 'text' in data and 'api' in data and 'dialog' in data:
                if data['api'] == 'jghvhivh65789797T6RJHB':
                    if dayreq >= 9999:
                        return 'Извините, сервер не в состоянии отвечать. Попробуйте позже.', 429
                    else:
                        one = {
                            'Authorization': f'Bearer {os.getenv('API')}',
                            'Content-Type': 'application/json'
                        }
                        two = {
                            'model': 'llama-3.1-8b-instant',
                            'messages': [
                                {
                                    'role': 'system',
                                    'content': 'Ты очень хорошо понимаешь математику. Решай математические задачи идеально и кратко. Не добавляй и не выделяй текст спец символами типа * ** и так далее. История ' + str(data['dialog'])[:3000]
                                },
                                {
                                    'role': 'user',
                                    'content': data['text']
                                }
                            ],
                            'max_tokens': 349,
                            'temperature': 0.7
                        }
                        get = await prmptgrd(data['text'])
                        if get == 1:
                          if 'llama-3.1-8b-instant' not in notam:
                            await asyncio.sleep(random.randint(1, 7))
                            if time.time() - servs[str(client_ip)]['time'] > 1:
                              async with aiohttp.ClientSession() as sess:
                                  async with sess.post(url, headers=one, json=two) as pos:
                                      if pos.status == 200:
                                          pos_json = await pos.json()
                                          pos_text = pos_json['choices'][0]['message']['content']
                                          dayreq += 1
                                          rpts += 1
                                          servs[str(client_ip)]['time'] = time.time()
                                          try:
                                            ipis[str(client_ip)] += 1
                                            reqts[str(client_ip)] += 1
                                            zaponhour += 1
                                          except:
                                            pass
                                          return pos_text, 200
                                      else:
                                          notam.append('llama-3.1-8b-instant')
                                          servs[str(client_ip)]['time'] = time.time()
                                          try:
                                            ipis[str(client_ip)] += 1
                                            reqts[str(client_ip)] += 1
                                            zaponhour += 1
                                          except:
                                            pass
                                          return 'Произошла ошибка при генерации. Пожалуйста, подождите чуть-чуть.', 400
                            else:
                              servs[str(client_ip)]['time'] = time.time()
                              try:
                                ipis[str(client_ip)] += 1
                                reqts[str(client_ip)] += 1
                                zaponhour += 1
                              except:
                                pass
                              return 'Ошибка при генерации.', 400
                          else:
                            return 'Модель временно недоступна. Попробуйте повторить генерацию через минуту.', 400
                        elif get == 2:
                            return 'Простите, но я не буду обрабатывать такой текст.'
                        else:
                            return 'Простите, я не смогла обработать ваш запрос.'
                else:
                    return 'Ошибка обработки вашего запроса.', 400
            else:
                return 'Ошибка обработки вашего запроса.', 400
        except Exception as e:
            print(f"Error: {e}")
            return 'Ошибка обработки вашего запроса.', 400

@app.route('/profi', methods=['POST'])
async def profi():
        global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, url, notam, proreq, lastlstmgen, lstmgen, potoks
        user_agent = request.headers.get('User-Agent', '')
        origin = request.headers.get('Origin', '')
        referer = request.headers.get('Referer', '')
        host = request.headers.get('Host', '')
        accept_lang = request.headers.get('Accept-Language', '')
        sec_fetch_site = request.headers.get('Sec-Fetch-Site', '')
        x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        client_ip = x_forwarded_for
        client = x_forwarded_for
        if zaponhour > 5999:
          servers = False 
          url = ''
        if servers == False:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) not in reqts:
          reqts[str(client_ip)] = 0
        if str(client_ip) not in servs:
          servs[str(client_ip)] = {'time': 0}
        ipy = await getip(client_ip)
        if reqts[str(client_ip)] > 10:
          bansipis.append(str(client_ip))
        if ipy == 2:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        # Смягчаем проверки для локальной разработки
        if host and host != 'nai-chat.onrender.com':
            return 'forbidden', 403
        if 'python' in user_agent.lower() or 'curl' in user_agent.lower() or 'requests' in user_agent.lower():
            return '403', 403
        if rpts >  15:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) in bansipis:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
        if str(client_ip) not in ipis:
          ipis[str(client_ip)] = 0
        try:
            data = await request.get_json()
            if 'text' in data and 'api' in data and 'dialog' in data and 'user' in data and 'parol' in data and 'model' in data:
                if data['user'] in users:
                    if users[data['user']]['parol'] == data['parol']:
                        if data['api'] == 'jghvhivh65789797T6RJHB':
                            if proreq >= 3999:
                                return 'Извините, сервер не в состоянии отвечать. Возможно, квота на PRO исчерпана до завтра. Попробуйте позже.', 429
                            else:
                                model = ''
                                if data['model'] == 'ChatGPT-20B':
                                  model = 'openai/gpt-oss-20b'
                                elif data['model'] == 'ChatGPT-120B':
                                  model = 'openai/gpt-oss-120b'
                                elif data['model'] == 'LLaMA 3.3 70b':
                                  model = 'llama-3.3-70b-versatile'
                                elif data['model'] == 'Qwen-3 32B':
                                  model = 'qwen/qwen3-32b'
                                elif data['model'] == 'MagicText-1.2 1M':
                                  model = 'RadmirRyan/MagicText-1.2'
                                elif data['model'] == 'LLaMA-3.1 8B':
                                  model = 'llama-3.1-8b-instant'
                                elif data['model'] == 'LLaMA-4 Scout':
                                  model = 'meta-llama/llama-4-scout-17b-16e-instruct'
                                else:
                                  model = 'llama-3.1-8b-instant'
                                one = {
                                    'Authorization': f'Bearer {os.getenv('API')}',
                                    'Content-Type': 'application/json'
                                }
                                two = {
                                    'model': model,
                                    'messages': [
                                        {
                                            'role': 'system',
                                            'content': 'Отвечай качественно и кратко. Не добавляй и не выделяй текст спец символами типа * ** и так далее. История ' + str(data['dialog'])[:4000]
                                        },
                                        {
                                            'role': 'user',
                                            'content': data['text']
                                        }
                                    ],
                                    'max_tokens': 599,
                                    'temperature': 0.7
                                }
                                get = await prmptgrd(data['text'])
                                if get == 1:
                                  if model == 'RadmirRyan/MagicText-1.2':
                                    if time.time() - servs[str(client_ip)]['time'] > 2:
                                      if time.time() - lastlstmgen < 5:
                                        return 'Простите. Лимиты для модели MagicText исчерпаны в течении пяти секунд.', 400
                                      if lstmgen > 99:
                                        return 'Лимиты для модели MagicText исчерпаны до завтра. Используйте наши другие модели - https://nai-chat.onrender.com/models', 400
                                      if potoks >= 4:
                                        return 'Простите, но общее число потоков (4) не позволяет запустить генерацию для модели MagicText. Подождите, пока поток освободится.', 400
                                      try:
                                        potoks += 1
                                        try:
                                          text = await asyncio.to_thread(generation, data['text'])
                                        except:
                                          potoks -= 1
                                          return 'Произошла ошибка при генерации. Повторите попытку позже.', 400
                                        post_text = {
                                          'think': 'Данная модель помечена знаком (❗) в связи с низким качеством генерации. Пожалуйста, проверяйте качество текста перед тем, как слушать ее совет. Подробнее о моделях - https://nai-chat.onrender.com/models',
                                          'mes': text
                                        }
                                        lstmgen += 1
                                        lastlstmgen = time.time()
                                        potoks -= 1
                                        return post_text, 200
                                      except:
                                        return 'Произошла ошибка при генерации.', 400
                                    else:
                                      return 'Простите, но для MagicText действуют ограничения. Попробуйте через две секунды.', 400

                                  if model not in notam:
                                    await asyncio.sleep(random.randint(1, 3))
                                    if time.time() - servs[str(client_ip)]['time'] > 1 and model not in notam:
                                      async with aiohttp.ClientSession() as sess:
                                          async with sess.post(url, headers=one, json=two) as pos:
                                              if pos.status == 200:
                                                  pos_json = await pos.json()
                                                  pos_text = pos_json['choices'][0]['message']['content']
                                                  proreq += 1
                                                  servs[str(client_ip)]['time'] = time.time()
                                                  rpts += 1
                                                  try:
                                                    ipis[str(client_ip)] += 1
                                                    zaponhour += 1
                                                    reqts[str(client_ip)] += 1
                                                  except:
                                                    pass
                                                  if model == 'qwen/qwen3-32b':
                                                      pos_text = pos_text.split('</think>')
                                                      pos_t1 = pos_text[0].replace('<think>', '').strip()
                                                      pos_t2 = pos_text[1].strip()
                                                      post_text = {
                                                        'think': pos_t1,
                                                        'mes': pos_t2
                                                      }
                                                  else:
                                                      post_text = {
                                                        'think': 'Простите, данная модель не поддерживает рассуждение. Использйте Qwen-3 32B в каталоге моделей. Подробнее о моделях - https://nai-chat.onrender.com/models',
                                                        'mes': pos_text
                                                      }
                                                  return post_text, 200
                                              else:
                                                  notam.append(model)
                                                  servs[str(client_ip)]['time'] = time.time()
                                                  try:
                                                    ipis[str(client_ip)] += 1
                                                    reqts[str(client_ip)] += 1
                                                    zaponhour += 1
                                                  except:
                                                    pass
                                                  return 'Произошла ошибка при генерации. Пожалуйста, подождите чуть-чуть.', 400
                                    else:
                                      servs[str(client_ip)]['time'] = time.time()
                                      try:
                                        ipis[str(client_ip)] += 1
                                        reqts[str(client_ip)] += 1
                                        zaponhour += 1
                                      except:
                                        pass
                                      return'Простите, произошла ошибка при генерации.', 400                                  
                                  else:
                                    return 'Модель временно недоступна. Попробуйте повторить генерацию через минуту.', 400
                                elif get == 2:
                                    return 'Простите, но я не буду обрабатывать такой текст.'
                                else:
                                    return 'Простите, я не смогла обработать ваш запрос.'
                        else:
                            return 'Ошибка обработки вашего запроса. 101', 400
                    else:
                        return 'Ошибка обработки вашего запроса. 102', 400
                else:
                    return 'Ошибка обработки вашего запроса. 103', 400
            else:
                return 'Ошибка обработки вашего запроса. 104', 400
        except Exception as e:
            print(f"Error: {e}")
            return 'Ошибка обработки вашего запроса. 105', 400
@app.route('/reg', methods=['POST'])
async def profujyfi():
    global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, notam, url
    x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    client = x_forwarded_for
    if str(client) not in servs:
      servs[str(client)] = {'time': 0}
    servs[str(client)]['time'] = time.time()
    if str(client) not in reqts:
      reqts[str(client)] = 0
    ipy = await getip(client)
    if ipy == 2:
      return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
    if str(client) not in ipis:
        ipis[str(client)] = 0
    try:
        ipis[str(client)] += 1
        reqts[str(client)] += 1
    except:
        pass
    if str(client) in bansipis:
          return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
    try:
        data = await request.get_json()
        if 'user' in data and 'parol' in data:
            if data['user'] not in users:
                users[data['user']] = {
                    'parol': data['parol']
                }
                return 'Успешная регистрация. Теперь войдите.'
            else:
                return 'Такой пользователь уже существует. Введите пароль, если это вы.', 403
        else:
            return 'Ошибка обработки запроса.', 400
    except Exception as e:
        print(e)
        return 'Ошибка обработки запроса.', 400

@app.route('/regcheck', methods=['POST'])
async def profujyfiesth():
    global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, notam, url
    x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    client = x_forwarded_for
    if str(client) not in reqts:
      reqts[str(client)] = 0
    if str(client) not in servs:
      servs[str(client)] = {'time': 0}
    servs[str(client)]['time'] = time.time()
    ipy = await getip(client)
    if ipy == 2:
        return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
    if str(client) not in ipis:
        ipis[str(client)] = 0
    try:
        ipis[str(client)] += 1
        reqts[str(client)] += 1
    except:
        pass
    if str(client) in bansipis:
        return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
    try:
        data = await request.get_json()
        if 'user' in data and 'parol' in data:
            if data['user'] not in users:
                return 'Такого пользователя нет.', 404
            else:
                if users[data['user']]['parol'] == data['parol']:
                    return 'Успешный вход!', 200
                else:
                    return 'Не верный пароль.', 403
        else:
            return 'Ошибка обработки запроса.', 400
    except Exception as e:
        print(e)
        return 'Ошибка обработки запроса.', 400
@app.route('/limit')
async def limits():
    global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, notam, url
    x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    client = x_forwarded_for
    if str(client) not in servs:
      servs[str(client)] = {'time': 0}
    servs[str(client)]['time'] = time.time()
    if str(client) not in ipis:
        ipis[str(client)] = 0
    try:
        ipis[str(client)] += 1
    except:
        pass
    if str(client) in bansipis:
        return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
    return f'Chat-not-pro {dayreq}, generation-photo {dayreqgen}, pro mode {proreq}', 200
@app.route('/health')
async def kuhu():
    global dayreq, rpts, zaponhour, servers, bansipis, reqts, ipis, servs, notam, url
    x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    client = x_forwarded_for
    if str(client) not in servs:
      servs[str(client)] = {'time': 0}
    servs[str(client)]['time'] = time.time()
    if str(client) not in ipis:
        ipis[str(client)] = 0
    try:
        ipis[str(client)] += 1
    except:
        pass
    if str(client) in bansipis:
        return 'К сожалению, мы заподозрили неладное. Ваш доступ к NAI запрещен до завтра.', 403
    return '', 200

if __name__ == '__main__':
    async def main():
        asyncio.create_task(nolim())
        asyncio.create_task(ping_server())
        asyncio.create_task(rptd())
        asyncio.create_task(modelscheck())
        asyncio.create_task(ipischeck())
        asyncio.create_task(rptsts())
        asyncio.create_task(hour())
        asyncio.create_task(ddosanti())
        asyncio.create_task(hoii())
        await app.run_task(host='0.0.0.0', port=10000)
    asyncio.run(main())
