# GCC1734 - Inteligência Artificial

Este ambiente reúne todas as bibliotecas necessárias para os trabalhos práticos sobre agentes com LLMs, reconhecimento de entidades nomeadas (NER), e visualizações.

## Requisitos

- Python 3.10 ou 3.11 (recomendado)
- Conda ou virtualenv instalado

## Criação do ambiente com conda

```bash
conda create -n gcc1734 python=3.10
conda activate gcc1734
```

## Instalação das dependências

Faça o clone deste repositório (que contém o arquivo `requirements.txt` na raiz) e execute:

```bash
pip install -r requirements.txt
```

## Instalação de modelos do spaCy

Para usar o `spaCy` em visualizações e testes:

```bash
python -m spacy download en_core_web_sm
```

Opcional: verifique se o modelo foi instalado corretamente:

```bash
python -m spacy validate
```
