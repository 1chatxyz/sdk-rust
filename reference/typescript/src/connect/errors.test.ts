import { Code, ConnectError } from "@connectrpc/connect";
import { describe, expect, it } from "vitest";

import { formatConnectError } from "./errors.js";

describe("formatConnectError", () => {
  it("formats ConnectError with code and metadata", () => {
    const err = new ConnectError("unauthenticated", Code.Unauthenticated);
    err.metadata.set("grpc-status-details-bin", "detail");
    const formatted = formatConnectError(err);
    expect(formatted).toMatchObject({
      name: "ConnectError",
      code: Code.Unauthenticated,
      metadata: { "grpc-status-details-bin": "detail" },
    });
    expect(String(formatted.message)).toContain("unauthenticated");
  });

  it("formats generic Error", () => {
    expect(
      formatConnectError(new Error("connection refused")),
    ).toMatchObject({
      name: "Error",
      message: "connection refused",
    });
  });
});
