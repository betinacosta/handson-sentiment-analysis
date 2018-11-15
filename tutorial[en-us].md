# Hands On Sentiment Analysis

Imagine if you were able to identify users' emotional responses to a particular entity of interest, be able to find out if people were happy with the sale of GitHub to Microsoft, or sadder than Tony Stark at the end of Infinity War. If you found that interesting, you've came the right place. In this tutorial we will learn how to implement Sentiment Analysis using Twitter Data in a simple and educative way. Let's go?

## Requirements

- Python3
- Git
- Pip
- TextBlob
- TweePy
- Numpy
- A Twitter account

### Installing the libraries

- `pip install -r requirements.txt`
- `python -m textblob.download_corpora`

## Requesting a developer profile

Let's begin with the boring part: create a developer profile and an APP on Twitter. This part used to be very simple, but now twitter requires a lot of explanations and descriptions that can be a little annoying to fill, so... I will give you some templates that you can use in order to ~~cheat~~ waste less time.

**1**. Let's start by accessing https://developer.twitter.com/ and clicking on `Apply`:

![Apply](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/apply.png)

**2**. On the next page, click `Apply for a developer account` and `Continue` on the the page that follows it to proceed:

![Apply for a developer account](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/apply-developer.png)

![Continue](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/continue.jpeg)

**3**. Enter the type of account you are creating (`Personal Use` most likely) and fill the required information:

![Account Type](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/tipo-de-conta.png)

**4**. On the next page there will be some info that needs to be fill. Fill the field `What use case(s) are you interested in?` according to the image bellow and at `Describe in your own words what you are building` enter the following text:

```text
1. I’m using Twitter’s APIs to run a PyCon Tutorial about Sentiment Analysis;
2. I plan to analyse Tweets to understand how people are feeling regarding some subject.
3. The solution does not involve tweeting, retweeting, neither liking content on twitter. It is just for analysis;
4. The solution does not involve displaying twitter explicitly, but its polarity and subjectivity
```

![Use Cases](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/casos-de-uso.png)

On `Will your product, service, or analysis make Twitter content or derived information available to a government entity?` select `no`

**5**. ~~Pretend to~~ read  the `Terms of Service` and click `agree`

**6**. Now you only have to **confirm your email** and proceed to the next part :)

## Creating an APP on Twitter

**1**. Access [Twitter's development site](https://developer.twitter.com/en/apps) and click `Create an APP`


![Creating an App](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/craindo-app.png)

**2**. Enter the required information. In the field `Tell us how this app will be used` you can use the following text:

```text
This app is for personal use and will be used to develop a simple Sentiment Analysis App for a tutorial.
```

Regarding to `website`, you can enter any URL you like, including your twitter profile.

**3**. Access `Keys and Tokens` to view your authentication info.

![Keys and Tokens](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/keys-and-tokens.png)

*Obs.: In order to the `Access Token` and the `Access Token Secret` be available, you have to click `Create Tokens` (Or something very close to that) that's located down the page.*

**4**. Now that you have your APP and all the permissions we can proceed to the fun part!

## Let's get to work!

**1**. Finally we can proceed to what this tutorial is really about! Let's start by creating an .py file at the editor you feel more    comfortable with and import the libs we are going to use: 

```python
import tweepy
import numpy as np
from textblob import TextBlob
```

**2**. Now, let's set the variables that will receive your API keys:

```python
consumer_key='your_consumer_key'
consumer_secret='consumer_secret'

access_token='access_token'
access_token_secret='access_token_secret'
```

*__Obs.: If you prefere, you can put the keys in a separated file__*

*__Obs2.: If you intend to commit this code somewhere, I recommend [setting the keys as environment variables and import them](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/src/keys.py)__*

**3**. Having set our keys, let's do the authentication in our script:

```python
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
```

*Obs.: If you wish to know whether your authentication is working, `tweepy.API(auth)` should return something like `<tweepy.api.API object at 0x10d3c3240>` when called*

*__Obs2.: If you're having a `SyntaxError: invalid syntax` error at `def _start(self, async):`, run `$pip3 install --upgrade git+https://github.com/tweepy/tweepy.git` to fix it__*

**4**. Now, let's search for our tweets! To do that we are going to use tweepy. As the most important thing this week is definitely PyCon, we can look for tweets that make reference to this subject.

```python
tweets = api.search('PyCon')
```

or ignore RTs to have a slightly more targeted result:

```python
tweets = api.search('PyCon -filter:retweets')
```

**5**. And iterate over the results by taking our tweets `tweet.text` and putting in TextBlob

```python
for tweet in tweets:
    phrase = TextBlob(tweet.text)
```

**6**. Once we have our tweets, we analyse the sentiment withing its content. However, we may have a problem: TextBlob algorithm was trained to do analysis in english. If there's a chance that you search will return results in other languages, translation will be necessary (Don't worry, TextBlob uses google translator and can do all this for us). The only thing we have to do is testing our input to see if it needs translation:

