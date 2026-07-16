//! Listen on DM streams and echo replies.
//!
//! ```bash
//! export API_1CHAT_URL=...
//! export TENANT_ID=...
//! export BOT_TOKEN=...
//! cargo run --example dm_echo_bot
//! ```

use futures_util::StreamExt;
use onechat_sdk::{Client, IncomingEvent};

#[tokio::main]
async fn main() -> onechat_sdk::Result<()> {
    let client = Client::from_env()?;
    let mut events = client.subscribe_dms().await?;
    println!("listening for DMs on {}", client.base_url());

    while let Some(item) = events.next().await {
        match item? {
            IncomingEvent::DirectMessage(msg) => {
                println!(
                    "dm thread={} from={}: {}",
                    msg.thread_id, msg.sender_username, msg.text
                );
                let _ = client.set_dm_typing(msg.thread_id, true).await;
                if let Err(err) = client
                    .reply_dm(
                        msg.thread_id,
                        msg.sender_user_id,
                        format!("echo: {}", msg.text),
                    )
                    .await
                {
                    eprintln!("reply failed: {err}");
                }
                let _ = client.set_dm_typing(msg.thread_id, false).await;
            }
            IncomingEvent::GroupMessage(_)
            | IncomingEvent::Typing(_)
            | IncomingEvent::DirectTyping { .. } => {}
        }
    }
    Ok(())
}
