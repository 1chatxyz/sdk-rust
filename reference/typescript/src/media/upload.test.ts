import { describe, expect, it, vi } from "vitest";
import { uploadBuffer } from "./upload.js";

describe("uploadBuffer", () => {
  it("creates multipart, puts parts, completes, returns object key", async () => {
    const put = vi.fn().mockResolvedValue('"etag-1"');
    const edge = {
      createMultipartUpload: vi.fn().mockResolvedValue({
        uploadId: "up-1",
        objectKey: "api/v1/upload/92/1_uuid.png",
        parts: [{ partNumber: 1, url: "https://r2/part1" }],
      }),
      completeMultipartUpload: vi.fn().mockResolvedValue({}),
      abortMultipartUpload: vi.fn().mockResolvedValue({}),
      putPart: put,
    };

    const key = await uploadBuffer({
      edge: edge as never,
      userId: "92",
      fileName: "photo.png",
      contentType: "image/png",
      body: Buffer.from("hello"),
      putPart: async (url, body) => put(url, body),
    });

    expect(key).toBe("api/v1/upload/92/1_uuid.png");
    expect(edge.createMultipartUpload).toHaveBeenCalledOnce();
    expect(edge.completeMultipartUpload).toHaveBeenCalledOnce();
    expect(put).toHaveBeenCalledOnce();
  });

  it("aborts multipart on failure", async () => {
    const edge = {
      createMultipartUpload: vi.fn().mockResolvedValue({
        uploadId: "up-1",
        objectKey: "api/v1/upload/92/x.png",
        parts: [{ partNumber: 1, url: "https://r2/part1" }],
      }),
      completeMultipartUpload: vi.fn(),
      abortMultipartUpload: vi.fn().mockResolvedValue({}),
    };

    await expect(
      uploadBuffer({
        edge: edge as never,
        userId: "92",
        fileName: "photo.png",
        contentType: "image/png",
        body: Buffer.from("hello"),
        putPart: async () => {
          throw new Error("put failed");
        },
      }),
    ).rejects.toThrow("put failed");

    expect(edge.abortMultipartUpload).toHaveBeenCalledWith({
      objectKey: "api/v1/upload/92/x.png",
      uploadId: "up-1",
    });
  });
});
