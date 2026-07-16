import { describe, expect, it } from "vitest";

import { asNumber, getStreamEventMessage, getStreamEventTyping } from "./types.js";

describe("connect type helpers", () => {
  it("converts bigint ids to numbers", () => {
    expect(asNumber(42n)).toBe(42);
    expect(asNumber(undefined)).toBe(0);
  });

  it("extracts message and typing oneof cases", () => {
    const message = { id: 7n, groupId: 16n, senderUserId: 1n };
    const typing = { groupId: 16n, userId: 92n, typing: true };

    expect(
      getStreamEventMessage({
        item: { case: "message", value: message },
      } as never),
    ).toBe(message);
    expect(
      getStreamEventTyping({
        item: { case: "typing", value: typing },
      } as never),
    ).toBe(typing);
    expect(
      getStreamEventMessage({
        item: { case: "ping", value: { serverTimeUnixMs: 1n } },
      } as never),
    ).toBeUndefined();
  });
});
