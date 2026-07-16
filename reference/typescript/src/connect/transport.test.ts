import { describe, expect, it } from "vitest";

import {
  normalizeGrpcBaseUrl,
  shouldUseGrpcWebTransport,
} from "./transport.js";

describe("normalizeGrpcBaseUrl", () => {
  it("keeps explicit https URLs", () => {
    expect(normalizeGrpcBaseUrl("https://gw01.trolybehai.com")).toBe(
      "https://gw01.trolybehai.com",
    );
  });

  it("keeps explicit http URLs", () => {
    expect(normalizeGrpcBaseUrl("http://mc:8080")).toBe("http://mc:8080");
  });

  it("uses https for :443 host:port", () => {
    expect(normalizeGrpcBaseUrl("gateway01.example.com:443")).toBe(
      "https://gateway01.example.com:443",
    );
  });

  it("defaults public hostnames to https on 443", () => {
    expect(normalizeGrpcBaseUrl("gw01.trolybehai.com")).toBe(
      "https://gw01.trolybehai.com:443",
    );
  });

  it("uses http for non-443 ports", () => {
    expect(normalizeGrpcBaseUrl("mc:8080")).toBe("http://mc:8080");
    expect(
      normalizeGrpcBaseUrl("myconversation.myconversation.svc.cluster.local:8080"),
    ).toBe("http://myconversation.myconversation.svc.cluster.local:8080");
  });
});

describe("shouldUseGrpcWebTransport", () => {
  it("uses grpc-web for https gateway endpoints", () => {
    expect(shouldUseGrpcWebTransport("https://gw01.trolybehai.com")).toBe(true);
  });

  it("uses native grpc for in-cluster http endpoints", () => {
    expect(
      shouldUseGrpcWebTransport(
        "http://myconversation.myconversation.svc.cluster.local:8080",
      ),
    ).toBe(false);
    expect(shouldUseGrpcWebTransport("http://mc:8080")).toBe(false);
  });
});
