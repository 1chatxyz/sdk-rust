const MENTION_TOKEN_RE = /\[\[@([^:\]]+):(\d+)\]\]/g;

export type ParsedMention = { displayName: string; userId: number };

export function parseMentionsFromContent(content: string): ParsedMention[] {
  const mentions: ParsedMention[] = [];

  for (const match of content.matchAll(MENTION_TOKEN_RE)) {
    mentions.push({
      displayName: match[1],
      userId: Number(match[2]),
    });
  }

  return mentions;
}

export function extractMentionedUserIds(content: string): number[] {
  const seen = new Set<number>();
  const ids: number[] = [];

  for (const mention of parseMentionsFromContent(content)) {
    if (seen.has(mention.userId)) {
      continue;
    }
    seen.add(mention.userId);
    ids.push(mention.userId);
  }

  return ids;
}

export function contentMentionsUserId(
  content: string | undefined,
  userId: number | string | undefined,
): boolean {
  if (content === undefined || userId === undefined) {
    return false;
  }

  const normalizedUserId = String(userId);
  return extractMentionedUserIds(content).some(
    (id) => String(id) === normalizedUserId,
  );
}

export function formatMention(
  displayName: string,
  userId: number | string,
): string {
  return `[[@${displayName}:${userId}]]`;
}
