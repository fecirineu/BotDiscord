# 🎮 Game Discord Bot

Um bot Discord de gamificação com sistema de pontos, níveis, experiência, espadas, guildas e muito mais! Desenvolvido para criar uma experiência envolvente de RPG dentro do seu servidor Discord.
desenvolvido para fins educacionais.

## ✨ Funcionalidades Principais

### 💰 Sistema de Economia
- **Farm de Pontos**: Ganhe pontos a cada 10 minutos
- **Recompensa Diária**: Receba 100 pontos diários (200 para VIPs)
- **Baú da Sorte**: Aposte pontos e tente ganhar até 50 pontos extras
- **Doação entre usuários**: Transfira pontos para outros jogadores
- **Sistema de Convites**: Ganhe 100 pontos por cada novo membro convidado

### 📊 Sistema de Progressão
- **Níveis e Experiência**: Sistema de XP baseado em atividade no chat
- **Categorias de Jogador**: 8 níveis diferentes (Iniciante até MestreSupremo)
- **Cargos Automáticos**: Receba cargos Discord baseados no seu nível
- **Compra de EXP**: Acelere sua progressão gastando pontos

### ⚔️ Sistema de Equipamentos
- **10 Tipos de Espadas**: De Madeira até Espada dos Deuses
- **Sistema de Upgrade**: Melhore sua espada para aumentar o farm
- **Bônus de Farm**: Espadas fornecem pontos extras ao farmar

### 🏰 Sistema de Guildas
- **Criação de Guildas**: Crie ou entre em uma guilda (até 3 caracteres)
- **Sorteios para Guildas**: Sorteie pontos exclusivamente para membros da guilda

### 🎰 Sistemas de Sorteio e Rifas
- **Sorteio Público**: Sorteie pontos para qualquer usuário do servidor
- **Sorteio para Amigos**: Sorteie especificamente para usuários mencionados
- **Sistema de Rifas**: Participe de rifas automáticas com prêmios crescentes

### 🏪 Loja e Códigos
- **Loja de Produtos**: Troque pontos por códigos de diamantes do jogo
- **Códigos Automáticos**: Códigos são liberados automaticamente nos canais
- **Códigos Premiados**: Sistema de resgate de códigos especiais

### 👑 Sistema VIP
- **Benefícios Exclusivos**: Dobro de pontos em farm e recompensas diárias
- **Canal Exclusivo**: Acesso a conteúdos especiais

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **discord.py**: Biblioteca principal para integração com Discord
- **SQLite3**: Banco de dados local para persistência
- **asyncio**: Programação assíncrona para tarefas em background
- **datetime**: Manipulação de datas e cooldowns
- **random**: Sistema de sorteios e drops aleatórios

## 📋 Comandos Disponíveis

### Comandos Básicos
```
/criarconta - Cria sua conta no sistema
/saldo - Verifica seu saldo e status
/meustatus - Informações detalhadas da conta
/ajuda - Lista de comandos básicos
/dicas - Acesso ao canal de dicas
```

### Comandos de Economia
```
/farmar - Farma pontos (cooldown 10min)
/recompensadiaria - Coleta recompensa diária
/baudasorte - Jogo de aposta com pontos
/doar @usuario quantidade - Doa pontos para outro usuário
/top10 - Ranking dos usuários com mais pontos
```

### Comandos de Progressão
```
/categoria - Verifica/atualiza sua categoria
/comprarexp - Compra EXP com pontos
```

### Comandos de Equipamentos
```
/comprarespada - Compra espada de madeira (50 pontos)
/uparespada - Melhora sua espada
/espada - Informações sobre sua espada atual
```

### Comandos de Loja
```
/lojinha - Ver produtos disponíveis
/comprar produto - Compra um produto
/codigopremiado - Troca pontos por código premiado (1000 pontos)
/resgatarpontos codigo - Resgata código de pontos
```

### Comandos de Guildas
```
/addguilda TAG - Cria/entra em uma guilda (100 pontos)
```

