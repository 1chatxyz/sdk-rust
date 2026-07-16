import type { Interceptor } from "@connectrpc/connect";
import {
  createGrpcTransport,
  createGrpcWebTransport,
} from "@connectrpc/connect-node";
import { MyConversation } from "@genjutsu/myconversation-connect/myconversation_connect";

import type { MyConversationChannelConfig } from "../config.js";

export function normalizeGrpcBaseUrl(endpoint: string): string {
  const trimmed = endpoint.trim();
  if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
    return trimmed;
  }

  // host:port without scheme — gateway01 is TLS (443); in-cluster listeners use plain HTTP.
  if (trimmed.endsWith(":443")) {
    return `https://${trimmed}`;
  }

  const colon = trimmed.lastIndexOf(":");
  const hasPort = colon > 0 && /^\d+$/.test(trimmed.slice(colon + 1));
  if (hasPort) {
    return `http://${trimmed}`;
  }

  const looksInternal =
    trimmed.includes(".svc.") ||
    trimmed.startsWith("127.") ||
    trimmed === "localhost";
  if (looksInternal) {
    return `http://${trimmed}`;
  }

  return `https://${trimmed}:443`;
}

/** gateway01 (HTTPS / Cloudflare) speaks grpc-web; in-cluster HTTP listeners use native gRPC. */
export function shouldUseGrpcWebTransport(baseUrl: string): boolean {
  return baseUrl.startsWith("https://");
}

export function createMyConversationAuthInterceptor(
  config: Pick<MyConversationChannelConfig, "tenantId" | "token">,
): Interceptor {
  return (next) => async (req) => {
    req.header.set("x-tenant-id", config.tenantId);
    req.header.set("Authorization", `Bearer ${config.token}`);
    return next(req);
  };
}

export function createMyConversationTransport(
  config: MyConversationChannelConfig,
) {
  const baseUrl = normalizeGrpcBaseUrl(config.endpoint);
  const transportOptions = {
    baseUrl,
    interceptors: [createMyConversationAuthInterceptor(config)],
    jsonOptions: {
      ignoreUnknownFields: true,
    },
    binaryOptions: {
      readUnknownFields: true,
    },
  };

  if (shouldUseGrpcWebTransport(baseUrl)) {
    return createGrpcWebTransport({
      ...transportOptions,
      httpVersion: "1.1",
    });
  }

  return createGrpcTransport({
    ...transportOptions,
    httpVersion: "2",
  });
}

export { MyConversation };
