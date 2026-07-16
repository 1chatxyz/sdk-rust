export const MAX_ATTACHMENTS = 5;
export const MAX_FILE_BYTES = 20 * 1024 * 1024;

export type InboundAttachmentRef = {
  kind: "image" | "document";
  path: string;
};

export function selectInboundAttachments(params: {
  images?: string[];
  files?: string[];
}): InboundAttachmentRef[] {
  const out: InboundAttachmentRef[] = [];
  for (const path of params.images ?? []) {
    const trimmed = path.trim();
    if (!trimmed) continue;
    out.push({ kind: "image", path: trimmed });
    if (out.length >= MAX_ATTACHMENTS) return out;
  }
  for (const path of params.files ?? []) {
    const trimmed = path.trim();
    if (!trimmed) continue;
    out.push({ kind: "document", path: trimmed });
    if (out.length >= MAX_ATTACHMENTS) return out;
  }
  return out;
}

export function assertOutboundAttachmentLimits(
  items: Array<{ size: number; name: string }>,
): void {
  if (items.length > MAX_ATTACHMENTS) {
    throw new Error(
      `myconversation: at most ${MAX_ATTACHMENTS} attachments allowed (got ${items.length})`,
    );
  }
  for (const item of items) {
    if (item.size > MAX_FILE_BYTES) {
      throw new Error(
        `myconversation: attachment ${item.name} exceeds 20MB limit (${item.size} bytes)`,
      );
    }
  }
}
