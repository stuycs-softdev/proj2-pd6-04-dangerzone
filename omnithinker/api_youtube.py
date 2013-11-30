#!/usr/bin/python 

from apiclient.discovery import build
from optparse import OptionParser

import json
import urllib

DEVELOPER_KEY = "AIzaSyCmBiXQBlUnuYehSvCcM_5CxNuT2hu41Qs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"

def get_topic_id(options):
  freebase_params = dict(query=options.query, key=DEVELOPER_KEY)
  freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
  freebase_response = json.loads(urllib.urlopen(freebase_url).read())

  if len(freebase_response["result"]) == 0:
    exit("No matching terms were found in Freebase.")

  mids = []
  index = 1
  print "The following topics were found:"
  for result in freebase_response["result"]:
    mids.append(result["mid"])
    print "  %2d. %s (%s)" % (index, result.get("name", "Unknown"),
      result.get("notable", {}).get("name", "Unknown"))
    index += 1

  mid = None
  while mid is None:
    index = raw_input("Enter a topic number to find related YouTube %ss: " %
      options.type)
    try:
      mid = mids[int(index) - 1]
    except ValueError:
      pass
  return mid


def youtube_search(mid, options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    topicId=mid,
    type=options.type,
    part="id,snippet",
    maxResults=options.maxResults
  ).execute()

  Videos = list()
  Channels = list()
  Playlists = list()

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      print "%s (http://www.youtube.com/watch?v=%s)" % (search_result["snippet"]["title"],
        search_result["id"]["videoId"])
      Videos.append("%s (http://www.youtube.com/watch?v=%s)" % (search_result["snippet"]["title"],
        search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      print "%s (http://www.youtube.com/channel/%s)" % (search_result["snippet"]["title"],
        search_result["id"]["channelId"])
      Channels.append("%s (http://www.youtube.com/channel/%s)" % (search_result["snippet"]["title"],
        search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      print "%s (http://www.youtube.com/playlist?list=%s)" % (search_result["snippet"]["title"],
        search_result["id"]["playlistId"])
      Playlists.append("%s (http://www.youtube.com/playlist?list=%s)" % (search_result["snippet"]["title"],
        search_result["id"]["playlistId"]))

  print("Testing")
  if len(Videos) > 0 :
    print("Printing out Videos")
    print Videos
    return Videos
  elif len(Channels) > 0 : 
    print("Printing out Channels")
    print Channels
    return Channels
  else:
    print("Printing out Playlists")
    print Playlists
    return Playlists



if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("--query", dest="query", help="Freebase search term",
    default="Goo Goo Dolls")
  parser.add_option("--max-results", dest="maxResults",
    help="Max YouTube results", default=25)
  parser.add_option("--type", dest="type",
    help="YouTube result type: video, playlist, or channel", default="video")
  (options, args) = parser.parse_args()

  mid = get_topic_id(options)
  youtube_search(mid, options)

