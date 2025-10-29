import re

# 1.1. Negasyon (Olumsuzluk) Listesi
# En sık kullanılan olumsuzluk kelimeleri ve ekleri
NEGATORS = ['deyil', 'yox', 'yoxdur', 'değil', 'olmasın', 'bilmirəm', 'əsla', 'heç'] 

# 1.2. Emoji Haritası (Duyguya göre basitleştirilmiş)
# Emojilerin anlamlı metin karşılıklarına dönüştürülmesi
EMOJI_MAP = {
    '😊': ' EMO_POS ', '😀': ' EMO_POS ', '😃': ' EMO_POS ', '😂': ' EMO_POS ',
    '😍': ' EMO_LOVE ', '😘': ' EMO_LOVE ', '🥰': ' EMO_LOVE ',
    '🙁': ' EMO_NEG ', '😥': ' EMO_NEG ', '😞': ' EMO_NEG ', '😭': ' EMO_NEG ',
    '😡': ' EMO_NEG ', '😠': ' EMO_NEG ', '👎': ' EMO_NEG ',
    '🤔': ' EMO_NEU ', '🤷‍♀️': ' EMO_NEU ', '🤦‍♀️': ' EMO_NEU ' 
    # Not: Gerçek projede bu liste çok daha geniş olmalıdır.
}

# 1.4. Deasciify (Slang Düzeltme) Haritası
# Azerbaycanca sosyal medya hataları için (çox, yaxşı gibi karakterler)
SLANG_MAP = {
    r'\bcox\b': 'çox', 
    r'\byaxsi\b': 'yaxşı', 
    r'\bcunki\b': 'çünki',
    r'\bele\b': 'belə',
    r'\bgulle\b': 'güllə',
    r'\bolkeler\b': 'ölkələr',
    r'\boz\b': 'öz'
}

def handle_negation(text):
    """Olumsuzluk kelimesinden (deyil, yox vb.) sonraki 3 kelimeyi _NEG etiketiyle işaretler."""
    tokens = text.split()
    new_tokens = []
    negate_until = -1 # Olumsuzlama etkisinin biteceği kelime indeksi

    for i, token in enumerate(tokens):
        # 1. Olumsuzluk kelimesi mi?
        if token in NEGATORS:
            new_tokens.append(token)
            # Etiketlemeyi kendisinden sonraki 3 kelime için yap
            negate_until = i + 3
        # 2. Olumsuzluk etkisi devam ediyor mu?
        elif i < negate_until:
            # Token eğer bir etiket değilse (örn. <PRICE> veya EMO_POS) etiketle
            if not re.match(r'<.*?>|EMO_.*?', token):
                 new_tokens.append(token + "_NEG")
            else:
                 new_tokens.append(token) # Etiketleri bozmamak için
        # 3. Normal kelime
        else:
            new_tokens.append(token)

    return " ".join(new_tokens)

def map_emojis_and_normalize(text):
    """Metindeki emojileri EMOJI_MAP'e göre metin etiketlerine dönüştürür."""
    for emo, replacement in EMOJI_MAP.items():
        text = text.replace(emo, replacement)
    return text

def split_hashtags(text):
    """Hashtag'lerdeki CamelCase yapısını ayırır (#QarabagIsBack -> Qarabag Is Back)."""
    
    # 1. # işaretini kaldır
    text = re.sub(r'#', '', text) 
    
    # 2. Bir küçük harf, ardından bir büyük harf gelirse araya boşluk ekle
    # Örneğin: 'GozelAzerbaycan' -> 'Gozel Azerbaycan'
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Not: Kişi 1 bu çıktıyı lower_az'a beslemelidir.
    return text

def deasciify_slang(text):
    """Yaygın Azerbaycan sosyal medya kısaltmalarını/hatalarını düzeltir (Deasciify)."""
    for pattern, replacement in SLANG_MAP.items():
        # \b tam kelime sınırını kontrol eder (örn: 'boxca' kelimesini etkilemeden 'cox' kelimesini değiştirir)
        text = re.sub(pattern, replacement, text)
    return text

def detect_domain(text):
    """Metnin türünü (news, social, reviews, general) kural tabanlı tespit eder."""
    text_lower = text.lower()
    
    # Kural 1: Social Media (Çok sayıda hashtag, kullanıcı adı, slang)
    if text_lower.count('#') > 1 or text_lower.count('@') > 1 or 'həhəhə' in text_lower or 'lol' in text_lower:
        return 'social'
    
    # Kural 2: Reviews (Fiyat, puan, hizmet/ürün kelimeleri)
    elif any(keyword in text_lower for keyword in ['fiyat', 'qiymət', 'ulduz', 'star', 'hizmet', 'xidmət', 'kargo', 'teslimat']):
        return 'reviews'
        
    # Kural 3: News (Resmiyet belirten kelimeler)
    elif any(keyword in text_lower for keyword in ['rəsmi', 'açıqlama', 'başkan', 'nazir', 'ölkə', 'parlament']):
        return 'news'
    
    # Diğerleri
    else:
        return 'general'

def add_domain_tag(text, domain):
    """Corpus için metnin başına domain etiketini ekler (Örn: DOM_NEWS Bu haber...)."""
    return f"DOM_{domain.upper()} {text}"

def domain_specific_normalize(text, domain):
    """Sadece Reviews domain'i için fiyat ve yıldız/puanları etiketler."""
    if domain == 'reviews':
        # 1. Fiyat etiketleme (Örn: 100 manat, 50TL, 25$) -> <PRICE>
        # (Sayılar, ardından boşluklar ve para birimleri)
        text = re.sub(r'\d+[\s\.]*(manat|azn|tl|usd|\$|€)', '<PRICE>', text, flags=re.IGNORECASE)
        
        # 2. Yüksek Puan Etiketleme (4, 5, Mükemmel) -> <STARS_HIGH>
        # 5/5, 4/5, 5 ulduz, 4 yıldız vb.
        text = re.sub(r'([4-5]\s*/\s*5)|([4-5]\s*ulduz)|([4-5]\s*yıldız)|mükəmməl|əla', '<STARS_HIGH>', text, flags=re.IGNORECASE)
        
        # 3. Düşük Puan Etiketleme (1, 2) -> <STARS_LOW>
        # 1/5, 2/5, 1 ulduz, 2 yıldız vb.
        text = re.sub(r'([1-2]\s*/\s*5)|([1-2]\s*ulduz)|([1-2]\s*yıldız)|kötü|pis', '<STARS_LOW>', text, flags=re.IGNORECASE)

    return text