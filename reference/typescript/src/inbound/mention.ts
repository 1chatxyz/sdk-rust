import {
  type MyConversationChannelConfig,
  mentionedUserIdsInclude,
  shouldAcceptGroup,
  shouldRequireMention,
  userIdMatches,
} from "../config.js";

const MENTION_TOKEN_RE = /\[\[@([^:\]]+):(\d+)\]\]/g;

export type InboundMentionCandidate = {
  groupId: number;
  senderUserId: number;
  content?: string;
  mentionedUserIds?: number[];
};

/** @deprecated Username matching uses config.username directly. */
export type MentionContext = {
  username?: string;
};

export function normalizeMentionedUserIds(mentionedUserIds: number[]): number[] {
  const normalized = new Set<number>();
  for (const id of mentionedUserIds) {
    if (Number.isFinite(id) && id > 0) {
      normalized.add(id);
    }
  }
  return [...normalized];
}

export function stripMentionTokensForCommandDetection(content: string): string {
  return content.replace(MENTION_TOKEN_RE, " ").replace(/\s+/g, " ").trim();
}

export function detectInboundControlCommand(params: {
  rawBody: string;
  cfg: unknown;
  hasControlCommand: (body: string, cfg: unknown) => boolean;
}): boolean {
  const trimmed = params.rawBody.trim();
  if (!trimmed) {
    return false;
  }
  if (params.hasControlCommand(trimmed, params.cfg)) {
    return true;
  }

  const withoutMentions = stripMentionTokensForCommandDetection(trimmed);
  if (withoutMentions && withoutMentions !== trimmed) {
    return params.hasControlCommand(withoutMentions, params.cfg);
  }

  return false;
}

export type MentionGateDebug = {
  requireMention: boolean;
  wasMentioned: boolean;
  mentionMatch: string;
  mentionedUserIds: number[];
  botUserId?: string;
  hasControlCommand: boolean;
  allowTextCommands: boolean;
  commandAuthorized: boolean;
};

export function contentContainsBotUsername(
  content: string | undefined,
  config: MyConversationChannelConfig,
): boolean {
  const username = config.username?.trim();
  if (!username || content == null || content === "") {
    return false;
  }
  return content.includes(username);
}

export function isBotMentionedByUserIds(
  config: MyConversationChannelConfig,
  mentionedUserIds: number[],
  content?: string,
): boolean {
  return describeBotMentionMatch(config, mentionedUserIds, content)
    .wasMentioned;
}

export function describeBotMentionMatch(
  config: MyConversationChannelConfig,
  mentionedUserIds: number[],
  content?: string,
): { wasMentioned: boolean; match: string } {
  if (
    config.userId != null &&
    mentionedUserIdsInclude(config.userId, mentionedUserIds)
  ) {
    return { wasMentioned: true, match: "mentioned-user-ids" };
  }

  if (contentContainsBotUsername(content, config)) {
    return { wasMentioned: true, match: "username-in-content" };
  }

  return { wasMentioned: false, match: "none" };
}

/** Self-message and allowlist checks only — mention gating is handled separately. */
export function shouldAcceptGroupMessage(
  candidate: InboundMentionCandidate,
  config: MyConversationChannelConfig,
): boolean {
  if (
    config.userId != null &&
    userIdMatches(config.userId, candidate.senderUserId)
  ) {
    return false;
  }

  return shouldAcceptGroup(config, candidate.groupId);
}

export function resolveMyConversationMentionGate(params: {
  account: MyConversationChannelConfig;
  groupId: number;
  rawBody: string;
  mentionedUserIds: number[];
  allowTextCommands: boolean;
  hasControlCommand: boolean;
  commandAuthorized: boolean;
}): {
  shouldSkip: boolean;
  reason: string;
  effectiveWasMentioned: boolean;
  debug: MentionGateDebug;
} {
  const mentionedUserIds = normalizeMentionedUserIds(params.mentionedUserIds);
  const requireMention = shouldRequireMention(params.account, params.groupId);
  const mentionMatch = describeBotMentionMatch(
    params.account,
    mentionedUserIds,
    params.rawBody,
  );
  const debug: MentionGateDebug = {
    requireMention,
    wasMentioned: mentionMatch.wasMentioned,
    mentionMatch: mentionMatch.match,
    mentionedUserIds,
    botUserId: params.account.userId,
    hasControlCommand: params.hasControlCommand,
    allowTextCommands: params.allowTextCommands,
    commandAuthorized: params.commandAuthorized,
  };

  if (!requireMention) {
    return {
      shouldSkip: false,
      reason: "mention-not-required",
      effectiveWasMentioned: mentionMatch.wasMentioned,
      debug,
    };
  }

  if (mentionMatch.wasMentioned) {
    return {
      shouldSkip: false,
      reason: "mentioned",
      effectiveWasMentioned: true,
      debug,
    };
  }

  if (
    params.hasControlCommand &&
    params.allowTextCommands &&
    params.commandAuthorized
  ) {
    return {
      shouldSkip: false,
      reason: "authorized-command",
      effectiveWasMentioned: true,
      debug,
    };
  }

  return {
    shouldSkip: true,
    reason: "missing-mention",
    effectiveWasMentioned: false,
    debug,
  };
}

/** @deprecated Use shouldAcceptGroupMessage + resolveMyConversationMentionGate. */
export function shouldHandleInboundMessage(
  candidate: InboundMentionCandidate,
  config: MyConversationChannelConfig,
  _context: MentionContext = {},
): boolean {
  if (!shouldAcceptGroupMessage(candidate, config)) {
    return false;
  }

  if (!shouldRequireMention(config, candidate.groupId)) {
    return true;
  }

  return isBotMentionedByUserIds(
    config,
    normalizeMentionedUserIds(candidate.mentionedUserIds ?? []),
    candidate.content,
  );
}

export function wasInboundBotMentioned(
  rawBody: string | undefined,
  mentionedUserIds: number[] | undefined,
  config: MyConversationChannelConfig,
  _context: MentionContext = {},
): boolean {
  return isBotMentionedByUserIds(
    config,
    normalizeMentionedUserIds(mentionedUserIds ?? []),
    rawBody,
  );
}
