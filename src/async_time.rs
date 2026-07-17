//! Small async sleep/timeout helpers (Tokio native, gloo-timers on wasm).

use std::future::Future;
use std::time::Duration;

#[cfg(target_arch = "wasm32")]
use futures_util::future::{Either, select};

/// Sleep for `dur`.
#[cfg_attr(target_arch = "wasm32", allow(dead_code))] // used by native `run_*_bot` reconnect
pub async fn sleep(dur: Duration) {
    #[cfg(not(target_arch = "wasm32"))]
    {
        tokio::time::sleep(dur).await;
    }
    #[cfg(target_arch = "wasm32")]
    {
        let ms = dur.as_millis().min(u128::from(u32::MAX)) as u32;
        gloo_timers::future::TimeoutFuture::new(ms.max(1)).await;
    }
}

/// Wait for `fut` or `dur`, whichever finishes first.
pub async fn timeout<T>(dur: Duration, fut: impl Future<Output = T>) -> Result<T, ()> {
    #[cfg(not(target_arch = "wasm32"))]
    {
        tokio::time::timeout(dur, fut).await.map_err(|_| ())
    }
    #[cfg(target_arch = "wasm32")]
    {
        let ms = dur.as_millis().min(u128::from(u32::MAX)) as u32;
        match select(
            Box::pin(fut),
            gloo_timers::future::TimeoutFuture::new(ms.max(1)),
        )
        .await
        {
            Either::Left((value, _)) => Ok(value),
            Either::Right((_, _)) => Err(()),
        }
    }
}
