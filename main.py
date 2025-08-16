import discord
from discord.ext import commands , tasks
import sqlite3
import time
import os
import datetime
import random
import string
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)


#=======CARGOS DISCORD====================
mod_role_id = 1175164740692090960
vip_role_id = 1192498388961345616
adm_role_id = 1175164740692090960
staff_role_id = 1169008903695114301
#["Iniciante", "Intermediario", "Avançado", "Especialista", "Mestre", "Lendario", "Supremo","MestreSupremo"]

idiniciante = 1192293321649963078
idintermediario=1192293392672116857
idavançado =1192293527112130672
idespecialista=1192293689666584707
idmestre =1192294029170327723
idlendario =1192294155934761090
idsupremo=1192294307256860682
idmestresupremo =1197197257133531136
#======= FIM CARGOS ======================
#=======ID CANAL DISCORD==================
idcanal_dicas = 1183079177105186856
idcanal_chatgeral = 1182676573787271262
idcanal = 1192295302967853056
idcanal_logstaff = 1192295863255568444
idcanal_vip = 1192492911057707008
idcanal_criadorconteudo = 1192492911057707008
idcanal_regras =1182671902452494427
idcanal_entrada =1182671802233782322
idcanal_sorteio =1182675379857674262
#======= FIM ID CANAL ====================
#======= BANCO DE DADOS ==================
conn = sqlite3.connect('points.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS points
             (user_id text, points integer)''')

c.execute('''CREATE TABLE IF NOT EXISTS codigos_premiados
             (codigo text, valido integer)''')

c.execute('''CREATE TABLE IF NOT EXISTS codigos_unicos
             (codigo text, valido integer,pontos integer)''')

c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id text, exp integer, level integer, category text)''')

c.execute('''CREATE TABLE IF NOT EXISTS espadas
             (nome_espada text, forca integer, user_id text)''')

c.execute('''CREATE TABLE IF NOT EXISTS produtos
             (id_prod INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, custo INTEGER, codigo TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Rifas (
                        datafinal TEXT,
                        participantes TEXT,
                        ganhador TEXT
                    )''')

c.execute('''CREATE TABLE IF NOT EXISTS guildas
             (id INTEGER PRIMARY KEY AUTOINCREMENT, guilda TEXT, user_id TEXT)''')


# Verificar se a tabela possui o campo "pontos"
c.execute("PRAGMA table_info(codigos_unicos)")
columns = c.fetchall()
pontos_exists = any(column[1] == 'pontos' for column in columns)

# Se o campo "pontos" não existir, crie-o
if not pontos_exists:
    c.execute("ALTER TABLE codigos_unicos ADD COLUMN pontos INTEGER DEFAULT 0") 
#c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id != ""', ('0', '1', 'Iniciante'))
#c.execute('UPDATE invites SET invites_count = 0  WHERE inviter_id !=0')
conn.commit()
#======= FIM BANCO DE DADOS ==================

@bot.command()
async def criarconta(ctx):
    if ctx.channel.id == idcanal:
     user_id = str(ctx.author.id)
     c.execute('SELECT * FROM points WHERE user_id=?', (user_id,))
     row = c.fetchone()
     if not row:
        c.execute('INSERT INTO points (user_id, points) VALUES (?, ?)', (user_id, 0))
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, 0, 1, "Iniciante"))
        conn.commit()
        await ctx.send(f'{ctx.author.name} Sua conta foi criada com sucesso!')
     else:
        await ctx.send(f'{ctx.author.name} Você já possui uma conta.')


@bot.command()
async def removerminhaconta(ctx, usermention: discord.Member, resposta: int):
    if resposta == 4 and usermention == ctx.author:
        c.execute('DELETE FROM users WHERE user_id = ?', (ctx.author.id,))
        c.execute('DELETE FROM points WHERE user_id = ?', (ctx.author.id,))
        conn.commit()
        await ctx.send(f"A conta de {usermention.mention} foi excluída com sucesso.")
    else:
        await ctx.send("Resposta incorreta ou menção inválida. A exclusão da conta não foi confirmada. \n Para remover responda quanto é 2+2 e Digite: /removerminhaconta @meunome resposta")
        
@bot.command()
async def doar(ctx, recipient: discord.Member, amount: int):
    if ctx.channel.id == idcanal:
     sender_id = str(ctx.author.id)
     recipient_id = str(recipient.id)
     if amount < 10:
        await ctx.send('Você não pode doar uma quantidade negativa de pontos ou menor que 10.')
        return
     if sender_id == recipient_id:
        await ctx.send('Você não pode doar pontos para si mesmo.')
        return
     c.execute('SELECT points FROM points WHERE user_id=?', (sender_id,))
     sender_row = c.fetchone()
     c.execute('SELECT points FROM points WHERE user_id=?', (recipient_id,))
     recipient_row = c.fetchone()
     if not sender_row or sender_row[0] < amount:
        await ctx.send('Você não tem 💰 pontos suficiente para doar.')
        return
     new_sender_points = sender_row[0] - amount
     new_recipient_points = (recipient_row[0] if recipient_row else 0) + amount
     c.execute('UPDATE points SET points=? WHERE user_id=?', (new_sender_points, sender_id))
     if recipient_row:
        c.execute('UPDATE points SET points=? WHERE user_id=?', (new_recipient_points, recipient_id))
     else:
        c.execute('INSERT INTO points (user_id, points) VALUES (?, ?)', (recipient_id, amount))
     conn.commit()
     await ctx.send(f'{ctx.author.name} deu 💰{amount} Pontos para {recipient.name}.')
    else:
     await ctx.send(f'Ajude agora Mesmo a manter o servidor do Game Online e o Bot Game Online a permacer Online:{os.linesep}  Basta fazer uma doação de R$ 1,00 ou mais, ao fazer a doação você ajudar a manter o bot e o servidor do jogo funcionando. {os.linesep} Doe agora mesmo e ajude o Servidor: https://livepix.gg/...')

    

@bot.command()
async def ajuda(ctx):
     await ctx.send(f'Com o bot Game Online você pode:{os.linesep} Adquirir Fun Pontos,Ganhar Exp,Lvl e subir de cargo, com os pontos você pode adiquirir codigos premiados do Jogo Game Online {os.linesep} para saber mais informações va no canal #✰〘👾〙fun-ᴄᴏᴍᴀɴᴅᴏs  e digite /dicas')


@bot.command()
async def dicas2(ctx):
        embed = discord.Embed(title="Dicas", description="Aqui estão alguns comandos úteis:", color=0x00ff00)
        embed.add_field(name="/regras", value="Para ver as regras do discord e jogo", inline=False)
        embed.add_field(name="/criarconta", value="Para criar sua conta no jogo", inline=False)
        embed.add_field(name="/saldo", value="Para ver o saldo de 💰 pontos da sua conta", inline=False)
        embed.add_field(name="/farmar", value="Para farmar 💰 10 pontos a cada 10 minutos", inline=False)
        embed.add_field(name="/top10", value="Para ver o rank dos usuários com mais 💰 pontos", inline=False)
        embed.add_field(name="/lojinha", value="Para ver os produtos disponiveis para trocar seus pontos", inline=False)
        embed.add_field(name="/doar", value="Para transferir uma quantia dos seus 💰 pontos para outro usuário", inline=False)
        embed.add_field(name="/comojogar", value="Para saber como jogar o Game Online", inline=False)
        embed.add_field(name="/recompensadiaria", value="Para ganhar 💰 100 pontos diários", inline=False)
        embed.add_field(name="/baudasorte", value="Para tentar a sorte e ganhar até 💰 50 pontos", inline=False)
        embed.add_field(name="/meustatus", value="Para ver mais informações sobre sua conta", inline=False)
        embed.add_field(name="/farmarstaff", value="Para farmar 💰 10 pontos a cada 10 minutos", inline=False)
        embed.add_field(name="/comoconvidar", value="Para saber como convidar alguém no Discord e ganhar 💰 100 pontos", inline=False)
        embed.add_field(name="/topconvites", value="Para ver o rank de usuários que mais convidaram novos membros", inline=False)
        embed.add_field(name="/sortearpontos", value="Para sortear pontos basta usar esse comando no canal de sorteio!", inline=False)
        embed.add_field(name="/sortearparaamigos", value="Para sortear pontos para amigos basta usar esse comando no canal de sorteio! a quantida de pontos e marcar seus amigos.", inline=False)
        embed.add_field(name="/comprarespada", value="Para comprar espada de madeira por 50 💰 que faz você ganhar +5 de Farm!", inline=False)
        embed.add_field(name="/uparespada", value="Para aumentar a força da sua espada 💰 +10 de Farm, custo: 💰 100", inline=False)
        embed.add_field(name="/rifa", value="Para participar da rifa e ganhar uma bolada em 💰 Pontos ", inline=False)
        embed.add_field(name="/addguilda", value="Para Adicionar a tag da sua guilda  Custo: 💰 100 Pontos ", inline=False)
        embed.add_field(name="/comprarexp", value="Para Ganhar + Exp e Level, Custo: 💰 100 Pontos ", inline=False)          
        await ctx.send(embed=embed)
        

    

