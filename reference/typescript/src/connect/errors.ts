import { ConnectError } from "@connectrpc/connect";

export function formatConnectError(error: unknown): Record<string, unknown> {
  if (error instanceof ConnectError) {
    const metadata: Record<string, string> = {};
    for (const [key, value] of error.metadata.entries()) {
      metadata[key] = value;
    }
    return {
      name: error.name,
      message: error.message,
      code: error.code,
      rawMessage: error.rawMessage,
      metadata,
    };
  }

  if (error instanceof Error) {
    const out: Record<string, unknown> = {
      name: error.name,
      message: error.message,
    };
    if (error.cause != null) {
      out.cause =
        error.cause instanceof Error
          ? error.cause.message
          : String(error.cause);
    }
    return out;
  }

  return { message: String(error) };
}

export function formatLogMeta(meta: Record<string, unknown>): string {
  return Object.entries(meta)
    .filter(([, value]) => value != null && value !== "")
    .map(([key, value]) => {
      if (typeof value === "object") {
        return `${key}=${JSON.stringify(value)}`;
      }
      return `${key}=${String(value)}`;
    })
    .join(" ");
}

export function formatLogLine(
  message: string,
  meta?: Record<string, unknown>,
): string {
  if (!meta || Object.keys(meta).length === 0) {
    return message;
  }
  const details = formatLogMeta(meta);
  return details ? `${message} ${details}` : message;
}
