import requests
import os
from random import choice
from langdetect import detect
from deep_translator import GoogleTranslator
import spacy
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
GOOGLE_CX = os.getenv("GOOGLE_CX")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

nlp = spacy.load("pt_core_news_sm")

cache = TTLCache(maxsize=100, ttl=3600)

contexto = []

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

def extrair_palavras_chave(texto):
    doc = nlp(texto)
    return [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"] and not token.is_stop]

def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return "en"

def traduzir(texto, origem="auto", destino="pt"):
    try:
        return GoogleTranslator(source=origem, target=destino).translate(texto)
    except:
        return texto

def pesquisar_wolfram(pergunta_en, app_id):
    url = f"http://api.wolframalpha.com/v1/result?i={requests.utils.quote(pergunta_en)}&appid={app_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return ""
    except:
        return ""

def pesquisar_google(pergunta_en, cx, api_key):
    url = f"https://www.googleapis.com/customsearch/v1?q={pergunta_en}&cx={cx}&key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            return data["items"][0]["snippet"]
        return ""
    except:
        return ""

def pesquisar_duckduckgo(pergunta_en):
    url = f"https://api.duckduckgo.com/?q={pergunta_en}&format=json&no_redirect=1&skip_disambig=1"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics"):
            for item in data["RelatedTopics"]:
                if isinstance(item, dict) and "Text" in item:
                    return item["Text"]
        return ""
    except:
        return ""

def pesquisar_wikipedia(pergunta_en):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{pergunta_en.replace(' ', '_')}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "")
        return ""
    except:
        return ""

def resposta_util(resposta, minimo=50):
    if not resposta:
        return False
    palavras = extrair_palavras_chave(resposta)
    return len(resposta.strip()) >= minimo and len(palavras) >= 1

intencoes = {
    "saudacao": ["oi", "olá", "e ai", "bom dia", "boa noite", "boa tarde", "eae", "hello"],
    "status": ["tudo bem", "como você está", "como está"],
    "nome": ["qual seu nome", "como se chama", "quem é você"],
    "funcao": ["o que você faz", "para que serve", "qual sua função"],
    "despedida": ["tchau", "adeus", "até logo", "sair"]
}

respostas = {
    "saudacao": ["Oi! Tudo certo por aí?", "Olá, como posso ajudar hoje?", "E aí, pronto para conversar?"],
    "status": ["Estou de boa, e você?", "Tudo ótimo por aqui! Como posso ajudar?"],
    "nome": ["Sou um bot simples, criado por um dev curioso!", "Não tenho um nome chique, só me chama de Bot!"],
    "funcao": ["Eu respondo perguntas, busco curiosidades e converso sobre quase tudo!"],
    "despedida": ["Tchau! Até a próxima!", "Valeu, até logo!"],
    "desconhecida": ["Ops, não sei responder isso ainda. Tenta outra pergunta?", "Hmm, essa é nova pra mim!"]
}

def take_intencao(mensagem):
    mensagem_limpa = normalizar_texto(mensagem)
    vectorizer = TfidfVectorizer()
    max_sim = 0
    intencao = "conhecimento"

    for key, exemplos in intencoes.items():
        textos = exemplos + [mensagem_limpa]
        tfidf_matrix = vectorizer.fit_transform(textos)
        sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).max()
        if sim > max_sim and sim > 0.5:
            max_sim = sim
            intencao = key

    return intencao

def responder(intencao, mensagem):
    global contexto
    mensagem_limpa = normalizar_texto(mensagem)

    contexto.append({"pergunta": mensagem_limpa, "intencao": intencao})
    if len(contexto) > 5:
        contexto.pop(0)

    if intencao == "conhecimento":
        if mensagem_limpa in cache:
            return cache[mensagem_limpa]

        palavras_chave = extrair_palavras_chave(mensagem)
        pergunta_refinada = " ".join(palavras_chave) if palavras_chave else mensagem
        idioma = detectar_idioma(mensagem)

        pergunta_en = pergunta_refinada if idioma == "en" else traduzir(pergunta_refinada, origem=idioma, destino="en")

        fontes = [
            lambda: pesquisar_wolfram(pergunta_en, WOLFRAM_APP_ID),
            lambda: pesquisar_google(pergunta_en, GOOGLE_CX, GOOGLE_API_KEY),
            lambda: pesquisar_duckduckgo(pergunta_en),
            lambda: pesquisar_wikipedia(pergunta_en)
        ]

        resposta_en = ""
        for fonte in fontes:
            tentativa = fonte()
            if resposta_util(tentativa):
                resposta_en = tentativa
                break

        if resposta_en:
            resposta = resposta_en if idioma == "en" else traduzir(resposta_en, origem="en", destino="pt")
        else:
            resposta = choice(respostas["desconhecida"])

        cache[mensagem_limpa] = resposta
        return resposta
    else:
        return choice(respostas[intencao])

def validar_entrada(mensagem):
    if len(mensagem) > 500:
        return False, "Mensagem muito longa! Tente algo mais curto."
    if not any(c.isalnum() for c in mensagem):
        return False, "Por favor, envie uma mensagem válida."
    return True, ""