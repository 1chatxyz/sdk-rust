import { basename } from "node:path";
import { classifyMediaKind } from "./classify.js";
import {
  assertOutboundAttachmentLimits,
  MAX_FILE_BYTES,
} from "./limits.js";
import { isExistingUploadPath, normalizeUploadPath } from "./paths.js";

export type PrepareOutboundMediaParams = {
  userId: string;
  mediaUrls?: string[];
  mediaUrl?: string;
  uploadFile: (args: {
    fileName: string;
    contentType: string;
    body: Buffer;
  }) => Promise<string>;
  readLocalFile: (path: string) => Promise<Buffer>;
  contentTypeForPath?: (path: string) => string | undefined;
  fetchHttp?: (url: string) => Promise<{
    ok: boolean;
    arrayBuffer: () => Promise<ArrayBuffer>;
    headers: { get: (n: string) => string | null };
  }>;
};

export type PrepareOutboundMediaResult = {
  images: string[];
  files: string[];
  skippedVideos: string[];
};

type HttpResponse = NonNullable<PrepareOutboundMediaParams["fetchHttp"]> extends (
  url: string,
) => Promise<infer R>
  ? R
  : never;

function isHttpUrl(url: string): boolean {
  return /^https?:\/\//i.test(url);
}

function safeBasename(path: string): string {
  const withoutQuery = path.split("?")[0] ?? path;
  return basename(withoutQuery);
}

function defaultContentType(path: string): string {
  const kind = classifyMediaKind({ path });
  if (kind === "image") return "image/png";
  if (kind === "video") return "video/mp4";
  return "application/octet-stream";
}

function resolveContentType(path: string, contentTypeForPath?: (path: string) => string | undefined, headerType?: string | null): string {
  return (
    contentTypeForPath?.(path) ??
    headerType?.split(";")[0]?.trim() ??
    defaultContentType(path)
  );
}

function bucketPath(
  path: string,
  images: string[],
  files: string[],
  skippedVideos: string[],
  contentType?: string,
): void {
  const kind = classifyMediaKind({ path, contentType });
  if (kind === "image") images.push(path);
  else if (kind === "video") skippedVideos.push(path);
  else files.push(path);
}

function assertSize(name: string, size: number): void {
  assertOutboundAttachmentLimits([{ size, name }]);
}

function oversizeContentLength(contentLength: string | null): boolean {
  if (contentLength == null) return false;
  const len = Number(contentLength);
  return !Number.isNaN(len) && len > MAX_FILE_BYTES;
}

/** Prefer mediaUrls[]; fall back to legacy mediaUrl — never concat both (OpenClaw sets both). */
export function resolveOutboundMediaUrlList(params: {
  mediaUrls?: string[];
  mediaUrl?: string;
}): string[] {
  const fromList = (params.mediaUrls ?? [])
    .map((u) => u.trim())
    .filter(Boolean);
  if (fromList.length > 0) {
    return fromList;
  }
  const single = params.mediaUrl?.trim();
  return single ? [single] : [];
}

export async function prepareOutboundMedia(
  params: PrepareOutboundMediaParams,
): Promise<PrepareOutboundMediaResult> {
  const urls = resolveOutboundMediaUrlList(params);

  if (urls.length === 0) {
    return { images: [], files: [], skippedVideos: [] };
  }

  if (!params.userId?.trim()) {
    throw new Error("myconversation: userId is required for media uploads");
  }

  assertOutboundAttachmentLimits(
    urls.map((u) => ({ size: 0, name: safeBasename(u) })),
  );

  const images: string[] = [];
  const files: string[] = [];
  const skippedVideos: string[] = [];

  for (const url of urls) {
    if (isExistingUploadPath(url)) {
      const path = normalizeUploadPath(url);
      bucketPath(path, images, files, skippedVideos);
      continue;
    }

    if (classifyMediaKind({ path: url }) === "video") {
      skippedVideos.push(url);
      continue;
    }

    if (isHttpUrl(url)) {
      const fetcher = params.fetchHttp ?? (globalThis.fetch.bind(globalThis) as (url: string) => Promise<HttpResponse>);
      const res = await fetcher(url);
      if (!res.ok) {
        throw new Error(`myconversation: failed to fetch ${url}`);
      }

      const fileName = safeBasename(url);
      if (oversizeContentLength(res.headers.get("content-length"))) {
        assertSize(fileName, MAX_FILE_BYTES + 1);
      }

      const body = Buffer.from(await res.arrayBuffer());
      assertSize(fileName, body.length);

      const contentType = resolveContentType(
        url,
        params.contentTypeForPath,
        res.headers.get("content-type"),
      );

      if (classifyMediaKind({ path: url, contentType }) === "video") {
        skippedVideos.push(url);
        continue;
      }

      const uploaded = await params.uploadFile({
        fileName,
        contentType,
        body,
      });
      bucketPath(uploaded, images, files, skippedVideos, contentType);
      continue;
    }

    const fileName = safeBasename(url);
    const body = await params.readLocalFile(url);
    assertSize(fileName, body.length);

    const contentType = resolveContentType(url, params.contentTypeForPath);
    if (classifyMediaKind({ path: url, contentType }) === "video") {
      skippedVideos.push(url);
      continue;
    }

    const uploaded = await params.uploadFile({
      fileName,
      contentType,
      body,
    });
    bucketPath(uploaded, images, files, skippedVideos, contentType);
  }

  return { images, files, skippedVideos };
}
