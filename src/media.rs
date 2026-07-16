//! Media helpers: classify attachments, send pre-uploaded URLs, download.

use std::path::{Path, PathBuf};

use reqwest::header::{AUTHORIZATION, HeaderMap, HeaderValue};

use crate::client::Client;
use crate::error::{Error, Result};

/// Max attachments per send (TS/Python parity).
pub const MAX_ATTACHMENTS: usize = 5;
/// Soft per-file size hint (bytes); enforced on local upload paths when present.
pub const MAX_FILE_BYTES: u64 = 20 * 1024 * 1024;

/// Outbound media already uploaded (object keys / URLs).
#[derive(Debug, Clone, Default)]
pub struct MediaUrls {
    /// Image paths/URLs for `images[]`.
    pub images: Vec<String>,
    /// File paths/URLs for `files[]` (documents, etc.). Videos are not supported in v1.
    pub files: Vec<String>,
}

impl MediaUrls {
    /// Validate attachment counts.
    pub fn validate(&self) -> Result<()> {
        let total = self.images.len() + self.files.len();
        if total > MAX_ATTACHMENTS {
            return Err(Error::Config(format!(
                "too many attachments: {total} > {MAX_ATTACHMENTS}"
            )));
        }
        Ok(())
    }
}

/// Classify a local path or URL into image vs file (videos rejected).
pub fn classify_media_path(path: &str) -> Result<MediaKind> {
    let lower = path.to_ascii_lowercase();
    if lower.ends_with(".mp4")
        || lower.ends_with(".mov")
        || lower.ends_with(".webm")
        || lower.ends_with(".mkv")
    {
        return Err(Error::Config(
            "video attachments are not supported in v1".into(),
        ));
    }
    if lower.ends_with(".png")
        || lower.ends_with(".jpg")
        || lower.ends_with(".jpeg")
        || lower.ends_with(".gif")
        || lower.ends_with(".webp")
    {
        return Ok(MediaKind::Image);
    }
    Ok(MediaKind::File)
}

/// Image vs generic file.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MediaKind {
    /// Image attachment.
    Image,
    /// Non-image file attachment.
    File,
}

/// Build [`MediaUrls`] from a list of paths/URLs.
pub fn media_urls_from_paths(
    paths: impl IntoIterator<Item = impl AsRef<str>>,
) -> Result<MediaUrls> {
    let mut out = MediaUrls::default();
    for path in paths {
        let path = path.as_ref();
        match classify_media_path(path)? {
            MediaKind::Image => out.images.push(path.to_string()),
            MediaKind::File => out.files.push(path.to_string()),
        }
    }
    out.validate()?;
    Ok(out)
}

impl Client {
    /// Download a media URL/path to `dest_dir`, returning the written path.
    ///
    /// Protected `api/v1/upload/...` paths are fetched from `API_1CHAT_URL` with
    /// bot auth headers. External https URLs are fetched without auth.
    pub async fn download_media(
        &self,
        path_or_url: &str,
        dest_dir: impl AsRef<Path>,
    ) -> Result<PathBuf> {
        let dest_dir = dest_dir.as_ref();
        std::fs::create_dir_all(dest_dir)
            .map_err(|e| Error::Transport(format!("create dest_dir: {e}")))?;

        let (url, authed) = resolve_fetch_url(self.base_url(), path_or_url);
        let mut headers = HeaderMap::new();
        if authed {
            let auth = format!("Bearer {}", self.config().bot_token);
            headers.insert(
                AUTHORIZATION,
                HeaderValue::from_str(&auth)
                    .map_err(|e| Error::Config(format!("invalid auth header: {e}")))?,
            );
            headers.insert(
                "x-tenant-id",
                HeaderValue::from_str(&self.config().tenant_id)
                    .map_err(|e| Error::Config(format!("invalid tenant header: {e}")))?,
            );
        }

        let client = reqwest::Client::new();
        let bytes = client
            .get(&url)
            .headers(headers)
            .send()
            .await
            .map_err(|e| Error::Transport(format!("download failed: {e}")))?
            .error_for_status()
            .map_err(|e| Error::Transport(format!("download status: {e}")))?
            .bytes()
            .await
            .map_err(|e| Error::Transport(format!("download body: {e}")))?;

        if bytes.len() as u64 > MAX_FILE_BYTES {
            return Err(Error::Transport(format!(
                "downloaded file exceeds {MAX_FILE_BYTES} bytes"
            )));
        }

        let name = Path::new(path_or_url)
            .file_name()
            .and_then(|s| s.to_str())
            .unwrap_or("download.bin");
        let dest = dest_dir.join(name);
        std::fs::write(&dest, &bytes)
            .map_err(|e| Error::Transport(format!("write download: {e}")))?;
        Ok(dest)
    }
}

fn resolve_fetch_url(base: &str, path_or_url: &str) -> (String, bool) {
    if path_or_url.starts_with("http://") || path_or_url.starts_with("https://") {
        let authed = path_or_url.contains("/api/v1/upload/");
        return (path_or_url.to_string(), authed);
    }
    let trimmed = path_or_url.trim_start_matches('/');
    let base = base.trim_end_matches('/');
    let authed = trimmed.starts_with("api/v1/upload/");
    (format!("{base}/{trimmed}"), authed)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn classifies_image_and_rejects_video() {
        assert_eq!(classify_media_path("a.PNG").unwrap(), MediaKind::Image);
        assert_eq!(classify_media_path("doc.pdf").unwrap(), MediaKind::File);
        assert!(classify_media_path("clip.mp4").is_err());
    }

    #[test]
    fn resolve_upload_path() {
        let (url, authed) = resolve_fetch_url("https://gw.example", "api/v1/upload/x/y.png");
        assert_eq!(url, "https://gw.example/api/v1/upload/x/y.png");
        assert!(authed);
    }
}
