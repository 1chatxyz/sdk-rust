import { randomUUID } from "node:crypto";

export const MULTIPART_PART_SIZE = 10 * 1024 * 1024;
export const MULTIPART_PART_CONCURRENCY = 4;

export type MyEdgeUploadApi = {
  createMultipartUpload(req: {
    fileName: string;
    contentType: string;
    objectKey: string;
    partCount: number;
  }): Promise<{
    uploadId: string;
    objectKey?: string;
    parts: Array<{ partNumber: number; url: string }>;
  }>;
  completeMultipartUpload(req: {
    objectKey: string;
    uploadId: string;
    parts: Array<{ partNumber: number; etag: string }>;
  }): Promise<unknown>;
  abortMultipartUpload(req: {
    objectKey: string;
    uploadId: string;
  }): Promise<unknown>;
  presignUploadParts?(req: {
    objectKey: string;
    uploadId: string;
    partNumbers: number[];
  }): Promise<{ parts: Array<{ partNumber: number; url: string }> }>;
};

export function buildObjectKey(userId: string, fileName: string): string {
  const ext = fileName.includes(".")
    ? fileName.slice(fileName.lastIndexOf(".") + 1)
    : "bin";
  return `api/v1/upload/${userId}/${Date.now()}_${randomUUID()}.${ext}`;
}

export async function uploadBuffer(params: {
  edge: MyEdgeUploadApi;
  userId: string;
  fileName: string;
  contentType: string;
  body: Buffer;
  putPart: (url: string, body: Buffer) => Promise<string>;
  signal?: AbortSignal;
}): Promise<string> {
  const objectKey = buildObjectKey(params.userId, params.fileName);
  const partCount = Math.max(
    1,
    Math.ceil(params.body.length / MULTIPART_PART_SIZE),
  );

  let uploadId = "";
  let key = objectKey;

  try {
    const created = await params.edge.createMultipartUpload({
      fileName: params.fileName,
      contentType: params.contentType || "application/octet-stream",
      objectKey,
      partCount,
    });
    uploadId = created.uploadId;
    key = created.objectKey || objectKey;

    const urlByPart = new Map(
      created.parts.map((p) => [p.partNumber, p.url] as const),
    );
    const etags: string[] = new Array(partCount);
    let nextPart = 0;

    const worker = async () => {
      while (nextPart < partCount) {
        if (params.signal?.aborted) {
          throw new Error("myconversation: upload aborted");
        }
        const idx = nextPart;
        nextPart += 1;
        const partNumber = idx + 1;
        const start = idx * MULTIPART_PART_SIZE;
        const chunk = params.body.subarray(
          start,
          start + MULTIPART_PART_SIZE,
        );
        etags[idx] = await params.putPart(
          urlByPart.get(partNumber) ?? "",
          Buffer.from(chunk),
        );
      }
    };

    const workers = Math.min(MULTIPART_PART_CONCURRENCY, partCount);
    await Promise.all(Array.from({ length: workers }, () => worker()));

    await params.edge.completeMultipartUpload({
      objectKey: key,
      uploadId,
      parts: etags.map((etag, i) => ({ partNumber: i + 1, etag })),
    });
    return key;
  } catch (error) {
    if (uploadId) {
      void params.edge
        .abortMultipartUpload({ objectKey: key, uploadId })
        .catch(() => undefined);
    }
    throw error;
  }
}

/** Default HTTP PUT for R2 presigned part URLs; returns ETag. */
export async function putPartHttp(
  url: string,
  body: Buffer,
  signal?: AbortSignal,
): Promise<string> {
  const res = await fetch(url, { method: "PUT", body, signal });
  if (!res.ok) {
    throw new Error(`myconversation: R2 part PUT failed: ${res.status}`);
  }
  const etag = res.headers.get("ETag");
  if (!etag) {
    throw new Error("myconversation: missing ETag on part response");
  }
  return etag;
}

export async function uploadFileForAccount(params: {
  edge: MyEdgeUploadApi;
  userId: string;
  fileName: string;
  contentType: string;
  body: Buffer;
  signal?: AbortSignal;
}): Promise<string> {
  return uploadBuffer({
    ...params,
    putPart: (url, body) => putPartHttp(url, body, params.signal),
  });
}