```python
def is_english(text):
    if text.detect_language() == 'en':
        return True
    return False
```

*Obs.: It's worth saying that translation can jeopardize the analysis, because some meanings can be lost in translation.*

**7**. Inside the for, we will check if the tweets language is different from english using the method we just created. If it is, we will translate and then proceed to the sentiment analysis.

```python
polarities = []

for tweet in tweets:
    phrase = TextBlob(tweet.text)

    if not is_english(phrase):
        phrase = TextBlob(str(phrase.translate(to='en')))

    print('Tweet: ' + tweet.text)
    print('Polarity: ' + str(phrase.sentiment.polarity) + ' \ Subjectivity: ' + str(phrase.sentiment.subjectivity))
    print('.....................')
```

### The more you know:

Before we proceed, let's understand what we are seeing:

**POLARITY:** It's a value from -1.0 to 1.0, where -1.0 referes to a 100% negative polarity and 1.0 to 100% positive polarity.

**SUBJECTIVITY:** It's a value from 0.0 e 1.0, where 0 referes to a 100% objective text and 1.0 a 100% subjetive text.

**SUBJECTIVITY x OBJECTIVITY:** Objective sentences usually contain facts and information, while subjective sentences express personal feelings and opinions.

### Continuing...

**8**. Well, now that we know what polarity and subjectivity is, we should ignore results where the polarity is neutral and are objectives (subjectivity 0.0), once we are only interested in sentences that express polarized feelings.

```python
if (phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0):
    polarities.append(phrase.sentiment.polarity)
```

Now that this part is finished, we can place this inside a function, to make everything more organized and clean:

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
        print('Polarity: ' + str(phrase.sentiment.polarity) + ' \ Subjectivity: ' + str(phrase.sentiment.subjectivity))
        print('.....................')

    return polarities
```

**9**. And use numpy to calculate the polarities mean and find out whether the average opinion is positive (closest to 1.0) or negative (closest to -1.0)

```python
polarity_mean = np.mean(polarities)

print('Mean: ' + str(polarity_mean))
if(polarity_mean > 0.0):
    print('POSITIVE')
else:
    print('NEGATIVE')
```

**10**. Done! Now we have a humble tweets analyser... However, and can go a little bit further.

### Going a little further

**11**. Let's change our search method a little: instead of `tweets = api.search('PyCon -filter:retweets')` let's use:

```python
tweets = tweepy.Cursor(api.search, q="PyCon -filter:retweets").items(20)
```

This ways, we will filter only the tweets that aren't retweets and get a chosen number of tweets

**12**. Another thing we can do, is pass `result_type='recent'` parameter in order to get only the most recent tweets

```python
tweets = tweepy.Cursor(api.search, q="PyCon -filter:retweets", result_type="recent").items(20)
```

**13**. Before we proceed to the next steps, we can refactor our code a bit to make things clearer. As for example, we can store our polarities and subjectivities in a dictionary and return it. This way, we can use this data the way we prefer:

```python
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
        print('Polarity: ' + str(phrase.sentiment.polarity) + ' \ Subjectivity: ' + str(phrase.sentiment.subjectivity))
        print('.....................')

    return {'polarity':polarities, 'subjectivity':subjectivities}
```

**14**. Now that we have a dictionary with all the information we need, an approach we can try is to calculate a weighted mean instead of simple mean...

![Meme nazare](https://github.com/betinacosta/handson-sentiment-analysis/blob/master/images/media-ponderada.jpg)

Don't panic... Weighted mean is nothing but a mean calculation where some values ​​have a greater weight than the other, this way we can calculate the polarity mean using subjectivity as weight. By doing that, more subjective tweets (more emotional) will have a greater weight.

```python
def get_weighted_polarity_mean(valid_tweets):
    return np.average(valid_tweets['polarity'],weights=valid_tweets['subjectivity'])
```

**15** Since we are here we can also put our simple mean inside a function to keep the pattern

```python
def get_polarity_mean(valid_tweets):
    return np.mean(valid_tweets['polarity'])
```

**16**. We can also receive our query as parameter for the function that will perform the analyse

```python
def tweet_analysis(query):
    tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(20)
```

**17**. For a better visualization of results, we can create a function that will responsible for showing results on screen:

```python
def print_result(mean):
    if mean > 0.0:
        print('POSITIVE')
    elif mean == 0.0:
        print('NEUTRO')
    else:
        print('NEGATIVE')
