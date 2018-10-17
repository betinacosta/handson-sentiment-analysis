# Hands on Análise de Sentimentos

Já pensou se você conseguisse identificar as respostas emocionais que usuários apresentam sobre uma determinada entidade de interesse? Saber se as pessoas ficaram felizes com a venda do GitHub para a Microsoft, ou mais tristes do que o Tony Stark no final de Guerra Infinita? Bom, você veio ao lugar certo, nesse turtorial vamos aprender da forma mais simples possível como criar um analisador de sentimentos com dados obtido pelo Twitter. Bora?

## Pré-Requisitos

- Python3
- Pip
- TextBlob
- TweePy
- Numpy
- Uma conta no Twitter

### Instalando as bibliotecas

- `pip install -r requirements.txt`
- `python -m textblob.download_corpora`

## Requisitando um perfil de Desenvolvedor

Vamos inciar com a parte mais chata e trabalhosa, criar um perfil de desenvolvedor e uma APP no twitter. Essa parte é simples, porém o Twitter agora pede altas explicações e descrições que podem ser um pouco chatas de preencher, então vou deixar um preenchimento padrão para quem quiser ~~colar~~ perder menos tempo.

**1**. Vamos começar acessando https://developer.twitter.com/ e clicando em `Apply`:

![Apply](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/apply.png)

**2**. Na próxima página, clique em `Apply for a developer account` e em `Continue` na página seguinte para seguir com a sua conta:

![Apply for a developer account](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/apply-developer.png)

![Continue](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/continue.jpeg)

**3**. Informe o tipo de conta que você está criando (`Personal Use` provavelmente) e preencha as informações solicitadas:

![Tipo de Conta](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/tipo-de-conta.png)

**4**. Na próxima página terão algumas informações a serem preenchidas, preencha o campo `What use case(s) are you interested in?` conforme a imagem e em `Describe in your own words what you are building` coloque o seguinte texto:

```text
1. I’m using Twitter’s APIs to run a Python Brasil Tutorial about Sentiment Analysis;
2. I plan to analyse Tweets to understand how people are feeling regarding some subject.
3. The solution does not involve tweeting, retweeting, neither liking content on twitter. It is just for analysis;
4. The solution does not involve displaying twitter explicitly, but its polarity and subjectivity
```

![Casos de Uso](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/casos-de-uso.png)

Em `Will your product, service, or analysis make Twitter content or derived information available to a government entity?` selecione `não`

**5**. ~~Finja ler~~ leia os `Termos de Serviço` e clique em `concordar`

**6**. Agora basta **confirmar o seu email** e seguir para a próxima parte :)

## Criando uma APP no Twitter

