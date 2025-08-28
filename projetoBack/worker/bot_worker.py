import logging
import requests
import time
from random import choice
from langdetect import detect
from deep_translator import GoogleTranslator
import spacy
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from cachetools import TTLCache
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nlp = spacy.load("pt_core_news_sm")

cache = TTLCache(maxsize=100, ttl=3600)

contexto = []

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

class BotWorker:
    def __init__(self):
        self.wolfram_app_id = Config.WOLFRAM_APP_ID
        self.google_cx = Config.GOOGLE_CX
        self.google_api_key = Config.GOOGLE_API_KEY
        if not all([self.wolfram_app_id, self.google_cx, self.google_api_key]):
            logger.warning("Algumas chaves de API não estão configuradas")
        logger.info("BotWorker inicializado com sucesso.")

    def process_query(self, query: str, usuario_id: int = None) -> dict:
        start_time = time.time()
        try:
            logger.info(f"Processando query: {query} (usuario_id: {usuario_id})")
            valid, message = self._validate_input(query)
            if not valid:
                return {"status": "error", "query": query, "message": message, "usuario_id": usuario_id}

            response, source = self._get_bot_response(query)
            processing_time = time.time() - start_time
            return {
                "status": "success",
                "query": query,
                "response": response,
                "source": source,
                "usuario_id": usuario_id,
                "processing_time": round(processing_time, 3)
            }
        except Exception as e:
            logger.error(f"Erro ao processar query: {str(e)}")
            return {
                "status": "error",
                "query": query,
                "message": f"Erro interno: {str(e)}",
                "usuario_id": usuario_id,
                "processing_time": round(time.time() - start_time, 3)
            }

    def _validate_input(self, mensagem: str) -> tuple:
        if len(mensagem) > 500:
            return False, "Mensagem muito longa! Tente algo mais curto."
        if not any(c.isalnum() for c in mensagem):
            return False, "Por favor, envie uma mensagem válida."
        return True, ""

    def _normalizar_texto(self, texto: str) -> str:
        texto = texto.lower()
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
        return texto

    def _extrair_palavras_chave(self, texto: str) -> list:
        doc = nlp(texto)
        return [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"] and not token.is_stop]

    def _detectar_idioma(self, texto: str) -> str:
        try:
            return detect(texto)
        except:
            return "en"

    def _traduzir(self, texto: str, origem: str = "auto", destino: str = "pt") -> str:
        try:
            return GoogleTranslator(source=origem, target=destino).translate(texto)
        except Exception as e:
            logger.error(f"Erro ao traduzir: {str(e)}")
            return texto

    def _pesquisar_wolfram(self, pergunta_en: str) -> str:
        if not self.wolfram_app_id:
            return ""
        url = f"http://api.wolframalpha.com/v1/result?i={requests.utils.quote(pergunta_en)}&appid={self.wolfram_app_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info(f"Resposta do Wolfram Alpha obtida para: {pergunta_en}")
                return response.text
            return ""
        except Exception as e:
            logger.error(f"Erro na busca do Wolfram Alpha: {str(e)}")
            return ""

    def _pesquisar_google(self, pergunta_en: str) -> str:
        if not (self.google_cx and self.google_api_key):
            return ""
        url = f"https://www.googleapis.com/customsearch/v1?q={pergunta_en}&cx={self.google_cx}&key={self.google_api_key}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if "items" in data:
                logger.info(f"Resposta do Google obtida para: {pergunta_en}")
                return data["items"][0]["snippet"]
            return ""
        except Exception as e:
            logger.error(f"Erro na busca do Google: {str(e)}")
            return ""

    def _pesquisar_duckduckgo(self, pergunta_en: str) -> str:
        url = f"https://api.duckduckgo.com/?q={pergunta_en}&format=json&no_redirect=1&skip_disambig=1"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get("AbstractText"):
                logger.info(f"Resposta do DuckDuckGo obtida para: {pergunta_en}")
                return data["AbstractText"]
            elif data.get("RelatedTopics"):
                for item in data["RelatedTopics"]:
                    if isinstance(item, dict) and "Text" in item:
                        return item["Text"]
            return ""
        except Exception as e:
            logger.error(f"Erro na busca do DuckDuckGo: {str(e)}")
            return ""

    def _pesquisar_wikipedia(self, pergunta_en: str) -> str:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{pergunta_en.replace(' ', '_')}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Resposta da Wikipédia obtida para: {pergunta_en}")
                return data.get("extract", "")
            return ""
        except Exception as e:
            logger.error(f"Erro na busca da Wikipédia: {str(e)}")
            return ""

    def _resposta_util(self, resposta: str, minimo: int = 50) -> bool:
        if not resposta:
            return False
        palavras = self._extrair_palavras_chave(resposta)
        return len(resposta.strip()) >= minimo and len(palavras) >= 1

    def _take_intencao(self, mensagem: str) -> str:
        mensagem_limpa = self._normalizar_texto(mensagem)
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

    def _responder(self, intencao: str, mensagem: str) -> tuple:
        global contexto
        mensagem_limpa = self._normalizar_texto(mensagem)

        contexto.append({"pergunta": mensagem_limpa, "intencao": intencao})
        if len(contexto) > 5:
            contexto.pop(0)

        if intencao == "conhecimento":
            if mensagem_limpa in cache:
                logger.info(f"Resposta obtida do cache para: {mensagem_limpa}")
                return cache[mensagem_limpa], "cache"

            palavras_chave = self._extrair_palavras_chave(mensagem)
            pergunta_refinada = " ".join(palavras_chave) if palavras_chave else mensagem
            idioma = self._detectar_idioma(mensagem)

            pergunta_en = pergunta_refinada if idioma == "en" else self._traduzir(pergunta_refinada, origem=idioma, destino="pt")

            fontes = [
                (self._pesquisar_wolfram, "wolfram"),
                (self._pesquisar_google, "google"),
                (self._pesquisar_duckduckgo, "duckduckgo"),
                (self._pesquisar_wikipedia, "wikipedia")
            ]

            resposta_en = ""
            fonte_usada = ""
            for fonte, nome in fontes:
                tentativa = fonte(pergunta_en)
                if self._resposta_util(tentativa):
                    resposta_en = tentativa
                    fonte_usada = nome
                    break

            if resposta_en:
                resposta = resposta_en if idioma == "en" else self._traduzir(resposta_en, origem="en", destino="pt")
            else:
                resposta = choice(respostas["desconhecida"])
                fonte_usada = "nenhuma"

            cache[mensagem_limpa] = resposta
            return resposta, fonte_usada
        else:
            return choice(respostas[intencao]), intencao

    def _get_bot_response(self, pergunta: str) -> tuple:
        try:
            intencao = self._take_intencao(pergunta)
            resposta, fonte = self._responder(intencao, pergunta)
            if resposta and resposta.strip():
                return resposta, fonte
            return choice(respostas["desconhecida"]), "nenhuma"
        except Exception as e:
            logger.error(f"Erro ao obter resposta do bot: {str(e)}")
            return "Ocorreu um erro ao processar sua pergunta.", "nenhuma"