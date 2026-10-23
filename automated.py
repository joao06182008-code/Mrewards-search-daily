import pyautogui as pag
import random
import time
 
pag.FAILSAFE = True  # mover o mouse para o canto superior esquerdo aborta o script
 
# ---------- CONFIGURAsAO ----------  #
TESTE = True             
PAUSA_PESQUISA = (1, 2) if TESTE == True else (13, 18)        # pausa entre pesquisas, em segundos (min, max)
QTD_PESQUISAS = 10                # quantas pesquisas fazer por rodada (se quiser aumentar se for gold/prata)
ARQUIVO_CARD = 'commone.png'     # recorte que se repete nos 3 cards pendentes
CONFIANCA = 0.8                   # aumenta pra 0.9 se o script clicar errado
ROLAGENS = 1                      # quantos "pagedown" ate os cards aparecerem
 
TERMOS = [
    "lionel messi", "neymar jr", "cristiano ronaldo", "kylian mbappe",
    "robert lewandowski", "mohamed salah", "virgil van dijk", "harry kane",
    "kevin de bruyne", "erling haaland", "vinicius junior", "rodrygo",      #pode colocar qualquer termo aqui
    "luka modric", "jude bellingham", "lamine yamal", "pedri",
    "bruno fernandes", "son heung-min", "thibaut courtois", "alisson becker",
]
 
 
def pesquisar(termo):
    pag.hotkey('ctrl', 'e')               # foca a barra de enderecos e seleciona tudo
    pag.write(termo, interval=0.05)       # o texto digitado substitui o que estava la
    pag.press('enter')
    time.sleep(random.uniform(*PAUSA_PESQUISA))
 
 
def clicar_todos(arquivo, confianca=CONFIANCA, distancia_min=30):
    centros = []
    try:
        caixas = list(pag.locateAllOnScreen(arquivo, confidence=confianca))
    except pag.ImageNotFoundException:
        caixas = []
 
    for caixa in caixas:
        c = pag.center(caixa)
        # descarta duplicatas 
        if all(abs(c.x - o.x) > distancia_min or abs(c.y - o.y) > distancia_min for o in centros):
            centros.append(c)
 
    centros.sort(key=lambda p: (p.y, p.x))  # de cima para baixo, esquerda para direita
    print(f'{len(centros)} cards encontrados')
 
    for c in centros:
        pag.click(c)
        time.sleep(3)                # espera a aba do card abrir
        pag.hotkey('ctrl', 'w')      # fecha a aba do card e volta ao Rewards
        time.sleep(1)
    return len(centros)
 
 
# ---------- EXECUCAO ----------
print('Comecando em 5 segundos... (mouse no canto superior esquerdo para cancelar)')
time.sleep(5)
 
# 1. Abre o Edge
pag.press('win')
time.sleep(3)
pag.write('microsoft edge')
pag.press('enter')
time.sleep(4)
 
# 2. Pesquisas (ordem e termos diferentes a cada execucao)
for termo in random.sample(TERMOS, k=min(QTD_PESQUISAS, len(TERMOS))):
    pesquisar(termo)
 
# 3. Abre o Rewards em uma nova aba
pag.hotkey('ctrl', 't')
time.sleep(1)
pag.write('rewards.bing.com')
pag.press('enter')
time.sleep(6)   # espera a pagina carregar
 
# 4. Desce ate os cards e clica em todos os pendentes
for _ in range(ROLAGENS):
    pag.press('pagedown')
    time.sleep(1)
 
clicar_todos(ARQUIVO_CARD)
print('Finalizado.')