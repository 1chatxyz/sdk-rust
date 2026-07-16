import { describe, expect, it, vi } from "vitest";
import { prepareOutboundMedia } from "./outbound.js";

describe("prepareOutboundMedia", () => {
  it("passes through existing upload paths without upload", async () => {
    const upload = vi.fn();
    const result = await prepareOutboundMedia({
      userId: "92",
      mediaUrls: ["api/v1/upload/92/a.png", "api/v1/upload/92/b.pdf"],
      uploadFile: upload,
      readLocalFile: async () => Buffer.from(""),
    });
    expect(upload).not.toHaveBeenCalled();
    expect(result.images).toEqual(["api/v1/upload/92/a.png"]);
    expect(result.files).toEqual(["api/v1/upload/92/b.pdf"]);
    expect(result.skippedVideos).toEqual([]);
  });

  it("uploads local files and buckets by MIME", async () => {
    const upload = vi
      .fn()
      .mockResolvedValueOnce("api/v1/upload/92/new.png")
      .mockResolvedValueOnce("api/v1/upload/92/new.pdf");
    const result = await prepareOutboundMedia({
      userId: "92",
      mediaUrls: ["/tmp/a.png", "/tmp/b.pdf"],
      uploadFile: upload,
      readLocalFile: async (p) =>
        Buffer.from(p.endsWith(".png") ? "img" : "pdf"),
      contentTypeForPath: (p) =>
        p.endsWith(".png") ? "image/png" : "application/pdf",
    });
    expect(upload).toHaveBeenCalledTimes(2);
    expect(result.images).toEqual(["api/v1/upload/92/new.png"]);
    expect(result.files).toEqual(["api/v1/upload/92/new.pdf"]);
  });

  it("skips videos and rejects >5 attachments", async () => {
    await expect(
      prepareOutboundMedia({
        userId: "92",
        mediaUrls: ["a", "b", "c", "d", "e", "f"],
        uploadFile: async () => "x",
        readLocalFile: async () => Buffer.from("x"),
      }),
    ).rejects.toThrow(/5/);
  });

  it("does not double-upload when mediaUrls and mediaUrl both set", async () => {
    const upload = vi.fn().mockResolvedValue("api/v1/upload/92/once.txt");
    const result = await prepareOutboundMedia({
      userId: "92",
      mediaUrls: ["/tmp/answer.txt"],
      mediaUrl: "/tmp/answer.txt",
      uploadFile: upload,
      readLocalFile: async () => Buffer.from("one plus one is two"),
      contentTypeForPath: () => "text/plain",
    });
    expect(upload).toHaveBeenCalledTimes(1);
    expect(result.files).toEqual(["api/v1/upload/92/once.txt"]);
  });
});
