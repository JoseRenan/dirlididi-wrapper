# Dirlididi Wrapper

Uma CLI wrapper para auxiliar no uso da ferramenta dirlididi.

## Instalação

Você precisa rodar o comando abaixo para instalar. Não se esqueça de substituir o `<TOKEN>` pelo token informado no dirlididi sem os `<>`.

```sh
$ wget https://raw.githubusercontent.com/JoseRenan/dirlididi-wrapper/master/dirlididi-wrapper.py && (python dirlididi-wrapper.py -i <TOKEN>; rm dirlididi-wrapper.py)
$ bash
```

## Submissão de código

Para submeter a solução dos problemas do site, basta informar o token do problema, o executável e o código fonte da solução, como mostra o código abaixo:

```sh
$ dirlididi -s <token_problema> <exec> <source>
```