#!/usr/bin/python

import json
import urllib

from apiclient.discovery import build

class Youtube():
    def __init__(self, topic):
        DEVELOPER_KEY = "AIzaSyCmBiXQBlUnuYehSvCcM_5CxNuT2hu41Qs"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"

        mid = self.get_topic_id(topic)
        self.videos = self.youtube_search(mid, topic)
        self.counter = 0


    def get_topic_id(self, options):
      DEVELOPER_KEY = "AIzaSyCmBiXQBlUnuYehSvCcM_5CxNuT2hu41Qs"
      YOUTUBE_API_SERVICE_NAME = "youtube"
      YOUTUBE_API_VERSION = "v3"
      FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"


      freebase_params = dict(query=options.query, key=DEVELOPER_KEY)
      freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
      freebase_response = json.loads(urllib.urlopen(freebase_url).read())

      mids = []
      if len(freebase_response["result"]) == 0:
#            exit("No matching terms were found in Freebase.")
        return mids

      index = 1
#        print "The following topics were found:"
      for result in freebase_response["result"]:
          mids.append(result["mid"])
#            print "  %2d. %s (%s)" % (index, result.get("name", "Unknown"), result.get("notable", {}).get("name", "Unknown"))
          index += 1

      mid = mids[0]
      while mid is None:
          index = raw_input("Enter a topic number to find related YouTube %ss: " % options.type)
          try:
              mid = mids[int(index) - 1]
          except ValueError:
            pass
      return mid


    def youtube_search(self, mid, options):
        DEVELOPER_KEY = "AIzaSyCmBiXQBlUnuYehSvCcM_5CxNuT2hu41Qs"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list( topicId=mid, type=options.type, part="id,snippet", maxResults=options.maxResults).execute()

        Videos = {}
        Channels = {}
        Playlists = {}
        Videos['Title'] = [0]*20
        Videos['Link'] = [0]*20
        i = 0
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
#                  print "%s (http://www.youtube.com/watch?v=%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"])
                Videos['Link'][i] ="http://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
                Videos['Title'][i] = search_result["snippet"]["title"]
                i += 1
                if i > 19:
                    break
            #elif search_result["id"]["kind"] == "youtube#channel":
#                print "%s (http://www.youtube.com/channel/%s)" % (search_result["snippet"]["title"], search_result["id"]["channelId"])
            #  Channels.append("%s (http://www.youtube.com/channel/%s)" % (search_result["snippet"]["title"], search_result["id"]["channelId"]))
            #elif search_result["id"]["kind"] == "youtube#playlist":
#                print "%s (http://www.youtube.com/playlist?list=%s)" % (search_result["snippet"]["title"], search_result["id"]["playlistId"])
            #  Playlists.append("%s (http://www.youtube.com/playlist?list=%s)" % (search_result["snippet"]["title"], search_result["id"]["playlistId"]))

        return Videos
#          if len(Videos) > 0 :
#                return Videos
#          elif len(Channels) > 0 :
#                return Channels
#          else:
#              return Playlists

    def getVideo(self):
        if self.videos['Title'][self.counter] == 0:
            return ""
        else:
            self.counter += 1
            ret = [0]*2
            ret[0] = self.videos['Title'][self.counter - 1]
            ret[1] = self.videos['Link'][self.counter - 1]
            return ret
if __name__ == "__main__":
    y = Youtube("Obama")
    print y.getVideo()
    print y.getVideo()
    print y.getVideo()
    print y.getVideo()
