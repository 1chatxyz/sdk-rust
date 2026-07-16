import { describe, expect, it } from "vitest";
import {
  MAX_ATTACHMENTS,
  MAX_FILE_BYTES,
  selectInboundAttachments,
  assertOutboundAttachmentLimits,
} from "./limits.js";

describe("selectInboundAttachments", () => {
  it("keeps images first then files, capped at MAX_ATTACHMENTS", () => {
    const images = ["i1", "i2", "i3"];
    const files = ["f1", "f2", "f3"];
    const selected = selectInboundAttachments({ images, files });
    expect(MAX_ATTACHMENTS).toBe(5);
    expect(selected).toEqual([
      { kind: "image", path: "i1" },
      { kind: "image", path: "i2" },
      { kind: "image", path: "i3" },
      { kind: "document", path: "f1" },
      { kind: "document", path: "f2" },
    ]);
  });

  it("ignores empty strings", () => {
    expect(
      selectInboundAttachments({ images: ["", "a"], files: ["  "] }),
    ).toEqual([{ kind: "image", path: "a" }]);
  });
});

describe("assertOutboundAttachmentLimits", () => {
  it("throws when more than MAX_ATTACHMENTS", () => {
    expect(() =>
      assertOutboundAttachmentLimits(
        Array.from({ length: 6 }, (_, i) => ({ size: 1, name: `f${i}` })),
      ),
    ).toThrow(/5/);
  });

  it("throws when a file exceeds MAX_FILE_BYTES", () => {
    expect(() =>
      assertOutboundAttachmentLimits([
        { size: MAX_FILE_BYTES + 1, name: "big.pdf" },
      ]),
    ).toThrow(/20/);
  });

  it("allows up to 5 files within size", () => {
    expect(() =>
      assertOutboundAttachmentLimits(
        Array.from({ length: 5 }, (_, i) => ({
          size: MAX_FILE_BYTES,
          name: `f${i}`,
        })),
      ),
    ).not.toThrow();
  });
});
