# OpenClaw Chat Group + Dev Test UI — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `SignalChatGroupTyping` in myconversation, a Telegram-style dev Web UI to test Staff Group Chat live (including typing), and scaffold the OpenClaw channel plugin for E2E bot replies.

**Architecture:** myconversation keeps its existing private gRPC listener (no auth in service; gateway01 validates bearer tokens and attaches `x-tenant-id` / `x-user-id`). OpenClaw plugin calls **gateway01** with `x-tenant-id` + `Authorization: Bearer <token>` (same trust path as staff). Optional plugin `userId` is for inbound filtering only (self-skip, mention-by-id) — not sent on the wire. Dev UI uses grpc-web via gateway01 like `scripts/_gateway_common.py`. Only new backend surface is typing RPC + stream event.

**Tech Stack:** Go, protobuf/Ent, Redis pub/sub (`chatgroupstream`), Vite + TypeScript + hand-rolled protobuf wire codec (mirrors Python scripts), OpenClaw plugin SDK (separate repo).

**Spec:** `docs/superpowers/specs/2026-06-08-openclaw-chatgroup-design.md`

**Repository split:** Backend typing RPC, dev UI (`web/chatgroup-test/`), and chat-group API live in [marketplace/myconversation](https://gitlab.genjutsu.ai/marketplace/myconversation). The OpenClaw channel plugin (Part C) lives in this repo.

---

## File map

| File | Responsibility |
|------|----------------|
| `api/myconversation.proto` | New RPC + messages + stream oneof field |
| `internal/chatgroup/stream.go` | `WrapStreamTyping`, `StreamSkip`, `StreamEventGroupID` |
| `internal/chatgroup/stream_test.go` | Unit tests for stream helpers |
| `internal/server/myconversation/grpc_myconversation_signalchatgrouptyping.go` | RPC handler |
| `internal/server/myconversation/grpc_myconversation_chatgroup_publish.go` | `publishChatGroupTyping` helper |
| `internal/server/myconversation/grpc_myconversation_signalchatgrouptyping_test.go` | Handler + hub publish tests |
| `web/chatgroup-test/*` | Dev Telegram-style UI |

---

## Part A — myconversation typing indicator

### Task 1: Proto changes

**Files:**
- Modify: `api/myconversation.proto` (~lines 101–107, 1415–1422)

- [ ] **Step 1: Add RPC** after `StreamChatGroups` (line ~106):

```protobuf
  rpc SignalChatGroupTyping(SignalChatGroupTypingRequest) returns (SignalChatGroupTypingReply);
```

- [ ] **Step 2: Add messages** before `StreamChatGroupsRequest` (~line 1383):

```protobuf
message SignalChatGroupTypingRequest {
  int64 group_id = 1 [(validate.rules).int64 = { gt: 0 }];
  bool typing    = 2;
}

message SignalChatGroupTypingReply {}

message ChatGroupTypingIndicator {
  int64 group_id  = 1;
  int64 user_id   = 2;
  string username = 3;
  bool typing     = 4;
}
```

- [ ] **Step 3: Extend stream oneof** in `ChatGroupStreamEvent`:

```protobuf
message ChatGroupStreamEvent {
  oneof item {
    ChatGroupStreamPing ping            = 1;
    ChatGroupMessageInfo message        = 2;
    ChatGroupMemberChange member_change = 3;
    ChatGroupMetaChange meta_change     = 4;
    ChatGroupTypingIndicator typing     = 5;
  }
}
```

- [ ] **Step 4: Codegen + build**

Run from repo root:

```bash
genkit generate go --skip-upgrade
go build ./...
```

Expected: exit 0, no compile errors.

---

### Task 2: Stream helpers + unit tests (TDD)

**Files:**
- Create: `internal/chatgroup/stream_test.go`
- Modify: `internal/chatgroup/stream.go`

- [ ] **Step 1: Write failing tests**

Create `internal/chatgroup/stream_test.go`:

```go
package chatgroup

import (
	"testing"

	pb "gitlab.genjutsu.ai/marketplace/myconversation/api/v1/myconversation"
)

func TestStreamSkip_typingNeverSkippedByMessageCursor(t *testing.T) {
	t.Parallel()
	ev := WrapStreamTyping(42, 99, "OpenClaw", true)
	if StreamSkip(ev, 1_000_000) {
		t.Fatal("typing events must not be skipped by message cursor")
	}
}

func TestStreamSkip_messageStillUsesCursor(t *testing.T) {
	t.Parallel()
	ev := WrapStreamMessage(&pb.ChatGroupMessageInfo{Id: 5, GroupId: 1})
	if !StreamSkip(ev, 10) {
		t.Fatal("old messages should be skipped")
	}
}

func TestWrapStreamTyping_fields(t *testing.T) {
	t.Parallel()
	ev := WrapStreamTyping(7, 3, "Bot", false)
	ind := ev.GetTyping()
	if ind == nil {
		t.Fatal("nil typing payload")
	}
	if ind.GetGroupId() != 7 || ind.GetUserId() != 3 || ind.GetUsername() != "Bot" || ind.GetTyping() {
		t.Fatalf("got %+v", ind)
	}
}

func TestStreamEventGroupID_typing(t *testing.T) {
	t.Parallel()
	ev := WrapStreamTyping(11, 2, "x", true)
	if got := StreamEventGroupID(ev); got != 11 {
		t.Fatalf("group_id=%d", got)
	}
}

func TestStreamAdvanceMessageCursor_ignoresTyping(t *testing.T) {
	t.Parallel()
	ev := WrapStreamTyping(1, 2, "x", true)
	if got := StreamAdvanceMessageCursor(ev, 99); got != 99 {
		t.Fatalf("cursor=%d", got)
	}
}
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
go test ./internal/chatgroup/... -run 'TestStreamSkip_typing|TestWrapStreamTyping|TestStreamEventGroupID_typing|TestStreamAdvance' -count=1
```

Expected: compile error (`WrapStreamTyping` undefined) or test failures.

- [ ] **Step 3: Implement in `internal/chatgroup/stream.go`**

Add function:

```go
func WrapStreamTyping(groupID, userID int64, username string, typing bool) *pb.ChatGroupStreamEvent {
	return &pb.ChatGroupStreamEvent{
		Item: &pb.ChatGroupStreamEvent_Typing{
			Typing: &pb.ChatGroupTypingIndicator{
				GroupId:  groupID,
				UserId:   userID,
				Username: username,
				Typing:   typing,
			},
		},
	}
}
```

Update `StreamSkip` switch — add case before `default`:

```go
	case *pb.ChatGroupStreamEvent_Typing:
		return false
```

Update `StreamEventGroupID` switch — add case:

```go
	case *pb.ChatGroupStreamEvent_Typing:
		if ind := t.Typing; ind != nil {
			return ind.GetGroupId()
		}
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
go test ./internal/chatgroup/... -run 'TestStreamSkip_typing|TestWrapStreamTyping|TestStreamEventGroupID_typing|TestStreamAdvance' -count=1
```

Expected: `ok gitlab.genjutsu.ai/marketplace/myconversation/internal/chatgroup`

---

### Task 3: Publish helper

**Files:**
- Modify: `internal/server/myconversation/grpc_myconversation_chatgroup_publish.go`

- [ ] **Step 1: Add helper** after `publishChatGroupMessage`:

```go
func (s *myConversationServer) publishChatGroupTyping(ctx context.Context, tenantID string, groupID, userID int64, username string, typing bool) {
	s.publishChatGroupStream(ctx, tenantID, chatgroup.WrapStreamTyping(groupID, userID, username, typing))
}
```

- [ ] **Step 2: Build**

```bash
go build ./...
```

Expected: exit 0.

---

### Task 4: SignalChatGroupTyping handler (TDD)

**Files:**
- Create: `internal/server/myconversation/grpc_myconversation_signalchatgrouptyping.go`
- Create: `internal/server/myconversation/grpc_myconversation_signalchatgrouptyping_test.go`

- [ ] **Step 1: Write failing handler tests**

Create `grpc_myconversation_signalchatgrouptyping_test.go`:

```go
package myconversation

import (
	"context"
	"fmt"
	"sync"
	"testing"

	_ "github.com/mattn/go-sqlite3"
	"go.uber.org/zap"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/proto"

	pbmodel "gitlab.genjutsu.ai/marketplace/myconversation/api/v1/model"
	pb "gitlab.genjutsu.ai/marketplace/myconversation/api/v1/myconversation"
	"gitlab.genjutsu.ai/marketplace/myconversation/internal/chatgroupstream"
	"gitlab.genjutsu.ai/marketplace/myconversation/internal/helpdeskstream"
	"gitlab.genjutsu.ai/marketplace/myconversation/pkg/ent/enttest"
)

type captureRedis struct {
	mu      sync.Mutex
	channel string
	payload []byte
}

func (r *captureRedis) Publish(_ context.Context, channel string, payload []byte) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.channel = channel
	r.payload = append([]byte(nil), payload...)
	return nil
}

func (r *captureRedis) Subscribe(context.Context, string) (helpdeskstream.Subscription, error) {
	return nil, fmt.Errorf("not implemented")
}

type stubMyID struct{}

func (stubMyID) DisplayNameByUserID(context.Context, int64) (string, bool) {
	return "OpenClaw", true
}

func (stubMyID) EnsureTenantMember(context.Context, string, int64) error { return nil }

func newTestServerWithChatHub(t *testing.T, client *ent.Client, rdb helpdeskstream.RedisClient) pb.MyConversationServer {
	t.Helper()
	hub := chatgroupstream.New(rdb, zap.NewNop())
	return NewServer(testDB(client), nil, "", "", nil, nil, hub, stubMyID{}, nil, "", nil)
}

func TestSignalChatGroupTyping_requiresMember(t *testing.T) {
	t.Parallel()
	dsn := fmt.Sprintf("file:ent-%s?mode=memory&cache=shared&_fk=1", t.Name())
	client := enttest.Open(t, "sqlite3", dsn)
	defer client.Close()

	ownerCtx := userCtx("tenant-1", 1)
	group := seedChatGroup(t, ownerCtx, client, "tenant-1", 1, "Ops", "", pbmodel.ChatGroupVisibility_CHAT_GROUP_VISIBILITY_PUBLIC)

	srv := newTestServerWithChatHub(t, client, &captureRedis{})
	_, err := srv.SignalChatGroupTyping(userCtx("tenant-1", 999), &pb.SignalChatGroupTypingRequest{
		GroupId: group.Group.ID,
		Typing:  true,
	})
	if status.Code(err) != codes.PermissionDenied {
		t.Fatalf("got err=%v want PermissionDenied", err)
	}
}

func TestSignalChatGroupTyping_publishesTypingEvent(t *testing.T) {
	t.Parallel()
	dsn := fmt.Sprintf("file:ent-%s?mode=memory&cache=shared&_fk=1", t.Name())
	client := enttest.Open(t, "sqlite3", dsn)
	defer client.Close()

	ownerCtx := userCtx("tenant-1", 1)
	group := seedChatGroup(t, ownerCtx, client, "tenant-1", 1, "Ops", "", pbmodel.ChatGroupVisibility_CHAT_GROUP_VISIBILITY_PUBLIC)

	cap := &captureRedis{}
	srv := newTestServerWithChatHub(t, client, cap)
	_, err := srv.SignalChatGroupTyping(ownerCtx, &pb.SignalChatGroupTypingRequest{
		GroupId: group.Group.ID,
		Typing:  true,
	})
	if err != nil {
		t.Fatal(err)
	}

	cap.mu.Lock()
	defer cap.mu.Unlock()
	if cap.channel != "chatgroup:tenant-1" {
		t.Fatalf("channel=%q", cap.channel)
	}
	ev := &pb.ChatGroupStreamEvent{}
	if err := proto.Unmarshal(cap.payload, ev); err != nil {
		t.Fatal(err)
	}
	ind := ev.GetTyping()
	if ind == nil || !ind.GetTyping() || ind.GetGroupId() != group.Group.ID || ind.GetUserId() != 1 {
		t.Fatalf("got %+v", ind)
	}
	if ind.GetUsername() != "OpenClaw" {
		t.Fatalf("username=%q", ind.GetUsername())
	}
}
```

Fix import: add `pbmodel` for visibility enum in seedChatGroup — use `pbmodel.ChatGroupVisibility_CHAT_GROUP_VISIBILITY_PUBLIC` or copy from search test (seed uses pbmodel).

- [ ] **Step 2: Run tests — expect FAIL**

```bash
go test ./internal/server/myconversation/... -run SignalChatGroupTyping -count=1
```

Expected: compile error (`SignalChatGroupTyping` method missing).

- [ ] **Step 3: Implement handler**

Create `grpc_myconversation_signalchatgrouptyping.go`:

```go
package myconversation

import (
	"context"
	"fmt"

	"go.uber.org/zap"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	"gitlab.genjutsu.ai/marketplace/logger/pkg/logging"
	pb "gitlab.genjutsu.ai/marketplace/myconversation/api/v1/myconversation"
	"gitlab.genjutsu.ai/marketplace/myconversation/internal/chatgroup"
	"gitlab.genjutsu.ai/marketplace/myconversation/internal/server/extractor"
)

func (s *myConversationServer) SignalChatGroupTyping(ctx context.Context, request *pb.SignalChatGroupTypingRequest) (*pb.SignalChatGroupTypingReply, error) {
	if err := request.Validate(); err != nil {
		return nil, err
	}

	tenantID := extractor.GetTenantID(ctx, "")
	if tenantID == "" {
		return nil, status.Error(codes.Unauthenticated, "unauthenticated")
	}
	userID, err := extractor.GetUserID(ctx)
	if err != nil {
		return nil, status.Error(codes.Unauthenticated, "unauthenticated")
	}

	groupID := request.GetGroupId()
	if _, err := chatgroup.ActiveMember(ctx, s.Ent, tenantID, groupID, userID); err != nil {
		return nil, err
	}

	username := ""
	if s.myidResolver != nil {
		if name, ok := s.myidResolver.DisplayNameByUserID(ctx, userID); ok {
			username = name
		}
	}

	s.publishChatGroupTyping(ctx, tenantID, groupID, userID, username, request.GetTyping())
	return &pb.SignalChatGroupTypingReply{}, nil
}
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
go test ./internal/server/myconversation/... -run SignalChatGroupTyping -count=1
```

Expected: both tests pass.

- [ ] **Step 5: Full build**

```bash
go build ./...
```

---

### Task 5: StreamChatGroups delivers typing to members

**Files:**
- Modify: `internal/server/myconversation/grpc_myconversation_streamchatgroups.go` (no change needed if `StreamSkip` returns false for typing and `StreamEventGroupID` returns group_id — membership filter at lines 166–177 already passes any event type when viewer is member)

- [ ] **Step 1: Verify** `sendChatGroupStreamEvent` — typing events with `groupID > 0` pass membership check (same as `MetaChange`). No code change unless manual test shows drop.

- [ ] **Step 2: Optional unit test** in `stream_test.go`:

```go
func TestStreamSkip_metaAndTypingNotSkipped(t *testing.T) {
	t.Parallel()
	meta := WrapStreamMetaChange(&pb.ChatGroupInfo{Id: 1})
	if StreamSkip(meta, 0) {
		t.Fatal("meta should not skip")
	}
}
```

Run: `go test ./internal/chatgroup/... -count=1`

---

## Part B — Dev test Web UI (`web/chatgroup-test/`)

### Task 6: Scaffold

**Files:**
- Create: `web/chatgroup-test/package.json`
- Create: `web/chatgroup-test/vite.config.ts`
- Create: `web/chatgroup-test/tsconfig.json`
- Create: `web/chatgroup-test/index.html`
- Create: `web/chatgroup-test/.gitignore`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "chatgroup-test",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "typescript": "^5.7.0",
    "vite": "^6.0.0"
  }
}
```

- [ ] **Step 2: Create `vite.config.ts`**

```typescript
import { defineConfig } from "vite";

