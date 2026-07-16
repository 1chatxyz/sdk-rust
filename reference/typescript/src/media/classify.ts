export type MediaKind = "image" | "document" | "video";

const IMAGE_EXT = new Set([
  ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".heic", ".heif",
]);
const VIDEO_EXT = new Set([
  ".mp4", ".webm", ".mov", ".mkv", ".m4v",
]);

function extOf(path: string): string {
  const base = path.split(/[\\/]/).pop() ?? path;
  const dot = base.lastIndexOf(".");
  return dot >= 0 ? base.slice(dot).toLowerCase() : "";
}

export function classifyMediaKind(params: {
  path?: string;
  contentType?: string;
}): MediaKind {
  const ct = (params.contentType ?? "").trim().toLowerCase();
  if (ct.startsWith("image/")) return "image";
  if (ct.startsWith("video/")) return "video";
  if (ct) return "document";

  const ext = extOf(params.path ?? "");
  if (IMAGE_EXT.has(ext)) return "image";
  if (VIDEO_EXT.has(ext)) return "video";
  return "document";
}

export function bucketOutboundPaths(
  items: Array<{ path: string; contentType?: string }>,
): { images: string[]; files: string[]; skippedVideos: string[] } {
  const images: string[] = [];
  const files: string[] = [];
  const skippedVideos: string[] = [];
  for (const item of items) {
    const kind = classifyMediaKind(item);
    if (kind === "image") images.push(item.path);
    else if (kind === "video") skippedVideos.push(item.path);
    else files.push(item.path);
  }
  return { images, files, skippedVideos };
}
