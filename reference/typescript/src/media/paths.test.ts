import { describe, expect, it } from "vitest";
import {
  isProtectedUploadPath,
  normalizeUploadPath,
  isExistingUploadPath,
  resolveMediaFetchUrl,
} from "./paths.js";

describe("normalizeUploadPath", () => {
  it("strips host from absolute upload URLs", () => {
    expect(
      normalizeUploadPath("https://gw.example.com/api/v1/upload/1/a.png"),
    ).toBe("api/v1/upload/1/a.png");
  });

  it("strips leading slash", () => {
    expect(normalizeUploadPath("/api/v1/upload/1/a.png")).toBe(
      "api/v1/upload/1/a.png",
    );
  });
});

describe("isProtectedUploadPath / isExistingUploadPath", () => {
  it("detects upload paths", () => {
    expect(isProtectedUploadPath("api/v1/upload/1/a.png")).toBe(true);
    expect(isExistingUploadPath("api/v1/upload/1/a.png")).toBe(true);
    expect(isExistingUploadPath("https://cdn.example.com/x.png")).toBe(false);
  });
});

describe("resolveMediaFetchUrl", () => {
  it("builds gateway URL for protected paths", () => {
    expect(
      resolveMediaFetchUrl("api/v1/upload/1/a.png", {
        endpoint: "https://gw.example.com",
      }),
    ).toEqual({
      url: "https://gw.example.com/api/v1/upload/1/a.png",
      auth: true,
    });
  });

  it("prefers staticUrl for protected paths when configured", () => {
    expect(
      resolveMediaFetchUrl("api/v1/upload/1/a.png", {
        endpoint: "https://gw.example.com",
        staticUrl: "https://s.example.com",
      }),
    ).toEqual({
      url: "https://s.example.com/api/v1/upload/1/a.png",
      auth: false,
      fallbackAuthUrl: "https://gw.example.com/api/v1/upload/1/a.png",
    });
  });

  it("passes through external absolute URLs without auth", () => {
    expect(
      resolveMediaFetchUrl("https://cdn.example.com/x.png", {
        endpoint: "https://gw.example.com",
      }),
    ).toEqual({ url: "https://cdn.example.com/x.png", auth: false });
  });
});
