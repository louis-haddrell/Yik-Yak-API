
class Yak(object):
    def __init__(self, json):
        self.can_downvote = json['canDownVote']
        self.can_reply = json['canReply']
        self.can_report = json['canReport']
        self.can_upvote = json['canUpVote']
        self.can_vote = json['canVote']
        self.comments = json['comments']
        self.delivery_id = json['deliveryID']
        self.gmt = json['gmt']
        self.handle = json['handle']
        self.hide_pin = json['hidePin']
        self.latitude = json['latitude']
        self.liked = json['liked']
        self.location = json['location']
        self.location_display_style = json['locationDisplayStyle']
        self.location_name = json['locationName']
        self.longitude = json['longitude']
        self.message = json['message']
        self.message_id = json['messageID']
        self.number_of_likes = json['numberOfLikes']
        self.poster_id = json['posterID']
        self.read_only = json['readOnly']
        self.reyaked = json['reyaked']
        self.score = json['score']
        self.time = json['time']
        self.type = json['type']

        # Image Yaks
        self.expand_in_feed = json.get('expandInFeed', 0)
        self.image_height = json.get('imageHeight', 0)
        self.image_width = json.get('imageWidth', 0)
        self.thumbnail_url = json.get('thumbNailUrl', None)
        self.url = json.get('url', None)


class Comment(object):
    def __init__(self, json):
        self.back_id = json['backID']
        self.comment = json['comment']
        self.comment_id = json['commentID']
        self.delivery_id = json['deliveryID']
        self.gmt = json['gmt']
        self.is_deleted = json['isDeleted']
        self.liked = json['liked']
        self.message_id = json['messageID']
        self.number_of_likes = json['numberOfLikes']
        self.overlay_id = json['overlayID']
        self.poster_id = json['posterID']
        self.time = json['time']
