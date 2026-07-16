import { createPromiseClient, type PromiseClient } from "@connectrpc/connect";
import {
  SendChatGroupMessageRequest,
  SignalChatGroupTypingRequest,
  StreamChatGroupsRequest,
} from "@genjutsu/myconversation-connect/myconversation_pb";

import type { MyConversationChannelConfig } from "../config.js";
import {
  createMyConversationTransport,
  MyConversation,
} from "./transport.js";
import type { SendChatGroupMessageReply } from "./types.js";
import { asBigInt } from "./types.js";

export type MyConversationClient = PromiseClient<typeof MyConversation>;

export class MyConversationConnectClient {
  private readonly client: MyConversationClient;
  private readonly transport: ReturnType<typeof createMyConversationTransport>;

  constructor(private readonly config: MyConversationChannelConfig) {
    this.transport = createMyConversationTransport(config);
    this.client = createPromiseClient(MyConversation, this.transport);
  }

  close(): void {
    // Connect transports are stateless; stream cancellation uses AbortSignal.
  }

  streamChatGroups(
    request: { resumeAfterMessageId?: bigint | number },
    signal?: AbortSignal,
  ) {
    return this.client.streamChatGroups(
      new StreamChatGroupsRequest({
        resumeAfterMessageId: asBigInt(request.resumeAfterMessageId),
      }),
      { signal },
    );
  }

  async signalChatGroupTyping(request: {
    groupId: bigint | number;
    typing: boolean;
  }): Promise<Record<string, never>> {
    await this.client.signalChatGroupTyping(
      new SignalChatGroupTypingRequest({
        groupId: asBigInt(request.groupId),
        typing: request.typing,
      }),
    );
    return {};
  }

  async sendChatGroupMessage(request: {
    groupId: bigint | number;
    content: string;
    images?: string[];
    videos?: string[];
    files?: string[];
    mentionedUserIds?: Array<bigint | number>;
    clientMessageId?: string;
  }): Promise<SendChatGroupMessageReply> {
    return this.client.sendChatGroupMessage(
      new SendChatGroupMessageRequest({
        groupId: asBigInt(request.groupId),
        content: request.content,
        images: request.images ?? [],
        videos: request.videos ?? [],
        files: request.files ?? [],
        mentionedUserIds: (request.mentionedUserIds ?? []).map(asBigInt),
        clientMessageId: request.clientMessageId,
      }),
    );
  }
}

/** @deprecated Use MyConversationConnectClient */
export { MyConversationConnectClient as MyConversationGrpcClient };
