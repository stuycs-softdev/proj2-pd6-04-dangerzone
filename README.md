OmniThinker
===========

*Project:* BUILD WEBSITE COMBINING IDEAS ON TOPIC SELECTED.

Our project features an interactive but clean writing and brainstorming tool
that allows users to insert a genre and then start typing. As the user starts
typing, suggestions pop up on a right hand toolbar of the window.

The genre chosen will have various points relating to it pop up on the toolbar,
which the user can click on to expand or contract (+ and -).

On expanding, the user decides whether the information is relevant to the topic
at hand. As the user writes and uses the suggestions from the toolbar, more
options pop up on the toolbar, offering more advice and possible points to hit
on in the course of writing. The information presented in the toolbar features
common sources from Google, Wikipedia and DuckDuckGo's API. By maintaining a
socket connection between the Python server and the JS client, we take input
from the user to create a list of relevant topics, and as the user crosses out
various topic boxes in the toolbar, more boxes pop up.

Depending on whether the user has a login or not, she can view the essays she
has written in the past or start with a blank template. With an SQlite database,
we store the data that the user, logged in or not, has written. To take input,
the user highlights certain words in the essay that they're writing and then our
software performs a search for those words, returning links, videos, article
titles, and snippets of information on the topic. The input is sent to the
SQlite which then sends the key words to a search function in the API mentioned.
They in turn, fetch data that is parsed in Python, which is then finally after
filtering, sent back and displayed via Javascript on the website. Once the user
has finished writing, he can then export what he has written into an external
PDF or text file stored in the SQlite database. The highlighted words won't show
up in the output file.

For instance: The user selects Obama as the topic of a history paper. Possible
links that pop up in the sidebar include: Patient Protection and Affordable
Care Act, Senate Filibuster, Government Shutdown, Obama versus Bush Legacy,
Nuclear Sanctions on Iran, and Tensions in Asia. As the user selects and uses
the information in a topic, she can then X them out and other ideas pop onto
the toolbar for the user's perusal that are directly related to the topic at
hand similar to how a Queue of Information. Included with such topics are other
broader topics indirectlyr related to Obama such as the American Government,
Michelle Obama, Joe Biden, and Presidential Election of 2012. Furthermore, if
the user wishes to search more specifically on these other relevant topics, she
can type for instasnce Michelle Obama and highlight it, thereby updating the
queue to hold information directly related to Michelle Obama and topics that
can be traced back to it (indirectly related). Through a recursive call on
topics, related topics, and direct information, the user may craft a work of
writing, letting our project, Omnithinker, do the data fetching and provoke
"thinking in all directions" by forcing the user to consider ideas and weigh in
data from various sources.

*Role Division:*

+ Aaron Coppa: DuckDuckGo API, API Aggregator
+ Edric Huang: FrontEnd Web Design
+ Ben Kurtovic: Websocket Connection, Javascript, SQLite Database
+ Jing Lin: Google API, Youtube API, NYT API

Installing
----------

    pip install virtualenv
    virtualenv env
    source env/bin/activate
    pip install flask flask-sockets gunicorn beautifulsoup4 google-api-python-client xhtml2pdf
    mkdir logs

Running
-------

    source env/bin/activate
    ./run.sh

Now go to [http://localhost:6004](http://localhost:6004).

**VERY IMPORTANT:** Since DOETWAC blocks connection requests to the server
hosting the data, only stuycs or a proxy server can run the project in school.
For our demo, we are running the project on Aaron's computer, which uses a
proxy server.
