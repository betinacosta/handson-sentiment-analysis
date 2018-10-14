# Hands on Análise de Sentimentos

Já pensou se você conseguisse identificar as respostas emocionais que usuários apresentam sobre uma determinada entidade de interesse? Saber se as pessoas ficaram mais felizes do que (insirir uma comparação de alegria) com a venda do GitHub para a Microsoft, ou ficaram mais tristes do que o Tony Stark no final de Guerra Infinita? Bom, você veio ao lugar certo, nesse turtorial vamos aprender da forma mais simples possível como criar um analisador de sentimentos com dados obtido pelo Twitter. Bora?

## Pré-Requisitos

- Python3
- Pip
- TextBlob
- TweetPy

### Instalando as bibliotecas

- `pip install requirements`
- `python -m textblob.download_corpora`

## Requisitando um perfil de Desenvolvedor

Vamos inciar com a parte mais chata trabalhosa, criar um perfil de desenvolvedor e uma APP no twitter. Essa parte é simples, porém o Twitter agora pede altas explicações e descrições que podem ser um pouco chatas de preencher, então vou deixar um preenchimento padrão aqui para quem quiser ~~colar~~ perder menos tempo.

## Criando uma APP no Twitter

1; Primeiramente ~~Fora Temer~~ acesse o [site de desenvolvimento do Twitter](https://developer.twitter.com/en/apps) e clique em `Create an APP`.

![Criando um APP](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/craindo-app.png)

2; Digite os dados obrigatórios solicitados *(App Name, Application description, Website URL, Tell us how this app will be used)*

3; Acesse `Keys and Tokens` para visualizar seus dados de autenticação.

![Keys and Tokens](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/keys-tokens.png)

*Obs.: Para o Access Token e o Access Token Secret aparecerem é preciso clicar em `Generate Tokens` (Ou algo muito próximo disso) que se encontra mais abaixo na página. ~~A Apressadinha já saiu apertando e não conseguiu tirar o print~~*

4; Agora que você está com seu APP criado e tem todas as permissões, podemos seguir para a parte divertida.

## Mão na Massa!

