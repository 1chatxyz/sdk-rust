import { describe, expect, it, vi, afterEach } from "vitest";
import { mkdtemp, rm, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { downloadInboundAttachments, cleanupTempDir } from "./download.js";

afterEach(async () => {
  // tests create dirs under os.tmpdir — cleaned in each test finally
});

describe("downloadInboundAttachments", () => {
  it("writes successful downloads and skips oversize", async () => {
    const root = await mkdtemp(join(tmpdir(), "myconv-dl-"));
    try {
      const fetcher = vi.fn(async (url: string) => {
        if (url.includes("big")) {
          return {
            ok: true,
            headers: { get: (h: string) => (h === "content-length" ? String(21 * 1024 * 1024) : null) },
            arrayBuffer: async () => new ArrayBuffer(0),
          };
        }
        return {
          ok: true,
          headers: { get: () => null },
          arrayBuffer: async () => Uint8Array.from([1, 2, 3]).buffer,
        };
      });

      const { results } = await downloadInboundAttachments({
        attachments: [
          { kind: "image", path: "api/v1/upload/1/ok.png" },
          { kind: "document", path: "api/v1/upload/1/big.pdf" },
        ],
        account: {
          endpoint: "https://gw.example.com",
          tenantId: "t",
          token: "tok",
        },
        tempRoot: root,
        messageId: "99",
        fetcher: fetcher as never,
      });

      expect(results[0]?.ok).toBe(true);
      expect(results[0]?.localPath).toBeTruthy();
      const bytes = await readFile(results[0]!.localPath!);
      expect(bytes.equals(Buffer.from([1, 2, 3]))).toBe(true);
      expect(results[1]?.ok).toBe(false);
    } finally {
      await cleanupTempDir(root);
    }
  });
});