@bot.command()
async def comojogar(ctx):
     await ctx.send(f'Para Jogar Game Online:{os.linesep} Basta entrar no Link Abaixo e Aceitar o Convite de teste aberto {os.linesep}  https://play.google.com/apps/testing/...')

@bot.command()
async def Bot(ctx):
    embed = discord.Embed(title="Informações do Bot", description="Aqui estão as informações sobre o bot:", color=0x00ff00)
    embed.set_thumbnail(url=bot.user.avatar)
    embed.add_field(name="Fun Bot", value=bot.user.name, inline=False)
    embed.add_field(name="Versão: ", value="1.10", inline=False)  # Substitua "1.0" pela versão real do seu bot
    embed.add_field(name="Com o bot Game Online você pode:", value="Adquirir Fun Pontos,Ganhar Exp,Lvl e subir de cargo, com os pontos você pode adiquirir codigos premiados do Jogo Game Online para saber mais informações va no canal #fun-comandos e digite /dicas", inline=False)
    embed.add_field(name="Canal de Comandos", value=ctx.guild.get_channel(idcanal).mention)  # Substitua pelo ID do canal de regras
    await ctx.send(embed=embed)

@bot.command()
async def funbot(ctx):
    embed = discord.Embed(title="Informações do Bot", description="Aqui estão as informações sobre o bot:", color=0x00ff00)
    embed.set_thumbnail(url=bot.user.avatar)
    embed.add_field(name="Fun Bot", value=bot.user.name, inline=False)
    embed.add_field(name="Versão:", value="1.10", inline=False)  # Substitua "1.0" pela versão real do seu bot
    embed.add_field(name="Com o bot Game Online você pode:", value="Adquirir Fun Pontos,Ganhar Exp,Lvl e subir de cargo, com os pontos você pode adiquirir codigos premiados do Jogo Game Online para saber mais informações va no canal #fun-comandos e digite /dicas", inline=False)
    embed.add_field(name="Canal de Comandos", value=ctx.guild.get_channel(idcanal).mention)  # Substitua pelo ID do canal de regras
    await ctx.send(embed=embed)

@bot.command()
async def vip(ctx):
     await ctx.send(f'Para conseguir o cargo vip aqui no discord e Conseguir Farmar em Dobro e recompensas diarias em dobro:{os.linesep}  Basta fazer uma doação de R$ 5,00 ou mais, ao fazer a doação você ajudar a manter o bot e o servidor do jogo funcionando.  {os.linesep} Doe agora mesmo e ajude o Servidor: https://livepix.gg/...')


@bot.command()
async def regras(ctx):
    embed = discord.Embed(
        title="Regras do Servidor",
        description="Por favor, leia as regras do servidor no canal de regras.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Canal de Regras", value=ctx.guild.get_channel(idcanal_regras).mention)  # Substitua pelo ID do canal de regras

    await ctx.send(embed=embed)
    
@bot.command()
async def dicas(ctx):
    embed = discord.Embed(
        title="Dias do Jogo Game Online e Bot Game Online",
        description="Veja diversas dicas sobre o jogo e todos os comando do Fun Bot..",
        color=discord.Color.blue()
    )
    embed.add_field(name="Canal De Dicas ", value=ctx.guild.get_channel(idcanal_dicas).mention)  # Substitua pelo ID do canal de regras

    await ctx.send(embed=embed)    




