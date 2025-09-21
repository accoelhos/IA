# Roteiro auxiliar

- Arquivos editados: ```search.py, searchAgent.py e twojars.py``` 

Pseudocódigo para as questões Q1 até Q3:

``` python
    frontier = {startNode} 
    expanded = {} 
    while frontier is not empty: 
        node = frontier.pop() 
        if isGoal(node): 
            return path_to_node 
        if node not in expanded: 
            expanded.add(node) 
            for each child of node's children: 
                frontier.push(child) 
    return failed 
```

## Q1 - DFS
- Nessa questão, iremos encontrar o programa de um agente de busca que planeja um caminho no Pacman e executa-o passo a passo, implementando os algoritmos de busca. 
- Para verificar que o agente de busca SearchAgent está funcionando, rodar: ```python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch```
- Nessa implementação, um nó da busca deve conter não só o estado, mas também toda info para reconstruir o caminho até aquele estado.
- As funções retornam uma lista de ações que irão levar o agente do início até o objetivo, com direções válidas.
- Primeiro, é implementado o DFS na função ```depthFirstSearch```. 
- O DFS foi implementado utilizando uma **pilha (`util.Stack`)** para controlar a fronteira dos nós a serem explorados.  
- Cada elemento armazenado na pilha contém:  
  - O **estado atual** (posição no labirinto).  
  - O **caminho de ações** que levou até esse estado.  
- Um conjunto de **visitados** é usado para evitar ciclos e repetição de estados.  
- O funcionamento segue os passos:  
  1. Inicializa a pilha com o estado inicial e caminho vazio.  
  2. Remove um nó da pilha e verifica se ele é o objetivo.  
  3. Caso não seja e ainda não tenha sido expandido, adiciona-o ao conjunto de visitados.  
  4. Expande o nó com `problem.expand(state)` e insere cada sucessor na pilha, com o caminho atualizado.  
  5. Se o objetivo for encontrado, retorna imediatamente a sequência de ações acumulada.  
- Assim, o DFS percorre primeiro os caminhos mais profundos do grafo de estados antes de retroceder.  
- O resultado final é uma lista de direções (Norte, Sul, Leste, Oeste) que levam o Pacman até o objetivo.  
- Testando:
```
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
````

**Perguntas**
- A ordem de exploração foi de acordo com o esperado?
  Sim, ele explora o caminho mais profundo possível inicialmente (vermelho mais forte). No mediumMaze, a solução teve comprimento de 130, estando dentro do esperado. 
- O Pacman realmente passa por todos os estados explorados no seu caminho para o objetivo?
  Não. O DFS marca estados como visitados mesmo que não faça parte do caminho final, então o pacman só percorre estados que formam o caminho do início até o objetivo, mas o algoritmo pode ter expandido muitos outros estados durante a busca.
- Essa solução é ótima?
  Não. O DFS não garante caminhos de custo mínimo, ele só retorna o primeiro caminho achado de acordo com a ordem de exploração. Por conta dissi, em labirintos maiores, ele pode gerar caminhos muito longos.
- Se não, o que a busca em profundidade está fazendo de errado?
  A busca por DFS é limitada ao explorar sem considerar custo ou distância real até o objetivo, podendo gerar caminhos mais longos que o necessário e expandindo estados que não estão no caminho final, causando um desperdício de tempo.
- Verificar a corretude:
```python autograder.py -q q1```

**Concluindo: ** esse algoritmo é eficiente para explorar áreas profundass, mas não é adequado para encontrar o menor caminho em labirintos muito complexos.

## Q2 - BFS

```
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
````
```python eightpuzzle.py```

**Como foi implementado:**
- Utiliza uma **fila (`util.Queue`)** para controlar a fronteira dos nós a serem explorados, garantindo a ordem FIFO (primeiro a entrar, primeiro a sair).
- Cada elemento armazenado na fila contém:
  - O **estado atual** (posição no labirinto ou configuração do problema).
  - O **caminho de ações** que levou até esse estado.
- Um conjunto de **visitados** é usado para evitar a expansão repetida de estados já explorados.

**Funcionamento passo a passo:**
1. Inicializa a fila com o estado inicial e caminho vazio.
2. Remove um nó da fila e verifica se ele é o objetivo.
3. Caso não seja e ainda não tenha sido expandido, adiciona-o ao conjunto de visitados.
4. Expande o nó com `problem.expand(state)` e insere cada sucessor na fila, com o caminho atualizado.
5. Se o objetivo for encontrado, retorna imediatamente a sequência de ações acumulada.

**Características:**
- A BFS garante encontrar o menor caminho (ótimo) em termos de número de ações, desde que todos os custos sejam iguais.
- O Pacman (ou agente) só percorre o caminho final ótimo, mas o algoritmo pode expandir muitos outros estados durante a busca.
- O uso do conjunto de visitados evita ciclos e repetições, tornando a busca mais eficiente.

**Testando:**
```
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```
Para o quebra-cabeça:
```
python eightpuzzle.py
```

**Perguntas respondidas:**
- A solução é ótima? Sim, a BFS sempre encontra o menor caminho possível (em número de ações) quando todos os custos são iguais.
- Para o quebra-cabeças, quantas ações compõem a solução encontrada pelo BFS? O número de ações depende do estado inicial, mas será sempre o mínimo possível para resolver o problema.

**Concluindo:**
A BFS é adequada para encontrar caminhos mínimos em problemas de custo uniforme, sendo mais eficiente que o DFS para esse objetivo, embora possa consumir mais memória em problemas muito grandes.

