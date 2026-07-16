import { randomUUID } from "node:crypto";
import { mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { basename, join } from "node:path";
import type { InboundDownloadResult } from "./context.js";
import { MAX_FILE_BYTES, type InboundAttachmentRef } from "./limits.js";
import { resolveMediaFetchUrl } from "./paths.js";

export type MediaDownloadAccount = {
  endpoint: string;
  tenantId: string;
  token: string;
  staticUrl?: string;
  mediaTempDir?: string;
};

type FetchResponse = {
  ok: boolean;
  headers: { get(name: string): string | null };
  arrayBuffer(): Promise<ArrayBuffer>;
};

type Fetcher = (
  url: string,
  init?: RequestInit,
) => Promise<FetchResponse>;

export function defaultMediaTempRoot(account: Pick<MediaDownloadAccount, "mediaTempDir">): string {
  return account.mediaTempDir ?? join(tmpdir(), "openclaw-myconversation");
}

function safeBasename(path: string): string {
  const withoutQuery = path.split("?")[0] ?? path;
  const name = basename(withoutQuery);
  if (!name || name === "." || name === ".." || name.includes("..")) {
    throw new Error(`myconversation: unsafe attachment filename: ${path}`);
  }
  return name;
}

function oversize(contentLength: string | null, bufferLength?: number): boolean {
  if (contentLength != null) {
    const len = Number(contentLength);
    if (!Number.isNaN(len) && len > MAX_FILE_BYTES) return true;
  }
  if (bufferLength != null && bufferLength > MAX_FILE_BYTES) return true;
  return false;
}

async function fetchAttachment(
  target: ReturnType<typeof resolveMediaFetchUrl>,
  account: MediaDownloadAccount,
  fetcher: Fetcher,
): Promise<{ ok: true; buffer: Buffer } | { ok: false; error: string }> {
  const doFetch = async (url: string, auth: boolean) => {
    const headers: Record<string, string> = {};
    if (auth) {
      headers.Authorization = `Bearer ${account.token}`;
      headers["x-tenant-id"] = account.tenantId;
    }
    return fetcher(url, { headers });
  };

  let res = await doFetch(target.url, target.auth);

  if (!res.ok && !target.auth && target.fallbackAuthUrl) {
    res = await doFetch(target.fallbackAuthUrl, true);
  }

  if (!res.ok) {
    return { ok: false, error: "download failed" };
  }

  const contentLength = res.headers.get("content-length");
  if (oversize(contentLength)) {
    return { ok: false, error: "file exceeds 20MB limit" };
  }

  const arrayBuffer = await res.arrayBuffer();
  if (oversize(contentLength, arrayBuffer.byteLength)) {
    return { ok: false, error: "file exceeds 20MB limit" };
  }

  return { ok: true, buffer: Buffer.from(arrayBuffer) };
}

export async function downloadInboundAttachments(params: {
  attachments: InboundAttachmentRef[];
  account: MediaDownloadAccount;
  tempRoot: string;
  messageId: string;
  fetcher?: Fetcher;
}): Promise<{ results: InboundDownloadResult[]; tempDir: string }> {
  const fetcher = params.fetcher ?? (globalThis.fetch.bind(globalThis) as Fetcher);
  const dir = join(params.tempRoot, `${params.messageId}-${randomUUID()}`);
  await mkdir(dir, { recursive: true });

  const results: InboundDownloadResult[] = [];

  for (const attachment of params.attachments) {
    const originalPath = attachment.path;
    const base: InboundDownloadResult = {
      kind: attachment.kind,
      path: attachment.path,
      originalPath,
      ok: false,
    };

    try {
      const target = resolveMediaFetchUrl(originalPath, {
        endpoint: params.account.endpoint,
        staticUrl: params.account.staticUrl,
      });

      const fetched = await fetchAttachment(target, params.account, fetcher);
      if (!fetched.ok) {
        results.push({ ...base, error: fetched.error });
        continue;
      }

      const fileName = safeBasename(originalPath);
      const localPath = join(dir, fileName);
      await writeFile(localPath, fetched.buffer);
      results.push({ ...base, ok: true, localPath });
    } catch (error) {
      results.push({
        ...base,
        error: error instanceof Error ? error.message : String(error),
      });
    }
  }

  return { results, tempDir: dir };
}

export async function cleanupTempDir(dir: string): Promise<void> {
  await rm(dir, { recursive: true, force: true });
}