@bot.command()
async def regras2(ctx):
  if any(role.id in [staff_role_id] for role in ctx.author.roles):
    embed = discord.Embed(
        title="Regras!! Game Online",
        description="Não pode cometer nos chats:",
        color=discord.Color.blue()
    )
    embed.add_field(name="1️⃣ Trocas de contas e comércio.", value="2️⃣ Flood e Spam.", inline=False)
    embed.add_field(name="3️⃣ Pornográfia.", value="4️⃣ Menções excessivas á membros e staffs.", inline=False)
    embed.add_field(name="5️⃣ Explanação de Informações, prints ou vídeos.", value="6️⃣ Links desconhecidos, vírus e sites.", inline=False)
    embed.add_field(name="7️⃣ Discriminação, homofobia, racismo, xenofobia e gordofobia.", value="8️⃣ Xingamentos, ameaças e discursão de ódio, Assuntos depressivo ou negativos.", inline=False)
    embed.add_field(name="9️⃣ Fingindo ser alguém.", value="🔟 Perseguição e roubos.", inline=False)
    embed.add_field(name="Não pode cometer nas calls:", value="1️⃣1️⃣ Áudio estourado.", inline=False)
    embed.add_field(name="1️⃣2️⃣ Modificador de Voz.", value="1️⃣3️⃣ Gritar", inline=False)
    embed.add_field(name="1️⃣4️⃣ Pertubação & Ameaçar.", value="1️⃣5️⃣ Ficar conversando no momento de falar o código.", inline=False)
    embed.add_field(name="1️⃣6️⃣ Remover da sala, sem nenhum motivo.", value="1️⃣7️⃣ Transmissões +18, armas, vídeos.", inline=False)
    embed.add_field(name="1️⃣8️⃣ Jogar em calls inapropriadas.", value="1️⃣9️⃣ Ouvindo músicas em calls inapropriadas.", inline=False)
    embed.add_field(name="Não pode cometer em GERAL:", value="2️⃣0️⃣ Proibido falar de outros jogos", inline=False)
    embed.add_field(name="2️⃣1️⃣ Bullying.", value="2️⃣2️⃣ Desrespeitar um Staff.", inline=False)
    embed.add_field(name="2️⃣3️⃣ Discriminação, homofobia, racismo, xenofobia e gordofobia.", value="2️⃣4️⃣ Trocar contas, e comércio.", inline=False)
    embed.add_field(name="2️⃣5️⃣ Pornográfia.", value="2️⃣6️⃣ Fingindo ser algum staff.", inline=False)
    embed.add_field(name="2️⃣7️⃣ Explanação de Informações de membro, prints ou vídeos sem permissão.", value="2️⃣8️⃣ Aproveitamento de BUG", inline=False)
    embed.add_field(name="2️⃣9️⃣ Proibido uso de hack", value="3️⃣0️⃣ Sem brigas e poluição", inline=False)
    embed.add_field(name="3️⃣1️⃣ Mencionar ou fala sobre assuntos Ilícitos", value=".", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def dicas3(ctx):
 if any(role.id in [staff_role_id] for role in ctx.author.roles):
    embed = discord.Embed(title="💎 Como Conseguir Muitos Diamantes de Graça 💎", description="A cada level que você sobe, você pode ganhar 1 a 99 💎 Diamantes, quanto maior o level, maior a chance de conseguir mais diamantes.", color=0x00ff00)
# Adiciona os campos de recompensa por nível
    embed.add_field(name="Recompensas por Nível", value="Lvl:10 Recompensa: 💎 +10 Diamantes Extras.\nLvl:20 Recompensa: 💎 +25 Diamantes Extras.\nLvl:30 Recompensa: 💎 +50 Diamantes Extras.\nLvl:40 Recompensa: 💎 +75 Diamantes Extras.\nLvl:50 Recompensa: 💎 +100 Diamantes Extras.\nLvl:60 Recompensa: 💎 +120 Diamantes Extras.\nLvl:70 Recompensa: 💎 +150 Diamantes Extras.\nLvl:80 Recompensa: 💎 +175 Diamantes Extras.\nLvl:90 Recompensa: 💎 +500 Diamantes Extras.", inline=False)
# Adiciona os campos de outras formas de ganhar diamantes
    embed.add_field(name="Outras Formas de Ganhar Diamantes", value="Nas Recompensas de Login Diário, Completando os 7 Dias, é possível ganhar até 💎 500 Diamantes.\nNa Roleta da Sorte Grátis, você ganha 4 Giros Diários Grátis. Você pode Ganhar até 💎 25 Diamantes por Giro.\nNo Baú da Sorte, você pode ganhar até 💎 15 Diamantes Grátis.\nPasse De Batalha, você pode ganhar 💎 700 Diamantes Grátis.\nPegando Top1 no Rank é Possível ganhar: 💎 +1500 Diamantes.", inline=False)
# Adiciona os campos de sistemas adicionais
    embed.add_field(name="Sistemas Adicionais", value="Sistema de Guilda: Tem 2 Estilos de Guilda: Guilda Simples: com 5 Membros e 1 Bandeira fixo. Guilda VIP: com 10 Membros, TAG Colorida, 5 Bandeiras para Escolher.\nSistema de Patente: Ordem Crescente: Patente Inicial, Patente Bronze, Patente Prata, Patente Ouro, Patente Diamante.\nSistema de Pets: Inicialmente estão disponíveis 6 Pets Diferentes para ser adquiridos para te acompanhar nessa jornada.\nSistema de SKIN: Estão disponíveis Milhares de combinações Diferentes para Elevar ainda mais sua diversão.\nSistema VIP: Nick Colorido(30 Dias), ícone VIP (30 Dias), Asa VIP (30 Dias), Remoção do Banner (30 dias).", inline=False)
# Envia a embed para o canal
    await ctx.send(embed=embed)

@bot.command()
async def enviar(ctx, msg: str):
   if any(role.id in [staff_role_id] for role in ctx.author.roles):
    await ctx.send(msg)  # Envia a nova mensagem
    await ctx.message.delete()  # Apaga a mensagem original
    
server_status = "offline"
@bot.command()
async def status(ctx, msg: str):
    global server_status
    if ctx.author.guild_permissions.administrator:
        mensagem = msg;
        server_status = mensagem
        embed=discord.Embed(title="Status do Servidor", description=f"Status do servidor atualizado para {mensagem}! \U0001F680", color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Status do Servidor", description=f"O status do servidor é: {server_status} \U0001F4E2", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def servidor(ctx):
        embed=discord.Embed(title="Status do Servidor", description=f"O status do servidor é: {server_status} \U0001F4E2", color=0xff0000)
        await ctx.send(embed=embed)
        
@bot.command()
async def veratualizacao(ctx):
        c.execute("SELECT * FROM atualizacoes ORDER BY data DESC LIMIT 1")
        result = c.fetchone()
        if result:
            server_versao = result[1]
            server_att = result[2]
            embed = discord.Embed(title="Última Atualização", description=f"Versão: {server_versao}! \U0001F680", color=0x00ff00)
            embed.add_field(name="Descrição:", value=f"{server_att}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Nenhuma atualização registrada.")    
  
@bot.command()
async def atualizacao(ctx, msg: str, versao: str):
    if ctx.author.guild_permissions.administrator:
        server_versao = versao
        server_att = msg
        data_atual = datetime.datetime.now()
        
        c.execute('''CREATE TABLE IF NOT EXISTS atualizacoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        versao TEXT,
                        atualizacao TEXT,
                        data TEXT)''')
        
        c.execute("INSERT INTO atualizacoes (versao, atualizacao, data) VALUES (?, ?, ?)", (server_versao, server_att, data_atual))
        conn.commit()
        
        embed = discord.Embed(title="Atualização", description=f"Versão: {server_versao}! \U0001F680", color=0x00ff00)
        embed.add_field(name="Descrição:", value=f"{server_att}", inline=False)
        await ctx.send(embed=embed)
    else:
        c.execute("SELECT * FROM atualizacoes ORDER BY data DESC LIMIT 1")
        result = c.fetchone()
        if result:
            server_versao = result[1]
            server_att = result[2]
            embed = discord.Embed(title="Última Atualização", description=f"Versão: {server_versao}! \U0001F680", color=0x00ff00)
            embed.add_field(name="Descrição:", value=f"{server_att}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Nenhuma atualização registrada.")
                

@bot.command()
async def comoconvidar(ctx):
    if ctx.channel.id == idcanal:
     await ctx.send(f'No Discord, os membros podem convidar outras pessoas para um servidor por meio de convites. Eles podem fazer isso clicando com o botão direito do mouse no nome do servidor e selecionando a opção "Convidar Pessoas" ou clicando no ícone de configurações do servidor e selecionando a opção "Convites". Isso gera um link de convite que pode ser compartilhado com outras pessoas. Quando alguém se junta ao servidor usando esse link de convite, o membro que o compartilhou é registrado como o convidador e o uso desse convite é contabilizado.{os.linesep} Cada Membro Novo que você convidar e ele entrar no Servidor você ganha 💰 100 Pontos')

@bot.command()
async def top10(ctx):
    if ctx.channel.id == idcanal:
        c.execute('SELECT user_id, points FROM points ORDER BY points DESC LIMIT 10')
        rows = c.fetchall()
        if rows:
            embed = discord.Embed(
                title='🏆 Top 10 Fun Pontos',
                color=discord.Color.gold()
            )
            leaderboard = ""
            for i, row in enumerate(rows, 1):
                user = await bot.fetch_user(int(row[0]))
                leaderboard += f"{i}. {user.display_name} - 💰{row[1]} pontos\n"
                if i==1:
                 embed.set_thumbnail(url=user.avatar)
            embed.description = leaderboard
            await ctx.send(embed=embed)
        else:
            await ctx.send("No users found in the leaderboard.")


@bot.command()
@commands.has_permissions(administrator=True)
async def criarcodigo(ctx, codigo: str):
    c.execute('INSERT INTO codigos_premiados (codigo, valido) VALUES (?, 1)', (codigo,))
    conn.commit()
    await ctx.send(f'Código premiado "{codigo}" criado com sucesso!')

@bot.command()
async def espada(ctx):
    if ctx.channel.id == idcanal:
        c.execute("SELECT forca,nome_espada FROM espadas WHERE user_id=?", (ctx.author.id,))
        row = c.fetchone()  # Usar fetchone() em vez de fetchall()
        if row:
            forca = row[0]  # Ajustar o índice para 0
            espada = row[1]  # Ajustar o índice para 1
            await ctx.send(f'Sua Espada: {espada}  com ela você aumenta + {forca} De Farm. \n Digite /uparespada para melhorar ela. \n Espada de Madeira: +10 Farm, Espada de Ferro: +15 Farm, Espada de Bronze: +20 Farm, Espada de Ouro: +25 Farm, Espada de Diamante: +30 Farm, Espada de Fogo Flamejante: +40 Farm, Espada de Gelo Congelante: +50 Farm, Espada Ceifadora das Sombras: +60 Farm,Espada da Galaxia + 70, Espada dos Deuses + 80')
        else:
            await ctx.send(f'Você não tem espada, Digite /comprarespada.')

        
@bot.command()
async def codigopremiado(ctx):
    if ctx.channel.id == idcanal:    
     user_id = str(ctx.author.id)
     c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
     row = c.fetchone()
     if row:
        user_points = row[0]
        if user_points >= 1000:
            c.execute('SELECT codigo FROM codigos_premiados WHERE valido=1 ORDER BY RANDOM() LIMIT 1')
            premio_row = c.fetchone()
            if premio_row:
                codigo_premiado = premio_row[0]
                # Deduz 100 pontos do usuário
                new_points = user_points - 1000
                c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
                conn.commit()

                # Marca o código como inválido
                c.execute('UPDATE codigos_premiados SET valido=0 WHERE codigo=?', (codigo_premiado,))
                conn.commit()
                await ctx.author.send(f'Você trocou 💰1000 pontos pelo código premiado de :gem: 150 Diamantes: "{codigo_premiado}"!')
                await ctx.send(f'{ctx.author.display_name}Código premiado enviado para a sua DM.')
            else:
                await ctx.send('Não há códigos premiados disponíveis no momento.')
        else:
            await ctx.send(f'{ctx.author.display_name} Você não tem pontos suficientes para resgatar um código premiado. valor é de: 1000 Pontos')
     else:
        await ctx.send(f'{ctx.author.display_name} Usuário não encontrado no banco de dados, digite /criarconta , para criar usa conta.')


@bot.command()
@commands.has_permissions(administrator=True)
async def addpontos(ctx, member: discord.Member, amount: int):
    user_id = str(member.id)
    c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if row:
        current_points = row[0]
        new_points = current_points + amount
        c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
    else:
        c.execute('INSERT INTO points (user_id, points) VALUES (?, ?)', (user_id, amount))
    conn.commit()
    await ctx.send(f'Você adicionou {amount}  Pontos para {member.display_name}.')
    


    




def verificar_forca_espada(user_id):
    c.execute("SELECT forca FROM espadas WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        return row[0]  # Retorna a força da espada se o usuário possuir uma
    else:
        return 0  # Retorna 0 se o usuário não possuir uma espada
    

    
       
cooldown = 600  # Tempo de cooldown em segundos
last_farm_times = {}  # Dicionário para rastrear o último horário de resgate de cada usuário
last_farm_times2 = {}
@bot.command()
async def farmar(ctx):
    if ctx.channel.id == idcanal:
        user_id = str(ctx.author.id)
        current_time = time.time()
        if user_id in last_farm_times and current_time - last_farm_times[user_id] < cooldown:
            remaining_time = int(cooldown - (current_time - last_farm_times[user_id]))
            await ctx.send(f'{ctx.author.display_name}, você só pode farmar a cada 10 minuto. Tente novamente em {remaining_time} segundos.')
        else:
            last_farm_times[user_id] = current_time

            # Adicionar 10 pontos para o usuário no banco de dados
            c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
            row = c.fetchone()
            if row:
                pontos = random.randint(5, 15)
                pontosvip =0
                if any(role.id == vip_role_id for role in ctx.author.roles):
                    pontosvip = random.randint(20, 40)
    
                espadaPoints = verificar_forca_espada(ctx.author.id)
                pontos = pontos + espadaPoints + pontosvip
                current_points = row[0]
                new_points = current_points + pontos 
                c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
                conn.commit()
                if any(role.id == vip_role_id for role in ctx.author.roles):
                    await ctx.send(f'{ctx.author.display_name}, você farmou como vip obteve pontos a mais 💰 { pontos } pontos!')
                else:
                   await ctx.send(f'{ctx.author.display_name}, você farmou com sucesso e obteve 💰 { pontos } pontos!') 
            else:
                await ctx.send(f'{ctx.author.display_name}, usuário não encontrado no banco de dados. Digite /criarconta para começar a farmar.')

#if any(role.id == mod_role_id for role in ctx.author.roles):   
@bot.command()
async def farmarstaff(ctx):
    if ctx.channel.id == idcanal:
       if any(role.id in [mod_role_id, staff_role_id] for role in ctx.author.roles):
        user_id = str(ctx.author.id)
        current_time = time.time()
        pontos = random.randint(10, 20)
        if any(role.id == vip_role_id for role in ctx.author.roles):
            pontos=random.randint(20, 40)
        if user_id in last_farm_times2 and current_time - last_farm_times2[user_id] < cooldown:
            remaining_time = int(cooldown - (current_time - last_farm_times2[user_id]))
            await ctx.send(f'{ctx.author.display_name}, você só pode farmar a cada 10 minuto. Tente novamente em {remaining_time} segundos.')
        else:
            last_farm_times2[user_id] = current_time

            # Adicionar 10 pontos para o usuário no banco de dados
            c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
            row = c.fetchone()
            if row:
                espadaPoints = verificar_forca_espada(ctx.author.id)
                pontos = pontos + espadaPoints
                current_points = row[0]
                new_points = current_points + pontos
                c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
                conn.commit()
                await ctx.send(f'{ctx.author.display_name}, você farmou com sucesso e obteve 💰{pontos} pontos!')
            else:
                await ctx.send(f'{ctx.author.display_name}, usuário não encontrado no banco de dados. Digite /criarconta para começar a farmar.')
        
last_daily_rewards = {}  # Dicionário para armazenar o último resgate diário de cada usuário

@bot.command()
async def recompensadiaria(ctx):
 if ctx.channel.id == idcanal:
    user_id = str(ctx.author.id)
    current_time = datetime.datetime.now()

    if user_id in last_daily_rewards:
        last_reward_time = last_daily_rewards[user_id]
        time_difference = current_time - last_reward_time
        if time_difference.days < 1:
            await ctx.send(f'{ctx.author.display_name} Você já resgatou a recompensa 💰 diária hoje. Tente novamente amanhã.')
            return

    # Adicionar 10 pontos para o usuário na tabela "points"
    c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
    pontos  = 100
    if any(role.id == vip_role_id for role in ctx.author.roles):
     pontos =200
    row = c.fetchone()
    if row:
        current_points = row[0]
        pointsvip = 0;
        if any(role.id == vip_role_id for role in ctx.author.roles):
            pointsvip = 100;
        new_points = current_points + pontos + pointsvip
        c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
    else:
        c.execute('INSERT INTO points (user_id, points) VALUES (?, ?)', (user_id, pontos))
    conn.commit()

    last_daily_rewards[user_id] = current_time
    await ctx.send(f'{ctx.author.display_name} Você resgatou a recompensa diária com sucesso. Você recebeu 💰 100 pontos.')   
    
@bot.command()
async def baudasorte(ctx):
 if ctx.channel.id == idcanal:
    user_id = str(ctx.author.id)

    # Verificar se o usuário tem pelo menos 20 pontos
    c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if row:
        current_points = row[0]
        if current_points < 20:
            await ctx.send('Você não tem 20 pontos suficientes para jogar.')
            return
    else:
        await ctx.send('Você não tem 20 pontos suficientes para jogar.')
        return

    # Deduzir 20 pontos do usuário
    new_points = current_points - 20
    c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))

    # Realizar a roleta da sorte
    outcome = random.choices(['win50', 'win40', 'lose'], weights=[0.1, 0.2, 0.7], k=1)[0]

    if outcome == 'win50':
        new_points = new_points + 70
        c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
        await ctx.send('Parabéns! Você ganhou 50 pontos.')
    elif outcome == 'win40':
        new_points = new_points + 60
        c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
        await ctx.send('Você ganhou 40 pontos.')
    else:
        await ctx.send('Você perdeu 20 pontos,Não foi dessa vez. Tente novamente.')

    conn.commit()         
                   





async def soltar_codigo(channel, intervalo, pontos, valor):
    while True:
        await asyncio.sleep(intervalo)
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        c.execute('INSERT INTO codigos_unicos (codigo, valido, pontos) VALUES (?, 1, ?)', (codigo, pontos))
        conn.commit()
        await channel.send(f'Código Premiado de Pontos do FunBot: "{codigo}"\nPara resgatar o Código de {valor} Pontos digite /resgatarpontos {codigo}')
        print(f'Código Premiado de {valor} Pontos do FunBot: "{codigo}", para resgatar digite /resgatarpontos')



     
async def soltar_codigoCriadorConteudo():
    channel = bot.get_channel(idcanal_criadorconteudo)  # Substitua YOUR_CHANNEL_ID pelo ID do canal específico
    while True:
        await asyncio.sleep(2800)  # Espera 30 minutos
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # Gera um código único
        c.execute('INSERT INTO codigos_unicos (codigo, valido, pontos) VALUES (?, 1, 50)', (codigo,))
        conn.commit()
        await channel.send(f'Código Premiado de Pontos do FunBot Para Criadores de Conteudo: "{codigo}"\nPara resgatar o Código de 💰 100 Pontos digite /resgatarpontos {codigo}')
        print(f'Código Premiado de  💰 100 Pontos do FunBot Especial para Criadores de Conteudo: "{codigo}", para resgatar digite /resgatarpontos')





@bot.command()
async def resgatarpontos(ctx, codigo: str):
 if ctx.channel.id == idcanal:
    c.execute('SELECT valido,pontos FROM codigos_unicos WHERE codigo=?', (codigo,))
    row = c.fetchone()
    if row and row[0] == 1:
        pontos = row[1]
        user_id = str(ctx.author.id)
        c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
        row = c.fetchone()
        if row:
            current_points = row[0]
            new_points = current_points + pontos
            c.execute('UPDATE points SET points=? WHERE user_id=?', (new_points, user_id))
        else:
            c.execute('INSERT INTO points (user_id, points) VALUES (?, ?)', (user_id, 10))
        c.execute('UPDATE codigos_unicos SET valido=0 WHERE codigo=?', (codigo,))
        conn.commit()
        await ctx.send(f'{ctx.author.display_name} Parabéns! Você resgatou o código Premiado de FunPontos "{codigo}" e ganhou 💰 {pontos} pontos.')
    else:
        await ctx.send('Código inválido ou já resgatado.')
              
              
#--------------------------------EVENTOS---------------------------------#
invites_count = {}


@bot.event
async def on_member_join(member):
    # Obter a lista de convites do servidor
    invites = await member.guild.invites()
    channel = bot.get_channel(idcanal_entrada)  # Substitua idcanal_entrada pelo ID do canal de boas-vindas
    if channel:
        embed = discord.Embed(
            title=f'👉 Bem-vindo ao servidor, {member.name}!',
            description='Esperamos que você se divirta e aproveite sua estadia.',
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar)
        await channel.send(embed=embed)

    # Verificar se o membro já existe na tabela de invites
    c.execute('SELECT * FROM invites WHERE convidado_id = ?', (member.id,))
    existing_member = c.fetchone()
    if existing_member:
        return  # Se o membro já existe, não faz nada

    # Atualizar a contagem de convites para cada convidador no banco de dados
    for invite in invites:
        inviter_id = invite.inviter.id
        c.execute('UPDATE points SET points = points + 100 WHERE user_id = ?', (inviter_id,))
        c.execute('INSERT OR IGNORE INTO invites (convidador_id, convidado_id) VALUES (?, ?)', (str(inviter_id), str(member.id)))
        c.execute('UPDATE invites SET invites_count = invites_count + 1 WHERE convidador_id = ?', (str(inviter_id),))

    # Salvar as alterações e fechar a conexão com o banco de dados
    conn.commit()
    
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(idcanal_logstaff)  # Substitua idcanal_logstaff pelo ID do canal para enviar a mensagem
    if channel:
        await channel.send(f'O membro {member.name} saiu do servidor. Até logo!')
        
        
   
    
    
message_count = {}

@bot.event
async def on_message(message):
    if message.channel.id == idcanal_chatgeral:  # Substitua SEU_CANAL_ID pelo ID do canal específico
        user_id = str(message.author.id)
        if user_id not in message_count:
            message_count[user_id] = 1
        else:
            message_count[user_id] += 1
            if message_count[user_id] > 10:
                await addexpintern(message.channel,message.author.id, 50)
                message_count[user_id] = 0  # Zera o contador
    await bot.process_commands(message)
    
    
@bot.event
async def on_ready():
    allow_resgate.start()
    allow_resgatestaff.start()
    await soltar_codigo(bot.get_channel(idcanal_chatgeral), 1800, 40, '💰40')
    await soltar_codigo(bot.get_channel(idcanal_criadorconteudo), 2400, 50, '💰50')

async def soltar_codigo(channel, intervalo, pontos, valor):
    while True:
        await asyncio.sleep(intervalo)
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        c.execute('INSERT INTO codigos_unicos (codigo, valido, pontos) VALUES (?, 1, ?)', (codigo, pontos))
        conn.commit()
        await channel.send(f'Código Premiado de Pontos do FunBot: "{codigo}"\nPara resgatar o Código de {valor} Pontos digite /resgatarpontos {codigo}')
        print(f'Código Premiado de {valor} Pontos do FunBot: "{codigo}", para resgatar digite /resgatarpontos')

last_resgate_times = {} 
last_resgate_timesStaff = {} 
@tasks.loop(minutes=1)
async def allow_resgate():
    for user_id, last_time in list(last_resgate_times.items()):
        current_time = time.time()
        if current_time - last_time >= 600:  # 60 segundos = 1 minuto
            del last_resgate_times[user_id]

@tasks.loop(minutes=1)
async def allow_resgatestaff():
    for user_id, last_time in list(last_resgate_timesStaff.items()):
        current_time = time.time()
        if current_time - last_time >= 600:  # 60 segundos = 1 minuto
            del last_resgate_timesStaff[user_id]


#--------------------------------- FIM EVENTOS -----------------------------------------------------
@bot.command()
async def topconvites(ctx):
    if ctx.channel.id == idcanal:   
        invites = await ctx.guild.invites()
        sorted_invites = sorted(invites, key=lambda invite: invite.uses, reverse=True)[:15]

        unique_invites = []  # Lista para armazenar convites únicos

        for invite in sorted_invites:
            if invite.inviter.name not in [i.inviter.name for i in unique_invites]:  # Verifica se o nome do convidador já está na lista de convites únicos
                unique_invites.append(invite)  # Adiciona o convite à lista de convites únicos

        embed = discord.Embed(
            title='🏆 Top 15 Convites',
            color=discord.Color.gold()
        )

        for index, invite in enumerate(unique_invites):
            member = ctx.guild.get_member(invite.inviter.id)
            if member:
                inviter_name = member.name
            else:
                inviter_name = 'Usuário Desconhecido'

            if invite.inviter.id == invite.inviter.id:
                status = 'Regular'
            else:
                status = 'Left'

            embed.add_field(
                name=f'{index + 1}. {inviter_name} . Convites: {invite.uses} - Status: {status}',
                value='',
                inline=False
            )

        await ctx.send(embed=embed)    
        

@bot.command()
async def saldo(ctx):
    if ctx.channel.id == idcanal:   
        user_id = str(ctx.author.id)
        c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
        row = c.fetchone()
        if row:
            points = row[0]
        else:
            points = 0
        
        c.execute('SELECT nome_espada FROM espadas WHERE user_id=?', (user_id,))
        espada=''
        row = c.fetchone()
        if row:
            espada = row[0]    
        
        c.execute('SELECT exp, level, category FROM users WHERE user_id=?', (user_id,))
        row = c.fetchone()
        if row:
            exp, level, category = row
            c.execute('SELECT guilda FROM guildas WHERE user_id=?', (user_id,))
            row_guilda = c.fetchone()
            if row_guilda:
                guilda = row_guilda[0]
            else:
                guilda = "Sem guilda"
            vip = 'não'    
            if any(role.id == vip_role_id for role in ctx.author.roles):  
                vip = "sim"  
            embed = discord.Embed(title="Status", description=f"Seu Perfil ↓ \n Nome: {ctx.author.display_name}\n Exp: {exp}\nLevel: {level}\n titutlo: {category}\nFunPontos: {points} \nEspada: {espada}\n Guilda: {guilda}\n Vip: {vip}", color=0x00ff00)
            embed.set_thumbnail(url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Você não tem um status registrado.")       
    else:
        await ctx.send("Este comando só pode ser usado em um canal específico.")


@bot.command()
async def meustatus(ctx):
    if ctx.channel.id == idcanal:   
        user_id = str(ctx.author.id)
        c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
        row = c.fetchone()
        if row:
            points = row[0]
        else:
            points = 0
        
        c.execute('SELECT nome_espada FROM espadas WHERE user_id=?', (user_id,))
        espada=''
        row = c.fetchone()
        if row:
            espada = row[0]    
        
        c.execute('SELECT exp, level, category FROM users WHERE user_id=?', (user_id,))
        row = c.fetchone()
        if row:
            exp, level, category = row
            c.execute('SELECT guilda FROM guildas WHERE user_id=?', (user_id,))
            row_guilda = c.fetchone()
            if row_guilda:
                guilda = row_guilda[0]
            else:
                guilda = "Sem guilda"
            vip = 'não'    
            if any(role.id == vip_role_id for role in ctx.author.roles):  
                vip = "sim"  
            embed = discord.Embed(title="Status", description=f"Seu Perfil ↓ \n Nome: {ctx.author.display_name}\n Exp: {exp}\nLevel: {level}\n titutlo: {category}\nFunPontos: {points} \nEspada: {espada}\n Guilda: {guilda}\n Vip: {vip}", color=0x00ff00)
            embed.set_thumbnail(url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Você não tem um status registrado.")       
    else:
        await ctx.send("Este comando só pode ser usado em um canal específico.")

@bot.command()        
async def categoria(ctx):
    if ctx.channel.id == idcanal:  
        c.execute('SELECT category,level FROM users WHERE user_id=?', (ctx.author.id,))
        row = c.fetchone()
        if row:
            level = row[1]
            category = row[0]  
            if level >= 5 and level <10:
                id_role = idiniciante
                category = 'Iniciante'
            elif  level >= 10 and level <20:
                id_role = idintermediario
                category = 'Intermediario' 
            elif level >= 20 and level <30:
                id_role = idavançado
                category = 'Avançado' 
            elif  level >= 30 and level <40:
                id_role = idespecialista
                category = 'Especialista' 
            elif  level >= 40 and level <50:
                id_role = idmestre
                category = 'Mestre'
            elif  level >= 50 and level <60:
                id_role = idlendario
                category = 'Lendario' 
            elif  level >= 60 and level <70:
                id_role = idsupremo
                category = 'Supremo' 
            elif   level >= 70:
                category = 'MestreSupremo'
                id_role = idmestresupremo
     
            c.execute('UPDATE users SET category = ? WHERE user_id = ?', (category,ctx.author.id,))
            await ctx.send(f'{ctx.author.mention} Seu Level é: {level} Seu Cargo è: "{category}"')
            role = ctx.guild.get_role(id_role)
            if role:
                if role in ctx.author.roles:
                    return
                else:
                    await ctx.author.add_roles(role)
                    c.execute('UPDATE points SET points = points + 100 WHERE user_id = ?', (ctx.author.id,))
                    conn.commit()
                    await ctx.send(f'{ctx.author.mention} Parabéns, você recebeu o cargo "{category}" e mais 💰 100 Pontos!')
            else:
                await ctx.send('A função não foi encontrada.')
        else:
            await ctx.send('Categoria não encontrada no banco de dados para este usuário.')
    else:
        await ctx.send("Este comando só pode ser usado em um canal específico.")

async def attcategoria(ctx):
    if ctx.channel.id == idcanal:  
        c.execute('SELECT category,level FROM users WHERE user_id=?', (ctx.author.id,))
        row = c.fetchone()
        if row:
            level = row[1]
            category = row[0]  
            if level >= 5 and level <10:
                id_role = idiniciante
                category = 'Iniciante'
            elif  level >= 10 and level <20:
                id_role = idintermediario
                category = 'Intermediario' 
            elif level >= 20 and level <30:
                id_role = idavançado
                category = 'Avançado' 
            elif  level >= 30 and level <40:
                id_role = idespecialista
                category = 'Especialista' 
            elif  level >= 40 and level <50:
                id_role = idmestre
                category = 'Mestre'
            elif  level >= 50 and level <60:
                id_role = idlendario
                category = 'Lendario' 
            elif  level >= 60 and level <70:
                id_role = idsupremo
                category = 'Supremo' 
            elif   level >= 70:
                category = 'MestreSupremo'
                id_role = idmestresupremo
     
            c.execute('UPDATE users SET category = ? WHERE user_id = ?', (category,ctx.author.id,))
            await ctx.send(f'{ctx.author.mention} seu Cargo è: "{category}"')
            role = ctx.guild.get_role(id_role)
            if role:
                if role in ctx.author.roles:
                    return
                else:
                    await ctx.author.add_roles(role)
                    c.execute('UPDATE points SET points = points + 100 WHERE user_id = ?', (ctx.author.id,))
                    conn.commit()
                    await ctx.send(f'{ctx.author.mention} Parabéns, você recebeu o cargo "{category}" e mais 💰 100 Pontos!')
            else:
                await ctx.send('A função não foi encontrada.')
        else:
            await ctx.send('Categoria não encontrada no banco de dados para este usuário.')
    else:
        await ctx.send("Este comando só pode ser usado em um canal específico.")
                
@bot.command()
@commands.has_permissions(administrator=True)
async def addexp(ctx, member: discord.Member, exp: int):
    user_id = str(member.id)
    c.execute('SELECT exp, level FROM users WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if row:
        current_exp = row[0]
        level = row[1]
        new_exp = current_exp + exp
        if new_exp >= 100:
            new_exp -= 100
            level += 1
            category='Iniciante'
            categories = ["Iniciante", "Intermediario", "Avançado", "Especialista", "Mestre", "Lendario", "Supremo","MestreSupremo"]
            if level == 5:
                category = categories[1]
                c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
                await ctx.send(f'Categoria Atualizada {category}.')
            elif  level == 10:
                category = categories[2]
                c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
                await ctx.send(f'Categoria Atualizada {category}.')
            elif  level == 20:
                category = categories[3]   
                c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
                await ctx.send(f'Categoria Atualizada {category}.')    
            elif  level == 30:
                category = categories[4]  
                c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
                await ctx.send(f'Categoria Atualizada {category}.') 
            elif  level == 40:
                category = categories[5]  
                c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
                await ctx.send(f'Categoria Atualizada {category}.')
            elif  level == 50:
                category = categories[6]   
                c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
                await ctx.send(f'Categoria Atualizada {category}.') 
            elif  level == 60:
                category = categories[7]   
                c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
                await ctx.send(f'Categoria Atualizada {category}.')                                                                                 
            c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
        else:
            await ctx.send(f'Somente ganho EXP.')
            c.execute('UPDATE users SET exp=? WHERE user_id=?', (new_exp, user_id))
    else:
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, exp, 1, "Iniciante"))
    conn.commit()
    await ctx.send(f'100 pontos adicionados a {member.display_name}.')




async def addexpintern(usuario,user:str, exp: int):
    user_id = str(user)
     # Verificar se o usuário já está registrado na tabela points
    c.execute('SELECT * FROM points WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if row:
        # O usuário já está registrado na tabela points
        # Verificar se o usuário já está registrado na tabela users
        c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        row_users = c.fetchone()
        if not row_users:
            # O usuário não está registrado na tabela users, adicionar o novo usuário
            c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, 0, 1, "Iniciante"))
    c.execute('SELECT exp, level FROM users WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if row:
        current_exp = row[0]
        level = row[1]
        new_exp = current_exp + exp
        if new_exp >= 100:
            new_exp -= 100
            level +=1
            category='Iniciante'
            categories = ["Iniciante", "Intermediario", "Avançado", "Especialista", "Mestre", "Lendario", "Supremo","MestreSupremo"]
            if level == 5:
              category = categories[1]
              c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
            elif level == 10:
              category = categories[2]
              c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
            elif level == 20:
              category = categories[3]       
              c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
            elif  level == 30:
              category = categories[4] 
              c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))  
            elif  level == 40:
              category = categories[5]
              c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
            elif  level == 50:
              category = categories[6]
              c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
            elif  level == 60:
              category = categories[7]
              c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))              
                                                   
            c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))                       
        else:
            c.execute('UPDATE users SET exp=? WHERE user_id=?', (new_exp, user_id))
    else:
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, exp, 1, "Iniciante"))
    conn.commit()
    



