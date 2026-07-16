import type { InboundAttachmentRef } from "./limits.js";

export type InboundDownloadResult = InboundAttachmentRef & {
  ok: boolean;
  localPath?: string;
  originalPath: string;
  error?: string;
};

export function appendMediaContextLines(
  results: InboundDownloadResult[],
): string[] {
  const lines: string[] = [];
  for (const r of results) {
    if (r.ok && r.localPath) {
      lines.push(
        r.kind === "image"
          ? `[Ảnh: ${r.localPath}]`
          : `[Tệp: ${r.localPath}]`,
      );
    } else {
      lines.push(
        r.kind === "image"
          ? `[Ảnh không tải được: ${r.originalPath}]`
          : `[Tệp không tải được: ${r.originalPath}]`,
      );
    }
  }
  return lines;
}

export function buildInboundMediaBody(params: {
  content: string;
  results: InboundDownloadResult[];
}): string {
  const lines = appendMediaContextLines(params.results);
  if (lines.length === 0) return params.content;
  if (!params.content.trim()) return lines.join("\n");
  return `${params.content}\n${lines.join("\n")}`;
}

export function successfulLocalPaths(
  results: InboundDownloadResult[],
): string[] {
  return results
    .filter((r) => r.ok && r.localPath)
    .map((r) => r.localPath!);
}
