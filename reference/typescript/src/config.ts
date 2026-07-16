/** Which chat groups the plugin listens to (not OpenClaw sender security `groupPolicy`). */
export type ActiveGroupsPolicy = "allowlist" | "all";

export type MyConversationGroupConfig = {
  requireMention?: boolean;
};

export type MyConversationChannelConfig = {
  endpoint: string;
  tenantId: string;
  token: string;
  /** Optional myid user id for self-message drop and mention-by-id gating (not sent on the wire). */
  userId?: string;
  /** Optional display username for @mention matching in message text (without leading @). */
  username?: string;
  activeGroupsPolicy: ActiveGroupsPolicy;
  groups: Record<string, MyConversationGroupConfig>;
  /** Public static host for inbound media read fallback (no trailing slash). */
  staticUrl?: string;
  /** Override root for inbound download temp dirs. */
  mediaTempDir?: string;
};

export const myConversationChannelConfigSchema = {
  type: "object",
  additionalProperties: false,
  properties: {
    endpoint: {
      type: "string",
      minLength: 1,
      description: "myconversation gRPC host:port (direct or via gateway)",
    },
    tenantId: {
      type: "string",
      minLength: 1,
      description: "Tenant id attached as x-tenant-id",
    },
    token: {
      type: "string",
      minLength: 1,
      description: "Bearer token sent as Authorization on every RPC",
    },
    userId: {
      type: "string",
      minLength: 1,
      description:
        "Optional service user id for self/mention filtering in the plugin only",
    },
    username: {
      type: "string",
      minLength: 1,
      description:
        "Optional username for @mention text matching when requireMention is true",
    },
    activeGroupsPolicy: {
      type: "string",
      enum: ["allowlist", "all"],
      description:
        "allowlist = only groups listed under groups are active; all = every group the bot belongs to",
    },
    groups: {
      type: "object",
      description: "Per-group activation and mention policy overrides",
      additionalProperties: {
        type: "object",
        additionalProperties: false,
        properties: {
          requireMention: {
            type: "boolean",
            description: "Require an explicit mention before dispatching to OpenClaw",
          },
        },
      },
    },
    staticUrl: {
      type: "string",
      description:
        "Optional public static host for inbound media reads (e.g. https://s.example.com)",
    },
    mediaTempDir: {
      type: "string",
      description: "Optional override for inbound media temp directory root",
    },
  },
  required: ["endpoint", "tenantId", "token"],
} as const;

function assertNonEmptyString(value: unknown, field: string): string {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`myconversation: ${field} must be a non-empty string`);
  }
  return value.trim();
}

function parseOptionalUserId(value: unknown, field: string): string | undefined {
  if (value == null) {
    return undefined;
  }

  if (typeof value === "string") {
    const trimmed = value.trim();
    if (trimmed === "") {
      return undefined;
    }
    value = trimmed;
  }

  const raw =
    typeof value === "number"
      ? // Legacy JSON configs may still store userId as a number.
        Number.isInteger(value) && Number.isFinite(value) && value > 0
        ? String(value)
        : null
      : typeof value === "string"
        ? value
        : null;

  if (raw == null) {
    throw new Error(`myconversation: ${field} must be a positive integer string`);
  }

  if (!/^\d+$/.test(raw)) {
    throw new Error(`myconversation: ${field} must be a positive integer string`);
  }

  const parsed = Number(raw);
  if (!Number.isInteger(parsed) || parsed <= 0 || !Number.isSafeInteger(parsed)) {
    throw new Error(`myconversation: ${field} must be a positive integer string`);
  }

  return raw;
}

/** Compare configured userId (string) with a stream/API numeric id. */
export function userIdMatches(
  configUserId: string,
  candidate: number,
): boolean {
  if (!Number.isFinite(candidate) || candidate <= 0) {
    return false;
  }
  if (String(candidate) === configUserId) {
    return true;
  }
  const parsed = Number(configUserId);
  return Number.isInteger(parsed) && parsed === candidate;
}

export function mentionedUserIdsInclude(
  configUserId: string,
  ids: number[],
): boolean {
  return ids.some((id) => userIdMatches(configUserId, id));
}