@bot.command()
async def comprarexp(ctx):
    user_id = ctx.author.id
    c.execute('SELECT exp, level, category FROM users WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if row:
        current_exp = row[0]
        level = row[1]
        category = row[2]
    else:
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, 0, 1, "Iniciante"))
        conn.commit()
        await ctx.send('Novo usuário registrado.')
        return

    c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if row:
        mypoints = row[0]
    else:
        mypoints = 0

    if mypoints < 100:
        await ctx.send('Pontos insuficientes para comprar EXP.')
        return

    c.execute('UPDATE points SET points = points - 100 WHERE user_id=?', (user_id,))
    new_exp = current_exp + 100

    if new_exp >= 100:
        new_exp -= 100
        gained_exp = random.randint(10, 100)
        new_exp += gained_exp

        if new_exp >= 100:
            new_exp -= 100
            level += 1
            categories = ["Iniciante", "Intermediario", "Avançado", "Especialista", "Mestre", "Lendario", "Supremo", "MestreSupremo"]
            if level in [5, 10, 20, 30, 40, 50, 60]:
                category = categories[level // 10]

            c.execute('UPDATE users SET exp=?, level=?, category=? WHERE user_id=?', (new_exp, level, category, user_id))
            conn.commit()
            await ctx.send(f'Categoria Atualizada para {category}.')
        else:
            c.execute('UPDATE users SET exp=? WHERE user_id=?', (new_exp, user_id))
            conn.commit()
            await ctx.send(f'{gained_exp} pontos de EXP adicionados para {ctx.author.display_name}.')
    else:
        await ctx.send('Erro ao adicionar EXP.')



@bot.command()
async def sortearpontos(ctx, quantidade: int):
  if ctx.channel.id == idcanal_sorteio:
    if quantidade < 50:
        await ctx.send("A quantidade mínima para ser sorteado é de 50 pontos.")
        return

    c.execute("SELECT user_id FROM points WHERE points >= 50 ORDER BY RANDOM() LIMIT 1")
    user_sorteado = c.fetchone()
    if user_sorteado:
        if str(user_sorteado[0]) != str(ctx.author.id):
            c.execute("SELECT points FROM points WHERE user_id = ?", (str(ctx.author.id),))
            user = c.fetchone()
            if user and user[0] >= quantidade:
                c.execute("UPDATE points SET points = points - ? WHERE user_id = ?", (quantidade, str(ctx.author.id)))
                c.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (quantidade, user_sorteado[0]))
                conn.commit()
                await ctx.send(f"{quantidade} pontos foram sorteados para <@{user_sorteado[0]}>!")
            else:
                await ctx.send("Você não tem pontos suficientes para realizar este sorteio.")
        else:
            await ctx.send("Você não pode se sortear!")
    else:
        await ctx.send("Não há usuários com pelo menos 50 pontos para serem sorteados.")


        
