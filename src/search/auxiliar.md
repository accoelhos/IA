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
````

## Q1
- Nessa questão, iremos encontrar o programa de um agente de busca que planeja um caminho no Pacman e executa-o passo a passo, implementando os algoritmos de busca. 
- Para verificar que o agente de busca SearchAgent está funcionando, rodar: ```python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch```
- Nessa implementação, um nó da busca deve conter não só o estado, mas também toda info para reconstruir o caminho até aquele estado.
- As funções retornam uma lista de ações que irão levar o agente do início até o objetivo, com direções válidas.
- Primeiro, é implementado o DFS na função ```depthFirstSearch``` 