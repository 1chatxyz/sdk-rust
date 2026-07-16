import { createPromiseClient, type PromiseClient } from "@connectrpc/connect";
import { MyEdge } from "@genjutsu/myedge-connect/myedge_connect";
import type { MyConversationChannelConfig } from "../config.js";
import { createMyConversationTransport } from "./transport.js";

export type MyEdgeClient = PromiseClient<typeof MyEdge>;

export function createMyEdgeClient(
  config: MyConversationChannelConfig,
): MyEdgeClient {
  const transport = createMyConversationTransport(config);
  return createPromiseClient(MyEdge, transport);
}
