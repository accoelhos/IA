# Jogo Quarto

## Detalhes:

### Regras do Jogo

O Quarto é um jogo estratégico de tabuleiro para dois jogadores onde o objetivo é formar uma linha (horizontal, vertical ou diagonal) de 4 peças que compartilhem pelo menos um atributo comum.

**Características das Peças:**
- Cada peça possui 4 atributos binários:
  - **Altura**: Alta (▲) ou Baixa (▼)
  - **Cor**: Ciano ou Magenta
  - **Forma**: Quadrada (#) ou Redonda (O)
  - **Textura**: Sólida ( ) ou Furada (.)

**Mecânica de Jogo:**
1. O jogo inicia com uma peça sorteada aleatoriamente
2. Na sua vez, o jogador coloca a peça atual no tabuleiro (4x4)
3. Após colocar, o jogador escolhe a próxima peça que o oponente irá jogar
4. O jogo continua alternando entre os jogadores
5. Vence quem formar primeiro uma linha com 4 peças que compartilhem ao menos um atributo

**Condições de Vitória:**
- 4 peças em linha (horizontal, vertical ou diagonal) com mesmo atributo
- Exemplo: 4 peças redondas em linha, independente dos outros atributos

### Implementação

O projeto foi estruturado em módulos bem definidos seguindo princípios de programação orientada a objetos:

**Arquitetura do Sistema:**

1. **`quarto_board.py`** - Classe base para representação visual
   - Implementa o tabuleiro 4x4 
   - Métodos de formatação e exibição das peças com cores
   - Utiliza a biblioteca `colorama` para interface colorida no terminal

2. **`quarto_game.py`** - Lógica principal do jogo
   - Herda de `QuartoBoard`
   - Gerencia estado do jogo (peças disponíveis, jogador atual, peça selecionada)
   - Implementa validações de movimento e detecção de vitória
   - Métodos principais:
     - `available_moves()`: retorna posições vazias
     - `make_move()`: coloca peça e alterna jogador
     - `select_next_piece()`: escolhe próxima peça
     - `check_win()`: verifica condições de vitória
     - `copy()`: cria cópia do estado para simulações

3. **`quarto_minimax.py`** - Implementação do algoritmo Minimax
   - Algoritmo de busca adversarial com poda Alpha-Beta
   - Função de avaliação baseada em vitória/derrota
   - Profundidade configurável (padrão: 2)

4. **`quarto_mcts.py`** - Implementação do Monte Carlo Tree Search
   - Árvore de busca com nós representando estados
   - Política UCB1 para seleção de nós
   - Simulações aleatórias para avaliação
   - Iterações configuráveis (padrão: 5000) com limite de tempo

5. **`play_quarto.py`** - Interface principal e controle de fluxo
   - Menu interativo para escolha de oponente
   - Tutorial integrado explicando as regras
   - Turnos alternados entre humano e IA
   - Tratamento de entrada do usuário

**Representação de Dados:**
- Peças: tuplas `(altura, cor, forma, textura)` com valores binários (0/1)
- Tabuleiro: matriz 4x4 com referências às peças ou None para posições vazias
- Estado: jogador atual, peça selecionada, peças disponíveis

### Heurística do Minimax

A implementação do Minimax utiliza uma função de avaliação simplificada mas eficaz:

**Função de Avaliação:**
```python
def evaluate(game, player_at_root):
    winner = game.winner()
    if winner:
        if é_o_jogador_desejado:
            return 1000 + movimentos_restantes  # Vitória rápida
        else:
            return -1000 - movimentos_restantes  # Derrota lenta
    return 0  # Estado neutro
```

**Características da Heurística:**
- **Vitória/Derrota**: Valores extremos (±1000) para estados terminais
- **Preferência Temporal**: Bonifica vitórias rápidas e penaliza derrotas lentas
- **Estados Intermediários**: Avaliação neutra (0) para posições não terminais
- **Limitação**: Não considera padrões intermediários ou ameaças potenciais

**Otimizações Implementadas:**
- **Poda Alpha-Beta**: Reduz significativamente o espaço de busca
- **Aleatorização**: Embaralha movimentos para variedade no jogo
- **Profundidade Limitada**: Controla tempo de resposta vs qualidade da jogada

**Pontos de Melhoria da Heurística:**
- Poderia avaliar linhas parciais (2-3 peças com atributo comum)
- Não considera posições estratégicas do tabuleiro
- Ausência de avaliação de ameaças do oponente

### Política de simulação utilizada no MCTS

O MCTS implementado utiliza uma política de simulação puramente aleatória:

**Estratégia de Simulação:**
- **Seleção de Movimentos**: Escolha completamente aleatória entre movimentos válidos
- **Dois Passos**: Cada jogada envolve (1) colocar peça + (2) escolher próxima peça
- **Parada**: Simulação continua até vitória ou empate (tabuleiro cheio)

**Fases do MCTS:**

1. **Seleção**: Utiliza política UCB1 para navegar pela árvore
   - Formula: `wins/visits + c * sqrt(log(parent_visits)/visits)`
   - Parâmetro c = 1.41 (√2) - balanceio exploração/explotação

2. **Expansão**: Adiciona novos nós filhos para movimentos não explorados
   - Um movimento não testado por iteração
   - Aleatoriza ordem dos movimentos para variedade

3. **Simulação (Playout)**: Jogadas aleatórias até o final
   - Nenhuma heurística ou preferência
   - Movimentos válidos escolhidos uniformemente

4. **Retropropagação**: Atualiza estatísticas do caminho percorrido
   - Incrementa visitas em todos os nós do caminho
   - Incrementa vitórias apenas para o jogador vencedor

**Configurações Padrão:**
- **Iterações**: 5000 por jogada
- **Limite de Tempo**: 2 segundos máximo
- **Política de Seleção Final**: Nó filho mais visitado (robustez)

### Comparação qualitativa entre os 2 agentes

**Minimax (Profundidade 2):**

*Pontos Fortes:*
- **Determinístico**: Sempre escolhe a mesma jogada em situações idênticas
- **Garantias Teóricas**: Joga perfeitamente dentro da profundidade analisada
- **Rápido**: Resposta quase instantânea com profundidade 2
- **Previsível**: Comportamento consistente facilita análise e depuração

*Pontos Fracos:*
- **Horizonte Limitado**: Profundidade 2 é insuficiente para análise profunda
- **Heurística Simplista**: Não avalia posições intermediárias adequadamente
- **Rigidez**: Não adapta estratégia conforme o oponente
- **Escalabilidade**: Crescimento exponencial impede profundidades maiores

**MCTS (5000 iterações, 2s):**

*Pontos Fortes:*
- **Adaptativo**: Aprende durante o jogo e se adapta ao oponente
- **Sem Heurística**: Não depende de conhecimento específico do domínio
- **Escalável**: Tempo de resposta controlável via iterações/tempo
- **Robusto**: Política de simulação aleatória evita vieses

*Pontos Fracos:*
- **Estocástico**: Pode escolher jogadas diferentes em situações idênticas
- **Convergência Lenta**: Simulações aleatórias podem ser ineficientes
- **Dependente de Recursos**: Qualidade aumenta com mais iterações/tempo
- **Menos Intuitivo**: Dificulta análise das decisões tomadas

**Comparação Prática:**
- **Força de Jogo**: MCTS geralmente superior em posições complexas
- **Tempo de Resposta**: Minimax mais rápido, MCTS configurável
- **Consistência**: Minimax mais previsível, MCTS mais adaptável
- **Facilidade de Ajuste**: Minimax requer heurística melhor, MCTS apenas mais recursos

### Observações sobre desempenho, limitações e sugestões de melhoria

**Desempenho Atual:**

*Pontos Positivos:*
- Interface amigável com tutorial integrado
- Código bem estruturado e modular
- Algoritmos implementados corretamente
- Tratamento adequado de erros e casos extremos

*Limitações Identificadas:*
- Heurística do Minimax muito simplista
- Simulações MCTS puramente aleatórias
- Ausência de opening book ou patterns conhecidos
- Falta de persistência de aprendizado

**Sugestões de Melhoria:**

**Para o Minimax:**
1. **Heurística Avançada**: 
   - Avaliar linhas parciais (2-3 peças com atributo comum)
   - Considerar controle do centro do tabuleiro
   - Ponderar ameaças múltiplas

2. **Otimizações Técnicas**:
   - Tabela de transposição para estados repetidos
   - Ordenação de movimentos para melhor poda
   - Busca iterativa por profundidade

**Para o MCTS:**
1. **Política de Simulação Inteligente**:
   - Priorizar movimentos que completam linhas
   - Evitar dar peças "perigosas" ao oponente
   - Usar heurísticas leves para guiar simulações

2. **Otimizações da Árvore**:
   - Paralelização das simulações
   - Reciclagem da árvore entre jogadas
   - Políticas de seleção mais sofisticadas

**Melhorias Gerais:**
1. **Interface**: Modo gráfico com pygame/tkinter
2. **Análise**: Logs detalhados e métricas de performance
3. **Flexibilidade**: Configuração de parâmetros via interface
4. **Extensibilidade**: Framework para novos algoritmos (Alpha-Zero, etc.)


