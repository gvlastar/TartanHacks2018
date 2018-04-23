# File for creating a list of articles based on NewsAPI

from newsapi import NewsApiClient
from newspaper import Article
from urllib.request import *
import string

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Creates client & organizes categories
newsapi = NewsApiClient('01ca7b6450ef4d35b9036e3392e54fdd')
cat = ["", "business", "entertainment", "general", "health", "science", "sports", "technology"]
client = language.LanguageServiceClient()

class newsGetter():
    #Initializes default parameters
    def __init__(self, keyword = "trump"):
        self.keyword = keyword
        self.catNum = 0
        self.top_headlines = ""
        self.artList = []
        self.lim = 10
        self.bestArticles = []

    # Changes keyword
    def setKeyWord(self, input):
        self.keyword = input

    # Changes category based on int input
    def setCategory(self, input):
        self.catNum = input % 8

    # Refreshes headlines based on current parameters
    def getHeadlines(self):
        self.top_headlines = newsapi.get_top_headlines(q=self.keyword, category=cat[self.catNum], language="en")

    # Processes json file into separate data types
    def listArticles(self):
        if(self.top_headlines["totalResults"] > 0):
            if(len(self.artList) != 0):
                self.artList = []
            if(self.lim > 0 and self.lim <= self.top_headlines['totalResults']):
                for i in range(self.lim):
                    art = self.top_headlines['articles'][i]

                    # Extract Text
                    new = Article(art['url'])
                    new.download()
                    new.parse()
                    storyText = "".join(filter(lambda x: x in string.printable, new.text))
                    descr = "".join(filter(lambda x: x in string.printable, art['description']))
                    title = "".join(filter(lambda x: x in string.printable, art['title']))

                    # Sentiment Analysis
                    document = types.Document(content=storyText,type=enums.Document.Type.PLAIN_TEXT)
                    sentiment = client.analyze_sentiment(document=document).document_sentiment

                    newStory = Story(url=art['url'], title=title, source=art['source']['name'], 
                        text=storyText, author=art['author'], imageURL=art['urlToImage'], 
                        date=art['publishedAt'][:10], des=descr, sent=sentiment.score,
                        mag=sentiment.magnitude)
                    self.artList.append(newStory)
            else:
                for art in self.top_headlines["articles"]:
                    new = Article(art['url'])
                    new.download()
                    new.parse()
                    storyText = "".join(filter(lambda x: x in string.printable, new.text))
                    descr = "".join(filter(lambda x: x in string.printable, art['description']))
                    title = "".join(filter(lambda x: x in string.printable, art['title']))
                    
                    # Sentiment Analysis
                    document = types.Document(content=storyText,type=enums.Document.Type.PLAIN_TEXT)
                    sentiment = client.analyze_sentiment(document=document).document_sentiment

                    newStory = Story(url=art['url'], title=title, source=art['source']['name'], 
                        text=storyText, author=art['author'], imageURL=art['urlToImage'], 
                        date=art['publishedAt'][:10], des=descr, sent=sentiment.score,
                        mag=sentiment.magnitude)

                    self.artList.append(newStory)
        else:
            print("There were no articles with the query :", self.keyword)

    # Outputs a list of article objects
    def output(self):
        return self.artList

    # Runs complete cycle once
    def run(self):
        self.getHeadlines()
        self.listArticles()
        self.output()
        self.getBest()
        for artc in self.bestArticles:
            print(artc.__dict__, end="\n\n")
        return self.bestArticles

    def getBest(self):
        best = 0
        bestArt = None
        worst = 0
        worstArt = None
        neut = None
        neutBest = None
        for art in self.artList:
            if(art.sent >= best):
                best = art.sent
                bestArt = art
            elif(art.sent <= worst):
                worst = art.sent
                worstArt = art

            if(neut == None or art.mag < neut):
                neut = art.mag
                neutBest = art

        self.bestArticles.append(bestArt)
        print("hi")
        self.bestArticles.append(neutBest)
        self.bestArticles.append(worstArt)


# Class for storing data from each article
class Story():
    def __init__(self, url, imageURL, title, date, source, text, sent, mag, 
        author, des):
        self.url = url
        self.title = title
        self.source = source
        self.text = text
        self.date = date
        self.author = author
        self.imageURL = imageURL
        self.description = des
        self.sent = sent
        self.mag = mag

def main():
    news = newsGetter()
    news.run()

if __name__ == '__main__':
    main()





#search = input("Enter a keyword : ")

# top_headlines = newsapi.get_top_headlines(q="Donald Trump", category=cat[0], language="en")

# # print(top_headlines)
# print(top_headlines["totalResults"])

# urls = []
# titles = []


# for key in top_headlines["articles"]:
#     urls.append(key['url'])
#     titles.append(key['title'])
#     print(key["publishedAt"][:10])
#     print(key['description'])

# for i in range(len(urls)):
#     print(urls[i], end="\n")
#     print(titles[i], end="\n\n")
#     art = Article(urls[i])
#     art.download()
#     art.parse()
