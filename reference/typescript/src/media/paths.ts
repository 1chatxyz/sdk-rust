import { normalizeGrpcBaseUrl } from "../connect/transport.js";

export function normalizeUploadPath(pathOrUrl: string): string {
  const trimmed = pathOrUrl.trim();
  if (!trimmed) return "";
  if (/^https?:\/\//i.test(trimmed)) {
    try {
      const url = new URL(trimmed);
      return `${url.pathname.replace(/^\//, "")}${url.search}`;
    } catch {
      return trimmed;
    }
  }
  return trimmed.replace(/^\//, "");
}

export function isProtectedUploadPath(pathOrUrl: string): boolean {
  const path = normalizeUploadPath(pathOrUrl);
  return path.startsWith("api/v1/upload/") || path.startsWith("upload/");
}

export function isExistingUploadPath(pathOrUrl: string): boolean {
  return isProtectedUploadPath(pathOrUrl);
}

export type MediaFetchTarget = {
  url: string;
  auth: boolean;
  fallbackAuthUrl?: string;
};

export function resolveMediaFetchUrl(
  pathOrUrl: string,
  opts: { endpoint: string; staticUrl?: string },
): MediaFetchTarget {
  const trimmed = pathOrUrl.trim();
  if (!trimmed) {
    throw new Error("myconversation: empty media path");
  }

  if (/^https?:\/\//i.test(trimmed) && !isProtectedUploadPath(trimmed)) {
    return { url: trimmed, auth: false };
  }

  const path = normalizeUploadPath(trimmed);
  const base = normalizeGrpcBaseUrl(opts.endpoint).replace(/\/+$/, "");
  const gatewayUrl = `${base}/${path}`;

  const staticBase = opts.staticUrl?.replace(/\/+$/, "");
  if (staticBase && isProtectedUploadPath(path)) {
    return {
      url: `${staticBase}/${path}`,
      auth: false,
      fallbackAuthUrl: gatewayUrl,
    };
  }

  return { url: gatewayUrl, auth: true };
}