@bot.command()
async def sortearparaamigos(ctx, quantidade: int, *usuarios: discord.Member):
    if ctx.channel.id == idcanal_sorteio:
        if quantidade < 50:
            await ctx.send("A quantidade mínima para ser sorteado é de 50 pontos.")
            return

        if len(usuarios) < 2:
            await ctx.send("Você precisa mencionar pelo menos dois usuários para o sorteio.")
            return

        for usuario in usuarios:
            c.execute("SELECT points FROM points WHERE user_id = ?", (str(usuario.id),))
            user = c.fetchone()
            if not user or user[0] < 50:
                await ctx.send(f"O usuário {usuario.mention} não tem pontos suficientes para participar do sorteio.")
                return

        user_sorteado = random.choice(usuarios)
        while str(user_sorteado.id) == str(ctx.author.id):
            user_sorteado = random.choice(usuarios)

        quantidade_por_usuario = quantidade // len(usuarios)

        for usuario in usuarios:
            c.execute("UPDATE points SET points = points - ? WHERE user_id = ?", (quantidade_por_usuario, str(ctx.author.id)))

        c.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (quantidade, str(user_sorteado.id)))
        conn.commit()
        await ctx.send(f"{quantidade} pontos foram sorteados para {user_sorteado.mention}!")
    else:
        await ctx.send("Este comando só pode ser usado no canal de sorteios.")
        
        