### Comandos de Sorteios
```
/sortearpontos quantidade - Sorteia para usuário aleatório
/sortearparaamigos quantidade @user1 @user2 - Sorteia para amigos
/sortearparaguilda TAG quantidade - Sorteia para membros da guilda
/rifa - Cria/participa de rifa
/participar - Entra na rifa ativa
```

### Comandos de Convites
```
/comoconvidar - Instruções de como convidar
/topconvites - Ranking de usuários que mais convidaram
```

### Comandos Informativos
```
/regras - Link para as regras
/comojogar - Link do jogo
/vip - Informações sobre VIP
/Bot - Informações do bot
/servidor - Status do servidor
/atualizacao - Última atualização
```

### Comandos de Staff (Apenas para Staff)
```
/criarcodigo codigo - Cria código premiado
/addpontos @user quantidade - Adiciona pontos ao usuário
/addexp @user exp - Adiciona experiência
/criarproduto nome custo codigo - Cria produto na loja
/status mensagem - Atualiza status do servidor
/enviar mensagem - Envia mensagem como bot
/dicas3 - Envia dicas especiais
/regras2 - Envia regras detalhadas
/atualizacao descrição versão - Registra nova atualização
```

## 🚀 Como Hospedar no Discloud 24h Online

### 1. Preparar os Arquivos
Certifique-se de ter estes arquivos na raiz do projeto:

**requirements.txt:**
```txt
discord.py
requests
```

**discloud.config:**
```
TYPE=bot
MAIN=bot.py
NAME=GameOnlineBot
AVATAR=https://imgur.com/your-bot-avatar.png
RAM=100
AUTORESTART=true
VERSION=latest
```

### 2. Configurações Necessárias
1. **Substitua o token**: Na última linha do `bot.py`, adicione seu token:
```python
bot.run('SEU_TOKEN_AQUI')
```

2. **Configure os IDs**: No início do código, substitua todos os IDs pelos do seu servidor:
```python
# IDs dos seus cargos
mod_role_id = SEU_ID_AQUI
vip_role_id = SEU_ID_AQUI
# ... outros IDs
```

### 3. Upload para Discloud
1. Compacte todos os arquivos em um ZIP
2. Acesse [Discloud.app](https://discloud.app)
3. Faça upload do arquivo ZIP
4. Aguarde o deployment

## ⚙️ Configuração Inicial

### Canais Necessários
Configure estes canais no seu servidor e atualize os IDs no código:

- `#fun-comandos` - Canal principal de comandos
- `#chat-geral` - Chat para ganhar EXP
- `#dicas` - Canal de dicas
- `#regras` - Canal de regras
- `#entrada` - Canal de boas-vindas
- `#sorteio` - Canal de sorteios
- `#vip` - Canal VIP
- `#logs-staff` - Canal de logs para staff

### Cargos Necessários
- Cargos de progressão (Iniciante, Intermediário, etc.)
- Cargo VIP
- Cargos de Staff/Moderação

## 📊 Banco de Dados

O bot utiliza SQLite com as seguintes tabelas:
- `points` - Pontos dos usuários
- `users` - XP, nível e categoria
- `espadas` - Equipamentos dos usuários  
- `guildas` - Sistema de guildas
- `produtos` - Loja de itens
- `codigos_premiados` - Códigos de resgate
- `codigos_unicos` - Códigos temporários
- `rifas` - Sistema de rifas
- `atualizacoes` - Histórico de atualizações
- `invites` - Sistema de convites

## 🔧 Personalização

### Modificar Valores
- **Cooldown do farm**: Altere `cooldown = 600` (em segundos)
- **Pontos por farm**: Modifique `random.randint(5, 15)`
- **Preços de espadas**: Ajuste valores em `uparespada()`
- **Intervalos de códigos**: Altere valores em `soltar_codigo()`

## 📝 Notas Importantes

- O bot requer permissões de administrador para funcionar completamente
- Mantenha o token do bot seguro e nunca compartilhe
- Teste todos os comandos em um servidor de desenvolvimento primeiro

## Suporte

Se encontrar problemas:
1. Verifique os logs do Discloud
2. Confirme se todos os IDs estão corretos
3. Verifique se o bot tem as permissões necessárias
4. Teste os comandos em ordem (criarconta → farmar → etc.)

---

