
class Yak(object):
    def __init__(self, json):
        self.canDownVote = json['canDownVote']
        self.canReport = json['canReport']
        self.canReply = json['canReply']
        self.canUpVote = json['canUpVote']
        self.canVote = json['canVote']
        self.comments = json['comments']
        self.deliveryID = json['deliveryID']
        self.gmt = json['gmt']
        self.handle = json['handle']
        self.hidePin = json['hidePin']
        self.liked = json['liked']
        self.latitude = json['latitude']
        self.location = json['location']
        self.locationDisplayStyle = json['locationDisplayStyle']
        self.locationName = json['locationName']
        self.longitude = json['longitude']
        self.message = json['message']
        self.messageID = json['messageID']
        self.numberOfLikes = json['numberOfLikes']
        self.posterID = json['posterID']
        self.readOnly = json['readOnly']
        self.reyaked = json['reyaked']
        self.score = json['score']
        self.time = json['time']
        self.type = json['type']

        # Image Yaks
        self.expandInFeed = json.get('expandInFeed', 0)
        self.imageHeight = json.get('imageHeight', 0)
        self.imageWidth = json.get('imageWidth', 0)
        self.thumbNailUrl = json.get('thumbNailUrl', None)
        self.url = json.get('url', None)
