import { describe, expect, it } from "vitest";
import {
  classifyMediaKind,
  bucketOutboundPaths,
} from "./classify.js";

describe("classifyMediaKind", () => {
  it("classifies image MIME and extensions", () => {
    expect(classifyMediaKind({ contentType: "image/png" })).toBe("image");
    expect(classifyMediaKind({ path: "photo.JPG" })).toBe("image");
  });

  it("classifies video as video", () => {
    expect(classifyMediaKind({ contentType: "video/mp4" })).toBe("video");
    expect(classifyMediaKind({ path: "clip.webm" })).toBe("video");
  });

  it("classifies everything else as document", () => {
    expect(classifyMediaKind({ contentType: "application/pdf" })).toBe(
      "document",
    );
    expect(classifyMediaKind({ path: "notes.txt" })).toBe("document");
    expect(classifyMediaKind({ path: "archive.zip" })).toBe("document");
  });
});

describe("bucketOutboundPaths", () => {
  it("splits images and files and skips videos", () => {
    const result = bucketOutboundPaths([
      { path: "a.png", contentType: "image/png" },
      { path: "b.pdf", contentType: "application/pdf" },
      { path: "c.mp4", contentType: "video/mp4" },
    ]);
    expect(result.images).toEqual(["a.png"]);
    expect(result.files).toEqual(["b.pdf"]);
    expect(result.skippedVideos).toEqual(["c.mp4"]);
  });
});
