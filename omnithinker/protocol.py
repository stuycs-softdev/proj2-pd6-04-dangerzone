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
SVERB_UPDATE = "UPDATE"
SVERB_BYE = "GOODBYE"
SVERB_INVALID = "INVALID"

# Human-readable server replies
REPLY_INVALID = "Your client sent invalid data to the server."
REPLY_NODOC = "This document doesn't exist."
REPLY_LOCKED = "This document is read-only because someone else already has it open."