**1**. Primeiramente ~~Fora Temer~~ acesse o [site de desenvolvimento do Twitter](https://developer.twitter.com/en/apps) e clique em `Create an APP`.

![Criando um APP](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/craindo-app.png)

**2**. Digite os dados obrigatórios solicitados. No campo `Tell us how this app will be used` você pode usar o seguinte texto:

```text
This app will be used to develop a simple Sentiment Analysis App for a tutorial at Python Brasil 2018
```

Quanto ao `website`, você pode colcar qualquer URL, incluisive a do seu perfil do twitter;

**3**. Acesse `Keys and Tokens` para visualizar seus dados de autenticação.

![Keys and Tokens](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/keys-and-tokens.png)

*Obs.: Para o Access Token e o Access Token Secret aparecerem é preciso clicar em `Create Tokens` (Ou algo muito próximo disso) que se encontra mais abaixo na página. ~~A Apressadinha já saiu apertando e não conseguiu tirar o print~~*

**4**. Agora que você está com seu APP criado e tem todas as permissões, podemos seguir para a parte divertida.

## Mão na Massa!

**1**. Finalmente vamos dar inicio a parte interessante! Vamos iniciar criando um arquivo .py no editor de sua preferencia e **importar** as bibliotecas que vamos utilizar

```python
import tweepy
import numpy as np
from textblob import TextBlob
```

**2**. Agora vamos setar as variaveis que vão receber as chaves da sua API do Twitter

```python
consumer_key='your_consumer_key'
consumer_secret='consumer_secret'

access_token='access_token'
access_token_secret='access_token_secret'
```

*Obs.: Se você preferir, pode colocar as chaves em um arquivo separado*

*Obs2.: Se você for commitar esse código am algum lugar, recomendo [settar as chaves como variaveis de ambiente e importá-las](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/src/keys.py)*

**3**. Tendo setado as variaveis, vamos fazer a autenticação do nosso script na API do Twitter:

```python
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
```

*Obs.: Se você quiser saber se a autenticação está funcionando, `tweepy.API(auth)` deve retornar algo parecido com `<tweepy.api.API object at 0x10d3c3240>`*

*Obs2.: Caso vocês estejam tendo o erro `SyntaxError: invalid syntax` em `def _start(self, async):`, execute `$pip3 install --upgrade git+https://github.com/tweepy/tweepy.git`*

**4**. Agora vamos buscar pelos nosso tweets, para isso, vamos utilizar a busca do tweepy. Como a coisa mais importante essa semana certamente é a `Python Brasil`, podemos buscar os tweetes que façam referência a esse tópico.

```python
tweets = api.search('Python Brasil')
```

ou para ignorar RTs e ter um resultado um pouco mais direcionado

```python
tweets = api.search('Python Brasil -filter:retweets')
```

**5**. E iterar em cima dos resultados, pegando nossos tweets `tweet.text` e colocando no TextBlob

```python
for tweet in tweets:
    phrase = TextBlob(tweet.text)
```

**6**. Uma vez que temos os tweets, podemos fazer a análise de sentimento contido em seu texto. Entretanto, temos um problema: O algoritimo da TextBlob foi treinado para fazer análise de textos em língua inglesa. Por isso, vamos ter que utilizar um recurso que faz a tradução para a inglês dos textos que estiverem em um  idioma diferenete (O TextBlob utiliza o google tradutor para isso). Para isso, vamos criar uma função para verificar o idioma do tweet:

```python
def is_english(text):
    if text.detect_language() == 'en':
        return True
    return False
```

*Obs.: Vale lembrar que isso pode prejudicar um pouco a análise, pois alguns significado podem se perder durante a tradução. Existem outras formas de realizar análise de sentimento diretamente na língua portuguesa, porém, o objetivo desse tutorial é aprendermos primeiramente a maneira mais simples antes de recorrer a técnicas mais avançadas.*

**7**. Dentro do `for`, vamos verificar se o idioma do tweet é diferente do inglês com a função que acabamos de criar. Caso seja, vamos traduzir antes de realizar a análise de sentimento

```python
polarities = []

for tweet in tweets:
    phrase = TextBlob(tweet.text)

    if not is_english(phrase):
        phrase = TextBlob(str(phrase.translate(to='en')))

    print('Tweet: ' + tweet.text)
    print('Polarity: ' + str(phrase.sentiment.polarity) + " \ " + str(phrase.sentiment.subjectivity))
    print('.....................')
```

### Senta que la vem história:

Antes de continuarmos, vamos entender um pouco do que estamos vendo:

**POLARITY (POLARIDADE):** Um valor entre -1.0 e 1.0, onde -1.0 se refere a uma polaridade 100% negativa, 1.0 uma polaridade positiva

**SUBJECTIVITY (SUBJETIVIDADE):** Um valor variante entre 0.0 e 1.0, onde 0 se refere a um valor 100% objetivo e 1.0 um 100% subjetivo

**SUBJETIVIDADE x OBJETIVIDA:** Sentenças objetivas normalmente possuem fatos ou informaçãoes, enquanto sentenças subjetivas expressam sentimentos pessoais e opiniões

### Continuando...

**8**. Bom, agora que nós sabemos a **polaridade** e a **subjetividade**, devemos ignorar valores cuja a polaridade é neutra (0.0) e são objetivas (subjetividade 0.0), uma vez que temos interesse somente em sentenças que expressam sentimentos.

```python
if (phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0):
    polarities.append(phrase.sentiment.polarity)
```

Agora que está parte está finalizada, podemos colocar isso dentro de uma função para deixar tudo mais bonito e organizado:

```python
def tweet_analysis():
    polarities = []

    for tweet in tweets:
        phrase = TextBlob(tweet.text)

        if not is_english(phrase):
            phrase = TextBlob(str(phrase.translate(to='en')))
            
        if (phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0):
            polarities.append(phrase.sentiment.polarity)

        print('Tweet: ' + tweet.text)
        print('Polarity: ' + str(phrase.sentiment.polarity) + " \ " + str(phrase.sentiment.subjectivity))
        print('.....................')
        
        return polarities
```

**9**. E usar o numpy para calcular a média das polaridades e descobrir se a média da opinião é positiva (mais próxima de 1) ou negativa (mais próxima de -1)

```python
polarity_mean = np.mean(polarities)

print('Média: ' + str(polarity_mean))
if(polarity_mean > 0.0):
    print('POSITIVE')
else:
    print('NEGATIVE')
```

**10**. Pronto! Agora temos um simples analisador de tweets... Porém ainda podemos ir mais adiante.

### Indo um pouco mais longe

**11**. Vamos modificar um pouco nosso método de busca: ao invés de `tweets = api.search('Python Brasil -filter:retweets')` vamos usar:

```python
tweets = tweepy.Cursor(api.search, q="Python Brasil -filter:retweets").items(20)
```

Dessa forma, iremos filtrar somente os tweets que não forem retweets e pegar o numero de tweets determinados;

**12**. Outra coisa que podemos fazer, é passar o parametro result_type='recent' para pegarmos os tweets mais recentes:

```python
tweets = tweepy.Cursor(api.search, q="Python Brasil -filter:retweets", result_type="recent").items(20)
```

**13**. Outra abordagem que podemos tentar, é aplicar uma média ponderada ao invés de uma média simples...

![Meme nazare](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/media-ponderada.jpg)

Calma... a média ponderada nada mais é do que o calculo de média onde alguns valores tem um peso maior do que o outro, assim podemos calcular a média de polaridade utilizando a subjetividade como peso. Desta forma, tweetes mais subjetivos (mais carregados de emoção) terão um peso maior.

```python
def get_weighted_polarity_mean(valid_tweets):
    return np.average(valid_tweets['polarity'],weights=valid_tweets['subjectivity'])
```

**14**. Como vocês devem ter percebido, a função `np.average` está recebendo um dicionário, coisa que nós não fizemos. Essa é outra pequena mudança que podemos fazer para armazenar todos os valores relevantes para a nossa análise. Desta forma ficamos com:

```python
    if phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0:
        polarities.append(phrase.sentiment.polarity)
        subjectivities.append(phrase.sentiment.subjectivity)

return {'polarity':polarities, 'subjectivity':subjectivities}
```
*Obs.: É necessário setar o `subjectivities = []` da mesma forma que o `polarities`.*

**14.1**. Podemos aproveitar o embalo e transformar a média simples em um método também:

```python
def get_polarity_mean(valid_tweets):
    return np.mean(valid_tweets['polarity'])
```

*Obs.: O `valid_tweets` nada mais é do que o retorno da nossa função*

**15**. Também podemos transformar a query utilizada (`q`) em um parametro recebido pela função que irá reralizar a análise:

```python
def tweet_analysis(query):
    tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(20)
```

**17**. Para conseguirmos vizualizar melhor nossos resultados podemos criar a seguinte função que se responsabiliza por mostrá-los na tela:

```python
def print_result(mean):
    if mean > 0.0:
        print('POSITIVE')
    elif mean == 0.0:
        print('NEUTRO')
    else:
        print('NEGATIVE')
```

**18**. E, para mostrar tudo que fizemos até agora:

```python
if __name__ == "__main__":
    query = input("Entre a query de analise: ")
    analysis = tweet_analysis(query)

    print('MÉDIA PONDERADA: ' + str(get_weighted_polarity_mean(analysis)))
    print_result(get_weighted_polarity_mean(analysis))

    print('MÉDIA: ' + str(get_polarity_mean(analysis)))
    print_result(get_polarity_mean(analysis))
```

**16**. O Código final ficaria assim:

```python
import tweepy
import numpy as np
from textblob import TextBlob

consumer_key='your_consumer_key'
consumer_secret='consumer_secret'

access_token='access_token'
access_token_secret='access_token_secret'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

def is_english(text):
    if text.detect_language() == 'en':
        return True
    return False

def tweet_analysis(query):
    tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(20)

    subjectivities = []
    polarities = []

    for tweet in tweets:
        phrase = TextBlob(tweet.text)

        if not is_english(phrase):
            phrase = TextBlob(str(phrase.translate(to='en')))

        if phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0:
            polarities.append(phrase.sentiment.polarity)
            subjectivities.append(phrase.sentiment.subjectivity)

        print('Tweet: ' + tweet.text)
        print('Polarity: ' + str(phrase.sentiment.polarity) + " \ " + str(phrase.sentiment.subjectivity))
        print('.....................')

    return {'polarity':polarities, 'subjectivity':subjectivities}

def get_weighted_polarity_mean(valid_tweets):
    return np.average(valid_tweets['polarity'],weights=valid_tweets['subjectivity'])

def get_polarity_mean(valid_tweets):
    return np.mean(valid_tweets['polarity'])

def print_result(mean):
    if mean > 0.0:
        print('POSITIVE')
    elif mean == 0.0:
        print('NEUTRO')
    else:
        print('NEGATIVE')

if __name__ == "__main__":
    query = input("Entre a query de analise: ")
    analysis = tweet_analysis(query)

    print('MÉDIA PONDERADA: ' + str(get_weighted_polarity_mean(analysis)))
    print_result(get_weighted_polarity_mean(analysis))

    print('MÉDIA: ' + str(get_polarity_mean(analysis)))
    print_result(get_polarity_mean(analysis))
```

**Obs.: Fiquem a vontade para testar entidades de interesse diferentes, aumentar ou diminuir o numero de resultados;**

## Analisando os resultados

Agora que já conseguimos gerar alguns resultados, vale a pena parar um pouco e analisá-los, assim poderemos observar algumas das dificuldades da Análise de sentimento.

### Significados ambíguos

Enquanto eu estava ajeitando os últimos detalhers desse tutorial no ~~domingo~~ com vários meses de antecedência, me deparei com um resultado curioso ao pesquisar por um dos Trending Topics do Brasil: `Fantastico`:

Na noite de domingo uma galera no Twitter estava **furiosa** com alguma matéria que saiu no programa *Fantástico*:

```sh
Tweet: #Fantástico Mestre na arte da manipulação das massas! Admira Hitler #fantastico #pas
Polarity: 0.45 \ 0.9
.....................
Tweet: #fantásticolixo #Fantástico #globolixo
Polarity: 0.4 \ 0.9
.....................
Tweet: #Faustão na militância, e quando acaba vc se lembra que vem logo à seguir o #Fantástico. Esse ano não assisto mais. #BoicoteAGlobo
Polarity: 0.2 \ 0.5
.....................
```

Como é possivel observar, não são tweets muito amigáveis, entretanto, se observarmos a polaridade deles, ela está tendendo mais para o positivo... Por quê? A resposta é simples: o nome do programa. *"Fantástico"* nesse caso está sendo interpretado como uma caracteristica muito positiva, quando na verdade é somente o nome de um programa.

### Tamanho do dataset

Outra coisa que pode gerar dificuldade é o numero de entradas com que temos que trabalhar. Quanto mais dados nós temos (tweets no contexto desse tutorial) melhor e mais precisa será a nossa análise, porém iremos precisar de mais capacidade de processamento. Experimente aumentar o numero de tweets buscados para `100` (que não é nem próximo de uma quantidade satidfatória de análise) e veja quanto tempo demora para o nosso programinha terminar de executar;

```python
def tweet_analysis(query):
    tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(30)
```

Demora não é? Capacidade de processamento é um desafio recorrendte quando se trata de análise textual;

### Perdidos na Tradução

Como já havia mencionado anteriormente no tutorial, a maioria dos processadore textuais livres estão setados para a língua inglesa, então quando se trata de realizar análises para outros idiomas, é necessário que haja um processo de tradução. Veja o que acontece quando a frase `Choque de cultura é irado!` (que tem uma conotação positiva em português) é traduzida pelo google tradutor:

![Choque de cultura is angry](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/choque-de-cultura.png)

`angry` (irritado, irado) em inglês tem uma conotação negativa, fazendo com que um tweet com esse texto, seja interpretado como tendo uma polaridade negativa por causa da tradução, quando na verdade o seu sentido era exatamente o oposto.

## Considerações finais

Chegamos ao fim do nosso tutorial! Espero que tenha sido possível aprender um pouco sobre análise de sentimentos e manipulação textual. Quaisquer dúvidas, podem entrar em contato:

- **E-mail:** bmcosta13@gmail.com
- **Facebook:** fb.com/error404not
- **Twitter:** @ngasonicunicorn

Também gostaria de lembrar que sexta feira dia 19 as 13h40, eu vou apresentar a palestra **Mas afinal, pra que serve Análise de Sentimentos**, onde vocês vão poder saber mais sobre o assunto.

### Referências

Eu utilizei de alguns artigos maravilhosos sobre o assunto para conseguir montar esse tutorial, são eles:

- [Criando um analisador de sentimentos para tweets](https://medium.com/@viniljf/criando-um-analisador-de-sentimentos-para-tweets-a53bae0c5147)
- [Aprenda a fazer um Analisador de Sentimentos do Twitter em Python](https://paulovasconcellos.com.br/aprenda-a-fazer-um-analisador-de-sentimentos-do-twitter-em-python-3979454f2d0d)
- [Introduction to Sentiment Analysis](https://lct-master.org/files/MullenSentimentCourseSlides.pdf)
- [TextBlob: Simplified Text Processing](https://textblob.readthedocs.io/en/dev/)
- [Tweepy](http://www.tweepy.org/)
