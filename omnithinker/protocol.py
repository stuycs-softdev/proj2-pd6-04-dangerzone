# States
STATE_WAITING = 0
STATE_READY = 1
STATE_CLOSING = 2

# Client verbs
CVERB_OPEN = "HELLO"
CVERB_UPDATE = "UPDATE"
CVERB_CLOSE = "BYE"

# Server verbs
SVERB_READY = "READY"
SVERB_OK = "OK"
SVERB_BYE = "GOODBYE"
SVERB_INVALID = "INVALID"

# Human-readable server replies
REPLY_INVALID = "Bad transmission."
REPLY_NODOC = "Document doesn't exist."