export default defineConfig({
  server: { port: 5173, host: true },
});
```

- [ ] **Step 3: Create `index.html`**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Chat Group Test</title>
    <link rel="stylesheet" href="/src/telegram.css" />
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 4: Install + verify dev server starts**

```bash
cd web/chatgroup-test && npm install && npm run dev
```

Expected: Vite ready on `http://localhost:5173` (Ctrl+C to stop).

---

### Task 7: Protobuf wire codec (port from Python scripts)

**Files:**
- Create: `web/chatgroup-test/src/pb/codec.ts`

- [ ] **Step 1: Implement codec** — port `pb_string`, `pb_varint`, `pb_message`, `decode_fields`, `grpc_web_frame`, `parse_grpc_web_body` from `scripts/_gateway_common.py` lines 225–359 to TypeScript.

Minimal starter (expand in implementation):

```typescript
export function encodeVarint(value: number): Uint8Array { /* ... */ }
export function pbString(fieldNum: number, value: string): Uint8Array { /* ... */ }
export function pbVarint(fieldNum: number, value: number): Uint8Array { /* ... */ }
export function pbMessage(fieldNum: number, inner: Uint8Array): Uint8Array { /* ... */ }
export function decodeFields(data: Uint8Array): Map<number, unknown[]> { /* ... */ }
export function grpcWebFrame(message: Uint8Array): Uint8Array {
  const out = new Uint8Array(5 + message.length);
  out[0] = 0;
  new DataView(out.buffer).setUint32(1, message.length, false);
  out.set(message, 5);
  return out;
}
export function parseGrpcWebBody(body: Uint8Array): Uint8Array { /* ... */ }
```

