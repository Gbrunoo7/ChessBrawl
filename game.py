# -*- coding: utf-8 -*-

import pygame
import sys
import os
import random
import mysql.connector
from datetime import datetime

pygame.init()
pygame.mixer.init()

# Função deve vir ANTES do uso
def caminho_absoluto(rel_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

#  Música de fundo
try:
    pygame.mixer.music.load(caminho_absoluto("song.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop infinito
except pygame.error:
    print("Aviso: song.mp3 nao carregada. Prosseguindo sem musica de fundo.")

###############################
#FRONT END ####################
###############################

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (200, 0, 0)
CINZA_ESCURO = (40, 40, 40)
CINZA_CLARO = (80, 80, 80)
CINZA = (100, 100, 100)
TEXTO_COR = (30, 30, 30)
BRANCO_QUASE = (230, 230, 230)
VERMELHO_CLARO = (255, 80, 80)

# Tela cheia
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h

# Carregamento do fundo
def carregar_imagem_fundo(caminho, largura_tela, altura_tela):
    try:
        imagem = pygame.image.load(caminho).convert()
        largura_img, altura_img = imagem.get_size()
        proporcao_tela = largura_tela / altura_tela
        proporcao_imagem = largura_img / altura_img

        if proporcao_tela > proporcao_imagem:
            nova_altura = int(largura_tela / proporcao_imagem)
            return pygame.transform.scale(imagem, (largura_tela, nova_altura))
        else:
            nova_largura = int(altura_tela * proporcao_imagem)
            return pygame.transform.scale(imagem, (nova_largura, altura_tela))
    except Exception as e:
        print(f"Aviso: imagem de fundo nao carregada: {str(e)}")
        return None

#  Imagem de fundo
background_img = carregar_imagem_fundo(caminho_absoluto("ceu_com_nuvens.jpg"), LARGURA, ALTURA)

#  Ícone do jogo
try:
    icone = pygame.image.load(caminho_absoluto("icone_game.png"))
    pygame.display.set_icon(icone)
except pygame.error:
    print("Aviso: icone_game.png nao suportado ou nao encontrado. Prosseguindo sem icone.")


fonte = pygame.font.SysFont("Segoe UI", 48, bold=True)
fonte_pequena = pygame.font.SysFont("Segoe UI", 36)
fonte_input = pygame.font.SysFont("Segoe UI", 28)
fonte_titulo = pygame.font.SysFont("Consolas", 60, bold=True)
fonte_botao = pygame.font.SysFont("Consolas", 36)

try:
    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error:
    print("Aviso: song.mp3 nao carregada. Prosseguindo sem musica de fundo.")

jogadores = []
confrontos_sorteados = []

class Botao:
    def __init__(self, texto, centro_x, y, padding_x, altura, callback):
        self.texto = texto
        self.altura = altura
        self.callback = callback
        self.label = fonte_botao.render(texto, True, BRANCO)
        self.largura = self.label.get_width() + 2 * padding_x
        self.rect = pygame.Rect(centro_x - self.largura // 2, y, self.largura, altura)

    def desenhar(self, mouse_pos):
        cor = CINZA_CLARO if self.rect.collidepoint(mouse_pos) else CINZA_ESCURO
        pygame.draw.rect(screen, cor, self.rect, border_radius=12)
        pygame.draw.rect(screen, VERMELHO, self.rect, 2, border_radius=12)
        screen.blit(self.label, (
            self.rect.centerx - self.label.get_width() // 2,
            self.rect.centery - self.label.get_height() // 2
        ))

    def checar_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()


    @staticmethod
    def dummy():
        print("Botao pressionado")

def input_box(prompt, restrito_sn=False):
    texto = ""
    ativo = True
    clock = pygame.time.Clock()
    while ativo:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        # Caixa de entrada escura
        largura_caixa = LARGURA - 200
        altura_caixa = 180
        desenhar_caixa_translucida(100, ALTURA // 2 - 60, largura_caixa, 120)

        # Pergunta e entrada com sombra
        desenhar_texto_com_sombra(
            prompt,
            fonte,
            BRANCO,
            PRETO,
            LARGURA // 2 - fonte.size(prompt)[0] // 2,
            ALTURA // 3
        )

        desenhar_texto_com_sombra(
            texto,
            fonte_pequena,
            VERMELHO,
            PRETO,
            LARGURA // 2 - fonte_pequena.size(texto)[0] // 2,
            ALTURA // 2
        )

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if not restrito_sn or texto.lower() in ["s", "n"]:
                        ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    texto += evento.unicode
        clock.tick(30)
    return texto.strip()


def exibir_mensagem(texto):
    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        # Caixa translucida
        largura_caixa = LARGURA - 200
        altura_caixa = 160
        desenhar_caixa_translucida(100, ALTURA // 2 - 80, largura_caixa, altura_caixa)

        # Mensagem principal com sombra
        desenhar_texto_com_sombra(
            texto,
            fonte,
            BRANCO,
            PRETO,
            LARGURA // 2 - fonte.size(texto)[0] // 2,
            ALTURA // 2 - 40
        )

        # Instrucao ESC
        instrucao = "Pressione ESC para continuar"
        desenhar_texto_com_sombra(
            instrucao,
            fonte_input,
            VERMELHO,
            PRETO,
            LARGURA // 2 - fonte_input.size(instrucao)[0] // 2,
            ALTURA // 2 + 20
        )

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
        clock.tick(30)

def menu_principal():
    botoes_info = [
        ("Cadastrar Jogador", cadastrar_jogador),
        ("Listar Jogadores", listar_jogadores),
        ("Sortear Batalhas", sortear_batalhas),
        ("Administrar Batalha Manual", administrar_batalha),
        ("Executar Torneio Completo", executar_torneio),
        ("Leaderboard", mostrar_leaderboard),
        ("Limpar Banco de Dados", limpar_dados),
        ("Sair", lambda: sys.exit())
    ]

    botoes = []
    espacamento = 25
    altura_botao = 60
    padding_horizontal = 40
    altura_total = len(botoes_info) * (altura_botao + espacamento) - espacamento
    y_inicial = ALTURA // 2 - altura_total // 2 + 80

    for i, (texto, acao) in enumerate(botoes_info):
        botao = Botao(
            texto=texto,
            centro_x=LARGURA // 2,
            y=y_inicial + i * (altura_botao + espacamento),
            padding_x=padding_horizontal,
            altura=altura_botao,
            callback=acao
        )
        botoes.append(botao)

    rodando = True
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        # Titulo com sombra aprimorado
        titulo_txt = "CHESS BRAWL - MENU PRINCIPAL"
        titulo = fonte_titulo.render(titulo_txt, True, BRANCO)
        sombra = fonte_titulo.render(titulo_txt, True, PRETO)
        x = LARGURA // 2 - titulo.get_width() // 2
        y = 50
        screen.blit(sombra, (x + 3, y + 3))
        screen.blit(titulo, (x, y))

        for botao in botoes:
            botao.desenhar(mouse_pos)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes:
                    botao.checar_click(mouse_pos)

def desenhar_tela_inicial():
    if background_img:
         screen.blit(background_img, (0, 0))
    else:
         screen.fill(PRETO)

    def desenhar_tela_inicial():
    
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

    # Titulo com sombra
    desenhar_texto_com_sombra(
        "CHESS BRAWL",
        fonte,
        BRANCO,
        PRETO,
        LARGURA // 2 - fonte.size("CHESS BRAWL")[0] // 2,
        ALTURA // 3
    )

    # Subtitulo com sombra
    desenhar_texto_com_sombra(
        "Pressione ENTER para iniciar",
        fonte,
        VERMELHO,
        PRETO,
        LARGURA // 2 - fonte.size("Pressione ENTER para iniciar")[0] // 2,
        ALTURA // 2
    )

    pygame.display.flip()


def desenhar_texto_com_sombra(texto, fonte, cor_texto, cor_sombra, x, y):
    sombra = fonte.render(texto, True, cor_sombra)
    screen.blit(sombra, (x + 2, y + 2))
    renderizado = fonte.render(texto, True, cor_texto)
    screen.blit(renderizado, (x, y))

def desenhar_caixa_translucida(x, y, largura, altura, cor=(0, 0, 0), alpha=180):
    s = pygame.Surface((largura, altura))
    s.set_alpha(alpha)
    s.fill(cor)
    screen.blit(s, (x, y))

def exibir_relatorio_final():
    jogadores_ordenados = sorted(jogadores, key=lambda j: j['pontuacao'], reverse=True)
    rodando = True
    clock = pygame.time.Clock()

    # Consulta ao banco para buscar as pontuacoes oficiais
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT nick, pontuacao_total FROM jogadores")
    dados_banco = {nick: pontuacao for nick, pontuacao in cursor.fetchall()}
    cursor.close()
    conn.close()

    while rodando:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        # Caixa escura semi-transparente ao fundo
        caixa_x = 40
        caixa_y = 80
        caixa_largura = LARGURA - 80
        caixa_altura = 420  # ajuste conforme necessario
        desenhar_caixa_translucida(caixa_x, caixa_y, caixa_largura, caixa_altura)

        # Titulo com sombra
        titulo_txt = "Relatorio Final do Torneio"
        titulo_render = fonte.render(titulo_txt, True, BRANCO)
        desenhar_texto_com_sombra(
            titulo_txt,
            fonte,
            BRANCO,
            PRETO,
            LARGURA // 2 - titulo_render.get_width() // 2,
            30
        )

        y = 100
        for jogador in jogadores_ordenados:
            nick = jogador['nick']
            pont_mem = jogador['pontuacao']
            pont_db = dados_banco.get(nick, 0)

            texto = (
                f"{nick} - Mem: {pont_mem} | DB: {pont_db} | "
                f"Jogadas originais: {jogador.get('jogadas_originais', 0)}, "
                f"Gafes: {jogador.get('gafes', 0)}, "
                f"Pos. vantajosos: {jogador.get('pos_vantajoso', 0)}, "
                f"Desrespeitos: {jogador.get('desrespeito', 0)}, "
                f"Furias: {jogador.get('furia', 0)}"
            )
            desenhar_texto_com_sombra(texto, fonte_input, BRANCO, PRETO, 60, y)
            y += 35

        instrucao_txt = "Pressione ESC para voltar"
        desenhar_texto_com_sombra(
            instrucao_txt,
            fonte_input,
            VERMELHO,
            PRETO,
            LARGURA // 2 - fonte_input.size(instrucao_txt)[0] // 2,
            ALTURA - 50
        )

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
        clock.tick(30)

def sair_jogo():
    exibir_mensagem("Use o botao 'Sair' no menu principal.")

def blitz_match(j1, j2):
    clock = pygame.time.Clock()
    rodando = True

    vencedor_blitz = random.choice([j1, j2])

    while rodando:
        # Fundo com imagem ou preto
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        # Caixa escura semi-transparente (metade da altura)
        caixa_x = 40
        caixa_y = ALTURA // 4  # Comeca a 1/4 da altura
        caixa_largura = LARGURA - 80
        caixa_altura = ALTURA // 2  # Metade da altura
        desenhar_caixa_translucida(caixa_x, caixa_y, caixa_largura, caixa_altura)

        # Titulo com sombreamento
        desenhar_texto_com_sombra(
            "BLITZ MATCH!",
            fonte,
            VERMELHO,
            PRETO,
            LARGURA // 2 - fonte.size("BLITZ MATCH!")[0] // 2,
            caixa_y + 20  # Ajustado para a posicao relativa da caixa
        )

        # Texto do vencedor com sombreamento
        vencedor_txt = f"{vencedor_blitz['nick']} venceu e ganhou +2 pontos!"
        desenhar_texto_com_sombra(
            vencedor_txt,
            fonte,
            BRANCO,
            PRETO,
            LARGURA // 2 - fonte.size(vencedor_txt)[0] // 2,
            caixa_y + caixa_altura // 2 - 20
        )

        # Instrucao com sombreamento
        desenhar_texto_com_sombra(
            "Pressione ESC para continuar",
            fonte_input,
            VERMELHO,
            PRETO,
            LARGURA // 2 - fonte_input.size("Pressione ESC para continuar")[0] // 2,
            caixa_y + caixa_altura - 40  # Perto da borda inferior da caixa
        )

        # Atualiza a tela
        pygame.display.flip()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
        clock.tick(30)

    return vencedor_blitz

def main():
    tela_inicial = True
    while tela_inicial:
        desenhar_tela_inicial()
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                tela_inicial = False
    carregar_jogadores_do_banco()
    menu_principal()

###############################
#FIM FRONT END ################
###############################

####################################################
# AREA BANCO DE DADOS###############################
####################################################

def conectar_mysql():
    try:
        return mysql.connector.connect( 
            host="localhost",
            user="chess.brawl",
            password="S@Nha123!@",
            database="chess_brawl"
        )
    except mysql.connector.Error as err: 
        exibir_mensagem(f"Erro ao conectar no banco: {str(err)}")
        return None


def carregar_jogadores_do_banco():
    global jogadores 
    jogadores.clear()

    conn = conectar_mysql() 
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nick, nome, pontuacao_total, ranking FROM jogadores")
        dados = cursor.fetchall()  
        for nick, nome, pontuacao, ranking in dados:
            jogadores.append({
                "nick": nick,
                "nome": nome,
                "pontuacao": pontuacao,
                "ranking": ranking
            })
        cursor.close()
        conn.close()
    except Exception as e:
        exibir_mensagem(f"Erro ao carregar jogadores: {str(e)}")

# Inserir estatisticas ao final da partida
def gravar_estatisticas(jogador_1, jogador_2, vencedor, movimentos, duracao):
    conn = conectar_mysql()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO partida_estatisticas (
                jogador_1, jogador_2, vencedor, numero_de_movimentos, duracao_segundos
            ) VALUES (%s, %s, %s, %s, %s)
        """
        valores = (jogador_1, jogador_2, vencedor, movimentos, duracao)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        exibir_mensagem(f"Erro ao gravar estatisticas: {str(e)}")

# Mostrar todas as estatisticas
def tabela_de_estatisticas():
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM partida_estatisticas ORDER BY data_partida DESC")
    resultados = cursor.fetchall()

    print(f"\n{'ID':<4} {'Jogador 1':<15} {'Jogador 2':<15} {'Vencedor':<15} {'Movs':<5} {'Duracao(s)':<10} {'Data'}")
    print("-" * 80)
    for row in resultados:
        print(f"{row[0]:<4} {row[1]:<15} {row[2]:<15} {row[3]:<15} {row[4]:<5} {row[5]:<10} {row[6]}")
    
    cursor.close()
    conn.close()

def mostrar_leaderboard():
    conn = conectar_mysql()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nick, nome, partidas, vitorias, derrotas, empates, pontuacao_total,
               ROUND((vitorias / partidas) * 100, 2) AS winrate
        FROM jogadores
        WHERE partidas > 0
        ORDER BY pontuacao_total DESC
        LIMIT 10
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    rodando = True
    clock = pygame.time.Clock()

    fonte_mono = pygame.font.SysFont("Consolas", 30)
    margem_x = 100
    largura_caixa = LARGURA - 2 * margem_x
    altura_caixa = 500
    y_caixa = 120

    while rodando:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        desenhar_caixa_translucida(margem_x, y_caixa, largura_caixa, altura_caixa)

        # Titulo com sombra                                                                               # Front End 
        titulo_texto = "LEADERBOARD"
        titulo = fonte.render(titulo_texto, True, BRANCO)
        sombra = fonte.render(titulo_texto, True, PRETO)
        screen.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 2, 50 + 2))
        screen.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))

        y = y_caixa + 20
        cabecalho = f"{'Nick':<12} {'Vitorias':<9} {'Derrotas':<9} {'Empates':<9} {'Partidas':<10} {'Pts':<6} {'Winrate (%)':<12}"
        sombra_cab = fonte_mono.render(cabecalho, True, PRETO)
        texto_cab = fonte_mono.render(cabecalho, True, VERMELHO)
        screen.blit(sombra_cab, (margem_x + 2, y + 2))
        screen.blit(texto_cab, (margem_x, y))
        y += 42

        for row in resultados:
            winrate = f"{row[7]:.2f}" if row[7] is not None else "0.00"
            linha = f"{row[0]:<12} {row[3]:<9} {row[4]:<9} {row[5]:<9} {row[2]:<10} {row[6]:<6} {winrate:<12}"
            sombra_linha = fonte_mono.render(linha, True, PRETO)
            texto_linha = fonte_mono.render(linha, True, BRANCO)
            screen.blit(sombra_linha, (margem_x + 2, y + 2))
            screen.blit(texto_linha, (margem_x, y))
            y += 38

        instrucao = fonte_input.render("Pressione ESC para voltar", True, VERMELHO)
        sombra_instr = fonte_input.render("Pressione ESC para voltar", True, PRETO)
        screen.blit(sombra_instr, (LARGURA // 2 - instrucao.get_width() // 2 + 2, ALTURA - 48))
        screen.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, ALTURA - 50))                 # Front End

        pygame.display.flip()

        for evento in pygame.event.get():                                       
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:  # Permite voce sair da tela ao apertar Esc
                rodando = False

        clock.tick(30)  # Limita o framerate a 30 nesta tela, evitando bugs



def atualizar_estatisticas_jogador(nick, nome, resultado, pontuacao_atual):
    conn = conectar_mysql()
    if not conn:
        return
    try:
        cursor = conn.cursor()  # O cursor e uma funcao de SQL que permite que voce leia uma linha de tabela de banco de dados
        cursor.execute("SELECT * FROM jogadores WHERE nick = %s", (nick,)) # Seleciona TODOS valores da tabela jogadores onde o nick e parametro
        existe = cursor.fetchone()

        if not existe:         # Se a string do nick nao for encontrada vai inserir os dados de forma que esteja devidamente registrada
            cursor.execute("""
             INSERT INTO jogadores (nick, nome, partidas, vitorias, derrotas, empates, pontuacao_total, ranking)
             VALUES (%s, %s, 1, %s, %s, %s, %s, %s)
             """, (
    nick, nome,
    1 if resultado == "vitoria" else 0,
    1 if resultado == "derrota" else 0,
    1 if resultado == "empate" else 0,
    pontuacao_atual,
    9999  # <-- Valor padrao de ranking
))

        else:
            campo = {
                "vitoria": "vitorias",
                "derrota": "derrotas",
                "empate": "empates"
            }[resultado]

            sql = f"""
                UPDATE jogadores
                SET partidas = partidas + 1,
                    {campo} = {campo} + 1,
                    pontuacao_total = %s
                WHERE nick = %s
            """
            cursor.execute(sql, (pontuacao_atual, nick))

        conn.commit()
        cursor.close()
        conn.close()  # fecha a conexao com MySQL para que nao hajam problemas
    except Exception as e: # Caso nao seja possivel realizar a atualizacao das estatisticas, notificar o usuario
        exibir_mensagem(f"Erro ao atualizar estatisticas do jogador {nick}: {str(e)}") # Exibir mensagem é uma funcao que faz texto aparecer na tela


####################################################
# FIM DA AREA BANCO DE DADOS########################
####################################################

####################################################
# PAGINAS DO MENU ##################################
####################################################
def cadastrar_jogador():
    nome = input_box("Digite o nome do jogador:")
    nick = input_box("Digite o nickname:")

    # Verifica se ja existe um jogador com o mesmo nickname
    for jogador in jogadores:
        if jogador["nick"].lower() == nick.lower():
            exibir_mensagem("Nickname ja cadastrado. Escolha outro.")
            return

    ranking = input_box("Digite o ranking (1 a 15000):")
    if ranking.isdigit():
        ranking = int(ranking)
        if 1 <= ranking <= 15000:
            # Adiciona localmente com pontuacao inicial de 70 (para exibicao no jogo)
            jogadores.append({
                "nome": nome,
                "nick": nick,
                "ranking": ranking,
                "pontuacao": 70
            })

            # Registra no banco com pontuacao total zerada
            conn = conectar_mysql()
            cursor = conn.cursor()
            cursor.execute("""
                 INSERT INTO jogadores (nick, nome, partidas, vitorias, derrotas, empates, pontuacao_total, ranking)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                 """, (nick, nome, 0, 0, 0, 0, 70, ranking))

            conn.commit()  # <-- Adicione isso aqui
            cursor.close()
            conn.close()


            exibir_mensagem("Jogador cadastrado!")
            return

    exibir_mensagem("Ranking invalido. Nao cadastrado.")


def listar_jogadores():
    rodando = True
    clock = pygame.time.Clock()
    fonte_mono = pygame.font.SysFont("Consolas", 30)

    margem_x = 100
    largura_caixa = LARGURA - 2 * margem_x
    altura_caixa = 500
    y_caixa = 120

    while rodando:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        # Caixa translucida de fundo
        desenhar_caixa_translucida(margem_x, y_caixa, largura_caixa, altura_caixa)

        # Titulo com sombra
        titulo_txt = "JOGADORES CADASTRADOS"
        titulo = fonte.render(titulo_txt, True, BRANCO)
        sombra = fonte.render(titulo_txt, True, PRETO)
        screen.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 2, 50 + 2))
        screen.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))

        y = y_caixa + 20
        cabecalho = f"{'Nick':<12} {'Nome':<15} {'Ranking':<10} {'Pontuacao':<10}"
        sombra_cab = fonte_mono.render(cabecalho, True, PRETO)
        texto_cab = fonte_mono.render(cabecalho, True, VERMELHO)
        screen.blit(sombra_cab, (margem_x + 2, y + 2))
        screen.blit(texto_cab, (margem_x, y))
        y += 42

        for jogador in jogadores:
            linha = f"{jogador['nick']:<12} {jogador['nome']:<15} {jogador['ranking']:<10} {jogador['pontuacao']:<10}"
            sombra_linha = fonte_mono.render(linha, True, PRETO)
            texto_linha = fonte_mono.render(linha, True, BRANCO)
            screen.blit(sombra_linha, (margem_x + 2, y + 2))
            screen.blit(texto_linha, (margem_x, y))
            y += 38

        instrucao = fonte_input.render("Pressione ESC para voltar", True, VERMELHO)
        sombra_instr = fonte_input.render("Pressione ESC para voltar", True, PRETO)
        screen.blit(sombra_instr, (LARGURA // 2 - instrucao.get_width() // 2 + 2, ALTURA - 48))
        screen.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, ALTURA - 50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
        clock.tick(30)

def sortear_batalhas():
    global confrontos_sorteados
    if len(jogadores) < 4 or len(jogadores) > 8 or len(jogadores) % 2 != 0:
        exibir_mensagem("Numero invalido de jogadores.")
        return

    random.shuffle(jogadores)
    confrontos_sorteados = [(jogadores[i], jogadores[i + 1]) for i in range(0, len(jogadores), 2)]

    rodando = True
    clock = pygame.time.Clock()

    margem_x = 100
    largura_caixa = LARGURA - 2 * margem_x
    altura_caixa = 400
    y_caixa = 160

    while rodando:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        desenhar_caixa_translucida(margem_x, y_caixa, largura_caixa, altura_caixa)

        # Titulo com sombra
        titulo_txt = "Confrontos Sorteados"
        titulo = fonte.render(titulo_txt, True, BRANCO)
        sombra = fonte.render(titulo_txt, True, PRETO)
        screen.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 2, 60 + 2))
        screen.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 60))

        y = y_caixa + 40
        for j1, j2 in confrontos_sorteados:
            texto = f"{j1['nick']} VS {j2['nick']}"
            sombra_txt = fonte_input.render(texto, True, PRETO)
            texto_render = fonte_input.render(texto, True, BRANCO)
            screen.blit(sombra_txt, (LARGURA // 2 - texto_render.get_width() // 2 + 2, y + 2))
            screen.blit(texto_render, (LARGURA // 2 - texto_render.get_width() // 2, y))
            y += 42

        instrucao = fonte_input.render("Pressione ESC para voltar", True, VERMELHO)
        sombra_instr = fonte_input.render("Pressione ESC para voltar", True, PRETO)
        screen.blit(sombra_instr, (LARGURA // 2 - instrucao.get_width() // 2 + 2, ALTURA - 48))
        screen.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, ALTURA - 50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
        clock.tick(30)

def administrar_batalha():
    if not confrontos_sorteados:
        exibir_mensagem("Nenhuma batalha sorteada.")
        return

    index = 0
    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(PRETO)

        caixa_x = 40
        caixa_y = 40
        caixa_largura = LARGURA - 80
        caixa_altura = ALTURA - 80
        desenhar_caixa_translucida(caixa_x, caixa_y, caixa_largura, caixa_altura)

        desenhar_texto_com_sombra(
            "Escolha o duelo (ENTER para iniciar, ESC para sair)",
            fonte,
            BRANCO,
            PRETO,
            LARGURA // 2 - fonte.size("Escolha o duelo (ENTER para iniciar, ESC para sair)")[0] // 2,
            50
        )

        for idx, (j1, j2) in enumerate(confrontos_sorteados):
            cor = VERMELHO if idx == index else BRANCO
            texto = f"{j1['nick']} vs {j2['nick']}"
            desenhar_texto_com_sombra(
                texto,
                fonte_input,
                cor,
                PRETO,
                LARGURA // 2 - fonte_input.size(texto)[0] // 2,
                150 + idx * 40
            )

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    index = (index - 1) % len(confrontos_sorteados)
                elif evento.key == pygame.K_DOWN:
                    index = (index + 1) % len(confrontos_sorteados)
                elif evento.key == pygame.K_RETURN:
                    rodando = False
                elif evento.key == pygame.K_ESCAPE:
                    return
        clock.tick(30)

    j1, j2 = confrontos_sorteados[index]

    pont_j1_real = j1['pontuacao']
    pont_j2_real = j2['pontuacao']

    j1['pontuacao'] = j2['pontuacao'] = min(pont_j1_real, pont_j2_real)

    eventos = [
        ("Jogada original", 5),
        ("Gafe", -3),
        ("Posicionamento vantajoso", 2),
        ("Desrespeito ao adversario", -5),
        ("Ataque de furia", -7)
    ]

    for jogador in [j1, j2]:
        for nome, pontos in eventos:
            resposta = input_box(f"{jogador['nick']} fez {nome}? (s/n)", restrito_sn=True)
            if resposta.lower() == "s":
                jogador['pontuacao'] += pontos

    if j1['pontuacao'] > j2['pontuacao']:
        vencedor = j1
    elif j2['pontuacao'] > j1['pontuacao']:
        vencedor = j2
    else:
        vencedor = blitz_match(j1, j2)
        vencedor['pontuacao'] += 2 

    # Calcula penalidades permanentes
    penalidade_j1 = j1['pontuacao'] - min(pont_j1_real, pont_j2_real)
    penalidade_j2 = j2['pontuacao'] - min(pont_j1_real, pont_j2_real)

    if vencedor == j1:
        j1['pontuacao'] = pont_j1_real + 30 + (j1['pontuacao'] - min(pont_j1_real, pont_j2_real))
        j2['pontuacao'] = pont_j2_real + (j2['pontuacao'] - min(pont_j1_real, pont_j2_real))
    else:
        j2['pontuacao'] = pont_j2_real + 30 + (j2['pontuacao'] - min(pont_j1_real, pont_j2_real))
        j1['pontuacao'] = pont_j1_real + (j1['pontuacao'] - min(pont_j1_real, pont_j2_real))

    exibir_mensagem(f"{vencedor['nick']} venceu a batalha!")
    gravar_estatisticas(j1["nick"], j2["nick"], vencedor["nick"], movimentos=0, duracao=0)

    resultado_j1 = "vitoria" if vencedor == j1 else "derrota" if vencedor == j2 else "empate"
    resultado_j2 = "vitoria" if vencedor == j2 else "derrota" if vencedor == j1 else "empate"

    atualizar_estatisticas_jogador(j1["nick"], j1["nome"], resultado_j1, j1["pontuacao"])
    atualizar_estatisticas_jogador(j2["nick"], j2["nome"], resultado_j2, j2["pontuacao"])

def limpar_dados():
    confirmacao = input_box("Tem certeza? Digite 'CONFIRMAR'")
    if confirmacao != "CONFIRMAR":
        exibir_mensagem("Operacao cancelada.")
        return

    try:
        conn = conectar_mysql()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE partida_estatisticas")
        cursor.execute("TRUNCATE TABLE jogadores")
        conn.commit()
        cursor.close()
        conn.close()

        carregar_jogadores_do_banco()  # Atualiza dados em memoria
        exibir_mensagem("Dados apagados com sucesso.")
    except Exception as e:
        exibir_mensagem(f"Erro ao limpar dados: {str(e)}")

####################################################
# FIM PAGINAS DO MENU ##############################
####################################################

####################################################
# FUNCOES LOGICAS ##################################
####################################################
def executar_torneio():
    if len(jogadores) < 4 or len(jogadores) > 8 or len(jogadores) % 2 != 0:
        exibir_mensagem("Sao necessarios 4 a 8 jogadores em numero par.")
        return

    classificados = jogadores[:]
    fase = 1

    while len(classificados) > 1:
        random.shuffle(classificados)
        vencedores = []
        for i in range(0, len(classificados), 2):
            j1 = classificados[i]
            j2 = classificados[i+1]

            # Clona pontuacoes reais
            pont_j1_real = j1['pontuacao']
            pont_j2_real = j2['pontuacao']

            # Igualar temporariamente as pontuacoes para tornar a disputa justa
            j1['pontuacao'] = j2['pontuacao'] = min(pont_j1_real, pont_j2_real)
            exibir_mensagem(f"Fase {fase} - Batalha: {j1['nick']} VS {j2['nick']}")

            eventos = [
                ("Jogada original", 5, 'jogadas_originais'),
                ("Gafe", -3, 'gafes'),
                ("Posicionamento vantajoso", 2, 'pos_vantajoso'),
                ("Desrespeito ao adversario", -5, 'desrespeito'),
                ("Ataque de furia", -7, 'furia')
            ]

            for jogador in [j1, j2]:
                for nome, pontos, chave in eventos:
                    resposta = input_box(f"{jogador['nick']} fez {nome}? (s/n)", restrito_sn=True)
                    if resposta.lower() == "s":
                        jogador['pontuacao'] += pontos
                        jogador[chave] = jogador.get(chave, 0) + 1

            if j1['pontuacao'] > j2['pontuacao']:
                vencedor = j1
            elif j2['pontuacao'] > j1['pontuacao']:
                vencedor = j2
            else:
                vencedor = blitz_match(j1, j2)
                vencedor['pontuacao'] += 2 

            # Calcula penalidades permanentes
            penalidade_j1 = j1['pontuacao'] - min(pont_j1_real, pont_j2_real)
            penalidade_j2 = j2['pontuacao'] - min(pont_j1_real, pont_j2_real)

            # Aplica penalidade (se negativa) + bônus por vitoria
            j1['pontuacao'] = pont_j1_real + (j1['pontuacao'] - min(pont_j1_real, pont_j2_real)) + (30 if vencedor == j1 else 0)
            j2['pontuacao'] = pont_j2_real + (j2['pontuacao'] - min(pont_j1_real, pont_j2_real)) + (30 if vencedor == j2 else 0)

            exibir_mensagem(f"{vencedor['nick']} venceu a batalha!")
            gravar_estatisticas(j1["nick"], j2["nick"], vencedor["nick"], movimentos=0, duracao=0)

            resultado_j1 = "vitoria" if vencedor == j1 else "derrota" if vencedor == j2 else "empate"
            resultado_j2 = "vitoria" if vencedor == j2 else "derrota" if vencedor == j1 else "empate"

            # Atualiza banco com a pontuacao TOTAL atual, nao apenas o delta
            atualizar_estatisticas_jogador(j1["nick"], j1["nome"], resultado_j1, j1["pontuacao"])
            atualizar_estatisticas_jogador(j2["nick"], j2["nome"], resultado_j2, j2["pontuacao"])

            vencedores.append(vencedor)

        classificados = vencedores
        fase += 1

    campeao = classificados[0]
    exibir_mensagem(f"Campeao: {campeao['nick']} com {campeao['pontuacao']} pontos!")
    exibir_relatorio_final()



if __name__ == "__main__":
    main()

####################################################
# FIM FUNCOES LOGICAS ##############################
####################################################