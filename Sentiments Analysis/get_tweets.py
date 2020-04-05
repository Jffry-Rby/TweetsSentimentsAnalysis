import authorize
import tweepy
import sys

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id_str)
        is_retweet = hasattr(status, "retweet_status")
        
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text
        
        is_quote = hasattr(status, "quote_status")
        quoted_text = ""
        if is_quote:
            if hasattr(status.quoted_status.extended_tweet["full_text"]):
                quoted_text = status.quote_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        remove_characters = [",","\n"]
        for c in remove_characters:
            text.replace(c," ")
            quoted_text.replace(c, " ")

        with open("out.csv", "a", encoding='utf-8') as f:
            #f.write('%s,%s,%s,%s\n' % (status.created_at, status.user.screen_name, is_retweet, status.text))
            f.write('%s,\n' % (status.text))
    
    def on_error(self, status_code):
        print('Encoutered error in streaming:',status_code )
        sys.exit()

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(authorize.auth_params["app_key"], authorize.auth_params["app_secret"])
    auth.set_access_token(authorize.auth_params["oauth_token"], authorize.auth_params["oauth_token_secret"])
    api = tweepy.API(auth)

    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener = streamListener, tweet_mode='extended')

    tags = ["Covid-19","COVID","COVID19"]
    lang = ['en']
    stream.filter(track=tags,languages=lang)

    