- [ ] **Step 2: Add encoders** in `web/chatgroup-test/src/pb/messages.ts`:

```typescript
import { pbString, pbVarint, pbMessage } from "./codec";

export function encodeSignInUserpass(username: string, password: string): Uint8Array {
  const userpass = pbString(1, username) + pbString(2, password); // use concat helper
  const credential = pbMessage(1, concat(userpass));
  return pbMessage(1, concat(credential));
}

export function encodeCreateAccessToken(idToken: string): Uint8Array {
  return pbString(1, idToken);
}

export function encodeSendChatGroupMessage(groupId: number, content: string, mentionedUserIds: number[]): Uint8Array {
  let body = pbVarint(1, groupId) + pbString(2, content);
  for (const uid of mentionedUserIds) {
    body = concat(body, pbVarint(6, uid)); // field 6 repeated
  }
  return body;
}

export function encodeStreamChatGroups(resumeAfterMessageId: number): Uint8Array {
  if (resumeAfterMessageId <= 0) return new Uint8Array(0);
  return pbVarint(1, resumeAfterMessageId);
}
```

Add decoders for `ListMyChatGroupsReply`, `ListChatGroupMessagesReply`, `ChatGroupStreamEvent` (message + typing oneofs).

---

### Task 8: grpc-web client + auth

