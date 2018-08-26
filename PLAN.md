# Planning 

## Character Details
* Character Name
* Class(es) Level(s)
* Faction
* Player Name
* Player DCI
* Sheet (page) #

### Endpoints
POST /character

GET /characters
GET /characters/:cid:
PUT /characters/:cid:
DELETE /characters/:cid:

## Session Details
* Adventure Name
* Adventure Code
* Session #
* Date
* DM Name
* DM DCI
* Starting
    * XP
    * Gold
    * Downtime
    * Renown
    * Magic Items
* Earned
    * XP
    * Gold
    * Downtime
    * Renown
    * Magic Items
* Total
    * XP
    * Gold
    * Downtime
    * Renown
    * Magic Items
* Notes
    * Downtime activity
    * Bought/Acquired (Acquired)
    * Sold/Used (Removed)
    * Story Awards
    * Notes
        

### Endpoints
POST /characters/:cid:/session

GET /characters/:cid:/sessions
GET /characters/:cid:/sessions/:sid:
PUT /characters/:cid:/sessions/:sid:
DELETE /characters/:cid:/sessions/:sid:


# Resources
* http://flask.pocoo.org/docs/1.0/tutorial/