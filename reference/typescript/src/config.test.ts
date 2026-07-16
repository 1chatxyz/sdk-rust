import { describe, expect, it } from "vitest";

import {
  parseMyConversationChannelConfig,
  shouldAcceptGroup,
  shouldRequireMention,
  userIdMatches,
} from "./config.js";

describe("parseMyConversationChannelConfig", () => {
  it("parses the requested config shape", () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "myconversation.myconversation.svc.cluster.local:8080",
      tenantId: "tenant-abc",
      token: "secret-token",
      userId: "123456789",
      activeGroupsPolicy: "allowlist",
      groups: {
        "42": { requireMention: true },
      },
    });

    expect(config.endpoint).toBe(
      "myconversation.myconversation.svc.cluster.local:8080",
    );
    expect(config.tenantId).toBe("tenant-abc");
    expect(config.token).toBe("secret-token");
    expect(config.userId).toBe("123456789");
    expect(config.activeGroupsPolicy).toBe("allowlist");
    expect(config.groups["42"]?.requireMention).toBe(true);
  });

  it("parses optional username without leading @", () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "mc:8080",
      tenantId: "tenant-abc",
      token: "token",
      username: "@OpenClaw",
    });

    expect(config.username).toBe("OpenClaw");
  });

  it("accepts legacy numeric userId and normalizes to string", () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "mc:8080",
      tenantId: "tenant-abc",
      token: "token",
      userId: 92,
    });

    expect(config.userId).toBe("92");
  });

  it("defaults group policy and requireMention when omitted", () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "mc:8080",
      tenantId: "tenant-abc",
      token: "token",
    });

    expect(config.activeGroupsPolicy).toBe("allowlist");
    expect(config.userId).toBeUndefined();
    expect(shouldRequireMention(config, 999)).toBe(true);
  });

  it("parses optional staticUrl and mediaTempDir", () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "https://gw.example.com",
      tenantId: "tenant-abc",
      token: "token",
      staticUrl: "https://s.example.com/",
      mediaTempDir: "/tmp/myconv-media",
    });
    expect(config.staticUrl).toBe("https://s.example.com");
    expect(config.mediaTempDir).toBe("/tmp/myconv-media");
  });

  it("defaults staticUrl and mediaTempDir to undefined", () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "mc:8080",
      tenantId: "tenant-abc",
      token: "token",
    });
    expect(config.staticUrl).toBeUndefined();
    expect(config.mediaTempDir).toBeUndefined();
  });
});

describe("userIdMatches", () => {
  it("matches numeric stream ids against string config", () => {
    expect(userIdMatches("92", 92)).toBe(true);
    expect(userIdMatches("123", 456)).toBe(false);
  });
});

describe("group policy helpers", () => {
  it("accepts only listed groups when allowlist is enabled", () => {
    const config = parseMyConversationChannelConfig({
      endpoint: "mc:8080",
      tenantId: "tenant-abc",
      token: "token",
      activeGroupsPolicy: "allowlist",
      groups: {
        "42": { requireMention: false },
      },
    });

    expect(shouldAcceptGroup(config, 42)).toBe(true);
    expect(shouldAcceptGroup(config, 77)).toBe(false);
  });

  it("rejects malformed configuration", () => {
    expect(() =>
      parseMyConversationChannelConfig({
        tenantId: "tenant-abc",
        token: "token",
      }),
    ).toThrow(/endpoint/i);
  });
});
