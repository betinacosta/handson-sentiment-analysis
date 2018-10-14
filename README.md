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

![Keys and Tokens](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/keys-and-tokens.png)

*Obs.: Para o Access Token e o Access Token Secret aparecerem é preciso clicar em `Generate Tokens` (Ou algo muito próximo disso) que se encontra mais abaixo na página. ~~A Apressadinha já saiu apertando e não conseguiu tirar o print~~*

4; Agora que você está com seu APP criado e tem todas as permissões, podemos seguir para a parte divertida.

## Mão na Massa!

1; Finalmente vamos dar inicio a parte divertida! Vamos iniciar criando um arquivo .py no editor de sua preferencia e **importando** as bibliotecas que vamos utilizar

```python
import tweepy
import numpy as np
from textblob import TextBlob
```

2; Agora vamos setar as variaveis que vão receber as chaves da sua API do Twitter

```python
consumer_key='your_consumer_key'
consumer_secret='consumer_secret'

access_token='access_token'
access_token_secret='access_token_secret'
```

3; Tendo setado as variaveis, vamos fazer a autenticação do nosso script na API do Twitter:

```python
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
```

Obs.: Se você quiser saber se a autenticação está funcionando, `tweepy.API(auth)` deve retornar algo parecido com `<tweepy.api.API object at 0x10d3c3240>`

Obs2.: Caso vocês estejam tendo o erro `SyntaxError: invalid syntax` em `def _start(self, async):`, execute `$pip3 install --upgrade git+https://github.com/tweepy/tweepy.git`

4; Agora vamos buscar pelos nosso tweets, para isso, vamos utilizar a busca do tweepy. Como a coisa mais importante essa semana certamente é a #PythoBrasil, podemos buscar os tweetes que façam referência a esse tópico.

```python
tweets = api.search('Python Brasil')
```

ou para ignorar RTs e ter um resultado um pouco mais direcionado

```python
tweets = api.search('Python Brasil -filter:retweets')
```

5; Agora iterar em cima dos resultados, pegando nossos tweets `tweet.text` e colocando no TextBlob

```python
for tweet in tweets:
    phrase = TextBlob(tweet.text)
```

6; Uma vez que temos os tweets, podemos fazer a análise de sentimento contido em seu texto. Entretanto, temos um problema: O algoritimo da TextBlob foi treinado para fazer análise de textos em língua inglesa. Por isso, vamos ter que utilizar um recurso que faz a tradução para a inglês dos textos que estiverem em um  idioma diferenete. Vale lembrar que isso pode prejudicar um pouco a tradução, pois alguns significado podem se perder na tradução. Para isso, vamos criar uma função para verificar o idioma do tweet:

```python
def is_english(text):
    if text.detect_language() == 'en':
        return True
    return False
```

*Obs.: Existem outras formas de realizar análise de sentimento diretamente na língua portuguesa, porém, o objetivo desse tutorial é aprendermo primeiramente a maneira mais simples antes de recorrer a técnicas mais avançadas.*

7; Dentro do `for`, vamos verificar se o idioma do tweet é diferente do inglês com a função que acabamos de criar. Caso seja, vamos traduzir antes de realizar a análise de sentimento

```python
for tweet in tweets:
    phrase = TextBlob(tweet.text)

    if not is_english(phrase):
        phrase = TextBlob(str(phrase.translate(to='en')))

    print('Tweet: ' + tweet.text)
    print('Sentiment: ', phrase.sentiment)
```

### Senta que la vem história:

Antes de continuarmos, vamos entender um pouco do que estamos vendo:

**POLARITY (POLARIDADE):** Um valor entre -1.0 e 1.0, onde -1.0 se refere a uma polaridade 100% negativa, 1.0 uma polaridade positiva

**SUBJECTIVITY (SUBJETIVIDADE):** Um valor variante entre 0.0 e 1.0, onde 0 se refere a um valor 100% objetivo e 1.0 um 100% subjetivo

**SUBJETIVIDADE x OBJETIVIDA:** Sentenças objetivas normalmente possuem fatos ou informaçãoes, enquanto sentenças subjetivas expressam sentimentos pessoais e opiniões

### Continuando...

8; Bom, agora que nós sabemos a **polaridade** e a **subjetividade**, devemos ignorar valores cuja a polaridade é neutra (0.0) e são objetivas (uma vez que temos interesse somente em sentenças que expressam sentimentos)

```python
if (phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0):
    polarities.append(phrase.sentiment.polarity)
```

9; E usar o numpy para calcular a média das polaridades e descobrir se a média da opinião é positiva (mais próxima de 1) ou negativa (mais próxima de -1)

```python
print('Média: ' + polarity_mean)
if(polarity_mean > 0.0):
    print('POSITIVE')
else:
    print('NEGATIVE')
```

10; Pronto! Agora temos um simples analisador de tweets... Porém ainda podemos ir mais adiante.

### Indo um pouco mais longe