## Q3 - A*

**Como foi implementado:**
- Utiliza uma **fila de prioridade (`util.PriorityQueue`)** para controlar a fronteira dos nós, priorizando sempre o nó com menor custo total estimado (custo acumulado + heurística).
- Cada elemento armazenado na fila contém:
  - O **estado atual**.
  - O **caminho de ações** até esse estado.
  - O **custo acumulado** até esse estado.
- Um dicionário de **visitados** armazena o menor custo já encontrado para cada estado, evitando reexpansão desnecessária.
- A função de **heurística** é recebida como parâmetro e avalia o quão "longe" o estado está do objetivo (ex: distância de Manhattan).

**Funcionamento passo a passo:**
1. Inicializa a fila de prioridade com o estado inicial, caminho vazio e custo zero. A prioridade é a soma do custo e da heurística.
2. Remove o nó de menor prioridade (menor custo + heurística) da fila.
3. Se o estado já foi visitado com custo menor ou igual, ignora.
4. Marca o estado como visitado com o menor custo encontrado.
5. Se o objetivo for alcançado, retorna o caminho de ações.
6. Para cada sucessor, calcula o novo custo acumulado e a prioridade (novo custo + heurística). Se for melhor que o já visitado, insere na fila.
7. Repete até encontrar a solução ou esgotar a fila.

**Características:**
- A busca A* encontra sempre a solução ótima se a heurística for admissível (não superestima o custo até o objetivo).
- É geralmente mais eficiente que a busca de custo uniforme, pois usa a heurística para "guiar" a busca.
- O uso do dicionário de visitados garante que não há expansão desnecessária de estados já explorados com custo menor.

**Testando:**
```
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```
Verificar a corretude com:
```
python autograder.py -q q3
```

**Perguntas respondidas:**
- A busca A* encontra a solução ótima? Sim, desde que a heurística seja admissível.
- A A* é mais rápida que a busca de custo uniforme? Sim, pois expande menos nós ao usar a heurística.
- O que acontece em openMaze para as várias estratégias? A* e UCS tendem a ser mais eficientes, enquanto DFS e BFS podem expandir muitos estados desnecessários.

**Concluindo:**
A busca A* é uma das estratégias mais poderosas para encontrar caminhos ótimos em problemas de busca, combinando custo real e estimativa heurística para eficiência e qualidade de solução.

## Q4 - Encontrando todos os cantos

**Descrição:**
O objetivo do CornersProblem é encontrar o menor caminho que passe pelos quatro cantos do labirinto, independentemente de haver comida neles. O estado deve ser representado de forma abstrata, sem incluir informações irrelevantes como fantasmas ou comida extra.

**Como foi implementado:**
- O estado é representado como uma tupla: `((x, y), cantos_visitados)`, onde `(x, y)` é a posição atual do Pacman e `cantos_visitados` é uma tupla (ou conjunto imutável) com os cantos já visitados.
- O problema define os quatro cantos do labirinto na inicialização.
- O estado inicial contém a posição inicial do Pacman e nenhum canto visitado.
- A cada movimento, se o Pacman chega a um canto, esse canto é adicionado ao conjunto de visitados.
- O objetivo é alcançado quando todos os quatro cantos foram visitados.
- A expansão de nós gera novos estados considerando todas as ações válidas, atualizando a posição e os cantos visitados.

**Funcionamento passo a passo:**
1. Inicializa o estado com a posição inicial e conjunto vazio de cantos visitados.
2. Para cada ação válida, calcula a nova posição e atualiza o conjunto de cantos visitados se necessário.
3. O nó filho é adicionado à fronteira com custo 1.
4. O processo se repete até que todos os cantos tenham sido visitados.


**Testando:**
```
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```
corretude com:
```
python autograder.py -q q4
```
## Q5 - Heurística para o Problema dos Cantos

**Descrição:**  
A heurística do CornersProblem estima o menor custo restante para o Pacman visitar todos os cantos ainda não visitados. O objetivo é fornecer ao algoritmo A* uma estimativa eficiente que ajude a reduzir o número de nós expandidos.

**Como foi implementado:**  
- A heurística recebe o estado atual do Pacman, representado como `((x, y), cantos_visitados)`.  
- Cria uma lista de cantos ainda não visitados a partir do estado.  
- Se todos os cantos já foram visitados, retorna 0.  
- Caso contrário, existem duas formas comuns de estimar o custo restante:
  1. **Distância máxima até o canto mais distante:**  
     - Calcula a distância de Manhattan da posição atual até cada canto não visitado.  
     - Retorna a maior distância como estimativa do custo restante.
  2. **Caminho sequencial pelos cantos mais próximos:**  
     - Enquanto houver cantos não visitados, sempre vai para o canto mais próximo, somando as distâncias de Manhattan.  
     - Retorna a soma total como estimativa do custo restante.  
- A heurística é **admissível**, ou seja, nunca superestima o custo real.  
- É usada pelo A* para priorizar estados que provavelmente levam ao objetivo mais rapidamente.

**Funcionamento passo a passo:**  
1. Recebe o estado atual (posição e cantos visitados).  
2. Identifica os cantos que ainda não foram visitados.  
3. Calcula uma estimativa do custo restante usando a estratégia escolhida (distância máxima ou caminho pelo canto mais próximo).  
4. Retorna esse valor como heurística para o A*.  

**Testando:**  

```
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

**Corretude:**

```
python autograder.py -q q5
```