@bot.command()
async def comprarespada(ctx):
 if ctx.channel.id == idcanal:
    preco_espada = 50  # Preço da espada
    user_id = str(ctx.author.id)
    nome_espada = "Espada de Madeira"  # Nome da espada a ser comprada
    forca_espada = 5  # Força da espada de madeira
    
    c.execute("SELECT points FROM points WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row and row[0] >= preco_espada:
        c.execute("INSERT INTO espadas (nome_espada, forca, user_id) VALUES (?, ?, ?)", (nome_espada, forca_espada, user_id))
        c.execute("UPDATE points SET points = points - ? WHERE user_id = ?", (preco_espada, user_id))
        conn.commit()
        await ctx.send(f"{ctx.author.display_name} Você comprou a espada {nome_espada}!")
    else:
        await ctx.send(f"{ctx.author.display_name} Você não tem pontos suficientes para comprar esta espada.")

@bot.command()
async def uparespada(ctx):
    if ctx.channel.id == idcanal: 
        user_id = str(ctx.author.id)
        
        c.execute("SELECT forca, points FROM espadas INNER JOIN points ON espadas.user_id = points.user_id WHERE espadas.user_id=?", (user_id,))
        row = c.fetchone()
        if row:
            forca_espada = row[0]
            pontos_usuario = row[1]
            custo_up=0
            if forca_espada >= 10 and forca_espada < 20:
                custo_up = 100
            if forca_espada >= 120 and forca_espada < 30:
                custo_up = 200                
            if forca_espada >= 30 and forca_espada < 40:
                custo_up = 400
            if forca_espada >= 40 and forca_espada < 50:
                custo_up = 800
            if forca_espada >= 50 and forca_espada < 60:
                custo_up = 1600   
            if forca_espada >= 60 and forca_espada < 70:
                custo_up = 3200  
            if forca_espada >= 70 and forca_espada < 80:
                custo_up = 7200
            if forca_espada >= 80 and forca_espada < 90:
                custo_up = 14400                                               
            custo_up = forca_espada * 10  # Custo para upar a espada baseado na força
            
            if pontos_usuario >= custo_up:
                c.execute("UPDATE espadas SET forca = forca + 5 WHERE user_id = ?", (user_id,))
                c.execute("UPDATE points SET points = points - ? WHERE user_id = ?", (custo_up, user_id))
                conn.commit()
                
                if forca_espada == 5:
                    nome_espada = "Espada de Madeira"
                elif forca_espada == 10:
                    nome_espada = "Espada de Ferro"
                elif forca_espada == 15:
                    nome_espada = "Espada de Bronze"
                elif forca_espada == 20:
                    nome_espada = "Espada de Ouro"
                elif forca_espada == 25:
                    nome_espada = "Espada de Diamante"
                elif forca_espada == 30:
                    nome_espada = "Espada de Fogo Flamejante"
                elif forca_espada == 40:
                    nome_espada = "Espada de Gelo Congelante"
                elif forca_espada == 50:
                    nome_espada = "Espada Ceifadora das Sombras"
                elif forca_espada >= 60 and  forca_espada < 70:
                    nome_espada = "Espada da Galaxia"
                elif forca_espada >= 70 and  forca_espada < 80:
                    nome_espada = "Espada dos Deuses"
                # Adicione mais condições conforme necessário
                
                c.execute("UPDATE espadas SET nome_espada = ? WHERE user_id = ?", (nome_espada, user_id))
                conn.commit()
                
                await ctx.send(f"{ctx.author.display_name} Você upou a sua espada para {forca_espada} de força. Ela agora é uma {nome_espada}!")
            else:
                await ctx.send(f"{ctx.author.display_name} Você não tem pontos suficientes para upar a sua espada. Força atual da sua espada é: {row[0]}")
        else:
            await ctx.send(f"{ctx.author.display_name} Você não possui uma espada. Digite /comprarespada para obter")


     
@bot.command()
@commands.has_permissions(administrator=True)
async def criarproduto(ctx, nome: str, custo: int, codigo: str):
    c.execute('INSERT INTO produtos (nome, custo, codigo) VALUES (?, ?, ?)', (nome, custo, codigo))
    conn.commit()
    finalcod = codigo[6:]
    await ctx.send(f'O produto "{nome}" foi criado com final: {finalcod} codigo.scom sucesso!')
    await ctx.message.delete()

@bot.command()
async def lojinha(ctx):
  if ctx.channel.id == idcanal:  
    embed = discord.Embed(title="Loja de Produtos", description="Produtos disponíveis para compra:")
    c.execute('SELECT nome, MIN(custo) as custo FROM produtos GROUP BY nome ORDER BY custo ASC')
    produtos = c.fetchall()
    for produto in produtos:
        nome = produto[0]
        custo = produto[1]
        embed.add_field(name=nome, value=f"Preço: {custo} pontos", inline=False)
    embed.add_field(name="Para Comprar", value="Exemplo Digite: /comprar 50Diamantes", inline=False)   
    await ctx.send(embed=embed)

    


last_compra_times = {}  # Dicionário para rastrear o último horário de compra de cada usuário

@bot.command()
async def comprar(ctx, nome: str):
    if ctx.channel.id == idcanal:
        user_id = str(ctx.author.id)
        
        current_time = datetime.datetime.now()
        last_compra_time = last_compra_times.get(user_id, datetime.datetime.min)
        
        if (current_time - last_compra_time).days < 1:
            await ctx.send(f'{ctx.author.display_name}, você só pode comprar uma vez por dia.')
            return
        
        c.execute('SELECT points FROM points WHERE user_id=?', (user_id,))
        row = c.fetchone()
        
        if row:
            user_points = row[0]
            c.execute('SELECT custo, codigo FROM produtos WHERE nome=?', (nome,))
            produto = c.fetchone()
            
            if produto and user_points >= produto[0]:
                novo_pontos = user_points - produto[0]
                c.execute('DELETE FROM produtos WHERE nome=? LIMIT 1', (nome,))
                c.execute('UPDATE points SET points=? WHERE user_id=?', (novo_pontos, user_id))
                conn.commit()
                
                last_compra_times[user_id] = current_time  # Atualiza o horário da última compra
                
                await ctx.send(f'{ctx.author.display_name}, você comprou o produto "{nome}" por {produto[0]} pontos!')
                await ctx.author.send(f'{ctx.author.display_name}, você trocou {produto[0]} pontos pelo código premiado: "{produto[1]}"!')
                await ctx.send(f'{ctx.author.display_name}, código premiado enviado para a sua DM.')
            else:
                await ctx.send(f'{ctx.author.display_name}, você não tem pontos suficientes para comprar este produto.')
        else:
            await ctx.send(f'{ctx.author.display_name}, usuário não encontrado no banco de dados.')

        
        
@bot.command()
async def addguilda(ctx, tag_guilda: str):
    c.execute("SELECT points FROM points WHERE user_id = ?", (str(ctx.author.id),))
    user_points = c.fetchone()
    if user_points and user_points[0] >= 100:
        if len(tag_guilda) <= 3:
            c.execute("INSERT INTO guildas (guilda, user_id) VALUES (?, ?)", (tag_guilda, str(ctx.author.id)))
            c.execute("UPDATE points SET points = points - 100 WHERE user_id = ?", (str(ctx.author.id),))
            conn.commit()
            await ctx.send(f"Tag da guilda '{tag_guilda}' registrada com sucesso para o usuário {ctx.author.mention}.")
        else:
            await ctx.send("A tag da guilda deve ter no máximo 3 caracteres.")
    else:
        await ctx.send(f"{ctx.author.mention}, você não tem pontos suficientes para registrar a tag da guilda.")

@bot.command()
async def sortearparaguilda(ctx, guilda: str, quantidade: int):
    if ctx.channel.id == idcanal_sorteio:
        if quantidade < 50:
            await ctx.send("A quantidade mínima para ser sorteado é de 50 pontos.")
            return

        c.execute("SELECT user_id FROM guildas WHERE guilda = ?", (guilda,))
        users = c.fetchall()
        if users:
            user_sorteado = random.choice(users)
            if str(user_sorteado[0]) != str(ctx.author.id):
                c.execute("SELECT points FROM points WHERE user_id = ?", (str(ctx.author.id),))
                user = c.fetchone()
                if user and user[0] >= quantidade:
                    c.execute("UPDATE points SET points = points - ? WHERE user_id = ?", (quantidade, str(ctx.author.id)))
                    c.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (quantidade, user_sorteado[0]))
                    conn.commit()
                    await ctx.send(f"{quantidade} pontos foram sorteados para <@{user_sorteado[0]}>!")
                else:
                    await ctx.send("Você não tem pontos suficientes para realizar este sorteio.")
            else:
                await ctx.send("Você não pode se sortear!")
        else:
            await ctx.send("Não há usuários na guilda especificada.")
    else:
        await ctx.send("Este comando só pode ser usado no canal de sorteios.")

