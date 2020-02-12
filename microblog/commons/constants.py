"""Constants module."""

from microblog.commons.mixins import EnumChoicesMixin

PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
MAX_RESET_PWD_TOKENS_PER_USER = 200
NAMESPACE_NOTIFICATIONS = '/n'


class Roles:
    PROVIDER = 1
    REVIEWER = 2
    OPERATIONAL = 3
    ADMIN = 4
    DESIGNER = 5

    @classmethod
    def all(cls):
        """Return tuple with all roles."""
        return tuple(val for name, val in vars(cls).items() if name.isupper())


class MediaType(EnumChoicesMixin):
    """Media types."""

    AUDIO = 1
    VIDEO = 2
    IMG = 3
    PDF = 4


MIME_PDF = {'application/pdf'}
MIME_IMG = {'image/png', 'image/jpg', 'image/jpeg', 'image/tiff', 'image/gif'}
MIME_VIDEO = {'video/mp4', 'application/x-troff-msvideo', 'video/avi',
              'video/msvideo', 'video/x-msvideo', 'video/quicktime'}
MIME_AUDIO = {'audio/mpeg', 'audio/mp3', 'audio/mp4'}
ALLOWED_MIME_TYPES = {*MIME_AUDIO, *MIME_VIDEO, *MIME_IMG, *MIME_PDF}

MEDIA_MAPPING = {MediaType.AUDIO.name: MIME_AUDIO,
                 MediaType.VIDEO.name: MIME_VIDEO,
                 MediaType.PDF.name: MIME_PDF,
                 MediaType.IMG.name: MIME_IMG}


class Buckets:
    """List of Bluvalt buckets."""

    MEDIA = 'motherhood-admin-media'
    STAGE = 'motherhood-admin-stage'
    DEV = 'motherhood-admin-dev'
    QA = 'motherhood-admin-qa'


class LanguageType:
    """Language types."""

    ARABIC = 'ar'
    ENGLISH = 'en'


class ContentType(EnumChoicesMixin):
    """Content types."""

    ARTICLES = 1
    COURSES = 2
    EVENTS = 3
    FAQ = 4
    FUNTIME_ACTIVITY = 5
    FUNTIME_SOUND = 6
    FUNTIME_STORY = 7
    OTC = 8
    POSTS = 9
    TIPS = 10
    VIDEOS = 11


class StatusType(EnumChoicesMixin):
    """Status types."""

    PENDING_REVIEWER = 1
    DRAFT = 2
    PUBLISHED = 3
    REJECTED = 4
    DESIGN_REQUIRED = 5
    PENDING_ADMIN = 6


class TargetAudience(EnumChoicesMixin):
    """Target audience types."""

    PREG_ALL = 1
    PREG_LOW = 2
    PREG_HIGH = 3
    PRE_PREG = 4
    POSTPART = 5
    SINGLE = 6
    MARRIED = 7
    MOTHER = 8
    CHILD = 9
    FETAL = 10
    FAMILY = 11


class TargetAudience_new(EnumChoicesMixin):
    """New Target audience types."""

    SINGLE = 1
    MARRIED = 2
    PREV_MARRIED = 3
    PREGNANT = 4
    POSTPART = 5
    OTH_MOTHER = 6
    CHILD = 7


# Max allowed uploaded media per content type
MEDIA_LIMITS = {
    ContentType.ARTICLES: {MediaType.IMG: 10},
    ContentType.VIDEOS: {MediaType.VIDEO: 10},
    ContentType.FUNTIME_ACTIVITY: {MediaType.IMG: 10},
    ContentType.FUNTIME_SOUND: {MediaType.IMG: 10,
                                MediaType.AUDIO: 1},
    ContentType.FUNTIME_STORY: {MediaType.IMG: 10},
}

# in order to send notifications into proper namespace
NAME_SPACES = {
    StatusType.PENDING_REVIEWER: Roles.REVIEWER,
    StatusType.DESIGN_REQUIRED: Roles.DESIGNER,
    StatusType.PENDING_ADMIN: Roles.ADMIN
}


class ContentHandlerTypes:
    APPROVAL = 'approval'
    DASHBOARD_STATS = 'dashboard_stats'
    STATUS_TRANSITION = 'status_transition'


class WSEvents:
    """Web-socket event names."""
    NOTIFICATION = 'notification'


class NotificationUserRooms:
    """Web-socket notification room names."""
    PROVIDER_PERSONAL = 'provider_personal_{user_id}'
    SUPER_ADMIN_ALL = 'super_admin_all'
    SUPER_REVIEWER_ALL = 'super_reviewer_all'
    DESIGNER_ALL = 'designer_all'


ROOMS_PER_USER_ROLE = {
    Roles.ADMIN: (NotificationUserRooms.SUPER_ADMIN_ALL,),
    Roles.REVIEWER: (NotificationUserRooms.SUPER_REVIEWER_ALL,),
    Roles.DESIGNER: (NotificationUserRooms.DESIGNER_ALL,),
    Roles.PROVIDER: (NotificationUserRooms.PROVIDER_PERSONAL,)}

ROOMS_PER_CONTENT_STATUS = {
    StatusType.PUBLISHED.value: (NotificationUserRooms.PROVIDER_PERSONAL,
                                 NotificationUserRooms.SUPER_ADMIN_ALL),
    StatusType.REJECTED.value: (NotificationUserRooms.PROVIDER_PERSONAL,),
    StatusType.DESIGN_REQUIRED.value: (NotificationUserRooms.DESIGNER_ALL,),
    StatusType.PENDING_REVIEWER.value: (NotificationUserRooms.SUPER_REVIEWER_ALL,
                                        NotificationUserRooms.SUPER_ADMIN_ALL),
    StatusType.PENDING_ADMIN.value: (NotificationUserRooms.SUPER_ADMIN_ALL,)}


class ContentNotificationEventType(EnumChoicesMixin):
    STATUS_CHANGE = 1
    DELETE = 2


class UserScope:
    AUTHOR = 'author'
    ROLE = 'role'


NOTIFICATION_TPL_PER_CONTENT_STATUS = {
    StatusType.PUBLISHED.value: 'notifications/provider_published.html',
    StatusType.REJECTED.value: 'notifications/provider_rejected.html',
    StatusType.DESIGN_REQUIRED.value: 'notifications/designer.html',
    StatusType.PENDING_REVIEWER.value: 'notifications/reviewer.html',
    StatusType.PENDING_ADMIN.value: 'notifications/admin.html'}


class ContentStatusProcessingType:
    APPROVE = 'approve'
    SUBMIT = 'submit'
