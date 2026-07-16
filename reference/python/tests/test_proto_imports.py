from myconversation.proto.myconversation_pb2 import ChatGroupMessageInfo
from myconversation.proto.myconversation_pb2_grpc import MyConversationStub
from myconversation.proto.myconversation_connect import MyConversationClient


def test_stub_modules_importable():
    assert MyConversationStub is not None
    assert MyConversationClient is not None


def test_chat_group_message_info_has_sender_username_not_display_name():
    msg = ChatGroupMessageInfo(
        id=1,
        group_id=42,
        sender_user_id=100,
        sender_username="alice",
        content="hi",
    )
    assert msg.sender_username == "alice"
    assert not hasattr(msg, "sender_display_name")
