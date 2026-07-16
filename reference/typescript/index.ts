import { defineChannelPluginEntry } from "openclaw/plugin-sdk/channel-core";

import { myConversationChannelPlugin } from "./src/channel.js";
import { setMyConversationChannelRuntime } from "./src/runtime.js";

export default defineChannelPluginEntry({
  id: "myconversation",
  name: "myconversation",
  description: "myconversation staff group chat channel plugin scaffold",
  plugin: myConversationChannelPlugin,
  setRuntime(runtime) {
    setMyConversationChannelRuntime(
      runtime as Parameters<typeof setMyConversationChannelRuntime>[0],
    );
  },
});