```

**18**. And finally, we can add a `if __name__ == "__main__"` to easily execute our script:

```python
if __name__ == "__main__":
    query = input("Query: ")
    analysis = tweet_analysis(query)

    print('WEIGHTED MEAN: ' + str(get_weighted_polarity_mean(analysis)))
    print_result(get_weighted_polarity_mean(analysis))

    print('MEAN: ' + str(get_polarity_mean(analysis)))
    print_result(get_polarity_mean(analysis))
```

**16**. The final code will be something like this:

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
        print('Polarity: ' + str(phrase.sentiment.polarity) + ' \ Subjectivity: ' + str(phrase.sentiment.subjectivity))
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
        print('NEUTRAL')
    else:
        print('NEGATIVE')

if __name__ == "__main__":
    query = input("Entre a query de analise: ")
    analysis = tweet_analysis(query)

    print('WEIGHTED MEAN: ' + str(get_weighted_polarity_mean(analysis)))
    print_result(get_weighted_polarity_mean(analysis))

    print('MEAN: ' + str(get_polarity_mean(analysis)))
    print_result(get_polarity_mean(analysis))
```

**Obs.: Be comfortable to use different interest entities, increase or decrease the number of results;**=

## Analysing the Results

Now that we manage to generate some results, it's worth stopping a little and analyzing them, so we can observe some of the challenges  of Sentiment Analysis.

### Ambiguous meanings

On a beautiful Sunday night while I was doing the last tests of this code, I came across a curious result when searching for one of Trending Topics in Brazil: `Fantastico`:

*Obs.: The original tweets were in portuguese, but translated it for us :)*

```sh
Tweet: #Fantástico Master in the art of mass manipulation! Admirer of Hitler #fantastico #peace
Polarity: 0.45 \ 0.9
.....................
Tweet: #fantásticoisgarbage #Fantástico #globogarbage
Polarity: 0.4 \ 0.9
.....................
Tweet: #Faustão on militancy, and when it finishes you remember that soon follows #Fantastic. This year I won't watch it anymore. #boycottToGlobo
Polarity: 0.2 \ 0.5
.....................
```

So, I believe a little bit of context is necessary:

- __Fantástico:__ Is the of a late show in Brazil.
- __Faustão:__ Is the name of a TV host, very famous in Brazil.
- __Globo:__ Is a very famous TV channel in Brazil.

And, all this took place during election week in Brazil, one of the most disputed in recent times.

As you can see, those tweets are not exactly friendly, but if you observe their polarity is being calculated as mainly positive... But Why? Well the answer is very simple and yet frustrating: The name of the show. *__Fantástico__* in portuguese means *fantastic*, which is a positive word, because of that, our little script evaluates it as a very positive word (when in fact it is just the name of the show) and messes up the result.

![Facepalm](https://media.giphy.com/media/YaQIUCZ3FIcrS/giphy.gif)

### Dataset Size:

Another thing that may cause some difficulties is the number of entries that we are going to work with. The more data we have (tweets in the context of this tutorial) the better and more accurate our analysis will be, but we will need more processing power. Try increasing the number of searched tweets for `500` (which is not even close to a satisfactory amount for analysis) and see how long it takes for our program finish executing:

```python
def tweet_analysis(query):
    tweets = tweepy.Cursor(api.search, q=query + " -filter:retweets").items(500)
```

Almost as long as *The Return of the King* isn't it? Processing power is a constant challenge when it comes to textual analysis.

## Final Considerations

We reached the end of our tutorial! I hope it has been possible to learn a little bit about sentiment analysis and textual manipulation. Any questions, please let me know:

- **E-mail:** bmcosta13@gmail.com
- **Facebook:** fb.com/error404not
- **Twitter:** @ngasonicunicorn

### References

I made use of some amazing articles about the subject to be able to assemble this tutorial, check them for more:

- [Criando um analisador de sentimentos para tweets](https://medium.com/@viniljf/criando-um-analisador-de-sentimentos-para-tweets-a53bae0c5147)
- [Aprenda a fazer um Analisador de Sentimentos do Twitter em Python](https://paulovasconcellos.com.br/aprenda-a-fazer-um-analisador-de-sentimentos-do-twitter-em-python-3979454f2d0d)
- [Introduction to Sentiment Analysis](https://lct-master.org/files/MullenSentimentCourseSlides.pdf)
- [TextBlob: Simplified Text Processing](https://textblob.readthedocs.io/en/dev/)
- [Tweepy](http://www.tweepy.org/)
