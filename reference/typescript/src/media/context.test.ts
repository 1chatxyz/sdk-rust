import { describe, expect, it } from "vitest";
import { appendMediaContextLines, buildInboundMediaBody } from "./context.js";

describe("buildInboundMediaBody", () => {
  it("appends success and failure lines after content", () => {
    const body = buildInboundMediaBody({
      content: "hello",
      results: [
        {
          kind: "image",
          originalPath: "api/v1/upload/1/a.png",
          localPath: "/tmp/a.png",
          ok: true,
        },
        {
          kind: "document",
          originalPath: "api/v1/upload/1/b.pdf",
          ok: false,
        },
      ],
    });
    expect(body).toContain("hello");
    expect(body).toContain("[Ảnh: /tmp/a.png]");
    expect(body).toContain("[Tệp không tải được: api/v1/upload/1/b.pdf]");
  });
});
