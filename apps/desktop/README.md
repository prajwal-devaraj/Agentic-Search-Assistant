# PRAJNA Desktop

Tauri shell for macOS, Windows, and Linux. It packages the static export from `apps/web/out`.

```bash
pnpm --filter @prajna/web build
cd apps/desktop
cargo tauri build
```

For production, set `NEXT_PUBLIC_PRAJNA_API_URL` to your deployed API before building the web export.
