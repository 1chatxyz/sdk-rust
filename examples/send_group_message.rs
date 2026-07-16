//! Send a text message to a chat group.
//!
//! ```bash
//! export API_1CHAT_URL=...
//! export TENANT_ID=...
//! export BOT_TOKEN=...
//! export CHANNEL_ID_TEST=123
//! cargo run --example send_group_message -- "hello from onechat-sdk"
//! ```

use onechat_sdk::Client;

#[tokio::main]
async fn main() -> onechat_sdk::Result<()> {
    let text = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "hello from onechat-sdk".into());
    let group_id: i64 = std::env::var("CHANNEL_ID_TEST")
        .map_err(|_| onechat_sdk::Error::Config("missing CHANNEL_ID_TEST for this example".into()))?
        .trim()
        .parse()
        .map_err(|e| onechat_sdk::Error::Config(format!("invalid CHANNEL_ID_TEST: {e}")))?;

    let client = Client::from_env()?;
    let _ = client.set_typing(group_id, true).await;
    let result = client.reply_group(group_id, &text).await?;
    let _ = client.set_typing(group_id, false).await;
    println!("sent message_ids={:?}", result.message_ids);
    Ok(())
}