function parseActiveGroupsPolicy(
  input: Record<string, unknown>,
): ActiveGroupsPolicy {
  const explicit = input.activeGroupsPolicy;
  if (explicit != null) {
    if (explicit === "allowlist" || explicit === "all") {
      return explicit;
    }
    throw new Error(
      "myconversation: activeGroupsPolicy must be 'allowlist' or 'all'",
    );
  }

  // Legacy field name before OpenClaw security `groupPolicy` collision was fixed.
  const legacy = input.groupPolicy;
  if (legacy === "all") {
    return "all";
  }
  if (legacy == null || legacy === "allowlist") {
    return "allowlist";
  }

  return "allowlist";
}

function parseGroups(
  value: unknown,
): Record<string, MyConversationGroupConfig> {
  if (value == null) {
    return {};
  }
  if (typeof value !== "object" || Array.isArray(value)) {
    throw new Error("myconversation: groups must be an object map");
  }

  const groups: Record<string, MyConversationGroupConfig> = {};
  for (const [groupId, rawGroupConfig] of Object.entries(value)) {
    if (typeof rawGroupConfig !== "object" || rawGroupConfig == null) {
      throw new Error(`myconversation: groups.${groupId} must be an object`);
    }
    const rawRequireMention = (rawGroupConfig as Record<string, unknown>)
      .requireMention;
    const requireMention =
      typeof rawRequireMention === "boolean" ? rawRequireMention : undefined;
    if (rawRequireMention != null && typeof rawRequireMention !== "boolean") {
      throw new Error(
        `myconversation: groups.${groupId}.requireMention must be a boolean`,
      );
    }
    groups[groupId] = { requireMention };
  }

  return groups;
}

function parseOptionalUsername(value: unknown): string | undefined {
  if (value == null) {
    return undefined;
  }
  if (typeof value !== "string") {
    throw new Error("myconversation: username must be a string");
  }
  const normalized = value.trim().replace(/^@+/, "");
  return normalized === "" ? undefined : normalized;
}

function parseOptionalUrl(value: unknown, field: string): string | undefined {
  if (value == null) return undefined;
  if (typeof value !== "string") {
    throw new Error(`myconversation: ${field} must be a string`);
  }
  const trimmed = value.trim().replace(/\/+$/, "");
  return trimmed === "" ? undefined : trimmed;
}

function parseOptionalPath(value: unknown, field: string): string | undefined {
  if (value == null) return undefined;
  if (typeof value !== "string") {
    throw new Error(`myconversation: ${field} must be a string`);
  }
  const trimmed = value.trim();
  return trimmed === "" ? undefined : trimmed;
}

export function parseMyConversationChannelConfig(
  raw: unknown,
): MyConversationChannelConfig {
  if (typeof raw !== "object" || raw == null || Array.isArray(raw)) {
    throw new Error("myconversation: channel config must be an object");
  }

  const input = raw as Record<string, unknown>;
  return {
    endpoint: assertNonEmptyString(input.endpoint, "endpoint"),
    tenantId: assertNonEmptyString(input.tenantId, "tenantId"),
    token: assertNonEmptyString(input.token, "token"),
    userId: parseOptionalUserId(input.userId, "userId"),
    username: parseOptionalUsername(input.username),
    activeGroupsPolicy: parseActiveGroupsPolicy(input),
    groups: parseGroups(input.groups),
    staticUrl: parseOptionalUrl(input.staticUrl, "staticUrl"),
    mediaTempDir: parseOptionalPath(input.mediaTempDir, "mediaTempDir"),
  };
}

export function shouldAcceptGroup(
  config: MyConversationChannelConfig,
  groupId: number | string,
): boolean {
  if (config.activeGroupsPolicy === "all") {
    return true;
  }
  return Object.hasOwn(config.groups, String(groupId));
}

export function shouldRequireMention(
  config: MyConversationChannelConfig,
  groupId: number | string,
): boolean {
  return config.groups[String(groupId)]?.requireMention ?? true;
}
