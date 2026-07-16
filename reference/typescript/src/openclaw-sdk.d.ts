declare module "openclaw/plugin-sdk/channel-core" {
  export type OpenClawConfig = {
    channels?: Record<string, unknown>;
    [key: string]: unknown;
  };

  export function defineChannelPluginEntry<TPlugin>(options: {
    id: string;
    name: string;
    description: string;
    plugin: TPlugin;
    configSchema?: unknown;
    setRuntime?: (runtime: unknown) => void;
    registerCliMetadata?: (api: unknown) => void;
    registerFull?: (api: { runtime?: unknown; [key: string]: unknown }) => void;
  }): unknown;

  export function defineSetupPluginEntry<TPlugin>(plugin: TPlugin): unknown;

  export function createChannelPluginBase<TBase>(base: TBase): TBase;

  export function createChatChannelPlugin<TPlugin>(plugin: TPlugin): TPlugin;
}
