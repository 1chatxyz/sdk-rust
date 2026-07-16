//! Minimal listen → reply bot (OpenClaw / Hermes integration template).
//!
//! ```bash
//! export API_1CHAT_URL=...
//! export TENANT_ID=...
//! export BOT_TOKEN=...
//! # optional: ONECHAT_USER_ID / ONECHAT_USERNAME for self-filter / mentions
//! cargo run --example echo_bot
//! ```

use futures_util::StreamExt;
use onechat_sdk::{Client, IncomingEvent, SubscribeOptions};

#[tokio::main]
async fn main() -> onechat_sdk::Result<()> {
    let client = Client::from_env()?;
    let mut options = SubscribeOptions::new();
    options.require_mention = false;

    let mut events = client.subscribe_groups(options).await?;
    println!("listening on {}", client.base_url());

    while let Some(item) = events.next().await {
        match item? {
            IncomingEvent::GroupMessage(msg) => {
                println!(
                    "group={} from={}: {}",
                    msg.group_id, msg.sender_username, msg.text
                );
                let _ = client.set_typing(msg.group_id, true).await;
                let reply = format!("echo: {}", msg.text);
                if let Err(err) = client.reply_group(msg.group_id, reply).await {
                    eprintln!("reply failed: {err}");
                }
                let _ = client.set_typing(msg.group_id, false).await;
                let _ = client.react_group_message(msg.id, "👀", false).await;
            }
            IncomingEvent::Typing(_)
            | IncomingEvent::DirectMessage(_)
            | IncomingEvent::DirectTyping { .. } => {}
        }
    }
    Ok(())
}
