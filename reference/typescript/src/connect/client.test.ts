import { describe, expect, it, vi } from "vitest";

import { parseMyConversationChannelConfig } from "../config.js";
import { createMyConversationAuthInterceptor } from "./transport.js";

describe("createMyConversationAuthInterceptor", () => {
  it("uses bearer authorization instead of x-user-id", async () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "127.0.0.1:1",
      tenantId: "tenant-abc",
      token: "my-secret-token",
      userId: 92,
    });
    const interceptor = createMyConversationAuthInterceptor(config);
    const next = vi.fn(async (req) => {
      expect(req.header.get("x-tenant-id")).toBe("tenant-abc");
      expect(req.header.get("Authorization")).toBe("Bearer my-secret-token");
      expect(req.header.get("x-user-id")).toBeNull();
      return { message: {} };
    });

    await interceptor(next)({
      service: { typeName: "genjutsu.myconversation.v1.MyConversation" },
      method: { name: "StreamChatGroups" },
      signal: new AbortController().signal,
      header: new Headers(),
      contextValues: {},
      message: {},
    });

    expect(next).toHaveBeenCalledOnce();
  });
});