**Files:**
- Create: `web/chatgroup-test/src/api/grpc-web.ts`
- Create: `web/chatgroup-test/src/api/session.ts`
- Create: `web/chatgroup-test/src/api/auth.ts`

- [ ] **Step 1: `session.ts`** — localStorage keys `cg_gateway`, `cg_access_token`, `cg_tenant_id`, `cg_user_id`, `cg_bot_user_id_hint`.

- [ ] **Step 2: `grpc-web.ts`** — unary POST:

```typescript
export async function grpcWebUnary(
  gateway: string,
  path: string,
  body: Uint8Array,
  headers: Record<string, string>,
): Promise<Uint8Array> {
  const res = await fetch(`${gateway.replace(/\/$/, "")}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/grpc-web+proto",
      Accept: "application/grpc-web+proto",
      "X-Grpc-Web": "1",
      ...headers,
    },
    body: grpcWebFrame(body),
  });
  const grpcStatus = res.headers.get("grpc-status") ?? "0";
  if (grpcStatus !== "0") {
    throw new Error(`gRPC ${grpcStatus}: ${res.headers.get("grpc-message") ?? ""}`);
  }
  const buf = new Uint8Array(await res.arrayBuffer());
  return parseGrpcWebBody(buf);
}
```

Paths (match Python scripts):

| RPC | Path |
|-----|------|
| SignIn | `/genjutsu.myid.v2.MyID/SignIn` |
| CreateAccessToken | `/genjutsu.myid.v2.MyID/CreateAccessToken` |
| ListMyChatGroups | `/genjutsu.myconversation.v1.MyConversation/ListMyChatGroups` |
| ListChatGroupMessages | `/genjutsu.myconversation.v1.MyConversation/ListChatGroupMessages` |
| SendChatGroupMessage | `/genjutsu.myconversation.v1.MyConversation/SendChatGroupMessage` |
| CreateChatGroup | `/genjutsu.myconversation.v1.MyConversation/CreateChatGroup` |
| AddChatGroupMember | `/genjutsu.myconversation.v1.MyConversation/AddChatGroupMember` |
| ListChatGroupMembers | `/genjutsu.myconversation.v1.MyConversation/ListChatGroupMembers` |
| StreamChatGroups | `/genjutsu.myconversation.v1.MyConversation/StreamChatGroups` |

Metadata on MyConversation calls:

```typescript
function myConvHeaders(session: Session): Record<string, string> {
  return {
    Authorization: `Bearer ${session.accessToken}`,
    "x-tenant-id": session.tenantId,
    "x-user-id": String(session.userId),
  };
}
```

- [ ] **Step 3: `auth.ts`** — `login(gateway, username, password)` → SignIn → CreateAccessToken → save session (mirror `obtain_access_token` in `_gateway_common.py`).

- [ ] **Step 4: Server streaming** — `grpcWebStream(gateway, path, body, headers, onFrame)` using `fetch` + `ReadableStream` reader; parse frames with same 5-byte prefix as Python `iter_grpc_web_frames`. Note: if stg gateway buffers stream, document `--direct` port-forward fallback in README.

---

### Task 9: Telegram-style UI

**Files:**
- Create: `web/chatgroup-test/src/telegram.css`
- Create: `web/chatgroup-test/src/app.ts`
- Create: `web/chatgroup-test/src/main.ts`

- [ ] **Step 1: CSS variables** in `telegram.css`:

```css
:root {
  --bg: #0e1621;
  --sidebar: #17212b;
  --bubble-other: #182533;
  --bubble-self: #2aabee;
  --text: #f5f5f5;
  --muted: #7f91a4;
}
body { margin: 0; font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); }
.layout { display: flex; height: 100vh; }
.sidebar { width: 320px; background: var(--sidebar); border-right: 1px solid #0b1015; overflow-y: auto; }
.main { flex: 1; display: flex; flex-direction: column; }
.messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 8px; }
.bubble { max-width: 70%; padding: 8px 12px; border-radius: 12px; }
.bubble.self { align-self: flex-end; background: var(--bubble-self); }
.bubble.other { align-self: flex-start; background: var(--bubble-other); }
.typing { font-style: italic; color: var(--muted); padding: 0 16px 8px; min-height: 1.2em; }
.composer { display: flex; gap: 8px; padding: 12px; border-top: 1px solid #0b1015; }
.composer input { flex: 1; padding: 10px; border-radius: 8px; border: none; background: #242f3d; color: var(--text); }
```

- [ ] **Step 2: `app.ts` state machine**

```typescript
type Message = { id: number; groupId: number; senderUserId: number; senderUsername: string; content: string; mentionedUserIds: number[] };
type Group = { id: number; name: string; lastPreview?: string };

// On login success → listMyChatGroups() → render sidebar
// On group click → listChatGroupMessages(groupId) → render bubbles (sort by id asc)
// Start streamChatGroups(onEvent):
//   - message: upsert by id, update sidebar preview if matches
//   - typing: show "#typing" text "{username} is typing…" / clear when typing=false
//   - ping: ignore
// On send → sendChatGroupMessage(groupId, text, mentionIds)
```

- [ ] **Step 3: Login screen** — form with gateway (default `https://gw01-sales01.genjutsu.ai`), username, password.

- [ ] **Step 4: Modals** — "New group" (`CreateChatGroup` PUBLIC), "Add member" (prompt user_id → `AddChatGroupMember`), "@" picker from `ListChatGroupMembers`.

- [ ] **Step 5: Typing timeout** — hide typing line after 10s if no `typing=false` received.

---

### Task 10: README

**Files:**
- Create: `web/chatgroup-test/README.md`

- [ ] **Step 1: Document setup**

```markdown
# Chat Group Test UI

Dev-only Telegram-style UI for Staff Group Chat + OpenClaw E2E.

## Run
cd web/chatgroup-test
npm install
npm run dev
# open http://localhost:5173

## E2E with OpenClaw
1. Login with stg staff credentials.
2. Create group → Add member (OpenClaw bot user_id).
3. Ensure OpenClaw plugin is running with matching `tenantId` / `token` (and optional `userId` for @mention-by-id).
4. Send `@OpenClaw hello` → expect typing indicator → bot reply.

## CORS
If browser blocks gateway01, use Telepresence/port-forward or run UI from allowed origin.
```

---

## Part C — OpenClaw channel plugin (this repo)

> Plugin source: [marketplace/openclaw/myconversation](https://gitlab.genjutsu.ai/marketplace/openclaw/myconversation). Implement after Part A is on stg.

### Task 11: Plugin scaffold

**Files:** repository root (`package.json`, `src/`, …)

- [x] **Step 1:** `openclaw.plugin.json` with id `myconversation`, channel config schema (`endpoint`, `tenantId`, `token`, optional `userId`, optional `username`).
- [x] **Step 2:** `@genjutsu/myconversation-connect` + `@connectrpc/connect-node` client; metadata on every RPC:

```typescript
metadata.set("x-tenant-id", config.tenantId);
metadata.set("authorization", `Bearer ${config.token}`);
// no x-user-id — gateway injects it after token validation
```

- [x] **Step 3:** Connect to `config.endpoint` (**gateway01** host:port, not raw myconversation listener).

**Why optional `userId`?** Auth is entirely via `token`. Stream events only expose numeric `sender_user_id` / `mentioned_user_ids`, so the plugin needs a local copy of the service user's id to (a) skip self-echoed bot messages and (b) honor UI mention-by-id. Not sent on the wire.

**Why optional `username`?** When `requireMention: true`, users may type `@OpenClaw` in message text instead of using UI mention chips (`mentioned_user_ids`). Set `username` (without `@`) so the plugin can match that pattern.

### Task 12: Inbound stream

- [x] **Step 1:** `StreamChatGroups` with `resume_after_message_id`; exponential backoff reconnect.
- [x] **Step 2:** On `ChatGroupStreamEvent.message`: skip if `userId` set and `sender_user_id === userId`; apply `requireMention` from `channels.myconversation.groups[groupId]`.
- [x] **Step 3:** Session key = `myconversation:group:${groupId}`.

### Task 13: Outbound

- [x] **Step 1:** `SignalChatGroupTyping({ group_id, typing: true })` before agent (best-effort if RPC missing on server).
- [x] **Step 2:** Run OpenClaw agent turn.
- [x] **Step 3:** `SignalChatGroupTyping({ typing: false })` then `SendChatGroupMessage({ group_id, content, client_message_id: uuid })`.

---

## Spec coverage self-review

| Spec requirement | Task |
|------------------|------|
| SignalChatGroupTyping RPC | Task 1, 4 |
| ChatGroupTypingIndicator stream | Task 1, 2, 4 |
| No listener/auth changes | None (by design) |
| Plugin gRPC via gateway + bearer token | Part C |
| Optional userId for self/mention filter | Part C Task 11–12 |
| Dev UI login/list/send/stream | Part B |
| Typing in UI | Task 9 |
| Add bot via AddChatGroupMember | Task 9 modal |
| Mention gating in plugin | Task 12 |

---

## Verification checklist

```bash
# Backend
go test ./internal/chatgroup/... -count=1
go test ./internal/server/myconversation/... -run SignalChatGroupTyping -count=1
go build ./...

# UI
cd web/chatgroup-test && npm run build
```

Manual: login → create group → add bot user_id → send @mention → observe typing + reply with OpenClaw plugin running.

---

**Plan complete and saved to `docs/superpowers/plans/2026-06-08-openclaw-chatgroup.md`.**

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration.

2. **Inline Execution** — execute tasks in this session with checkpoints (`executing-plans` skill).

**Which approach?**
