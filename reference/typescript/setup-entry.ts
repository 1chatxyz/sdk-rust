import { defineSetupPluginEntry } from "openclaw/plugin-sdk/channel-core";

import { myConversationChannelPlugin } from "./src/channel.js";

export default defineSetupPluginEntry(myConversationChannelPlugin);
