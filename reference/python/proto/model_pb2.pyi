from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Platform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLATFORM_UNSPECIFIED: _ClassVar[Platform]
    PLATFORM_FACEBOOK: _ClassVar[Platform]
    PLATFORM_INSTAGRAM: _ClassVar[Platform]
    PLATFORM_WHATSAPP: _ClassVar[Platform]
    PLATFORM_EXTERNAL: _ClassVar[Platform]

class Sender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SENDER_UNSPECIFIED: _ClassVar[Sender]
    SENDER_CUSTOMER: _ClassVar[Sender]
    SENDER_SALES: _ClassVar[Sender]
    SENDER_BOT: _ClassVar[Sender]

class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METHOD_UNSPECIFIED: _ClassVar[Method]
    METHOD_FACEBOOK: _ClassVar[Method]
    METHOD_TELEGRAM: _ClassVar[Method]
    METHOD_BOT: _ClassVar[Method]
    METHOD_EXTERNAL: _ClassVar[Method]

class MessageStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MESSAGE_STATUS_UNSPECIFIED: _ClassVar[MessageStatus]
    MESSAGE_STATUS_PENDING: _ClassVar[MessageStatus]
    MESSAGE_STATUS_SENT: _ClassVar[MessageStatus]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_UNSPECIFIED: _ClassVar[Status]
    STATUS_ACTIVE: _ClassVar[Status]
    STATUS_INACTIVE: _ClassVar[Status]

class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODE_UNSPECIFIED: _ClassVar[Mode]
    MODE_AUTO: _ClassVar[Mode]
    MODE_TELEGRAM: _ClassVar[Mode]
    MODE_AUTO_TELEGRAM: _ClassVar[Mode]
    MODE_AI_RECOMMEND: _ClassVar[Mode]

class ConversationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONVERSATION_STATE_OPEN: _ClassVar[ConversationState]
    CONVERSATION_STATE_IN_PROGRESS: _ClassVar[ConversationState]
    CONVERSATION_STATE_PENDING: _ClassVar[ConversationState]
    CONVERSATION_STATE_RESOLVED: _ClassVar[ConversationState]

class ScheduledMessageStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCHEDULED_MESSAGE_STATUS_UNSPECIFIED: _ClassVar[ScheduledMessageStatus]
    SCHEDULED_MESSAGE_STATUS_PENDING: _ClassVar[ScheduledMessageStatus]
    SCHEDULED_MESSAGE_STATUS_SENT: _ClassVar[ScheduledMessageStatus]
    SCHEDULED_MESSAGE_STATUS_FAILED: _ClassVar[ScheduledMessageStatus]
    SCHEDULED_MESSAGE_STATUS_CANCELLED: _ClassVar[ScheduledMessageStatus]
    SCHEDULED_MESSAGE_STATUS_PARTIAL: _ClassVar[ScheduledMessageStatus]

class ScheduledDeliveryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCHEDULED_DELIVERY_STATUS_UNSPECIFIED: _ClassVar[ScheduledDeliveryStatus]
    SCHEDULED_DELIVERY_STATUS_PENDING: _ClassVar[ScheduledDeliveryStatus]
    SCHEDULED_DELIVERY_STATUS_SENT: _ClassVar[ScheduledDeliveryStatus]
    SCHEDULED_DELIVERY_STATUS_FAILED: _ClassVar[ScheduledDeliveryStatus]

class DeliveryFailureReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DELIVERY_FAILURE_REASON_UNSPECIFIED: _ClassVar[DeliveryFailureReason]
    DELIVERY_FAILURE_REASON_NONE: _ClassVar[DeliveryFailureReason]
    DELIVERY_FAILURE_REASON_INTERNAL: _ClassVar[DeliveryFailureReason]
    DELIVERY_FAILURE_REASON_PLATFORM_POLICY: _ClassVar[DeliveryFailureReason]
    DELIVERY_FAILURE_REASON_PLATFORM_PERMISSION: _ClassVar[DeliveryFailureReason]
    DELIVERY_FAILURE_REASON_PLATFORM_RATE_LIMIT: _ClassVar[DeliveryFailureReason]
    DELIVERY_FAILURE_REASON_INVALID_RECIPIENT: _ClassVar[DeliveryFailureReason]
    DELIVERY_FAILURE_REASON_UNKNOWN_PLATFORM_ERROR: _ClassVar[DeliveryFailureReason]

class RepeatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPEAT_TYPE_UNSPECIFIED: _ClassVar[RepeatType]
    REPEAT_TYPE_NONE: _ClassVar[RepeatType]
    REPEAT_TYPE_DAILY: _ClassVar[RepeatType]
    REPEAT_TYPE_WEEKLY: _ClassVar[RepeatType]

class LabelOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LABEL_OP_UNSPECIFIED: _ClassVar[LabelOp]
    LABEL_OP_ADD: _ClassVar[LabelOp]
    LABEL_OP_DELETE: _ClassVar[LabelOp]

class BusinessLine(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUSINESS_LINE_UNSPECIFIED: _ClassVar[BusinessLine]
    BUSINESS_LINE_CUSTOMER_SUPPORT: _ClassVar[BusinessLine]
    BUSINESS_LINE_AFFILIATE: _ClassVar[BusinessLine]

class ChatGroupVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_GROUP_VISIBILITY_UNSPECIFIED: _ClassVar[ChatGroupVisibility]
    CHAT_GROUP_VISIBILITY_PRIVATE: _ClassVar[ChatGroupVisibility]
    CHAT_GROUP_VISIBILITY_PUBLIC: _ClassVar[ChatGroupVisibility]

class ChatGroupRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_GROUP_ROLE_UNSPECIFIED: _ClassVar[ChatGroupRole]
    CHAT_GROUP_ROLE_OWNER: _ClassVar[ChatGroupRole]
    CHAT_GROUP_ROLE_ADMIN: _ClassVar[ChatGroupRole]
    CHAT_GROUP_ROLE_MEMBER: _ClassVar[ChatGroupRole]

class CustomerSentiment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CUSTOMER_SENTIMENT_UNSPECIFIED: _ClassVar[CustomerSentiment]
    CUSTOMER_SENTIMENT_SATISFIED: _ClassVar[CustomerSentiment]
    CUSTOMER_SENTIMENT_NEUTRAL: _ClassVar[CustomerSentiment]
    CUSTOMER_SENTIMENT_DISSATISFIED: _ClassVar[CustomerSentiment]

class QAEvaluationCriterion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QA_EVALUATION_CRITERION_UNSPECIFIED: _ClassVar[QAEvaluationCriterion]
    QA_EVALUATION_CRITERION_UNDERSTAND_ISSUE: _ClassVar[QAEvaluationCriterion]
    QA_EVALUATION_CRITERION_CORRECT_INFO: _ClassVar[QAEvaluationCriterion]
    QA_EVALUATION_CRITERION_CLEAR_SOLUTION: _ClassVar[QAEvaluationCriterion]
    QA_EVALUATION_CRITERION_ATTITUDE: _ClassVar[QAEvaluationCriterion]
    QA_EVALUATION_CRITERION_NATURAL_SPEECH: _ClassVar[QAEvaluationCriterion]
    QA_EVALUATION_CRITERION_FOLLOW_PROCESS: _ClassVar[QAEvaluationCriterion]
    QA_EVALUATION_CRITERION_NEAT_CLOSING: _ClassVar[QAEvaluationCriterion]

class QAEvaluationCriticalError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QA_EVALUATION_CRITICAL_ERROR_UNSPECIFIED: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_WRONG_MONEY_INFO: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_UNCERTAIN_PROMISE: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_INFO_LEAK: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_INSULT_CUSTOMER: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_OUT_OF_PROCESS: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_UNRESOLVED_CLOSING: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_WRONG_TRANSFER: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_UNCHECKED_AI_SUGGESTION: _ClassVar[QAEvaluationCriticalError]
    QA_EVALUATION_CRITICAL_ERROR_ABANDONED_CHAT: _ClassVar[QAEvaluationCriticalError]

class QAEvaluationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QA_EVALUATION_STATUS_UNSPECIFIED: _ClassVar[QAEvaluationStatus]
    QA_EVALUATION_STATUS_PENDING: _ClassVar[QAEvaluationStatus]
    QA_EVALUATION_STATUS_EVALUATED: _ClassVar[QAEvaluationStatus]
    QA_EVALUATION_STATUS_DISPUTE: _ClassVar[QAEvaluationStatus]

class QAEvaluationRatingTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QA_EVALUATION_RATING_TIER_UNSPECIFIED: _ClassVar[QAEvaluationRatingTier]
    QA_EVALUATION_RATING_TIER_GOOD: _ClassVar[QAEvaluationRatingTier]
    QA_EVALUATION_RATING_TIER_PASS: _ClassVar[QAEvaluationRatingTier]
    QA_EVALUATION_RATING_TIER_NEEDS_IMPROVEMENT: _ClassVar[QAEvaluationRatingTier]
    QA_EVALUATION_RATING_TIER_MUST_MENTOR: _ClassVar[QAEvaluationRatingTier]
PLATFORM_UNSPECIFIED: Platform
PLATFORM_FACEBOOK: Platform
PLATFORM_INSTAGRAM: Platform
PLATFORM_WHATSAPP: Platform
PLATFORM_EXTERNAL: Platform
SENDER_UNSPECIFIED: Sender
SENDER_CUSTOMER: Sender
SENDER_SALES: Sender
SENDER_BOT: Sender
METHOD_UNSPECIFIED: Method
METHOD_FACEBOOK: Method
METHOD_TELEGRAM: Method
METHOD_BOT: Method
METHOD_EXTERNAL: Method
MESSAGE_STATUS_UNSPECIFIED: MessageStatus
MESSAGE_STATUS_PENDING: MessageStatus
MESSAGE_STATUS_SENT: MessageStatus
STATUS_UNSPECIFIED: Status
STATUS_ACTIVE: Status
STATUS_INACTIVE: Status
MODE_UNSPECIFIED: Mode
MODE_AUTO: Mode
MODE_TELEGRAM: Mode
MODE_AUTO_TELEGRAM: Mode
MODE_AI_RECOMMEND: Mode
CONVERSATION_STATE_OPEN: ConversationState
CONVERSATION_STATE_IN_PROGRESS: ConversationState
CONVERSATION_STATE_PENDING: ConversationState
CONVERSATION_STATE_RESOLVED: ConversationState
SCHEDULED_MESSAGE_STATUS_UNSPECIFIED: ScheduledMessageStatus
SCHEDULED_MESSAGE_STATUS_PENDING: ScheduledMessageStatus
SCHEDULED_MESSAGE_STATUS_SENT: ScheduledMessageStatus
SCHEDULED_MESSAGE_STATUS_FAILED: ScheduledMessageStatus
SCHEDULED_MESSAGE_STATUS_CANCELLED: ScheduledMessageStatus
SCHEDULED_MESSAGE_STATUS_PARTIAL: ScheduledMessageStatus
SCHEDULED_DELIVERY_STATUS_UNSPECIFIED: ScheduledDeliveryStatus
SCHEDULED_DELIVERY_STATUS_PENDING: ScheduledDeliveryStatus
SCHEDULED_DELIVERY_STATUS_SENT: ScheduledDeliveryStatus
SCHEDULED_DELIVERY_STATUS_FAILED: ScheduledDeliveryStatus
DELIVERY_FAILURE_REASON_UNSPECIFIED: DeliveryFailureReason
DELIVERY_FAILURE_REASON_NONE: DeliveryFailureReason
DELIVERY_FAILURE_REASON_INTERNAL: DeliveryFailureReason
DELIVERY_FAILURE_REASON_PLATFORM_POLICY: DeliveryFailureReason
DELIVERY_FAILURE_REASON_PLATFORM_PERMISSION: DeliveryFailureReason
DELIVERY_FAILURE_REASON_PLATFORM_RATE_LIMIT: DeliveryFailureReason
DELIVERY_FAILURE_REASON_INVALID_RECIPIENT: DeliveryFailureReason
DELIVERY_FAILURE_REASON_UNKNOWN_PLATFORM_ERROR: DeliveryFailureReason
REPEAT_TYPE_UNSPECIFIED: RepeatType
REPEAT_TYPE_NONE: RepeatType
REPEAT_TYPE_DAILY: RepeatType
REPEAT_TYPE_WEEKLY: RepeatType
LABEL_OP_UNSPECIFIED: LabelOp
LABEL_OP_ADD: LabelOp
LABEL_OP_DELETE: LabelOp
BUSINESS_LINE_UNSPECIFIED: BusinessLine
BUSINESS_LINE_CUSTOMER_SUPPORT: BusinessLine
BUSINESS_LINE_AFFILIATE: BusinessLine
CHAT_GROUP_VISIBILITY_UNSPECIFIED: ChatGroupVisibility
CHAT_GROUP_VISIBILITY_PRIVATE: ChatGroupVisibility
CHAT_GROUP_VISIBILITY_PUBLIC: ChatGroupVisibility
CHAT_GROUP_ROLE_UNSPECIFIED: ChatGroupRole
CHAT_GROUP_ROLE_OWNER: ChatGroupRole
CHAT_GROUP_ROLE_ADMIN: ChatGroupRole
CHAT_GROUP_ROLE_MEMBER: ChatGroupRole
CUSTOMER_SENTIMENT_UNSPECIFIED: CustomerSentiment
CUSTOMER_SENTIMENT_SATISFIED: CustomerSentiment
CUSTOMER_SENTIMENT_NEUTRAL: CustomerSentiment
CUSTOMER_SENTIMENT_DISSATISFIED: CustomerSentiment
QA_EVALUATION_CRITERION_UNSPECIFIED: QAEvaluationCriterion
QA_EVALUATION_CRITERION_UNDERSTAND_ISSUE: QAEvaluationCriterion
QA_EVALUATION_CRITERION_CORRECT_INFO: QAEvaluationCriterion
QA_EVALUATION_CRITERION_CLEAR_SOLUTION: QAEvaluationCriterion
QA_EVALUATION_CRITERION_ATTITUDE: QAEvaluationCriterion
QA_EVALUATION_CRITERION_NATURAL_SPEECH: QAEvaluationCriterion
QA_EVALUATION_CRITERION_FOLLOW_PROCESS: QAEvaluationCriterion
QA_EVALUATION_CRITERION_NEAT_CLOSING: QAEvaluationCriterion
QA_EVALUATION_CRITICAL_ERROR_UNSPECIFIED: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_WRONG_MONEY_INFO: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_UNCERTAIN_PROMISE: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_INFO_LEAK: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_INSULT_CUSTOMER: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_OUT_OF_PROCESS: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_UNRESOLVED_CLOSING: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_WRONG_TRANSFER: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_UNCHECKED_AI_SUGGESTION: QAEvaluationCriticalError
QA_EVALUATION_CRITICAL_ERROR_ABANDONED_CHAT: QAEvaluationCriticalError
QA_EVALUATION_STATUS_UNSPECIFIED: QAEvaluationStatus
QA_EVALUATION_STATUS_PENDING: QAEvaluationStatus
QA_EVALUATION_STATUS_EVALUATED: QAEvaluationStatus
QA_EVALUATION_STATUS_DISPUTE: QAEvaluationStatus
QA_EVALUATION_RATING_TIER_UNSPECIFIED: QAEvaluationRatingTier
QA_EVALUATION_RATING_TIER_GOOD: QAEvaluationRatingTier
QA_EVALUATION_RATING_TIER_PASS: QAEvaluationRatingTier
QA_EVALUATION_RATING_TIER_NEEDS_IMPROVEMENT: QAEvaluationRatingTier
QA_EVALUATION_RATING_TIER_MUST_MENTOR: QAEvaluationRatingTier
