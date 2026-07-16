import datetime

from . import model_pb2 as _model_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from .validate import validate_pb2 as _validate_pb2
from .google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConversationOwnerFilter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONVERSATION_OWNER_FILTER_UNSPECIFIED: _ClassVar[ConversationOwnerFilter]
    CONVERSATION_OWNER_FILTER_ALL: _ClassVar[ConversationOwnerFilter]
    CONVERSATION_OWNER_FILTER_MINE: _ClassVar[ConversationOwnerFilter]
    CONVERSATION_OWNER_FILTER_OTHERS: _ClassVar[ConversationOwnerFilter]
    CONVERSATION_OWNER_FILTER_UNASSIGNED: _ClassVar[ConversationOwnerFilter]

class ListConversationsSort(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LIST_CONVERSATIONS_SORT_UNSPECIFIED: _ClassVar[ListConversationsSort]
    LIST_CONVERSATIONS_SORT_NEWEST_FIRST: _ClassVar[ListConversationsSort]
    LIST_CONVERSATIONS_SORT_OLDEST_FIRST: _ClassVar[ListConversationsSort]
    LIST_CONVERSATIONS_SORT_MOST_UNREAD: _ClassVar[ListConversationsSort]

class SearchMessagesSort(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEARCH_MESSAGES_SORT_UNSPECIFIED: _ClassVar[SearchMessagesSort]
    SEARCH_MESSAGES_SORT_NEWEST_FIRST: _ClassVar[SearchMessagesSort]
    SEARCH_MESSAGES_SORT_OLDEST_FIRST: _ClassVar[SearchMessagesSort]

class AiSuggestionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AI_SUGGESTION_STATUS_UNSPECIFIED: _ClassVar[AiSuggestionStatus]
    AI_SUGGESTION_STATUS_PENDING: _ClassVar[AiSuggestionStatus]
    AI_SUGGESTION_STATUS_FAILED: _ClassVar[AiSuggestionStatus]
    AI_SUGGESTION_STATUS_COMPLETED: _ClassVar[AiSuggestionStatus]

class DashboardTimePreset(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DASHBOARD_TIME_PRESET_UNSPECIFIED: _ClassVar[DashboardTimePreset]
    DASHBOARD_TIME_PRESET_TODAY: _ClassVar[DashboardTimePreset]
    DASHBOARD_TIME_PRESET_LAST_7_DAYS: _ClassVar[DashboardTimePreset]
    DASHBOARD_TIME_PRESET_LAST_30_DAYS: _ClassVar[DashboardTimePreset]
    DASHBOARD_TIME_PRESET_CUSTOM: _ClassVar[DashboardTimePreset]
    DASHBOARD_TIME_PRESET_1_SHIFT: _ClassVar[DashboardTimePreset]

class DashboardProcessingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DASHBOARD_PROCESSING_TYPE_UNSPECIFIED: _ClassVar[DashboardProcessingType]
    DASHBOARD_PROCESSING_TYPE_AI_ONLY: _ClassVar[DashboardProcessingType]
    DASHBOARD_PROCESSING_TYPE_HUMAN_ONLY: _ClassVar[DashboardProcessingType]
    DASHBOARD_PROCESSING_TYPE_AI_PLUS_HUMAN: _ClassVar[DashboardProcessingType]

class ChatGroupDeliveryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_GROUP_DELIVERY_STATUS_UNSPECIFIED: _ClassVar[ChatGroupDeliveryStatus]
    CHAT_GROUP_DELIVERY_STATUS_SENT: _ClassVar[ChatGroupDeliveryStatus]
    CHAT_GROUP_DELIVERY_STATUS_RECEIVED: _ClassVar[ChatGroupDeliveryStatus]
    CHAT_GROUP_DELIVERY_STATUS_READ: _ClassVar[ChatGroupDeliveryStatus]

class ChatGroupMemberChangeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_GROUP_MEMBER_CHANGE_TYPE_UNSPECIFIED: _ClassVar[ChatGroupMemberChangeType]
    CHAT_GROUP_MEMBER_CHANGE_TYPE_ADDED: _ClassVar[ChatGroupMemberChangeType]
    CHAT_GROUP_MEMBER_CHANGE_TYPE_REMOVED: _ClassVar[ChatGroupMemberChangeType]
    CHAT_GROUP_MEMBER_CHANGE_TYPE_LEFT: _ClassVar[ChatGroupMemberChangeType]
    CHAT_GROUP_MEMBER_CHANGE_TYPE_JOINED: _ClassVar[ChatGroupMemberChangeType]
    CHAT_GROUP_MEMBER_CHANGE_TYPE_ROLE_CHANGED: _ClassVar[ChatGroupMemberChangeType]

class ChatGroupTopicChangeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_GROUP_TOPIC_CHANGE_TYPE_UNSPECIFIED: _ClassVar[ChatGroupTopicChangeType]
    CHAT_GROUP_TOPIC_CHANGE_TYPE_CREATED: _ClassVar[ChatGroupTopicChangeType]
    CHAT_GROUP_TOPIC_CHANGE_TYPE_UPDATED: _ClassVar[ChatGroupTopicChangeType]
    CHAT_GROUP_TOPIC_CHANGE_TYPE_DELETED: _ClassVar[ChatGroupTopicChangeType]

class DirectMessageDeliveryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECT_MESSAGE_DELIVERY_STATUS_UNSPECIFIED: _ClassVar[DirectMessageDeliveryStatus]
    DIRECT_MESSAGE_DELIVERY_STATUS_SENT: _ClassVar[DirectMessageDeliveryStatus]
    DIRECT_MESSAGE_DELIVERY_STATUS_RECEIVED: _ClassVar[DirectMessageDeliveryStatus]
    DIRECT_MESSAGE_DELIVERY_STATUS_READ: _ClassVar[DirectMessageDeliveryStatus]

class PushPlatform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUSH_PLATFORM_UNSPECIFIED: _ClassVar[PushPlatform]
    PUSH_PLATFORM_ANDROID: _ClassVar[PushPlatform]
    PUSH_PLATFORM_IOS: _ClassVar[PushPlatform]
    PUSH_PLATFORM_WEB_CHROME: _ClassVar[PushPlatform]
    PUSH_PLATFORM_WEB_FIREFOX: _ClassVar[PushPlatform]

class PreviewLinkResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PREVIEW_LINK_RESULT_UNSPECIFIED: _ClassVar[PreviewLinkResult]
    PREVIEW_LINK_RESULT_OK: _ClassVar[PreviewLinkResult]
    PREVIEW_LINK_RESULT_NO_METADATA: _ClassVar[PreviewLinkResult]
    PREVIEW_LINK_RESULT_FETCH_FAILED: _ClassVar[PreviewLinkResult]
CONVERSATION_OWNER_FILTER_UNSPECIFIED: ConversationOwnerFilter
CONVERSATION_OWNER_FILTER_ALL: ConversationOwnerFilter
CONVERSATION_OWNER_FILTER_MINE: ConversationOwnerFilter
CONVERSATION_OWNER_FILTER_OTHERS: ConversationOwnerFilter
CONVERSATION_OWNER_FILTER_UNASSIGNED: ConversationOwnerFilter
LIST_CONVERSATIONS_SORT_UNSPECIFIED: ListConversationsSort
LIST_CONVERSATIONS_SORT_NEWEST_FIRST: ListConversationsSort
LIST_CONVERSATIONS_SORT_OLDEST_FIRST: ListConversationsSort
LIST_CONVERSATIONS_SORT_MOST_UNREAD: ListConversationsSort
SEARCH_MESSAGES_SORT_UNSPECIFIED: SearchMessagesSort
SEARCH_MESSAGES_SORT_NEWEST_FIRST: SearchMessagesSort
SEARCH_MESSAGES_SORT_OLDEST_FIRST: SearchMessagesSort
AI_SUGGESTION_STATUS_UNSPECIFIED: AiSuggestionStatus
AI_SUGGESTION_STATUS_PENDING: AiSuggestionStatus
AI_SUGGESTION_STATUS_FAILED: AiSuggestionStatus
AI_SUGGESTION_STATUS_COMPLETED: AiSuggestionStatus
DASHBOARD_TIME_PRESET_UNSPECIFIED: DashboardTimePreset
DASHBOARD_TIME_PRESET_TODAY: DashboardTimePreset
DASHBOARD_TIME_PRESET_LAST_7_DAYS: DashboardTimePreset
DASHBOARD_TIME_PRESET_LAST_30_DAYS: DashboardTimePreset
DASHBOARD_TIME_PRESET_CUSTOM: DashboardTimePreset
DASHBOARD_TIME_PRESET_1_SHIFT: DashboardTimePreset
DASHBOARD_PROCESSING_TYPE_UNSPECIFIED: DashboardProcessingType
DASHBOARD_PROCESSING_TYPE_AI_ONLY: DashboardProcessingType
DASHBOARD_PROCESSING_TYPE_HUMAN_ONLY: DashboardProcessingType
DASHBOARD_PROCESSING_TYPE_AI_PLUS_HUMAN: DashboardProcessingType
CHAT_GROUP_DELIVERY_STATUS_UNSPECIFIED: ChatGroupDeliveryStatus
CHAT_GROUP_DELIVERY_STATUS_SENT: ChatGroupDeliveryStatus
CHAT_GROUP_DELIVERY_STATUS_RECEIVED: ChatGroupDeliveryStatus
CHAT_GROUP_DELIVERY_STATUS_READ: ChatGroupDeliveryStatus
CHAT_GROUP_MEMBER_CHANGE_TYPE_UNSPECIFIED: ChatGroupMemberChangeType
CHAT_GROUP_MEMBER_CHANGE_TYPE_ADDED: ChatGroupMemberChangeType
CHAT_GROUP_MEMBER_CHANGE_TYPE_REMOVED: ChatGroupMemberChangeType
CHAT_GROUP_MEMBER_CHANGE_TYPE_LEFT: ChatGroupMemberChangeType
CHAT_GROUP_MEMBER_CHANGE_TYPE_JOINED: ChatGroupMemberChangeType
CHAT_GROUP_MEMBER_CHANGE_TYPE_ROLE_CHANGED: ChatGroupMemberChangeType
CHAT_GROUP_TOPIC_CHANGE_TYPE_UNSPECIFIED: ChatGroupTopicChangeType
CHAT_GROUP_TOPIC_CHANGE_TYPE_CREATED: ChatGroupTopicChangeType
CHAT_GROUP_TOPIC_CHANGE_TYPE_UPDATED: ChatGroupTopicChangeType
CHAT_GROUP_TOPIC_CHANGE_TYPE_DELETED: ChatGroupTopicChangeType
DIRECT_MESSAGE_DELIVERY_STATUS_UNSPECIFIED: DirectMessageDeliveryStatus
DIRECT_MESSAGE_DELIVERY_STATUS_SENT: DirectMessageDeliveryStatus
DIRECT_MESSAGE_DELIVERY_STATUS_RECEIVED: DirectMessageDeliveryStatus
DIRECT_MESSAGE_DELIVERY_STATUS_READ: DirectMessageDeliveryStatus
PUSH_PLATFORM_UNSPECIFIED: PushPlatform
PUSH_PLATFORM_ANDROID: PushPlatform
PUSH_PLATFORM_IOS: PushPlatform
PUSH_PLATFORM_WEB_CHROME: PushPlatform
PUSH_PLATFORM_WEB_FIREFOX: PushPlatform
PREVIEW_LINK_RESULT_UNSPECIFIED: PreviewLinkResult
PREVIEW_LINK_RESULT_OK: PreviewLinkResult
PREVIEW_LINK_RESULT_NO_METADATA: PreviewLinkResult
PREVIEW_LINK_RESULT_FETCH_FAILED: PreviewLinkResult

class MetaPageInfo(_message.Message):
    __slots__ = ("id", "page_id", "page_name", "picture_url", "status", "mode", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    page_id: str
    page_name: str
    picture_url: str
    status: _model_pb2.Status
    mode: _model_pb2.Mode
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., page_id: _Optional[str] = ..., page_name: _Optional[str] = ..., picture_url: _Optional[str] = ..., status: _Optional[_Union[_model_pb2.Status, str]] = ..., mode: _Optional[_Union[_model_pb2.Mode, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LinkFacebookRequest(_message.Message):
    __slots__ = ("authorization_code", "redirect_url")
    AUTHORIZATION_CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URL_FIELD_NUMBER: _ClassVar[int]
    authorization_code: str
    redirect_url: str
    def __init__(self, authorization_code: _Optional[str] = ..., redirect_url: _Optional[str] = ...) -> None: ...

class LinkFacebookReply(_message.Message):
    __slots__ = ("pages",)
    PAGES_FIELD_NUMBER: _ClassVar[int]
    pages: _containers.RepeatedCompositeFieldContainer[MetaPageInfo]
    def __init__(self, pages: _Optional[_Iterable[_Union[MetaPageInfo, _Mapping]]] = ...) -> None: ...

class MetaFacebookAccountInfo(_message.Message):
    __slots__ = ("id", "facebook_user_id", "display_name", "picture_url", "token_expires_at", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    FACEBOOK_USER_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    facebook_user_id: str
    display_name: str
    picture_url: str
    token_expires_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., facebook_user_id: _Optional[str] = ..., display_name: _Optional[str] = ..., picture_url: _Optional[str] = ..., token_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListFacebookAccountsRequest(_message.Message):
    __slots__ = ("page_size", "page")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListFacebookAccountsReply(_message.Message):
    __slots__ = ("accounts", "page_size", "page", "count")
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[MetaFacebookAccountInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, accounts: _Optional[_Iterable[_Union[MetaFacebookAccountInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ListPagesRequest(_message.Message):
    __slots__ = ("page_size", "page", "statuses", "modes")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    MODES_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    statuses: _containers.RepeatedScalarFieldContainer[_model_pb2.Status]
    modes: _containers.RepeatedScalarFieldContainer[_model_pb2.Mode]
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ..., statuses: _Optional[_Iterable[_Union[_model_pb2.Status, str]]] = ..., modes: _Optional[_Iterable[_Union[_model_pb2.Mode, str]]] = ...) -> None: ...

class ListPagesReply(_message.Message):
    __slots__ = ("pages", "page_size", "page", "count")
    PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    pages: _containers.RepeatedCompositeFieldContainer[MetaPageInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, pages: _Optional[_Iterable[_Union[MetaPageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class UpdatePageRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("status", "mode")
        STATUS_FIELD_NUMBER: _ClassVar[int]
        MODE_FIELD_NUMBER: _ClassVar[int]
        status: _model_pb2.Status
        mode: _model_pb2.Mode
        def __init__(self, status: _Optional[_Union[_model_pb2.Status, str]] = ..., mode: _Optional[_Union[_model_pb2.Mode, str]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdatePageRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdatePageRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdatePageReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateConversationRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("mode", "user_id", "state")
        MODE_FIELD_NUMBER: _ClassVar[int]
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        mode: _model_pb2.Mode
        user_id: int
        state: _model_pb2.ConversationState
        def __init__(self, mode: _Optional[_Union[_model_pb2.Mode, str]] = ..., user_id: _Optional[int] = ..., state: _Optional[_Union[_model_pb2.ConversationState, str]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdateConversationRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdateConversationRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateConversationReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LabelInfo(_message.Message):
    __slots__ = ("id", "title", "color", "description", "applied_at_unix_ms")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    APPLIED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    color: str
    description: str
    applied_at_unix_ms: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., color: _Optional[str] = ..., description: _Optional[str] = ..., applied_at_unix_ms: _Optional[int] = ...) -> None: ...

class AddConversationLabelsRequest(_message.Message):
    __slots__ = ("conversation_id", "ids", "labels")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    ids: _containers.RepeatedScalarFieldContainer[int]
    labels: _containers.RepeatedCompositeFieldContainer[LabelInfo]
    def __init__(self, conversation_id: _Optional[int] = ..., ids: _Optional[_Iterable[int]] = ..., labels: _Optional[_Iterable[_Union[LabelInfo, _Mapping]]] = ...) -> None: ...

class AddConversationLabelsReply(_message.Message):
    __slots__ = ("labels",)
    LABELS_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[LabelInfo]
    def __init__(self, labels: _Optional[_Iterable[_Union[LabelInfo, _Mapping]]] = ...) -> None: ...

class RemoveConversationLabelsRequest(_message.Message):
    __slots__ = ("conversation_id", "titles")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    TITLES_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    titles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, conversation_id: _Optional[int] = ..., titles: _Optional[_Iterable[str]] = ...) -> None: ...

class RemoveConversationLabelsReply(_message.Message):
    __slots__ = ("labels",)
    LABELS_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[LabelInfo]
    def __init__(self, labels: _Optional[_Iterable[_Union[LabelInfo, _Mapping]]] = ...) -> None: ...

class LabelCatalogInfo(_message.Message):
    __slots__ = ("id", "title", "color", "description", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    color: str
    description: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., color: _Optional[str] = ..., description: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListLabelsRequest(_message.Message):
    __slots__ = ("page_size", "page")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListLabelsReply(_message.Message):
    __slots__ = ("labels", "page_size", "page", "count")
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[LabelCatalogInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, labels: _Optional[_Iterable[_Union[LabelCatalogInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class CreateLabelRequest(_message.Message):
    __slots__ = ("title", "color", "description")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    title: str
    color: str
    description: str
    def __init__(self, title: _Optional[str] = ..., color: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateLabelReply(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: LabelCatalogInfo
    def __init__(self, label: _Optional[_Union[LabelCatalogInfo, _Mapping]] = ...) -> None: ...

class UpdateLabelRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("color", "description")
        COLOR_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        color: str
        description: str
        def __init__(self, color: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdateLabelRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdateLabelRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateLabelReply(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: LabelCatalogInfo
    def __init__(self, label: _Optional[_Union[LabelCatalogInfo, _Mapping]] = ...) -> None: ...

class DeleteLabelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteLabelReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ConversationInfo(_message.Message):
    __slots__ = ("id", "platform", "fanpage_id", "external_id", "customer_name", "fanpage_name", "last_message_at", "mode", "last_message", "labels", "unread_count", "user_id", "state", "avatar")
    ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    FANPAGE_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_NAME_FIELD_NUMBER: _ClassVar[int]
    FANPAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_AT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    id: int
    platform: _model_pb2.Platform
    fanpage_id: str
    external_id: str
    customer_name: str
    fanpage_name: str
    last_message_at: _timestamp_pb2.Timestamp
    mode: _model_pb2.Mode
    last_message: ConversationMessageInfo
    labels: _containers.RepeatedCompositeFieldContainer[LabelInfo]
    unread_count: int
    user_id: int
    state: _model_pb2.ConversationState
    avatar: str
    def __init__(self, id: _Optional[int] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ..., fanpage_id: _Optional[str] = ..., external_id: _Optional[str] = ..., customer_name: _Optional[str] = ..., fanpage_name: _Optional[str] = ..., last_message_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., mode: _Optional[_Union[_model_pb2.Mode, str]] = ..., last_message: _Optional[_Union[ConversationMessageInfo, _Mapping]] = ..., labels: _Optional[_Iterable[_Union[LabelInfo, _Mapping]]] = ..., unread_count: _Optional[int] = ..., user_id: _Optional[int] = ..., state: _Optional[_Union[_model_pb2.ConversationState, str]] = ..., avatar: _Optional[str] = ...) -> None: ...

class GetConversationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetConversationReply(_message.Message):
    __slots__ = ("conversation",)
    CONVERSATION_FIELD_NUMBER: _ClassVar[int]
    conversation: ConversationInfo
    def __init__(self, conversation: _Optional[_Union[ConversationInfo, _Mapping]] = ...) -> None: ...

class ListConversationsLabelsFilter(_message.Message):
    __slots__ = ("titles",)
    TITLES_FIELD_NUMBER: _ClassVar[int]
    titles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, titles: _Optional[_Iterable[str]] = ...) -> None: ...

class ListConversationsStatesFilter(_message.Message):
    __slots__ = ("states",)
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedScalarFieldContainer[_model_pb2.ConversationState]
    def __init__(self, states: _Optional[_Iterable[_Union[_model_pb2.ConversationState, str]]] = ...) -> None: ...

class ListConversationsCustomerNameFilter(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class ListConversationsFilter(_message.Message):
    __slots__ = ("labels", "states", "owner", "customer_name")
    LABELS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_NAME_FIELD_NUMBER: _ClassVar[int]
    labels: ListConversationsLabelsFilter
    states: ListConversationsStatesFilter
    owner: ConversationOwnerFilter
    customer_name: ListConversationsCustomerNameFilter
    def __init__(self, labels: _Optional[_Union[ListConversationsLabelsFilter, _Mapping]] = ..., states: _Optional[_Union[ListConversationsStatesFilter, _Mapping]] = ..., owner: _Optional[_Union[ConversationOwnerFilter, str]] = ..., customer_name: _Optional[_Union[ListConversationsCustomerNameFilter, _Mapping]] = ...) -> None: ...

class ListConversationsRequest(_message.Message):
    __slots__ = ("fanpage_id", "page_size", "page", "integration_client_id", "filters", "sort")
    FANPAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    fanpage_id: str
    page_size: int
    page: int
    integration_client_id: str
    filters: _containers.RepeatedCompositeFieldContainer[ListConversationsFilter]
    sort: ListConversationsSort
    def __init__(self, fanpage_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., integration_client_id: _Optional[str] = ..., filters: _Optional[_Iterable[_Union[ListConversationsFilter, _Mapping]]] = ..., sort: _Optional[_Union[ListConversationsSort, str]] = ...) -> None: ...

class ListConversationsReply(_message.Message):
    __slots__ = ("conversations", "page_size", "page", "count", "mine_count", "unassigned_count")
    CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    MINE_COUNT_FIELD_NUMBER: _ClassVar[int]
    UNASSIGNED_COUNT_FIELD_NUMBER: _ClassVar[int]
    conversations: _containers.RepeatedCompositeFieldContainer[ConversationInfo]
    page_size: int
    page: int
    count: int
    mine_count: int
    unassigned_count: int
    def __init__(self, conversations: _Optional[_Iterable[_Union[ConversationInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ..., mine_count: _Optional[int] = ..., unassigned_count: _Optional[int] = ...) -> None: ...

class ConversationMessageInfo(_message.Message):
    __slots__ = ("id", "conversation_id", "sender", "method", "content", "images", "videos", "audios", "files", "send_at", "seen", "sender_user_id", "sender_username", "edited_at", "deleted_at", "media_description", "delivery_status", "scheduled_at", "created_at", "received", "received_at", "seen_by_customer", "received_by_customer", "seen_at", "seen_by_customer_at", "received_by_customer_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    AUDIOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    SEND_AT_FIELD_NUMBER: _ClassVar[int]
    SEEN_FIELD_NUMBER: _ClassVar[int]
    SENDER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    EDITED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_FIELD_NUMBER: _ClassVar[int]
    SEEN_BY_CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_BY_CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    SEEN_AT_FIELD_NUMBER: _ClassVar[int]
    SEEN_BY_CUSTOMER_AT_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_BY_CUSTOMER_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    conversation_id: int
    sender: _model_pb2.Sender
    method: _model_pb2.Method
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    audios: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    send_at: _timestamp_pb2.Timestamp
    seen: bool
    sender_user_id: int
    sender_username: str
    edited_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    media_description: str
    delivery_status: _model_pb2.MessageStatus
    scheduled_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    received: bool
    received_at: _timestamp_pb2.Timestamp
    seen_by_customer: bool
    received_by_customer: bool
    seen_at: _timestamp_pb2.Timestamp
    seen_by_customer_at: _timestamp_pb2.Timestamp
    received_by_customer_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., sender: _Optional[_Union[_model_pb2.Sender, str]] = ..., method: _Optional[_Union[_model_pb2.Method, str]] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., audios: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., send_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., seen: _Optional[bool] = ..., sender_user_id: _Optional[int] = ..., sender_username: _Optional[str] = ..., edited_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., media_description: _Optional[str] = ..., delivery_status: _Optional[_Union[_model_pb2.MessageStatus, str]] = ..., scheduled_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., received: _Optional[bool] = ..., received_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., seen_by_customer: _Optional[bool] = ..., received_by_customer: _Optional[bool] = ..., seen_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., seen_by_customer_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., received_by_customer_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SeenRequest(_message.Message):
    __slots__ = ("conversation_id", "message_ids")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, conversation_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class SeenReply(_message.Message):
    __slots__ = ("unread_count",)
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    unread_count: int
    def __init__(self, unread_count: _Optional[int] = ...) -> None: ...

class UnseenRequest(_message.Message):
    __slots__ = ("conversation_id", "message_ids")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, conversation_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class UnseenReply(_message.Message):
    __slots__ = ("unread_count",)
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    unread_count: int
    def __init__(self, unread_count: _Optional[int] = ...) -> None: ...

class ReceivedRequest(_message.Message):
    __slots__ = ("message_ids",)
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, message_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class ReceivedReply(_message.Message):
    __slots__ = ("updated_count",)
    UPDATED_COUNT_FIELD_NUMBER: _ClassVar[int]
    updated_count: int
    def __init__(self, updated_count: _Optional[int] = ...) -> None: ...

class ListUnreceivedMessagesRequest(_message.Message):
    __slots__ = ("page_size", "before_message_id", "platform")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    before_message_id: int
    platform: _model_pb2.Platform
    def __init__(self, page_size: _Optional[int] = ..., before_message_id: _Optional[int] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ...) -> None: ...

class ListUnreceivedMessagesReply(_message.Message):
    __slots__ = ("messages", "page_size", "has_next")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[ConversationMessageInfo]
    page_size: int
    has_next: bool
    def __init__(self, messages: _Optional[_Iterable[_Union[ConversationMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., has_next: _Optional[bool] = ...) -> None: ...

class GetConversationMessagesRequest(_message.Message):
    __slots__ = ("conversation_id", "page_size", "before_id")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    page_size: int
    before_id: int
    def __init__(self, conversation_id: _Optional[int] = ..., page_size: _Optional[int] = ..., before_id: _Optional[int] = ...) -> None: ...

class GetConversationMessagesReply(_message.Message):
    __slots__ = ("messages", "page_size")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[ConversationMessageInfo]
    page_size: int
    def __init__(self, messages: _Optional[_Iterable[_Union[ConversationMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ...) -> None: ...

class SearchMessagesRequest(_message.Message):
    __slots__ = ("query", "page_size", "page", "sort")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_size: int
    page: int
    sort: SearchMessagesSort
    def __init__(self, query: _Optional[str] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., sort: _Optional[_Union[SearchMessagesSort, str]] = ...) -> None: ...

class SearchMessageHit(_message.Message):
    __slots__ = ("message", "customer_name", "fanpage_id", "platform", "state", "external_id")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_NAME_FIELD_NUMBER: _ClassVar[int]
    FANPAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    message: ConversationMessageInfo
    customer_name: str
    fanpage_id: str
    platform: _model_pb2.Platform
    state: _model_pb2.ConversationState
    external_id: str
    def __init__(self, message: _Optional[_Union[ConversationMessageInfo, _Mapping]] = ..., customer_name: _Optional[str] = ..., fanpage_id: _Optional[str] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ..., state: _Optional[_Union[_model_pb2.ConversationState, str]] = ..., external_id: _Optional[str] = ...) -> None: ...

class SearchMessagesReply(_message.Message):
    __slots__ = ("hits", "page_size", "page", "has_next")
    HITS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    hits: _containers.RepeatedCompositeFieldContainer[SearchMessageHit]
    page_size: int
    page: int
    has_next: bool
    def __init__(self, hits: _Optional[_Iterable[_Union[SearchMessageHit, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., has_next: _Optional[bool] = ...) -> None: ...

class ConversationTimelineItem(_message.Message):
    __slots__ = ("message", "update_event", "private_note")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_EVENT_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_NOTE_FIELD_NUMBER: _ClassVar[int]
    message: ConversationMessageInfo
    update_event: ConversationUpdateEventInfo
    private_note: PrivateNote
    def __init__(self, message: _Optional[_Union[ConversationMessageInfo, _Mapping]] = ..., update_event: _Optional[_Union[ConversationUpdateEventInfo, _Mapping]] = ..., private_note: _Optional[_Union[PrivateNote, _Mapping]] = ...) -> None: ...

class ConversationUpdateEventInfo(_message.Message):
    __slots__ = ("id", "conversation_id", "actor_user_id", "created_at", "state", "mode", "user_id", "label")
    class StateChange(_message.Message):
        __slots__ = ("old_state", "new_state")
        OLD_STATE_FIELD_NUMBER: _ClassVar[int]
        NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        old_state: _model_pb2.ConversationState
        new_state: _model_pb2.ConversationState
        def __init__(self, old_state: _Optional[_Union[_model_pb2.ConversationState, str]] = ..., new_state: _Optional[_Union[_model_pb2.ConversationState, str]] = ...) -> None: ...
    class ModeChange(_message.Message):
        __slots__ = ("old_mode", "new_mode")
        OLD_MODE_FIELD_NUMBER: _ClassVar[int]
        NEW_MODE_FIELD_NUMBER: _ClassVar[int]
        old_mode: _model_pb2.Mode
        new_mode: _model_pb2.Mode
        def __init__(self, old_mode: _Optional[_Union[_model_pb2.Mode, str]] = ..., new_mode: _Optional[_Union[_model_pb2.Mode, str]] = ...) -> None: ...
    class UserIdChange(_message.Message):
        __slots__ = ("old_user_id", "new_user_id")
        OLD_USER_ID_FIELD_NUMBER: _ClassVar[int]
        NEW_USER_ID_FIELD_NUMBER: _ClassVar[int]
        old_user_id: int
        new_user_id: int
        def __init__(self, old_user_id: _Optional[int] = ..., new_user_id: _Optional[int] = ...) -> None: ...
    class LabelChange(_message.Message):
        __slots__ = ("operator", "label")
        OPERATOR_FIELD_NUMBER: _ClassVar[int]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        operator: _model_pb2.LabelOp
        label: str
        def __init__(self, operator: _Optional[_Union[_model_pb2.LabelOp, str]] = ..., label: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    id: int
    conversation_id: int
    actor_user_id: int
    created_at: _timestamp_pb2.Timestamp
    state: ConversationUpdateEventInfo.StateChange
    mode: ConversationUpdateEventInfo.ModeChange
    user_id: ConversationUpdateEventInfo.UserIdChange
    label: ConversationUpdateEventInfo.LabelChange
    def __init__(self, id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., actor_user_id: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[_Union[ConversationUpdateEventInfo.StateChange, _Mapping]] = ..., mode: _Optional[_Union[ConversationUpdateEventInfo.ModeChange, _Mapping]] = ..., user_id: _Optional[_Union[ConversationUpdateEventInfo.UserIdChange, _Mapping]] = ..., label: _Optional[_Union[ConversationUpdateEventInfo.LabelChange, _Mapping]] = ...) -> None: ...

class ListMessagesRequest(_message.Message):
    __slots__ = ("conversation_id", "message_size", "before_message_id")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    message_size: int
    before_message_id: int
    def __init__(self, conversation_id: _Optional[int] = ..., message_size: _Optional[int] = ..., before_message_id: _Optional[int] = ...) -> None: ...

class ListMessagesReply(_message.Message):
    __slots__ = ("items", "message_size")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[ConversationTimelineItem]
    message_size: int
    def __init__(self, items: _Optional[_Iterable[_Union[ConversationTimelineItem, _Mapping]]] = ..., message_size: _Optional[int] = ...) -> None: ...

class PrivateNote(_message.Message):
    __slots__ = ("id", "conversation_id", "user_id", "content", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    conversation_id: int
    user_id: int
    content: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., user_id: _Optional[int] = ..., content: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListPrivateNotesRequest(_message.Message):
    __slots__ = ("conversation_id", "page_size", "before_id")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    page_size: int
    before_id: int
    def __init__(self, conversation_id: _Optional[int] = ..., page_size: _Optional[int] = ..., before_id: _Optional[int] = ...) -> None: ...

class ListPrivateNotesReply(_message.Message):
    __slots__ = ("notes", "page_size", "count")
    NOTES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    notes: _containers.RepeatedCompositeFieldContainer[PrivateNote]
    page_size: int
    count: int
    def __init__(self, notes: _Optional[_Iterable[_Union[PrivateNote, _Mapping]]] = ..., page_size: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class CreatePrivateNoteRequest(_message.Message):
    __slots__ = ("conversation_id", "content")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    content: str
    def __init__(self, conversation_id: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class CreatePrivateNoteReply(_message.Message):
    __slots__ = ("note",)
    NOTE_FIELD_NUMBER: _ClassVar[int]
    note: PrivateNote
    def __init__(self, note: _Optional[_Union[PrivateNote, _Mapping]] = ...) -> None: ...

class UpdatePrivateNoteRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("content",)
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        content: str
        def __init__(self, content: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdatePrivateNoteRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdatePrivateNoteRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdatePrivateNoteReply(_message.Message):
    __slots__ = ("note",)
    NOTE_FIELD_NUMBER: _ClassVar[int]
    note: PrivateNote
    def __init__(self, note: _Optional[_Union[PrivateNote, _Mapping]] = ...) -> None: ...

class DeletePrivateNotesRequest(_message.Message):
    __slots__ = ("conversation_id", "ids")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, conversation_id: _Optional[int] = ..., ids: _Optional[_Iterable[int]] = ...) -> None: ...

class DeletePrivateNotesReply(_message.Message):
    __slots__ = ("deleted_count",)
    DELETED_COUNT_FIELD_NUMBER: _ClassVar[int]
    deleted_count: int
    def __init__(self, deleted_count: _Optional[int] = ...) -> None: ...

class StreamMessagesRequest(_message.Message):
    __slots__ = ("resume_after_message_id", "resume_after_ai_suggestion_id", "resume_after_update_event_id")
    RESUME_AFTER_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    RESUME_AFTER_AI_SUGGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESUME_AFTER_UPDATE_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    resume_after_message_id: int
    resume_after_ai_suggestion_id: int
    resume_after_update_event_id: int
    def __init__(self, resume_after_message_id: _Optional[int] = ..., resume_after_ai_suggestion_id: _Optional[int] = ..., resume_after_update_event_id: _Optional[int] = ...) -> None: ...

class SendMessageRequest(_message.Message):
    __slots__ = ("conversation_id", "content", "images", "videos", "idempotency_key", "external_id", "integration_client_id", "external_name", "scheduled_at_unix_ms")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    idempotency_key: str
    external_id: str
    integration_client_id: str
    external_name: str
    scheduled_at_unix_ms: int
    def __init__(self, conversation_id: _Optional[int] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., idempotency_key: _Optional[str] = ..., external_id: _Optional[str] = ..., integration_client_id: _Optional[str] = ..., external_name: _Optional[str] = ..., scheduled_at_unix_ms: _Optional[int] = ...) -> None: ...

class SendMessageReply(_message.Message):
    __slots__ = ("message_id", "send_at_unix_ms", "duplicate", "conversation_id", "assigned", "scheduled")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    SEND_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    DUPLICATE_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    send_at_unix_ms: int
    duplicate: bool
    conversation_id: int
    assigned: bool
    scheduled: bool
    def __init__(self, message_id: _Optional[int] = ..., send_at_unix_ms: _Optional[int] = ..., duplicate: _Optional[bool] = ..., conversation_id: _Optional[int] = ..., assigned: _Optional[bool] = ..., scheduled: _Optional[bool] = ...) -> None: ...

class UpdateMessageRequest(_message.Message):
    __slots__ = ("message_id", "content", "images", "videos", "scheduled_at_unix_ms")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    scheduled_at_unix_ms: int
    def __init__(self, message_id: _Optional[int] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., scheduled_at_unix_ms: _Optional[int] = ...) -> None: ...

class UpdateMessageReply(_message.Message):
    __slots__ = ("message_id", "edited_at_unix_ms")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    EDITED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    edited_at_unix_ms: int
    def __init__(self, message_id: _Optional[int] = ..., edited_at_unix_ms: _Optional[int] = ...) -> None: ...

class DeleteMessageRequest(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    def __init__(self, message_id: _Optional[int] = ...) -> None: ...

class DeleteMessageReply(_message.Message):
    __slots__ = ("message_id", "deleted_at_unix_ms")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    deleted_at_unix_ms: int
    def __init__(self, message_id: _Optional[int] = ..., deleted_at_unix_ms: _Optional[int] = ...) -> None: ...

class AiReplySuggestionInfo(_message.Message):
    __slots__ = ("id", "tenant_id", "conversation_id", "trigger_message_id", "trigger_message_content", "suggested_reply", "images", "videos", "model_used", "created_at", "context_summary", "context_recent", "context_kb", "payload_json", "platform")
    ID_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_MESSAGE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    SUGGESTED_REPLY_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    MODEL_USED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_RECENT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_KB_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_JSON_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    id: int
    tenant_id: str
    conversation_id: int
    trigger_message_id: int
    trigger_message_content: str
    suggested_reply: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    model_used: str
    created_at: _timestamp_pb2.Timestamp
    context_summary: str
    context_recent: str
    context_kb: str
    payload_json: str
    platform: _model_pb2.Platform
    def __init__(self, id: _Optional[int] = ..., tenant_id: _Optional[str] = ..., conversation_id: _Optional[int] = ..., trigger_message_id: _Optional[int] = ..., trigger_message_content: _Optional[str] = ..., suggested_reply: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., model_used: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., context_summary: _Optional[str] = ..., context_recent: _Optional[str] = ..., context_kb: _Optional[str] = ..., payload_json: _Optional[str] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ...) -> None: ...

class HelpdeskAiSuggestionEvent(_message.Message):
    __slots__ = ("suggestion", "status")
    SUGGESTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    suggestion: AiReplySuggestionInfo
    status: AiSuggestionStatus
    def __init__(self, suggestion: _Optional[_Union[AiReplySuggestionInfo, _Mapping]] = ..., status: _Optional[_Union[AiSuggestionStatus, str]] = ...) -> None: ...

class ListAiReplySuggestionsRequest(_message.Message):
    __slots__ = ("conversation_id", "page_size", "before_id")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    page_size: int
    before_id: int
    def __init__(self, conversation_id: _Optional[int] = ..., page_size: _Optional[int] = ..., before_id: _Optional[int] = ...) -> None: ...

class ListAiReplySuggestionsReply(_message.Message):
    __slots__ = ("suggestions", "page_size", "count")
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    suggestions: _containers.RepeatedCompositeFieldContainer[AiReplySuggestionInfo]
    page_size: int
    count: int
    def __init__(self, suggestions: _Optional[_Iterable[_Union[AiReplySuggestionInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class HelpdeskStreamPing(_message.Message):
    __slots__ = ("server_time_unix_ms",)
    SERVER_TIME_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    server_time_unix_ms: int
    def __init__(self, server_time_unix_ms: _Optional[int] = ...) -> None: ...

class HelpdeskCustomerSeenEvent(_message.Message):
    __slots__ = ("conversation_id", "message_ids", "seen", "seen_at_unix_ms")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    SEEN_FIELD_NUMBER: _ClassVar[int]
    SEEN_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    seen: bool
    seen_at_unix_ms: int
    def __init__(self, conversation_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ..., seen: _Optional[bool] = ..., seen_at_unix_ms: _Optional[int] = ...) -> None: ...

class HelpdeskStaffSeenEvent(_message.Message):
    __slots__ = ("conversation_id", "message_ids", "staff_user_id", "seen", "seen_at_unix_ms", "unread_count")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    STAFF_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SEEN_FIELD_NUMBER: _ClassVar[int]
    SEEN_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    staff_user_id: int
    seen: bool
    seen_at_unix_ms: int
    unread_count: int
    def __init__(self, conversation_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ..., staff_user_id: _Optional[int] = ..., seen: _Optional[bool] = ..., seen_at_unix_ms: _Optional[int] = ..., unread_count: _Optional[int] = ...) -> None: ...

class HelpdeskCustomerReceivedEvent(_message.Message):
    __slots__ = ("conversation_id", "message_ids", "received", "received_at_unix_ms")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    received: bool
    received_at_unix_ms: int
    def __init__(self, conversation_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ..., received: _Optional[bool] = ..., received_at_unix_ms: _Optional[int] = ...) -> None: ...

class HelpdeskStaffReceivedEvent(_message.Message):
    __slots__ = ("conversation_id", "message_ids", "staff_user_id", "received_at_unix_ms")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    STAFF_USER_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    staff_user_id: int
    received_at_unix_ms: int
    def __init__(self, conversation_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ..., staff_user_id: _Optional[int] = ..., received_at_unix_ms: _Optional[int] = ...) -> None: ...

class HelpdeskStreamEvent(_message.Message):
    __slots__ = ("ping", "ai_suggestion", "chat_message", "update_event", "customer_seen", "staff_seen", "customer_received", "staff_received")
    PING_FIELD_NUMBER: _ClassVar[int]
    AI_SUGGESTION_FIELD_NUMBER: _ClassVar[int]
    CHAT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_EVENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_SEEN_FIELD_NUMBER: _ClassVar[int]
    STAFF_SEEN_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    STAFF_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    ping: HelpdeskStreamPing
    ai_suggestion: HelpdeskAiSuggestionEvent
    chat_message: ConversationMessageInfo
    update_event: ConversationUpdateEventInfo
    customer_seen: HelpdeskCustomerSeenEvent
    staff_seen: HelpdeskStaffSeenEvent
    customer_received: HelpdeskCustomerReceivedEvent
    staff_received: HelpdeskStaffReceivedEvent
    def __init__(self, ping: _Optional[_Union[HelpdeskStreamPing, _Mapping]] = ..., ai_suggestion: _Optional[_Union[HelpdeskAiSuggestionEvent, _Mapping]] = ..., chat_message: _Optional[_Union[ConversationMessageInfo, _Mapping]] = ..., update_event: _Optional[_Union[ConversationUpdateEventInfo, _Mapping]] = ..., customer_seen: _Optional[_Union[HelpdeskCustomerSeenEvent, _Mapping]] = ..., staff_seen: _Optional[_Union[HelpdeskStaffSeenEvent, _Mapping]] = ..., customer_received: _Optional[_Union[HelpdeskCustomerReceivedEvent, _Mapping]] = ..., staff_received: _Optional[_Union[HelpdeskStaffReceivedEvent, _Mapping]] = ...) -> None: ...

class ScheduledDeliveryInfo(_message.Message):
    __slots__ = ("id", "recipient_id", "snapshot_name", "snapshot_platform_id", "delivery_status", "error_message", "sent_at", "snapshot_picture_url", "failure_reason", "platform_error_code")
    ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_NAME_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SENT_AT_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    id: int
    recipient_id: int
    snapshot_name: str
    snapshot_platform_id: str
    delivery_status: _model_pb2.ScheduledDeliveryStatus
    error_message: str
    sent_at: _timestamp_pb2.Timestamp
    snapshot_picture_url: str
    failure_reason: _model_pb2.DeliveryFailureReason
    platform_error_code: int
    def __init__(self, id: _Optional[int] = ..., recipient_id: _Optional[int] = ..., snapshot_name: _Optional[str] = ..., snapshot_platform_id: _Optional[str] = ..., delivery_status: _Optional[_Union[_model_pb2.ScheduledDeliveryStatus, str]] = ..., error_message: _Optional[str] = ..., sent_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., snapshot_picture_url: _Optional[str] = ..., failure_reason: _Optional[_Union[_model_pb2.DeliveryFailureReason, str]] = ..., platform_error_code: _Optional[int] = ...) -> None: ...

class ScheduledMessageInfo(_message.Message):
    __slots__ = ("id", "content", "scheduled_at", "status", "repeat", "error_message", "sent_at", "created_at", "updated_at", "deliveries", "images", "videos", "platform")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REPEAT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SENT_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELIVERIES_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    id: int
    content: str
    scheduled_at: _timestamp_pb2.Timestamp
    status: _model_pb2.ScheduledMessageStatus
    repeat: _model_pb2.RepeatType
    error_message: str
    sent_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deliveries: _containers.RepeatedCompositeFieldContainer[ScheduledDeliveryInfo]
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    platform: _model_pb2.Platform
    def __init__(self, id: _Optional[int] = ..., content: _Optional[str] = ..., scheduled_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_model_pb2.ScheduledMessageStatus, str]] = ..., repeat: _Optional[_Union[_model_pb2.RepeatType, str]] = ..., error_message: _Optional[str] = ..., sent_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deliveries: _Optional[_Iterable[_Union[ScheduledDeliveryInfo, _Mapping]]] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ...) -> None: ...

class CreateScheduledMessageRequest(_message.Message):
    __slots__ = ("content", "scheduled_at", "repeat", "recipient_ids", "images", "videos")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_AT_FIELD_NUMBER: _ClassVar[int]
    REPEAT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_IDS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    content: str
    scheduled_at: _timestamp_pb2.Timestamp
    repeat: _model_pb2.RepeatType
    recipient_ids: _containers.RepeatedScalarFieldContainer[int]
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, content: _Optional[str] = ..., scheduled_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., repeat: _Optional[_Union[_model_pb2.RepeatType, str]] = ..., recipient_ids: _Optional[_Iterable[int]] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateScheduledMessageReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: ScheduledMessageInfo
    def __init__(self, message: _Optional[_Union[ScheduledMessageInfo, _Mapping]] = ...) -> None: ...

class ListScheduledMessagesRequest(_message.Message):
    __slots__ = ("page_size", "page", "status_filter", "search_query")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FILTER_FIELD_NUMBER: _ClassVar[int]
    SEARCH_QUERY_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    status_filter: _model_pb2.ScheduledMessageStatus
    search_query: str
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ..., status_filter: _Optional[_Union[_model_pb2.ScheduledMessageStatus, str]] = ..., search_query: _Optional[str] = ...) -> None: ...

class ListScheduledMessagesReply(_message.Message):
    __slots__ = ("messages", "page_size", "page", "count")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[ScheduledMessageInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, messages: _Optional[_Iterable[_Union[ScheduledMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class GetScheduledMessageRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetScheduledMessageReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: ScheduledMessageInfo
    def __init__(self, message: _Optional[_Union[ScheduledMessageInfo, _Mapping]] = ...) -> None: ...

class UpdateScheduledMessageRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("content", "scheduled_at", "repeat", "status")
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        SCHEDULED_AT_FIELD_NUMBER: _ClassVar[int]
        REPEAT_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        content: str
        scheduled_at: _timestamp_pb2.Timestamp
        repeat: _model_pb2.RepeatType
        status: _model_pb2.ScheduledMessageStatus
        def __init__(self, content: _Optional[str] = ..., scheduled_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., repeat: _Optional[_Union[_model_pb2.RepeatType, str]] = ..., status: _Optional[_Union[_model_pb2.ScheduledMessageStatus, str]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdateScheduledMessageRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdateScheduledMessageRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateScheduledMessageReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteScheduledMessageRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteScheduledMessageReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RecipientInfo(_message.Message):
    __slots__ = ("id", "name", "platform_id", "created_at", "updated_at", "picture_url", "platform", "integration_client_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    platform_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    picture_url: str
    platform: _model_pb2.Platform
    integration_client_id: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., platform_id: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., picture_url: _Optional[str] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ..., integration_client_id: _Optional[str] = ...) -> None: ...

class ListRecipientsRequest(_message.Message):
    __slots__ = ("page_size", "page")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListRecipientsReply(_message.Message):
    __slots__ = ("recipients", "page_size", "page", "count")
    RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    recipients: _containers.RepeatedCompositeFieldContainer[RecipientInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, recipients: _Optional[_Iterable[_Union[RecipientInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class CreateRecipientRequest(_message.Message):
    __slots__ = ("name", "platform_id", "picture_url", "facebook_page_id", "items", "platform", "integration_client_id")
    class Item(_message.Message):
        __slots__ = ("name", "platform_id", "picture_url", "facebook_page_id", "platform", "integration_client_id")
        NAME_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
        PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
        FACEBOOK_PAGE_ID_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_FIELD_NUMBER: _ClassVar[int]
        INTEGRATION_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
        name: str
        platform_id: str
        picture_url: str
        facebook_page_id: str
        platform: _model_pb2.Platform
        integration_client_id: str
        def __init__(self, name: _Optional[str] = ..., platform_id: _Optional[str] = ..., picture_url: _Optional[str] = ..., facebook_page_id: _Optional[str] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ..., integration_client_id: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    FACEBOOK_PAGE_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    platform_id: str
    picture_url: str
    facebook_page_id: str
    items: _containers.RepeatedCompositeFieldContainer[CreateRecipientRequest.Item]
    platform: _model_pb2.Platform
    integration_client_id: str
    def __init__(self, name: _Optional[str] = ..., platform_id: _Optional[str] = ..., picture_url: _Optional[str] = ..., facebook_page_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[CreateRecipientRequest.Item, _Mapping]]] = ..., platform: _Optional[_Union[_model_pb2.Platform, str]] = ..., integration_client_id: _Optional[str] = ...) -> None: ...

class CreateRecipientReply(_message.Message):
    __slots__ = ("recipient", "recipients")
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    recipient: RecipientInfo
    recipients: _containers.RepeatedCompositeFieldContainer[RecipientInfo]
    def __init__(self, recipient: _Optional[_Union[RecipientInfo, _Mapping]] = ..., recipients: _Optional[_Iterable[_Union[RecipientInfo, _Mapping]]] = ...) -> None: ...

class UpdateRecipientRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("name", "platform_id", "picture_url")
        NAME_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
        PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
        name: str
        platform_id: str
        picture_url: str
        def __init__(self, name: _Optional[str] = ..., platform_id: _Optional[str] = ..., picture_url: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdateRecipientRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdateRecipientRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateRecipientReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteRecipientRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteRecipientReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IntegrationInfo(_message.Message):
    __slots__ = ("id", "name", "client_id", "secret_prefix", "webhook_endpoint", "status", "created_at", "updated_at", "get_user_profile_endpoint", "user_id", "back_office_url")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_PREFIX_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    GET_USER_PROFILE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    BACK_OFFICE_URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    client_id: str
    secret_prefix: str
    webhook_endpoint: str
    status: _model_pb2.Status
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    get_user_profile_endpoint: str
    user_id: int
    back_office_url: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., client_id: _Optional[str] = ..., secret_prefix: _Optional[str] = ..., webhook_endpoint: _Optional[str] = ..., status: _Optional[_Union[_model_pb2.Status, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., get_user_profile_endpoint: _Optional[str] = ..., user_id: _Optional[int] = ..., back_office_url: _Optional[str] = ...) -> None: ...

class CreateIntegrationRequest(_message.Message):
    __slots__ = ("name", "webhook_endpoint", "get_user_profile_endpoint", "back_office_url")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    GET_USER_PROFILE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    BACK_OFFICE_URL_FIELD_NUMBER: _ClassVar[int]
    name: str
    webhook_endpoint: str
    get_user_profile_endpoint: str
    back_office_url: str
    def __init__(self, name: _Optional[str] = ..., webhook_endpoint: _Optional[str] = ..., get_user_profile_endpoint: _Optional[str] = ..., back_office_url: _Optional[str] = ...) -> None: ...

class CreateIntegrationReply(_message.Message):
    __slots__ = ("integration", "secret_key")
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    integration: IntegrationInfo
    secret_key: str
    def __init__(self, integration: _Optional[_Union[IntegrationInfo, _Mapping]] = ..., secret_key: _Optional[str] = ...) -> None: ...

class ListIntegrationsRequest(_message.Message):
    __slots__ = ("page_size", "page", "statuses")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    statuses: _containers.RepeatedScalarFieldContainer[_model_pb2.Status]
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ..., statuses: _Optional[_Iterable[_Union[_model_pb2.Status, str]]] = ...) -> None: ...

class ListIntegrationsReply(_message.Message):
    __slots__ = ("integrations", "page_size", "page", "count")
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[IntegrationInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, integrations: _Optional[_Iterable[_Union[IntegrationInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class UpdateIntegrationRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("name", "webhook_endpoint", "status", "get_user_profile_endpoint", "back_office_url")
        NAME_FIELD_NUMBER: _ClassVar[int]
        WEBHOOK_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        GET_USER_PROFILE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
        BACK_OFFICE_URL_FIELD_NUMBER: _ClassVar[int]
        name: str
        webhook_endpoint: str
        status: _model_pb2.Status
        get_user_profile_endpoint: str
        back_office_url: str
        def __init__(self, name: _Optional[str] = ..., webhook_endpoint: _Optional[str] = ..., status: _Optional[_Union[_model_pb2.Status, str]] = ..., get_user_profile_endpoint: _Optional[str] = ..., back_office_url: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdateIntegrationRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdateIntegrationRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateIntegrationReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RotateIntegrationSecretRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RotateIntegrationSecretReply(_message.Message):
    __slots__ = ("integration", "secret_key")
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    integration: IntegrationInfo
    secret_key: str
    def __init__(self, integration: _Optional[_Union[IntegrationInfo, _Mapping]] = ..., secret_key: _Optional[str] = ...) -> None: ...

class DeleteIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteIntegrationReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDashboardRequest(_message.Message):
    __slots__ = ("fanpage_id",)
    FANPAGE_ID_FIELD_NUMBER: _ClassVar[int]
    fanpage_id: str
    def __init__(self, fanpage_id: _Optional[str] = ...) -> None: ...

class PartnerCustomerProfile(_message.Message):
    __slots__ = ("external_id", "name", "display_name", "phone_number", "email", "facebook_psid", "messenger_handle", "telegram_user_id", "telegram_username", "attributes", "avatar", "country", "client_id", "client_name")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FACEBOOK_PSID_FIELD_NUMBER: _ClassVar[int]
    MESSENGER_HANDLE_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_USER_ID_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_USERNAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    name: str
    display_name: str
    phone_number: str
    email: str
    facebook_psid: str
    messenger_handle: str
    telegram_user_id: str
    telegram_username: str
    attributes: _containers.ScalarMap[str, str]
    avatar: str
    country: str
    client_id: str
    client_name: str
    def __init__(self, external_id: _Optional[str] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ..., phone_number: _Optional[str] = ..., email: _Optional[str] = ..., facebook_psid: _Optional[str] = ..., messenger_handle: _Optional[str] = ..., telegram_user_id: _Optional[str] = ..., telegram_username: _Optional[str] = ..., attributes: _Optional[_Mapping[str, str]] = ..., avatar: _Optional[str] = ..., country: _Optional[str] = ..., client_id: _Optional[str] = ..., client_name: _Optional[str] = ...) -> None: ...

class GetCustomerProfileRequest(_message.Message):
    __slots__ = ("external_id",)
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    def __init__(self, external_id: _Optional[str] = ...) -> None: ...

class GetCustomerProfileReply(_message.Message):
    __slots__ = ("profile", "back_office_url")
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    BACK_OFFICE_URL_FIELD_NUMBER: _ClassVar[int]
    profile: PartnerCustomerProfile
    back_office_url: str
    def __init__(self, profile: _Optional[_Union[PartnerCustomerProfile, _Mapping]] = ..., back_office_url: _Optional[str] = ...) -> None: ...

class GetDashboardReply(_message.Message):
    __slots__ = ("total_messages", "total_messages_pct", "active_customers", "active_customers_pct", "registration_rate", "registration_rate_pct", "deposit_rate", "deposit_rate_pct", "avg_response_seconds", "avg_response_change")
    TOTAL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MESSAGES_PCT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CUSTOMERS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CUSTOMERS_PCT_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_RATE_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_RATE_PCT_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_RATE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_RATE_PCT_FIELD_NUMBER: _ClassVar[int]
    AVG_RESPONSE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    AVG_RESPONSE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    total_messages: int
    total_messages_pct: float
    active_customers: int
    active_customers_pct: float
    registration_rate: float
    registration_rate_pct: float
    deposit_rate: float
    deposit_rate_pct: float
    avg_response_seconds: float
    avg_response_change: float
    def __init__(self, total_messages: _Optional[int] = ..., total_messages_pct: _Optional[float] = ..., active_customers: _Optional[int] = ..., active_customers_pct: _Optional[float] = ..., registration_rate: _Optional[float] = ..., registration_rate_pct: _Optional[float] = ..., deposit_rate: _Optional[float] = ..., deposit_rate_pct: _Optional[float] = ..., avg_response_seconds: _Optional[float] = ..., avg_response_change: _Optional[float] = ...) -> None: ...

class DashboardTimeRange(_message.Message):
    __slots__ = ("preset", "from_time", "to_time")
    PRESET_FIELD_NUMBER: _ClassVar[int]
    FROM_TIME_FIELD_NUMBER: _ClassVar[int]
    TO_TIME_FIELD_NUMBER: _ClassVar[int]
    preset: DashboardTimePreset
    from_time: _timestamp_pb2.Timestamp
    to_time: _timestamp_pb2.Timestamp
    def __init__(self, preset: _Optional[_Union[DashboardTimePreset, str]] = ..., from_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., to_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DashboardFilter(_message.Message):
    __slots__ = ("time_range", "platforms", "cs_user_ids", "processing_type")
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    PLATFORMS_FIELD_NUMBER: _ClassVar[int]
    CS_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_TYPE_FIELD_NUMBER: _ClassVar[int]
    time_range: DashboardTimeRange
    platforms: _containers.RepeatedScalarFieldContainer[_model_pb2.Platform]
    cs_user_ids: _containers.RepeatedScalarFieldContainer[int]
    processing_type: DashboardProcessingType
    def __init__(self, time_range: _Optional[_Union[DashboardTimeRange, _Mapping]] = ..., platforms: _Optional[_Iterable[_Union[_model_pb2.Platform, str]]] = ..., cs_user_ids: _Optional[_Iterable[int]] = ..., processing_type: _Optional[_Union[DashboardProcessingType, str]] = ...) -> None: ...

class GetDashboardConversationQualityReply(_message.Message):
    __slots__ = ("total_conversations", "total_conversations_change_pct", "satisfied_customers", "satisfied_change_pct", "neutral_customers", "neutral_change_pct", "dissatisfied_customers", "dissatisfied_change_pct", "resolution_rate", "resolution_rate_change_pct", "transfer_rate", "transfer_rate_change_pct")
    TOTAL_CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONVERSATIONS_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    SATISFIED_CUSTOMERS_FIELD_NUMBER: _ClassVar[int]
    SATISFIED_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    NEUTRAL_CUSTOMERS_FIELD_NUMBER: _ClassVar[int]
    NEUTRAL_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    DISSATISFIED_CUSTOMERS_FIELD_NUMBER: _ClassVar[int]
    DISSATISFIED_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_RATE_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_RATE_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_RATE_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_RATE_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    total_conversations: int
    total_conversations_change_pct: float
    satisfied_customers: int
    satisfied_change_pct: float
    neutral_customers: int
    neutral_change_pct: float
    dissatisfied_customers: int
    dissatisfied_change_pct: float
    resolution_rate: float
    resolution_rate_change_pct: float
    transfer_rate: float
    transfer_rate_change_pct: float
    def __init__(self, total_conversations: _Optional[int] = ..., total_conversations_change_pct: _Optional[float] = ..., satisfied_customers: _Optional[int] = ..., satisfied_change_pct: _Optional[float] = ..., neutral_customers: _Optional[int] = ..., neutral_change_pct: _Optional[float] = ..., dissatisfied_customers: _Optional[int] = ..., dissatisfied_change_pct: _Optional[float] = ..., resolution_rate: _Optional[float] = ..., resolution_rate_change_pct: _Optional[float] = ..., transfer_rate: _Optional[float] = ..., transfer_rate_change_pct: _Optional[float] = ...) -> None: ...

class GetDashboardSentimentReply(_message.Message):
    __slots__ = ("satisfied", "neutral", "dissatisfied")
    SATISFIED_FIELD_NUMBER: _ClassVar[int]
    NEUTRAL_FIELD_NUMBER: _ClassVar[int]
    DISSATISFIED_FIELD_NUMBER: _ClassVar[int]
    satisfied: int
    neutral: int
    dissatisfied: int
    def __init__(self, satisfied: _Optional[int] = ..., neutral: _Optional[int] = ..., dissatisfied: _Optional[int] = ...) -> None: ...

class DashboardComplaintItem(_message.Message):
    __slots__ = ("rank", "title", "count", "change_pct", "intensity")
    RANK_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    INTENSITY_FIELD_NUMBER: _ClassVar[int]
    rank: int
    title: str
    count: int
    change_pct: float
    intensity: float
    def __init__(self, rank: _Optional[int] = ..., title: _Optional[str] = ..., count: _Optional[int] = ..., change_pct: _Optional[float] = ..., intensity: _Optional[float] = ...) -> None: ...

class GetDashboardComplaintsReply(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[DashboardComplaintItem]
    def __init__(self, items: _Optional[_Iterable[_Union[DashboardComplaintItem, _Mapping]]] = ...) -> None: ...

class GetDashboardTimingMetricsReply(_message.Message):
    __slots__ = ("avg_first_response_seconds", "avg_handle_seconds", "avg_resolve_seconds", "fastest_resolve_seconds", "slowest_resolve_seconds")
    AVG_FIRST_RESPONSE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    AVG_HANDLE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    AVG_RESOLVE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    FASTEST_RESOLVE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SLOWEST_RESOLVE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    avg_first_response_seconds: float
    avg_handle_seconds: float
    avg_resolve_seconds: float
    fastest_resolve_seconds: float
    slowest_resolve_seconds: float
    def __init__(self, avg_first_response_seconds: _Optional[float] = ..., avg_handle_seconds: _Optional[float] = ..., avg_resolve_seconds: _Optional[float] = ..., fastest_resolve_seconds: _Optional[float] = ..., slowest_resolve_seconds: _Optional[float] = ...) -> None: ...

class DashboardTimingTrendPoint(_message.Message):
    __slots__ = ("bucket_start_unix_ms", "avg_first_response_seconds", "avg_handle_seconds", "avg_resolve_seconds")
    BUCKET_START_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    AVG_FIRST_RESPONSE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    AVG_HANDLE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    AVG_RESOLVE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    bucket_start_unix_ms: int
    avg_first_response_seconds: float
    avg_handle_seconds: float
    avg_resolve_seconds: float
    def __init__(self, bucket_start_unix_ms: _Optional[int] = ..., avg_first_response_seconds: _Optional[float] = ..., avg_handle_seconds: _Optional[float] = ..., avg_resolve_seconds: _Optional[float] = ...) -> None: ...

class GetDashboardTimingTrendReply(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[DashboardTimingTrendPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[DashboardTimingTrendPoint, _Mapping]]] = ...) -> None: ...

class DashboardStaffRankInfo(_message.Message):
    __slots__ = ("rank", "user_id", "display_name", "avatar_url", "initials", "top_performer", "conversations_handled", "avg_response_seconds", "satisfaction_score", "resolution_rate", "positive_feedback_rate")
    RANK_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    INITIALS_FIELD_NUMBER: _ClassVar[int]
    TOP_PERFORMER_FIELD_NUMBER: _ClassVar[int]
    CONVERSATIONS_HANDLED_FIELD_NUMBER: _ClassVar[int]
    AVG_RESPONSE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SATISFACTION_SCORE_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_RATE_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_FEEDBACK_RATE_FIELD_NUMBER: _ClassVar[int]
    rank: int
    user_id: int
    display_name: str
    avatar_url: str
    initials: str
    top_performer: bool
    conversations_handled: int
    avg_response_seconds: float
    satisfaction_score: float
    resolution_rate: float
    positive_feedback_rate: float
    def __init__(self, rank: _Optional[int] = ..., user_id: _Optional[int] = ..., display_name: _Optional[str] = ..., avatar_url: _Optional[str] = ..., initials: _Optional[str] = ..., top_performer: _Optional[bool] = ..., conversations_handled: _Optional[int] = ..., avg_response_seconds: _Optional[float] = ..., satisfaction_score: _Optional[float] = ..., resolution_rate: _Optional[float] = ..., positive_feedback_rate: _Optional[float] = ...) -> None: ...

class GetDashboardStaffRankingReply(_message.Message):
    __slots__ = ("staff",)
    STAFF_FIELD_NUMBER: _ClassVar[int]
    staff: _containers.RepeatedCompositeFieldContainer[DashboardStaffRankInfo]
    def __init__(self, staff: _Optional[_Iterable[_Union[DashboardStaffRankInfo, _Mapping]]] = ...) -> None: ...

class GetDashboardAiHumanAnalyticsReply(_message.Message):
    __slots__ = ("ai_only_handled", "human_handled", "ai_plus_human", "transferred_to_telegram", "staff_takeover_count", "ai_success_rate", "staff_intervention_rate")
    AI_ONLY_HANDLED_FIELD_NUMBER: _ClassVar[int]
    HUMAN_HANDLED_FIELD_NUMBER: _ClassVar[int]
    AI_PLUS_HUMAN_FIELD_NUMBER: _ClassVar[int]
    TRANSFERRED_TO_TELEGRAM_FIELD_NUMBER: _ClassVar[int]
    STAFF_TAKEOVER_COUNT_FIELD_NUMBER: _ClassVar[int]
    AI_SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
    STAFF_INTERVENTION_RATE_FIELD_NUMBER: _ClassVar[int]
    ai_only_handled: int
    human_handled: int
    ai_plus_human: int
    transferred_to_telegram: int
    staff_takeover_count: int
    ai_success_rate: float
    staff_intervention_rate: float
    def __init__(self, ai_only_handled: _Optional[int] = ..., human_handled: _Optional[int] = ..., ai_plus_human: _Optional[int] = ..., transferred_to_telegram: _Optional[int] = ..., staff_takeover_count: _Optional[int] = ..., ai_success_rate: _Optional[float] = ..., staff_intervention_rate: _Optional[float] = ...) -> None: ...

class DashboardHourlyBucket(_message.Message):
    __slots__ = ("hour", "message_count")
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    hour: int
    message_count: int
    def __init__(self, hour: _Optional[int] = ..., message_count: _Optional[int] = ...) -> None: ...

class GetDashboardPeakHoursReply(_message.Message):
    __slots__ = ("buckets",)
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    buckets: _containers.RepeatedCompositeFieldContainer[DashboardHourlyBucket]
    def __init__(self, buckets: _Optional[_Iterable[_Union[DashboardHourlyBucket, _Mapping]]] = ...) -> None: ...

class GetDashboardAiPerformanceReply(_message.Message):
    __slots__ = ("quality_score", "quality_change_pct", "avg_confidence", "avg_confidence_change_pct", "fallback_rate", "fallback_rate_change_pct", "failure_rate", "failure_rate_change_pct", "retraining_suggestions")
    QUALITY_SCORE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    AVG_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    AVG_CONFIDENCE_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_RATE_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_RATE_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    FAILURE_RATE_FIELD_NUMBER: _ClassVar[int]
    FAILURE_RATE_CHANGE_PCT_FIELD_NUMBER: _ClassVar[int]
    RETRAINING_SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    quality_score: float
    quality_change_pct: float
    avg_confidence: float
    avg_confidence_change_pct: float
    fallback_rate: float
    fallback_rate_change_pct: float
    failure_rate: float
    failure_rate_change_pct: float
    retraining_suggestions: int
    def __init__(self, quality_score: _Optional[float] = ..., quality_change_pct: _Optional[float] = ..., avg_confidence: _Optional[float] = ..., avg_confidence_change_pct: _Optional[float] = ..., fallback_rate: _Optional[float] = ..., fallback_rate_change_pct: _Optional[float] = ..., failure_rate: _Optional[float] = ..., failure_rate_change_pct: _Optional[float] = ..., retraining_suggestions: _Optional[int] = ...) -> None: ...

class ListDashboardCsStaffRequest(_message.Message):
    __slots__ = ("page_size", "page", "search_query")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_QUERY_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    search_query: str
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ..., search_query: _Optional[str] = ...) -> None: ...

class DashboardCsStaffInfo(_message.Message):
    __slots__ = ("user_id", "display_name", "avatar_url")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    display_name: str
    avatar_url: str
    def __init__(self, user_id: _Optional[int] = ..., display_name: _Optional[str] = ..., avatar_url: _Optional[str] = ...) -> None: ...

class ListDashboardCsStaffReply(_message.Message):
    __slots__ = ("staff", "page_size", "page", "count")
    STAFF_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    staff: _containers.RepeatedCompositeFieldContainer[DashboardCsStaffInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, staff: _Optional[_Iterable[_Union[DashboardCsStaffInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class QAEvaluationFilter(_message.Message):
    __slots__ = ("time_range", "cs_user_ids", "status_filter", "search_query")
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    CS_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FILTER_FIELD_NUMBER: _ClassVar[int]
    SEARCH_QUERY_FIELD_NUMBER: _ClassVar[int]
    time_range: DashboardTimeRange
    cs_user_ids: _containers.RepeatedScalarFieldContainer[int]
    status_filter: _model_pb2.QAEvaluationStatus
    search_query: str
    def __init__(self, time_range: _Optional[_Union[DashboardTimeRange, _Mapping]] = ..., cs_user_ids: _Optional[_Iterable[int]] = ..., status_filter: _Optional[_Union[_model_pb2.QAEvaluationStatus, str]] = ..., search_query: _Optional[str] = ...) -> None: ...

class GetQAEvaluationRubricRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QAEvaluationCriterionDef(_message.Message):
    __slots__ = ("criterion", "title", "description", "max_score", "allowed_scores")
    CRITERION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MAX_SCORE_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_SCORES_FIELD_NUMBER: _ClassVar[int]
    criterion: _model_pb2.QAEvaluationCriterion
    title: str
    description: str
    max_score: int
    allowed_scores: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, criterion: _Optional[_Union[_model_pb2.QAEvaluationCriterion, str]] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., max_score: _Optional[int] = ..., allowed_scores: _Optional[_Iterable[int]] = ...) -> None: ...

class QAEvaluationCriticalErrorDef(_message.Message):
    __slots__ = ("error", "title", "description", "deduction")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEDUCTION_FIELD_NUMBER: _ClassVar[int]
    error: _model_pb2.QAEvaluationCriticalError
    title: str
    description: str
    deduction: int
    def __init__(self, error: _Optional[_Union[_model_pb2.QAEvaluationCriticalError, str]] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., deduction: _Optional[int] = ...) -> None: ...

class QAEvaluationRatingTierDef(_message.Message):
    __slots__ = ("tier", "label", "min_score", "max_score")
    TIER_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    MIN_SCORE_FIELD_NUMBER: _ClassVar[int]
    MAX_SCORE_FIELD_NUMBER: _ClassVar[int]
    tier: _model_pb2.QAEvaluationRatingTier
    label: str
    min_score: int
    max_score: int
    def __init__(self, tier: _Optional[_Union[_model_pb2.QAEvaluationRatingTier, str]] = ..., label: _Optional[str] = ..., min_score: _Optional[int] = ..., max_score: _Optional[int] = ...) -> None: ...

class GetQAEvaluationRubricReply(_message.Message):
    __slots__ = ("criteria", "errors", "rating_tiers")
    CRITERIA_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    RATING_TIERS_FIELD_NUMBER: _ClassVar[int]
    criteria: _containers.RepeatedCompositeFieldContainer[QAEvaluationCriterionDef]
    errors: _containers.RepeatedCompositeFieldContainer[QAEvaluationCriticalErrorDef]
    rating_tiers: _containers.RepeatedCompositeFieldContainer[QAEvaluationRatingTierDef]
    def __init__(self, criteria: _Optional[_Iterable[_Union[QAEvaluationCriterionDef, _Mapping]]] = ..., errors: _Optional[_Iterable[_Union[QAEvaluationCriticalErrorDef, _Mapping]]] = ..., rating_tiers: _Optional[_Iterable[_Union[QAEvaluationRatingTierDef, _Mapping]]] = ...) -> None: ...

class ListQAEvaluationConversationsRequest(_message.Message):
    __slots__ = ("filter", "page_size", "page")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    filter: QAEvaluationFilter
    page_size: int
    page: int
    def __init__(self, filter: _Optional[_Union[QAEvaluationFilter, _Mapping]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class QAEvaluationConversationItem(_message.Message):
    __slots__ = ("conversation_id", "external_id", "customer_name", "cs_user_id", "cs_display_name", "last_message_at", "status", "total_score", "first_messages_content", "satisfaction")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_NAME_FIELD_NUMBER: _ClassVar[int]
    CS_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CS_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
    FIRST_MESSAGES_CONTENT_FIELD_NUMBER: _ClassVar[int]
    SATISFACTION_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    external_id: str
    customer_name: str
    cs_user_id: int
    cs_display_name: str
    last_message_at: _timestamp_pb2.Timestamp
    status: _model_pb2.QAEvaluationStatus
    total_score: int
    first_messages_content: str
    satisfaction: _model_pb2.CustomerSentiment
    def __init__(self, conversation_id: _Optional[int] = ..., external_id: _Optional[str] = ..., customer_name: _Optional[str] = ..., cs_user_id: _Optional[int] = ..., cs_display_name: _Optional[str] = ..., last_message_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_model_pb2.QAEvaluationStatus, str]] = ..., total_score: _Optional[int] = ..., first_messages_content: _Optional[str] = ..., satisfaction: _Optional[_Union[_model_pb2.CustomerSentiment, str]] = ...) -> None: ...

class ListQAEvaluationConversationsReply(_message.Message):
    __slots__ = ("conversations", "page_size", "page", "count", "pending_count")
    CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    PENDING_COUNT_FIELD_NUMBER: _ClassVar[int]
    conversations: _containers.RepeatedCompositeFieldContainer[QAEvaluationConversationItem]
    page_size: int
    page: int
    count: int
    pending_count: int
    def __init__(self, conversations: _Optional[_Iterable[_Union[QAEvaluationConversationItem, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ..., pending_count: _Optional[int] = ...) -> None: ...

class GetQAEvaluationRequest(_message.Message):
    __slots__ = ("conversation_id",)
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    def __init__(self, conversation_id: _Optional[int] = ...) -> None: ...

class QAEvaluationCriterionScore(_message.Message):
    __slots__ = ("criterion", "score")
    CRITERION_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    criterion: _model_pb2.QAEvaluationCriterion
    score: int
    def __init__(self, criterion: _Optional[_Union[_model_pb2.QAEvaluationCriterion, str]] = ..., score: _Optional[int] = ...) -> None: ...

class QAEvaluationInfo(_message.Message):
    __slots__ = ("id", "conversation_id", "evaluator_user_id", "cs_user_id", "criteria_scores", "critical_errors", "total_score", "status", "comment", "evaluated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    EVALUATOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CS_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_SCORES_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_ERRORS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    EVALUATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    conversation_id: int
    evaluator_user_id: int
    cs_user_id: int
    criteria_scores: _containers.RepeatedCompositeFieldContainer[QAEvaluationCriterionScore]
    critical_errors: _containers.RepeatedScalarFieldContainer[_model_pb2.QAEvaluationCriticalError]
    total_score: int
    status: _model_pb2.QAEvaluationStatus
    comment: str
    evaluated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., evaluator_user_id: _Optional[int] = ..., cs_user_id: _Optional[int] = ..., criteria_scores: _Optional[_Iterable[_Union[QAEvaluationCriterionScore, _Mapping]]] = ..., critical_errors: _Optional[_Iterable[_Union[_model_pb2.QAEvaluationCriticalError, str]]] = ..., total_score: _Optional[int] = ..., status: _Optional[_Union[_model_pb2.QAEvaluationStatus, str]] = ..., comment: _Optional[str] = ..., evaluated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetQAEvaluationReply(_message.Message):
    __slots__ = ("evaluation",)
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    evaluation: QAEvaluationInfo
    def __init__(self, evaluation: _Optional[_Union[QAEvaluationInfo, _Mapping]] = ...) -> None: ...

class SubmitQAEvaluationRequest(_message.Message):
    __slots__ = ("conversation_id", "criteria_scores", "critical_errors", "status", "comment")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_SCORES_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_ERRORS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    conversation_id: int
    criteria_scores: _containers.RepeatedCompositeFieldContainer[QAEvaluationCriterionScore]
    critical_errors: _containers.RepeatedScalarFieldContainer[_model_pb2.QAEvaluationCriticalError]
    status: _model_pb2.QAEvaluationStatus
    comment: str
    def __init__(self, conversation_id: _Optional[int] = ..., criteria_scores: _Optional[_Iterable[_Union[QAEvaluationCriterionScore, _Mapping]]] = ..., critical_errors: _Optional[_Iterable[_Union[_model_pb2.QAEvaluationCriticalError, str]]] = ..., status: _Optional[_Union[_model_pb2.QAEvaluationStatus, str]] = ..., comment: _Optional[str] = ...) -> None: ...

class SubmitQAEvaluationReply(_message.Message):
    __slots__ = ("evaluation",)
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    evaluation: QAEvaluationInfo
    def __init__(self, evaluation: _Optional[_Union[QAEvaluationInfo, _Mapping]] = ...) -> None: ...

class QAEvaluationStaffScoreInfo(_message.Message):
    __slots__ = ("user_id", "display_name", "conversations_evaluated", "critical_error_count", "avg_score", "score_change")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CONVERSATIONS_EVALUATED_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    AVG_SCORE_FIELD_NUMBER: _ClassVar[int]
    SCORE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    display_name: str
    conversations_evaluated: int
    critical_error_count: int
    avg_score: float
    score_change: float
    def __init__(self, user_id: _Optional[int] = ..., display_name: _Optional[str] = ..., conversations_evaluated: _Optional[int] = ..., critical_error_count: _Optional[int] = ..., avg_score: _Optional[float] = ..., score_change: _Optional[float] = ...) -> None: ...

class GetQAEvaluationStaffRankingReply(_message.Message):
    __slots__ = ("staff", "team_avg_score")
    STAFF_FIELD_NUMBER: _ClassVar[int]
    TEAM_AVG_SCORE_FIELD_NUMBER: _ClassVar[int]
    staff: _containers.RepeatedCompositeFieldContainer[QAEvaluationStaffScoreInfo]
    team_avg_score: float
    def __init__(self, staff: _Optional[_Iterable[_Union[QAEvaluationStaffScoreInfo, _Mapping]]] = ..., team_avg_score: _Optional[float] = ...) -> None: ...

class QAEvaluationCriticalErrorItem(_message.Message):
    __slots__ = ("error", "cs_user_id", "conversation_id", "evaluated_at")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CS_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    EVALUATED_AT_FIELD_NUMBER: _ClassVar[int]
    error: _model_pb2.QAEvaluationCriticalError
    cs_user_id: int
    conversation_id: int
    evaluated_at: _timestamp_pb2.Timestamp
    def __init__(self, error: _Optional[_Union[_model_pb2.QAEvaluationCriticalError, str]] = ..., cs_user_id: _Optional[int] = ..., conversation_id: _Optional[int] = ..., evaluated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListQAEvaluationCriticalErrorsReply(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[QAEvaluationCriticalErrorItem]
    def __init__(self, items: _Optional[_Iterable[_Union[QAEvaluationCriticalErrorItem, _Mapping]]] = ...) -> None: ...

class ChatGroupInfo(_message.Message):
    __slots__ = ("id", "name", "description", "visibility", "created_by_user_id", "last_message_at", "last_message_id", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    visibility: _model_pb2.ChatGroupVisibility
    created_by_user_id: int
    last_message_at: _timestamp_pb2.Timestamp
    last_message_id: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., visibility: _Optional[_Union[_model_pb2.ChatGroupVisibility, str]] = ..., created_by_user_id: _Optional[int] = ..., last_message_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_message_id: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MyChatGroupInfo(_message.Message):
    __slots__ = ("group", "my_role", "unread_count", "last_message", "last_message_in_thread", "last_message_thread_root_id")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MY_ROLE_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_IN_THREAD_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    group: ChatGroupInfo
    my_role: _model_pb2.ChatGroupRole
    unread_count: int
    last_message: ChatGroupMessageInfo
    last_message_in_thread: bool
    last_message_thread_root_id: int
    def __init__(self, group: _Optional[_Union[ChatGroupInfo, _Mapping]] = ..., my_role: _Optional[_Union[_model_pb2.ChatGroupRole, str]] = ..., unread_count: _Optional[int] = ..., last_message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ..., last_message_in_thread: _Optional[bool] = ..., last_message_thread_root_id: _Optional[int] = ...) -> None: ...

class CreateChatGroupRequest(_message.Message):
    __slots__ = ("name", "description", "visibility")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    visibility: _model_pb2.ChatGroupVisibility
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., visibility: _Optional[_Union[_model_pb2.ChatGroupVisibility, str]] = ...) -> None: ...

class CreateChatGroupReply(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: MyChatGroupInfo
    def __init__(self, group: _Optional[_Union[MyChatGroupInfo, _Mapping]] = ...) -> None: ...

class UpdateChatGroupRequest(_message.Message):
    __slots__ = ("id", "changes")
    class Change(_message.Message):
        __slots__ = ("name", "description", "visibility")
        NAME_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        VISIBILITY_FIELD_NUMBER: _ClassVar[int]
        name: str
        description: str
        visibility: _model_pb2.ChatGroupVisibility
        def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., visibility: _Optional[_Union[_model_pb2.ChatGroupVisibility, str]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdateChatGroupRequest.Change]
    def __init__(self, id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdateChatGroupRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateChatGroupReply(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: MyChatGroupInfo
    def __init__(self, group: _Optional[_Union[MyChatGroupInfo, _Mapping]] = ...) -> None: ...

class DeleteChatGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteChatGroupReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMyChatGroupsRequest(_message.Message):
    __slots__ = ("page_size", "page")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListMyChatGroupsReply(_message.Message):
    __slots__ = ("groups", "page_size", "page", "count")
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[MyChatGroupInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, groups: _Optional[_Iterable[_Union[MyChatGroupInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class GetChatGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetChatGroupReply(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: MyChatGroupInfo
    def __init__(self, group: _Optional[_Union[MyChatGroupInfo, _Mapping]] = ...) -> None: ...

class ChatGroupMemberInfo(_message.Message):
    __slots__ = ("user_id", "role", "joined_at")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    JOINED_AT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    role: _model_pb2.ChatGroupRole
    joined_at: _timestamp_pb2.Timestamp
    def __init__(self, user_id: _Optional[int] = ..., role: _Optional[_Union[_model_pb2.ChatGroupRole, str]] = ..., joined_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AddChatGroupMemberRequest(_message.Message):
    __slots__ = ("group_id", "user_id", "role")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    user_id: int
    role: _model_pb2.ChatGroupRole
    def __init__(self, group_id: _Optional[int] = ..., user_id: _Optional[int] = ..., role: _Optional[_Union[_model_pb2.ChatGroupRole, str]] = ...) -> None: ...

class AddChatGroupMemberReply(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: ChatGroupMemberInfo
    def __init__(self, member: _Optional[_Union[ChatGroupMemberInfo, _Mapping]] = ...) -> None: ...

class RemoveChatGroupMemberRequest(_message.Message):
    __slots__ = ("group_id", "user_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    user_id: int
    def __init__(self, group_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class RemoveChatGroupMemberReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateChatGroupMemberRoleRequest(_message.Message):
    __slots__ = ("group_id", "user_id", "role")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    user_id: int
    role: _model_pb2.ChatGroupRole
    def __init__(self, group_id: _Optional[int] = ..., user_id: _Optional[int] = ..., role: _Optional[_Union[_model_pb2.ChatGroupRole, str]] = ...) -> None: ...

class UpdateChatGroupMemberRoleReply(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: ChatGroupMemberInfo
    def __init__(self, member: _Optional[_Union[ChatGroupMemberInfo, _Mapping]] = ...) -> None: ...

class LeaveChatGroupRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    def __init__(self, group_id: _Optional[int] = ...) -> None: ...

class LeaveChatGroupReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListChatGroupMembersRequest(_message.Message):
    __slots__ = ("group_id", "page_size", "page")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    page_size: int
    page: int
    def __init__(self, group_id: _Optional[int] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListChatGroupMembersReply(_message.Message):
    __slots__ = ("members", "page_size", "page", "count")
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[ChatGroupMemberInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, members: _Optional[_Iterable[_Union[ChatGroupMemberInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class JoinChatGroupRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    def __init__(self, group_id: _Optional[int] = ...) -> None: ...

class JoinChatGroupReply(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: MyChatGroupInfo
    def __init__(self, group: _Optional[_Union[MyChatGroupInfo, _Mapping]] = ...) -> None: ...

class ChatGroupTopicInfo(_message.Message):
    __slots__ = ("id", "group_id", "name", "description", "created_by_user_id", "last_message_at", "last_message_id", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    group_id: int
    name: str
    description: str
    created_by_user_id: int
    last_message_at: _timestamp_pb2.Timestamp
    last_message_id: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., group_id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., created_by_user_id: _Optional[int] = ..., last_message_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_message_id: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MyChatGroupTopicInfo(_message.Message):
    __slots__ = ("topic", "unread_count", "last_message")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    topic: ChatGroupTopicInfo
    unread_count: int
    last_message: ChatGroupMessageInfo
    def __init__(self, topic: _Optional[_Union[ChatGroupTopicInfo, _Mapping]] = ..., unread_count: _Optional[int] = ..., last_message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ...) -> None: ...

class CreateChatGroupTopicRequest(_message.Message):
    __slots__ = ("group_id", "name", "description")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    name: str
    description: str
    def __init__(self, group_id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateChatGroupTopicReply(_message.Message):
    __slots__ = ("topic",)
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: MyChatGroupTopicInfo
    def __init__(self, topic: _Optional[_Union[MyChatGroupTopicInfo, _Mapping]] = ...) -> None: ...

class UpdateChatGroupTopicRequest(_message.Message):
    __slots__ = ("topic_id", "changes")
    class Change(_message.Message):
        __slots__ = ("name", "description")
        NAME_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        name: str
        description: str
        def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    topic_id: int
    changes: _containers.RepeatedCompositeFieldContainer[UpdateChatGroupTopicRequest.Change]
    def __init__(self, topic_id: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[UpdateChatGroupTopicRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateChatGroupTopicReply(_message.Message):
    __slots__ = ("topic",)
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: MyChatGroupTopicInfo
    def __init__(self, topic: _Optional[_Union[MyChatGroupTopicInfo, _Mapping]] = ...) -> None: ...

class DeleteChatGroupTopicRequest(_message.Message):
    __slots__ = ("topic_id",)
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    topic_id: int
    def __init__(self, topic_id: _Optional[int] = ...) -> None: ...

class DeleteChatGroupTopicReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListChatGroupTopicsRequest(_message.Message):
    __slots__ = ("group_id", "page_size", "page")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    page_size: int
    page: int
    def __init__(self, group_id: _Optional[int] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListChatGroupTopicsReply(_message.Message):
    __slots__ = ("topics", "page_size", "page", "count")
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    topics: _containers.RepeatedCompositeFieldContainer[MyChatGroupTopicInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, topics: _Optional[_Iterable[_Union[MyChatGroupTopicInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class GetChatGroupTopicRequest(_message.Message):
    __slots__ = ("topic_id",)
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    topic_id: int
    def __init__(self, topic_id: _Optional[int] = ...) -> None: ...

class GetChatGroupTopicReply(_message.Message):
    __slots__ = ("topic",)
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: MyChatGroupTopicInfo
    def __init__(self, topic: _Optional[_Union[MyChatGroupTopicInfo, _Mapping]] = ...) -> None: ...

class MessageThreadSummary(_message.Message):
    __slots__ = ("root_message_id", "reply_count", "last_reply_at", "last_reply_message_id", "unread_count")
    ROOT_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_REPLY_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_REPLY_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    root_message_id: int
    reply_count: int
    last_reply_at: _timestamp_pb2.Timestamp
    last_reply_message_id: int
    unread_count: int
    def __init__(self, root_message_id: _Optional[int] = ..., reply_count: _Optional[int] = ..., last_reply_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_reply_message_id: _Optional[int] = ..., unread_count: _Optional[int] = ...) -> None: ...

class MessageReaction(_message.Message):
    __slots__ = ("id", "user_id", "emoji")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    emoji: str
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ..., emoji: _Optional[str] = ...) -> None: ...

class ChatGroupMessageInfo(_message.Message):
    __slots__ = ("id", "group_id", "sender_user_id", "sender_username", "content", "images", "videos", "files", "mentioned_user_ids", "created_at", "edited_at", "deleted_at", "topic_id", "received_count", "read_count", "received_by_user_ids", "read_by_user_ids", "delivery_status", "reply_to", "message_thread_root_id", "message_thread", "sticker_id", "sticker_url", "reactions", "link_previews", "pinned", "pinned_at", "pinned_by_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    MENTIONED_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EDITED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_COUNT_FIELD_NUMBER: _ClassVar[int]
    READ_COUNT_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_BY_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    READ_BY_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_FIELD_NUMBER: _ClassVar[int]
    STICKER_ID_FIELD_NUMBER: _ClassVar[int]
    STICKER_URL_FIELD_NUMBER: _ClassVar[int]
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    LINK_PREVIEWS_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    PINNED_AT_FIELD_NUMBER: _ClassVar[int]
    PINNED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    group_id: int
    sender_user_id: int
    sender_username: str
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    mentioned_user_ids: _containers.RepeatedScalarFieldContainer[int]
    created_at: _timestamp_pb2.Timestamp
    edited_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    topic_id: int
    received_count: int
    read_count: int
    received_by_user_ids: _containers.RepeatedScalarFieldContainer[int]
    read_by_user_ids: _containers.RepeatedScalarFieldContainer[int]
    delivery_status: ChatGroupDeliveryStatus
    reply_to: ChatGroupMessageInfo
    message_thread_root_id: int
    message_thread: MessageThreadSummary
    sticker_id: int
    sticker_url: str
    reactions: _containers.RepeatedCompositeFieldContainer[MessageReaction]
    link_previews: _containers.RepeatedCompositeFieldContainer[LinkPreview]
    pinned: bool
    pinned_at: _timestamp_pb2.Timestamp
    pinned_by_user_id: int
    def __init__(self, id: _Optional[int] = ..., group_id: _Optional[int] = ..., sender_user_id: _Optional[int] = ..., sender_username: _Optional[str] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., mentioned_user_ids: _Optional[_Iterable[int]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., edited_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., topic_id: _Optional[int] = ..., received_count: _Optional[int] = ..., read_count: _Optional[int] = ..., received_by_user_ids: _Optional[_Iterable[int]] = ..., read_by_user_ids: _Optional[_Iterable[int]] = ..., delivery_status: _Optional[_Union[ChatGroupDeliveryStatus, str]] = ..., reply_to: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ..., message_thread_root_id: _Optional[int] = ..., message_thread: _Optional[_Union[MessageThreadSummary, _Mapping]] = ..., sticker_id: _Optional[int] = ..., sticker_url: _Optional[str] = ..., reactions: _Optional[_Iterable[_Union[MessageReaction, _Mapping]]] = ..., link_previews: _Optional[_Iterable[_Union[LinkPreview, _Mapping]]] = ..., pinned: _Optional[bool] = ..., pinned_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., pinned_by_user_id: _Optional[int] = ...) -> None: ...

class SendChatGroupMessageRequest(_message.Message):
    __slots__ = ("group_id", "content", "images", "videos", "files", "mentioned_user_ids", "client_message_id", "topic_id", "reply_to_message_id", "message_thread_root_id", "sticker_id", "link_previews")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    MENTIONED_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    STICKER_ID_FIELD_NUMBER: _ClassVar[int]
    LINK_PREVIEWS_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    mentioned_user_ids: _containers.RepeatedScalarFieldContainer[int]
    client_message_id: str
    topic_id: int
    reply_to_message_id: int
    message_thread_root_id: int
    sticker_id: int
    link_previews: _containers.RepeatedCompositeFieldContainer[LinkPreview]
    def __init__(self, group_id: _Optional[int] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., mentioned_user_ids: _Optional[_Iterable[int]] = ..., client_message_id: _Optional[str] = ..., topic_id: _Optional[int] = ..., reply_to_message_id: _Optional[int] = ..., message_thread_root_id: _Optional[int] = ..., sticker_id: _Optional[int] = ..., link_previews: _Optional[_Iterable[_Union[LinkPreview, _Mapping]]] = ...) -> None: ...

class SendChatGroupMessageReply(_message.Message):
    __slots__ = ("message", "duplicate")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DUPLICATE_FIELD_NUMBER: _ClassVar[int]
    message: ChatGroupMessageInfo
    duplicate: bool
    def __init__(self, message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ..., duplicate: _Optional[bool] = ...) -> None: ...

class UpdateChatGroupMessageRequest(_message.Message):
    __slots__ = ("message_id", "content", "images", "videos", "files", "mentioned_user_ids", "link_previews")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    MENTIONED_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    LINK_PREVIEWS_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    mentioned_user_ids: _containers.RepeatedScalarFieldContainer[int]
    link_previews: _containers.RepeatedCompositeFieldContainer[LinkPreview]
    def __init__(self, message_id: _Optional[int] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., mentioned_user_ids: _Optional[_Iterable[int]] = ..., link_previews: _Optional[_Iterable[_Union[LinkPreview, _Mapping]]] = ...) -> None: ...

class UpdateChatGroupMessageReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: ChatGroupMessageInfo
    def __init__(self, message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ...) -> None: ...

class DeleteChatGroupMessageRequest(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    def __init__(self, message_id: _Optional[int] = ...) -> None: ...

class DeleteChatGroupMessageReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: ChatGroupMessageInfo
    def __init__(self, message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ...) -> None: ...

class ListChatGroupMessagesRequest(_message.Message):
    __slots__ = ("group_id", "page_size", "topic_id", "before_message_id", "after_message_id", "around_message_id", "message_thread_root_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    BEFORE_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    AFTER_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    AROUND_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    page_size: int
    topic_id: int
    before_message_id: int
    after_message_id: int
    around_message_id: int
    message_thread_root_id: int
    def __init__(self, group_id: _Optional[int] = ..., page_size: _Optional[int] = ..., topic_id: _Optional[int] = ..., before_message_id: _Optional[int] = ..., after_message_id: _Optional[int] = ..., around_message_id: _Optional[int] = ..., message_thread_root_id: _Optional[int] = ...) -> None: ...

class ListChatGroupMessagesReply(_message.Message):
    __slots__ = ("messages", "page_size", "has_older", "has_newer", "items")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_OLDER_FIELD_NUMBER: _ClassVar[int]
    HAS_NEWER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[ChatGroupMessageInfo]
    page_size: int
    has_older: bool
    has_newer: bool
    items: _containers.RepeatedCompositeFieldContainer[ChatGroupStreamEvent]
    def __init__(self, messages: _Optional[_Iterable[_Union[ChatGroupMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., has_older: _Optional[bool] = ..., has_newer: _Optional[bool] = ..., items: _Optional[_Iterable[_Union[ChatGroupStreamEvent, _Mapping]]] = ...) -> None: ...

class MarkChatGroupReadRequest(_message.Message):
    __slots__ = ("group_id", "last_read_message_id", "topic_id", "message_thread_root_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    last_read_message_id: int
    topic_id: int
    message_thread_root_id: int
    def __init__(self, group_id: _Optional[int] = ..., last_read_message_id: _Optional[int] = ..., topic_id: _Optional[int] = ..., message_thread_root_id: _Optional[int] = ...) -> None: ...

class MarkChatGroupReadReply(_message.Message):
    __slots__ = ("unread_count",)
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    unread_count: int
    def __init__(self, unread_count: _Optional[int] = ...) -> None: ...

class MarkChatGroupReceivedRequest(_message.Message):
    __slots__ = ("group_id", "topic_id", "message_ids")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    topic_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, group_id: _Optional[int] = ..., topic_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class MarkChatGroupReceivedReply(_message.Message):
    __slots__ = ("accepted_count",)
    ACCEPTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    accepted_count: int
    def __init__(self, accepted_count: _Optional[int] = ...) -> None: ...

class SetChatGroupMessageReactionRequest(_message.Message):
    __slots__ = ("message_id", "emoji", "remove")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    emoji: str
    remove: bool
    def __init__(self, message_id: _Optional[int] = ..., emoji: _Optional[str] = ..., remove: _Optional[bool] = ...) -> None: ...

class SetChatGroupMessageReactionReply(_message.Message):
    __slots__ = ("reactions",)
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    reactions: _containers.RepeatedCompositeFieldContainer[MessageReaction]
    def __init__(self, reactions: _Optional[_Iterable[_Union[MessageReaction, _Mapping]]] = ...) -> None: ...

class SetChatGroupMessagePinnedRequest(_message.Message):
    __slots__ = ("message_id", "pinned", "notify")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    pinned: bool
    notify: bool
    def __init__(self, message_id: _Optional[int] = ..., pinned: _Optional[bool] = ..., notify: _Optional[bool] = ...) -> None: ...

class SetChatGroupMessagePinnedReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: ChatGroupMessageInfo
    def __init__(self, message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ...) -> None: ...

class ListChatGroupPinnedMessagesRequest(_message.Message):
    __slots__ = ("group_id", "topic_id", "page_size", "query", "before_pin_id", "page")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    BEFORE_PIN_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    topic_id: int
    page_size: int
    query: str
    before_pin_id: int
    page: int
    def __init__(self, group_id: _Optional[int] = ..., topic_id: _Optional[int] = ..., page_size: _Optional[int] = ..., query: _Optional[str] = ..., before_pin_id: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListChatGroupPinnedMessagesReply(_message.Message):
    __slots__ = ("messages", "page_size", "has_next")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[ChatGroupMessageInfo]
    page_size: int
    has_next: bool
    def __init__(self, messages: _Optional[_Iterable[_Union[ChatGroupMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., has_next: _Optional[bool] = ...) -> None: ...

class ListMyChatGroupMentionsRequest(_message.Message):
    __slots__ = ("page_size", "next_cursor")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    next_cursor: bytes
    def __init__(self, page_size: _Optional[int] = ..., next_cursor: _Optional[bytes] = ...) -> None: ...

class ChatGroupMentionHit(_message.Message):
    __slots__ = ("message", "group", "topic", "seen", "my_role")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    SEEN_FIELD_NUMBER: _ClassVar[int]
    MY_ROLE_FIELD_NUMBER: _ClassVar[int]
    message: ChatGroupMessageInfo
    group: ChatGroupInfo
    topic: ChatGroupTopicInfo
    seen: bool
    my_role: _model_pb2.ChatGroupRole
    def __init__(self, message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ..., group: _Optional[_Union[ChatGroupInfo, _Mapping]] = ..., topic: _Optional[_Union[ChatGroupTopicInfo, _Mapping]] = ..., seen: _Optional[bool] = ..., my_role: _Optional[_Union[_model_pb2.ChatGroupRole, str]] = ...) -> None: ...

class ListMyChatGroupMentionsReply(_message.Message):
    __slots__ = ("hits", "page_size", "next_cursor", "has_more_unread")
    HITS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_UNREAD_FIELD_NUMBER: _ClassVar[int]
    hits: _containers.RepeatedCompositeFieldContainer[ChatGroupMentionHit]
    page_size: int
    next_cursor: bytes
    has_more_unread: bool
    def __init__(self, hits: _Optional[_Iterable[_Union[ChatGroupMentionHit, _Mapping]]] = ..., page_size: _Optional[int] = ..., next_cursor: _Optional[bytes] = ..., has_more_unread: _Optional[bool] = ...) -> None: ...

class MarkChatGroupMentionReadRequest(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    def __init__(self, message_id: _Optional[int] = ...) -> None: ...

class MarkChatGroupMentionReadReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SearchChatGroupsRequest(_message.Message):
    __slots__ = ("query", "page_size", "page")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_size: int
    page: int
    def __init__(self, query: _Optional[str] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ChatGroupSearchHit(_message.Message):
    __slots__ = ("group", "my_role")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MY_ROLE_FIELD_NUMBER: _ClassVar[int]
    group: ChatGroupInfo
    my_role: _model_pb2.ChatGroupRole
    def __init__(self, group: _Optional[_Union[ChatGroupInfo, _Mapping]] = ..., my_role: _Optional[_Union[_model_pb2.ChatGroupRole, str]] = ...) -> None: ...

class SearchChatGroupsReply(_message.Message):
    __slots__ = ("hits", "page_size", "page", "count")
    HITS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    hits: _containers.RepeatedCompositeFieldContainer[ChatGroupSearchHit]
    page_size: int
    page: int
    count: int
    def __init__(self, hits: _Optional[_Iterable[_Union[ChatGroupSearchHit, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class SearchGroupMessagesRequest(_message.Message):
    __slots__ = ("group_id", "topic_ids", "query", "page_size", "page", "sort", "from_user_id", "from_time", "to_time", "message_thread_root_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_IDS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    FROM_USER_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_TIME_FIELD_NUMBER: _ClassVar[int]
    TO_TIME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    topic_ids: _containers.RepeatedScalarFieldContainer[int]
    query: str
    page_size: int
    page: int
    sort: SearchMessagesSort
    from_user_id: int
    from_time: _timestamp_pb2.Timestamp
    to_time: _timestamp_pb2.Timestamp
    message_thread_root_id: int
    def __init__(self, group_id: _Optional[int] = ..., topic_ids: _Optional[_Iterable[int]] = ..., query: _Optional[str] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., sort: _Optional[_Union[SearchMessagesSort, str]] = ..., from_user_id: _Optional[int] = ..., from_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., to_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., message_thread_root_id: _Optional[int] = ...) -> None: ...

class SearchGroupMessagesReply(_message.Message):
    __slots__ = ("hits", "page_size", "page", "has_next")
    HITS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    hits: _containers.RepeatedCompositeFieldContainer[ChatGroupMessageInfo]
    page_size: int
    page: int
    has_next: bool
    def __init__(self, hits: _Optional[_Iterable[_Union[ChatGroupMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., has_next: _Optional[bool] = ...) -> None: ...

class SignalChatGroupTypingRequest(_message.Message):
    __slots__ = ("group_id", "typing", "topic_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    typing: bool
    topic_id: int
    def __init__(self, group_id: _Optional[int] = ..., typing: _Optional[bool] = ..., topic_id: _Optional[int] = ...) -> None: ...

class SignalChatGroupTypingReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ChatGroupTypingIndicator(_message.Message):
    __slots__ = ("group_id", "user_id", "username", "typing", "topic_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    user_id: int
    username: str
    typing: bool
    topic_id: int
    def __init__(self, group_id: _Optional[int] = ..., user_id: _Optional[int] = ..., username: _Optional[str] = ..., typing: _Optional[bool] = ..., topic_id: _Optional[int] = ...) -> None: ...

class StreamChatGroupsRequest(_message.Message):
    __slots__ = ("resume_after_message_id", "resume_after_event_id")
    RESUME_AFTER_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    RESUME_AFTER_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    resume_after_message_id: int
    resume_after_event_id: int
    def __init__(self, resume_after_message_id: _Optional[int] = ..., resume_after_event_id: _Optional[int] = ...) -> None: ...

class ChatGroupStreamPing(_message.Message):
    __slots__ = ("server_time_unix_ms",)
    SERVER_TIME_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    server_time_unix_ms: int
    def __init__(self, server_time_unix_ms: _Optional[int] = ...) -> None: ...

class ChatGroupMemberChange(_message.Message):
    __slots__ = ("group_id", "change_type", "user_id", "role", "event_id", "actor_user_id", "event_at")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_AT_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    change_type: ChatGroupMemberChangeType
    user_id: int
    role: _model_pb2.ChatGroupRole
    event_id: int
    actor_user_id: int
    event_at: _timestamp_pb2.Timestamp
    def __init__(self, group_id: _Optional[int] = ..., change_type: _Optional[_Union[ChatGroupMemberChangeType, str]] = ..., user_id: _Optional[int] = ..., role: _Optional[_Union[_model_pb2.ChatGroupRole, str]] = ..., event_id: _Optional[int] = ..., actor_user_id: _Optional[int] = ..., event_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ChatGroupMetaChange(_message.Message):
    __slots__ = ("group_id", "group", "event_id", "actor_user_id", "event_at")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_AT_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    group: ChatGroupInfo
    event_id: int
    actor_user_id: int
    event_at: _timestamp_pb2.Timestamp
    def __init__(self, group_id: _Optional[int] = ..., group: _Optional[_Union[ChatGroupInfo, _Mapping]] = ..., event_id: _Optional[int] = ..., actor_user_id: _Optional[int] = ..., event_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ChatGroupTopicChange(_message.Message):
    __slots__ = ("group_id", "change_type", "topic", "event_id", "actor_user_id", "event_at")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_AT_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    change_type: ChatGroupTopicChangeType
    topic: ChatGroupTopicInfo
    event_id: int
    actor_user_id: int
    event_at: _timestamp_pb2.Timestamp
    def __init__(self, group_id: _Optional[int] = ..., change_type: _Optional[_Union[ChatGroupTopicChangeType, str]] = ..., topic: _Optional[_Union[ChatGroupTopicInfo, _Mapping]] = ..., event_id: _Optional[int] = ..., actor_user_id: _Optional[int] = ..., event_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ChatGroupReadChange(_message.Message):
    __slots__ = ("group_id", "topic_id", "reader_user_id", "last_read_message_id", "unread_count")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    READER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    topic_id: int
    reader_user_id: int
    last_read_message_id: int
    unread_count: int
    def __init__(self, group_id: _Optional[int] = ..., topic_id: _Optional[int] = ..., reader_user_id: _Optional[int] = ..., last_read_message_id: _Optional[int] = ..., unread_count: _Optional[int] = ...) -> None: ...

class ChatGroupReceivedChange(_message.Message):
    __slots__ = ("group_id", "topic_id", "receiver_user_id", "message_ids", "received_at_unix_ms")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    topic_id: int
    receiver_user_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    received_at_unix_ms: int
    def __init__(self, group_id: _Optional[int] = ..., topic_id: _Optional[int] = ..., receiver_user_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ..., received_at_unix_ms: _Optional[int] = ...) -> None: ...

class ChatGroupReactionChange(_message.Message):
    __slots__ = ("group_id", "topic_id", "message_id", "reactions", "last_reaction_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    LAST_REACTION_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    topic_id: int
    message_id: int
    reactions: _containers.RepeatedCompositeFieldContainer[MessageReaction]
    last_reaction_id: int
    def __init__(self, group_id: _Optional[int] = ..., topic_id: _Optional[int] = ..., message_id: _Optional[int] = ..., reactions: _Optional[_Iterable[_Union[MessageReaction, _Mapping]]] = ..., last_reaction_id: _Optional[int] = ...) -> None: ...

class ChatGroupPinnedChange(_message.Message):
    __slots__ = ("group_id", "topic_id", "message_id", "pinned", "pinned_by_user_id", "pinned_at", "event_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    PINNED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    PINNED_AT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    topic_id: int
    message_id: int
    pinned: bool
    pinned_by_user_id: int
    pinned_at: _timestamp_pb2.Timestamp
    event_id: int
    def __init__(self, group_id: _Optional[int] = ..., topic_id: _Optional[int] = ..., message_id: _Optional[int] = ..., pinned: _Optional[bool] = ..., pinned_by_user_id: _Optional[int] = ..., pinned_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., event_id: _Optional[int] = ...) -> None: ...

class ChatGroupStreamEvent(_message.Message):
    __slots__ = ("ping", "message", "member_change", "meta_change", "typing", "topic_change", "read_change", "received_change", "reaction_change", "pinned_change")
    PING_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_CHANGE_FIELD_NUMBER: _ClassVar[int]
    META_CHANGE_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    TOPIC_CHANGE_FIELD_NUMBER: _ClassVar[int]
    READ_CHANGE_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_CHANGE_FIELD_NUMBER: _ClassVar[int]
    REACTION_CHANGE_FIELD_NUMBER: _ClassVar[int]
    PINNED_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ping: ChatGroupStreamPing
    message: ChatGroupMessageInfo
    member_change: ChatGroupMemberChange
    meta_change: ChatGroupMetaChange
    typing: ChatGroupTypingIndicator
    topic_change: ChatGroupTopicChange
    read_change: ChatGroupReadChange
    received_change: ChatGroupReceivedChange
    reaction_change: ChatGroupReactionChange
    pinned_change: ChatGroupPinnedChange
    def __init__(self, ping: _Optional[_Union[ChatGroupStreamPing, _Mapping]] = ..., message: _Optional[_Union[ChatGroupMessageInfo, _Mapping]] = ..., member_change: _Optional[_Union[ChatGroupMemberChange, _Mapping]] = ..., meta_change: _Optional[_Union[ChatGroupMetaChange, _Mapping]] = ..., typing: _Optional[_Union[ChatGroupTypingIndicator, _Mapping]] = ..., topic_change: _Optional[_Union[ChatGroupTopicChange, _Mapping]] = ..., read_change: _Optional[_Union[ChatGroupReadChange, _Mapping]] = ..., received_change: _Optional[_Union[ChatGroupReceivedChange, _Mapping]] = ..., reaction_change: _Optional[_Union[ChatGroupReactionChange, _Mapping]] = ..., pinned_change: _Optional[_Union[ChatGroupPinnedChange, _Mapping]] = ...) -> None: ...

class DirectMessagePeerInfo(_message.Message):
    __slots__ = ("user_id", "display_name", "avatar_url", "user_name")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    display_name: str
    avatar_url: str
    user_name: str
    def __init__(self, user_id: _Optional[int] = ..., display_name: _Optional[str] = ..., avatar_url: _Optional[str] = ..., user_name: _Optional[str] = ...) -> None: ...

class DirectMessageThreadInfo(_message.Message):
    __slots__ = ("id", "peer", "last_message_at", "last_message_id", "last_message", "unread_count", "created_at", "last_message_in_thread", "last_message_thread_root_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    PEER_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_IN_THREAD_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    peer: DirectMessagePeerInfo
    last_message_at: _timestamp_pb2.Timestamp
    last_message_id: int
    last_message: DirectMessageInfo
    unread_count: int
    created_at: _timestamp_pb2.Timestamp
    last_message_in_thread: bool
    last_message_thread_root_id: int
    def __init__(self, id: _Optional[int] = ..., peer: _Optional[_Union[DirectMessagePeerInfo, _Mapping]] = ..., last_message_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_message_id: _Optional[int] = ..., last_message: _Optional[_Union[DirectMessageInfo, _Mapping]] = ..., unread_count: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_message_in_thread: _Optional[bool] = ..., last_message_thread_root_id: _Optional[int] = ...) -> None: ...

class DirectMessageInfo(_message.Message):
    __slots__ = ("id", "thread_id", "sender_user_id", "sender_username", "content", "images", "videos", "files", "created_at", "edited_at", "deleted_at", "reply_to_message_id", "reply_to", "delivery_status", "received_at_unix_ms", "read_at_unix_ms", "message_thread_root_id", "message_thread", "sticker_id", "sticker_url", "reactions", "link_previews", "pinned", "pinned_at", "pinned_by_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EDITED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    READ_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_FIELD_NUMBER: _ClassVar[int]
    STICKER_ID_FIELD_NUMBER: _ClassVar[int]
    STICKER_URL_FIELD_NUMBER: _ClassVar[int]
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    LINK_PREVIEWS_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    PINNED_AT_FIELD_NUMBER: _ClassVar[int]
    PINNED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    thread_id: int
    sender_user_id: int
    sender_username: str
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    edited_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    reply_to_message_id: int
    reply_to: DirectMessageInfo
    delivery_status: DirectMessageDeliveryStatus
    received_at_unix_ms: int
    read_at_unix_ms: int
    message_thread_root_id: int
    message_thread: MessageThreadSummary
    sticker_id: int
    sticker_url: str
    reactions: _containers.RepeatedCompositeFieldContainer[MessageReaction]
    link_previews: _containers.RepeatedCompositeFieldContainer[LinkPreview]
    pinned: bool
    pinned_at: _timestamp_pb2.Timestamp
    pinned_by_user_id: int
    def __init__(self, id: _Optional[int] = ..., thread_id: _Optional[int] = ..., sender_user_id: _Optional[int] = ..., sender_username: _Optional[str] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., edited_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., reply_to_message_id: _Optional[int] = ..., reply_to: _Optional[_Union[DirectMessageInfo, _Mapping]] = ..., delivery_status: _Optional[_Union[DirectMessageDeliveryStatus, str]] = ..., received_at_unix_ms: _Optional[int] = ..., read_at_unix_ms: _Optional[int] = ..., message_thread_root_id: _Optional[int] = ..., message_thread: _Optional[_Union[MessageThreadSummary, _Mapping]] = ..., sticker_id: _Optional[int] = ..., sticker_url: _Optional[str] = ..., reactions: _Optional[_Iterable[_Union[MessageReaction, _Mapping]]] = ..., link_previews: _Optional[_Iterable[_Union[LinkPreview, _Mapping]]] = ..., pinned: _Optional[bool] = ..., pinned_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., pinned_by_user_id: _Optional[int] = ...) -> None: ...

class CreateOrGetDirectMessageRequest(_message.Message):
    __slots__ = ("other_user_id",)
    OTHER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    other_user_id: int
    def __init__(self, other_user_id: _Optional[int] = ...) -> None: ...

class CreateOrGetDirectMessageReply(_message.Message):
    __slots__ = ("thread", "created")
    THREAD_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    thread: DirectMessageThreadInfo
    created: bool
    def __init__(self, thread: _Optional[_Union[DirectMessageThreadInfo, _Mapping]] = ..., created: _Optional[bool] = ...) -> None: ...

class ListMyDirectMessagesRequest(_message.Message):
    __slots__ = ("page_size", "page")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page: int
    def __init__(self, page_size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListMyDirectMessagesReply(_message.Message):
    __slots__ = ("threads", "page_size", "page", "count")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    threads: _containers.RepeatedCompositeFieldContainer[DirectMessageThreadInfo]
    page_size: int
    page: int
    count: int
    def __init__(self, threads: _Optional[_Iterable[_Union[DirectMessageThreadInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class GetDirectMessageRequest(_message.Message):
    __slots__ = ("thread_id",)
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    def __init__(self, thread_id: _Optional[int] = ...) -> None: ...

class GetDirectMessageReply(_message.Message):
    __slots__ = ("thread",)
    THREAD_FIELD_NUMBER: _ClassVar[int]
    thread: DirectMessageThreadInfo
    def __init__(self, thread: _Optional[_Union[DirectMessageThreadInfo, _Mapping]] = ...) -> None: ...

class SendDirectMessageRequest(_message.Message):
    __slots__ = ("thread_id", "other_user_id", "content", "images", "videos", "files", "client_message_id", "reply_to_message_id", "message_thread_root_id", "sticker_id", "link_previews")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    OTHER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    CLIENT_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    STICKER_ID_FIELD_NUMBER: _ClassVar[int]
    LINK_PREVIEWS_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    other_user_id: int
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    client_message_id: str
    reply_to_message_id: int
    message_thread_root_id: int
    sticker_id: int
    link_previews: _containers.RepeatedCompositeFieldContainer[LinkPreview]
    def __init__(self, thread_id: _Optional[int] = ..., other_user_id: _Optional[int] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., client_message_id: _Optional[str] = ..., reply_to_message_id: _Optional[int] = ..., message_thread_root_id: _Optional[int] = ..., sticker_id: _Optional[int] = ..., link_previews: _Optional[_Iterable[_Union[LinkPreview, _Mapping]]] = ...) -> None: ...

class SendDirectMessageReply(_message.Message):
    __slots__ = ("message", "thread_id", "duplicate")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    DUPLICATE_FIELD_NUMBER: _ClassVar[int]
    message: DirectMessageInfo
    thread_id: int
    duplicate: bool
    def __init__(self, message: _Optional[_Union[DirectMessageInfo, _Mapping]] = ..., thread_id: _Optional[int] = ..., duplicate: _Optional[bool] = ...) -> None: ...

class UpdateDirectMessageRequest(_message.Message):
    __slots__ = ("message_id", "content", "images", "videos", "files", "link_previews")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    LINK_PREVIEWS_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    content: str
    images: _containers.RepeatedScalarFieldContainer[str]
    videos: _containers.RepeatedScalarFieldContainer[str]
    files: _containers.RepeatedScalarFieldContainer[str]
    link_previews: _containers.RepeatedCompositeFieldContainer[LinkPreview]
    def __init__(self, message_id: _Optional[int] = ..., content: _Optional[str] = ..., images: _Optional[_Iterable[str]] = ..., videos: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[str]] = ..., link_previews: _Optional[_Iterable[_Union[LinkPreview, _Mapping]]] = ...) -> None: ...

class UpdateDirectMessageReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: DirectMessageInfo
    def __init__(self, message: _Optional[_Union[DirectMessageInfo, _Mapping]] = ...) -> None: ...

class DeleteDirectMessageRequest(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    def __init__(self, message_id: _Optional[int] = ...) -> None: ...

class DeleteDirectMessageReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: DirectMessageInfo
    def __init__(self, message: _Optional[_Union[DirectMessageInfo, _Mapping]] = ...) -> None: ...

class ListDirectMessagesRequest(_message.Message):
    __slots__ = ("thread_id", "page_size", "before_message_id", "after_message_id", "around_message_id", "message_thread_root_id")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    AFTER_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    AROUND_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    page_size: int
    before_message_id: int
    after_message_id: int
    around_message_id: int
    message_thread_root_id: int
    def __init__(self, thread_id: _Optional[int] = ..., page_size: _Optional[int] = ..., before_message_id: _Optional[int] = ..., after_message_id: _Optional[int] = ..., around_message_id: _Optional[int] = ..., message_thread_root_id: _Optional[int] = ...) -> None: ...

class ListDirectMessagesReply(_message.Message):
    __slots__ = ("messages", "page_size", "has_older", "has_newer")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_OLDER_FIELD_NUMBER: _ClassVar[int]
    HAS_NEWER_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[DirectMessageInfo]
    page_size: int
    has_older: bool
    has_newer: bool
    def __init__(self, messages: _Optional[_Iterable[_Union[DirectMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., has_older: _Optional[bool] = ..., has_newer: _Optional[bool] = ...) -> None: ...

class MarkDirectMessageReadRequest(_message.Message):
    __slots__ = ("thread_id", "last_read_message_id", "message_thread_root_id")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    last_read_message_id: int
    message_thread_root_id: int
    def __init__(self, thread_id: _Optional[int] = ..., last_read_message_id: _Optional[int] = ..., message_thread_root_id: _Optional[int] = ...) -> None: ...

class MarkDirectMessageReadReply(_message.Message):
    __slots__ = ("unread_count",)
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    unread_count: int
    def __init__(self, unread_count: _Optional[int] = ...) -> None: ...

class MarkDirectMessageReceivedRequest(_message.Message):
    __slots__ = ("thread_id", "message_ids")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, thread_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class MarkDirectMessageReceivedReply(_message.Message):
    __slots__ = ("accepted_count",)
    ACCEPTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    accepted_count: int
    def __init__(self, accepted_count: _Optional[int] = ...) -> None: ...

class SetDirectMessageReactionRequest(_message.Message):
    __slots__ = ("message_id", "emoji", "remove")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    emoji: str
    remove: bool
    def __init__(self, message_id: _Optional[int] = ..., emoji: _Optional[str] = ..., remove: _Optional[bool] = ...) -> None: ...

class SetDirectMessageReactionReply(_message.Message):
    __slots__ = ("reactions",)
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    reactions: _containers.RepeatedCompositeFieldContainer[MessageReaction]
    def __init__(self, reactions: _Optional[_Iterable[_Union[MessageReaction, _Mapping]]] = ...) -> None: ...

class SetDirectMessagePinnedRequest(_message.Message):
    __slots__ = ("message_id", "pinned", "notify")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    pinned: bool
    notify: bool
    def __init__(self, message_id: _Optional[int] = ..., pinned: _Optional[bool] = ..., notify: _Optional[bool] = ...) -> None: ...

class SetDirectMessagePinnedReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: DirectMessageInfo
    def __init__(self, message: _Optional[_Union[DirectMessageInfo, _Mapping]] = ...) -> None: ...

class ListDirectMessagePinnedMessagesRequest(_message.Message):
    __slots__ = ("thread_id", "page_size", "query", "before_pin_id", "page")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    BEFORE_PIN_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    page_size: int
    query: str
    before_pin_id: int
    page: int
    def __init__(self, thread_id: _Optional[int] = ..., page_size: _Optional[int] = ..., query: _Optional[str] = ..., before_pin_id: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...

class ListDirectMessagePinnedMessagesReply(_message.Message):
    __slots__ = ("messages", "page_size", "has_next")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[DirectMessageInfo]
    page_size: int
    has_next: bool
    def __init__(self, messages: _Optional[_Iterable[_Union[DirectMessageInfo, _Mapping]]] = ..., page_size: _Optional[int] = ..., has_next: _Optional[bool] = ...) -> None: ...

class SearchDirectMessagesRequest(_message.Message):
    __slots__ = ("thread_id", "query", "page_size", "page", "sort", "from_user_id", "from_time", "to_time", "message_thread_root_id")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    FROM_USER_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_TIME_FIELD_NUMBER: _ClassVar[int]
    TO_TIME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_THREAD_ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    query: str
    page_size: int
    page: int
    sort: SearchMessagesSort
    from_user_id: int
    from_time: _timestamp_pb2.Timestamp
    to_time: _timestamp_pb2.Timestamp
    message_thread_root_id: int
    def __init__(self, thread_id: _Optional[int] = ..., query: _Optional[str] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., sort: _Optional[_Union[SearchMessagesSort, str]] = ..., from_user_id: _Optional[int] = ..., from_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., to_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., message_thread_root_id: _Optional[int] = ...) -> None: ...

class SearchDirectMessageHit(_message.Message):
    __slots__ = ("message", "thread")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    THREAD_FIELD_NUMBER: _ClassVar[int]
    message: DirectMessageInfo
    thread: DirectMessageThreadInfo
    def __init__(self, message: _Optional[_Union[DirectMessageInfo, _Mapping]] = ..., thread: _Optional[_Union[DirectMessageThreadInfo, _Mapping]] = ...) -> None: ...

class SearchDirectMessagesReply(_message.Message):
    __slots__ = ("hits", "page_size", "page", "has_next")
    HITS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    hits: _containers.RepeatedCompositeFieldContainer[SearchDirectMessageHit]
    page_size: int
    page: int
    has_next: bool
    def __init__(self, hits: _Optional[_Iterable[_Union[SearchDirectMessageHit, _Mapping]]] = ..., page_size: _Optional[int] = ..., page: _Optional[int] = ..., has_next: _Optional[bool] = ...) -> None: ...

class SignalDirectMessageTypingRequest(_message.Message):
    __slots__ = ("thread_id", "typing")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    typing: bool
    def __init__(self, thread_id: _Optional[int] = ..., typing: _Optional[bool] = ...) -> None: ...

class SignalDirectMessageTypingReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DirectMessageTypingIndicator(_message.Message):
    __slots__ = ("thread_id", "user_id", "username", "typing")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    user_id: int
    username: str
    typing: bool
    def __init__(self, thread_id: _Optional[int] = ..., user_id: _Optional[int] = ..., username: _Optional[str] = ..., typing: _Optional[bool] = ...) -> None: ...

class StreamDirectMessagesRequest(_message.Message):
    __slots__ = ("resume_after_message_id", "resume_after_event_id")
    RESUME_AFTER_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    RESUME_AFTER_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    resume_after_message_id: int
    resume_after_event_id: int
    def __init__(self, resume_after_message_id: _Optional[int] = ..., resume_after_event_id: _Optional[int] = ...) -> None: ...

class DirectMessageStreamPing(_message.Message):
    __slots__ = ("server_time_unix_ms",)
    SERVER_TIME_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    server_time_unix_ms: int
    def __init__(self, server_time_unix_ms: _Optional[int] = ...) -> None: ...

class DirectMessageReadChange(_message.Message):
    __slots__ = ("thread_id", "reader_user_id", "last_read_message_id", "unread_count")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    READER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    reader_user_id: int
    last_read_message_id: int
    unread_count: int
    def __init__(self, thread_id: _Optional[int] = ..., reader_user_id: _Optional[int] = ..., last_read_message_id: _Optional[int] = ..., unread_count: _Optional[int] = ...) -> None: ...

class DirectMessageReceivedChange(_message.Message):
    __slots__ = ("thread_id", "receiver_user_id", "message_ids", "received_at_unix_ms")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    receiver_user_id: int
    message_ids: _containers.RepeatedScalarFieldContainer[int]
    received_at_unix_ms: int
    def __init__(self, thread_id: _Optional[int] = ..., receiver_user_id: _Optional[int] = ..., message_ids: _Optional[_Iterable[int]] = ..., received_at_unix_ms: _Optional[int] = ...) -> None: ...

class DirectMessageReactionChange(_message.Message):
    __slots__ = ("thread_id", "message_id", "reactions", "last_reaction_id")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    LAST_REACTION_ID_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    message_id: int
    reactions: _containers.RepeatedCompositeFieldContainer[MessageReaction]
    last_reaction_id: int
    def __init__(self, thread_id: _Optional[int] = ..., message_id: _Optional[int] = ..., reactions: _Optional[_Iterable[_Union[MessageReaction, _Mapping]]] = ..., last_reaction_id: _Optional[int] = ...) -> None: ...

class DirectMessagePinnedChange(_message.Message):
    __slots__ = ("thread_id", "message_id", "pinned", "pinned_by_user_id", "pinned_at", "event_id")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    PINNED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    PINNED_AT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    message_id: int
    pinned: bool
    pinned_by_user_id: int
    pinned_at: _timestamp_pb2.Timestamp
    event_id: int
    def __init__(self, thread_id: _Optional[int] = ..., message_id: _Optional[int] = ..., pinned: _Optional[bool] = ..., pinned_by_user_id: _Optional[int] = ..., pinned_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., event_id: _Optional[int] = ...) -> None: ...

class DirectMessageStreamEvent(_message.Message):
    __slots__ = ("ping", "message", "typing", "read_change", "received_change", "reaction_change", "pinned_change")
    PING_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    READ_CHANGE_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_CHANGE_FIELD_NUMBER: _ClassVar[int]
    REACTION_CHANGE_FIELD_NUMBER: _ClassVar[int]
    PINNED_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ping: DirectMessageStreamPing
    message: DirectMessageInfo
    typing: DirectMessageTypingIndicator
    read_change: DirectMessageReadChange
    received_change: DirectMessageReceivedChange
    reaction_change: DirectMessageReactionChange
    pinned_change: DirectMessagePinnedChange
    def __init__(self, ping: _Optional[_Union[DirectMessageStreamPing, _Mapping]] = ..., message: _Optional[_Union[DirectMessageInfo, _Mapping]] = ..., typing: _Optional[_Union[DirectMessageTypingIndicator, _Mapping]] = ..., read_change: _Optional[_Union[DirectMessageReadChange, _Mapping]] = ..., received_change: _Optional[_Union[DirectMessageReceivedChange, _Mapping]] = ..., reaction_change: _Optional[_Union[DirectMessageReactionChange, _Mapping]] = ..., pinned_change: _Optional[_Union[DirectMessagePinnedChange, _Mapping]] = ...) -> None: ...

class PushDevice(_message.Message):
    __slots__ = ("id", "platform", "token", "app_version", "locale", "created_at", "updated_at", "client_device_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    platform: PushPlatform
    token: str
    app_version: str
    locale: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    client_device_id: str
    def __init__(self, id: _Optional[int] = ..., platform: _Optional[_Union[PushPlatform, str]] = ..., token: _Optional[str] = ..., app_version: _Optional[str] = ..., locale: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., client_device_id: _Optional[str] = ...) -> None: ...

class NotificationPreferences(_message.Message):
    __slots__ = ("customer_new_conversation", "customer_messages", "group_messages", "group_mentions", "group_membership", "direct_messages", "group_reactions", "direct_message_reactions")
    CUSTOMER_NEW_CONVERSATION_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    GROUP_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    GROUP_MENTIONS_FIELD_NUMBER: _ClassVar[int]
    GROUP_MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    DIRECT_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    GROUP_REACTIONS_FIELD_NUMBER: _ClassVar[int]
    DIRECT_MESSAGE_REACTIONS_FIELD_NUMBER: _ClassVar[int]
    customer_new_conversation: bool
    customer_messages: bool
    group_messages: bool
    group_mentions: bool
    group_membership: bool
    direct_messages: bool
    group_reactions: bool
    direct_message_reactions: bool
    def __init__(self, customer_new_conversation: _Optional[bool] = ..., customer_messages: _Optional[bool] = ..., group_messages: _Optional[bool] = ..., group_mentions: _Optional[bool] = ..., group_membership: _Optional[bool] = ..., direct_messages: _Optional[bool] = ..., group_reactions: _Optional[bool] = ..., direct_message_reactions: _Optional[bool] = ...) -> None: ...

class RegisterPushDeviceRequest(_message.Message):
    __slots__ = ("platform", "token", "app_version", "locale", "client_device_id")
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    platform: PushPlatform
    token: str
    app_version: str
    locale: str
    client_device_id: str
    def __init__(self, platform: _Optional[_Union[PushPlatform, str]] = ..., token: _Optional[str] = ..., app_version: _Optional[str] = ..., locale: _Optional[str] = ..., client_device_id: _Optional[str] = ...) -> None: ...

class RegisterPushDeviceReply(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: PushDevice
    def __init__(self, device: _Optional[_Union[PushDevice, _Mapping]] = ...) -> None: ...

class UnregisterPushDeviceRequest(_message.Message):
    __slots__ = ("device_id", "token")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    token: str
    def __init__(self, device_id: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class UnregisterPushDeviceReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNotificationPreferencesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNotificationPreferencesReply(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: NotificationPreferences
    def __init__(self, preferences: _Optional[_Union[NotificationPreferences, _Mapping]] = ...) -> None: ...

class UpdateNotificationPreferencesRequest(_message.Message):
    __slots__ = ("changes",)
    class Change(_message.Message):
        __slots__ = ("customer_new_conversation", "customer_messages", "group_messages", "group_mentions", "group_membership", "direct_messages", "group_reactions", "direct_message_reactions")
        CUSTOMER_NEW_CONVERSATION_FIELD_NUMBER: _ClassVar[int]
        CUSTOMER_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        GROUP_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        GROUP_MENTIONS_FIELD_NUMBER: _ClassVar[int]
        GROUP_MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
        DIRECT_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        GROUP_REACTIONS_FIELD_NUMBER: _ClassVar[int]
        DIRECT_MESSAGE_REACTIONS_FIELD_NUMBER: _ClassVar[int]
        customer_new_conversation: bool
        customer_messages: bool
        group_messages: bool
        group_mentions: bool
        group_membership: bool
        direct_messages: bool
        group_reactions: bool
        direct_message_reactions: bool
        def __init__(self, customer_new_conversation: _Optional[bool] = ..., customer_messages: _Optional[bool] = ..., group_messages: _Optional[bool] = ..., group_mentions: _Optional[bool] = ..., group_membership: _Optional[bool] = ..., direct_messages: _Optional[bool] = ..., group_reactions: _Optional[bool] = ..., direct_message_reactions: _Optional[bool] = ...) -> None: ...
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    changes: _containers.RepeatedCompositeFieldContainer[UpdateNotificationPreferencesRequest.Change]
    def __init__(self, changes: _Optional[_Iterable[_Union[UpdateNotificationPreferencesRequest.Change, _Mapping]]] = ...) -> None: ...

class UpdateNotificationPreferencesReply(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: NotificationPreferences
    def __init__(self, preferences: _Optional[_Union[NotificationPreferences, _Mapping]] = ...) -> None: ...

class LinkPreview(_message.Message):
    __slots__ = ("url", "title", "description", "image_url", "site_name")
    URL_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    SITE_NAME_FIELD_NUMBER: _ClassVar[int]
    url: str
    title: str
    description: str
    image_url: str
    site_name: str
    def __init__(self, url: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., image_url: _Optional[str] = ..., site_name: _Optional[str] = ...) -> None: ...

class PreviewLinkRequest(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class PreviewLinkReply(_message.Message):
    __slots__ = ("preview", "result")
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    preview: LinkPreview
    result: PreviewLinkResult
    def __init__(self, preview: _Optional[_Union[LinkPreview, _Mapping]] = ..., result: _Optional[_Union[PreviewLinkResult, str]] = ...) -> None: ...
