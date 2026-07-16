import { describe, expect, it } from "vitest";

import {
  contentMentionsUserId,
  extractMentionedUserIds,
  formatMention,
  parseMentionsFromContent,
} from "./format.js";

describe("parseMentionsFromContent", () => {
  it("parses a single mention with spaces in display name", () => {
    expect(parseMentionsFromContent("[[@Win Helpers:100]] hello")).toEqual([
      { displayName: "Win Helpers", userId: 100 },
    ]);
  });

  it("parses multiple mentions in one message", () => {
    expect(
      parseMentionsFromContent("[[@Alice:42]] and [[@Bob:99]] please review"),
    ).toEqual([
      { displayName: "Alice", userId: 42 },
      { displayName: "Bob", userId: 99 },
    ]);
  });

  it("ignores malformed tokens without user id", () => {
    expect(parseMentionsFromContent("[[@no-id]] hello [[@Valid:7]]")).toEqual([
      { displayName: "Valid", userId: 7 },
    ]);
  });
});

describe("extractMentionedUserIds", () => {
  it("returns deduped user ids in order of first appearance", () => {
    expect(
      extractMentionedUserIds(
        "[[@Alice:42]] [[@Bob:99]] [[@Alice:42]] [[@Carol:42]]",
      ),
    ).toEqual([42, 99]);
  });
});

describe("contentMentionsUserId", () => {
  it("returns true when content mentions the numeric user id", () => {
    expect(contentMentionsUserId("[[@Win Helpers:100]] ping", 100)).toBe(
      true,
    );
  });

  it("returns true when content mentions the string user id", () => {
    expect(contentMentionsUserId("[[@Win Helpers:100]] ping", "100")).toBe(
      true,
    );
  });

  it("returns false when content does not mention the user id", () => {
    expect(contentMentionsUserId("[[@Other:999]] ping", 100)).toBe(false);
  });

  it("returns false for undefined content or user id", () => {
    expect(contentMentionsUserId(undefined, 100)).toBe(false);
    expect(contentMentionsUserId("[[@Win Helpers:100]]", undefined)).toBe(
      false,
    );
  });
});

describe("formatMention", () => {
  it("formats display name and numeric user id", () => {
    expect(formatMention("Win Helpers", 100)).toBe("[[@Win Helpers:100]]");
  });

  it("formats display name and string user id", () => {
    expect(formatMention("Alice", "42")).toBe("[[@Alice:42]]");
  });
});
