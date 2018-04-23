# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

import news
import json

from flask import Flask


app = Flask(__name__)

localGetter = news.newsGetter()


topics = ["bitcoin", "trump", "stocks", "government", "olympics", "north korea"]

rawResults = []

for i in range(len(topics)):
    # loops through the topics to generate articles for each one.
    localGetter.setKeyWord(topics[i])
    rawResults.append(localGetter.run())
    
#for item in range()

#localGetter = news.newsGetter()

#localResult = localGetter.run()

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hey maan'
    
@app.route('/top_stories')
def TopStories():
    #return "Top Stories my man"
    return json.dumps(topics)
    
@app.route('/story/<index>')
def story(index):
    ind = int(index)
    articles = rawResults[ind]
    
    outJson = [{"headline" : articles[0].title,
                "author" : articles[0].author,
                "url" : articles[0].url,
                "image" : articles[0].imageURL,
                "description" : articles[0].description,
                "sentiment" : articles[0].sent},
               {"headline" : articles[1].title,
                "author" : articles[1].author,
                "url" : articles[1].url,
                "image" : articles[1].imageURL,
                "description" : articles[1].description,
                "sentiment" : articles[1].sent},
               {"headline" : articles[2].title,
                "author" : articles[2].author,
                "url" : articles[2].url,
                "image" : articles[2].imageURL,
                "description" : articles[2].description,
                "sentiment" : articles[2].sent}]
                
    return json.dumps(outJson)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    
    #call news function
    
    app.run(host='127.0.0.1', port=8080, debug=True)
    #print("hello world")
    
# [END app]