@bot.command()
async def rifa(ctx):
    c.execute("SELECT * FROM Rifas")
    rifa = c.fetchone()
    if rifa:
        data_final = datetime.datetime.strptime(rifa[0], '%Y-%m-%d %H:%M:%S')
        participantes = rifa[1].split("_")
        premio = 50 + (25 * len(participantes))
        if datetime.datetime.now() > data_final:
            ganhador = random.choice(participantes)
            c.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (premio, ganhador))
            c.execute("DELETE FROM Rifas")
            conn.commit()
            await ctx.send(f"O ganhador da rifa é <@{ganhador}>! Ele ganhou {premio} pontos!")
        else:
            await ctx.send(f"A rifa termina em {data_final}. Há {len(participantes)} participantes e o prêmio é de {premio} pontos.")
    else:
        data_final = (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')  # Convertendo para string
        c.execute("INSERT INTO Rifas (datafinal, participantes) VALUES (?, ?)", (data_final, f"{ctx.author.id}_"))
        c.execute("UPDATE points SET points = points - 25 WHERE user_id = ?", (ctx.author.id,))
        conn.commit()
        await ctx.send("Rifa criada! Você está participando.")

        
@bot.command()
async def participar(ctx):
    c.execute("SELECT * FROM Rifas")
    rifa = c.fetchone()
    if rifa:
        data_final = datetime.datetime.strptime(rifa[0], '%Y-%m-%d %H:%M:%S')  # Convertendo para datetime
        if datetime.datetime.now() < data_final:
            c.execute("UPDATE Rifas SET participantes = participantes || ? WHERE datafinal = ?", (f"{ctx.author.id}_", rifa[0]))  # Usando rifa[0] em vez de data_final
            c.execute("UPDATE points SET points = points - 25 WHERE user_id = ?", (ctx.author.id,))
            conn.commit()
            participantes = rifa[1].split("_")
            premio = 50 + (25 * len(participantes))
            await ctx.send(f"Você já está participando da rifa! Ela termina em {data_final}. O prêmio final é de {premio} pontos.")
            await ctx.send("Você está participando da rifa!")
        else:
            await ctx.send("A rifa já terminou.")
    else:
        await ctx.send("Não há nenhuma rifa ativa no momento.")
 
 
        
bot.run('')
