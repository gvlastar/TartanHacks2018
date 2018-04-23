import news
import json

def run():
    localGetter = news.newsGetter()

    localResult = localGetter.run()
    
    for item in localResult:
        print (item)
        
run()