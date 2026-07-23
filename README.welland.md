# tmux — welland next-3.8 apt package

This branch (`mithro/welland`) packages a **pinned snapshot of upstream tmux
`next-3.8`** (commit [`5ed5e36`](https://github.com/tmux/tmux/commit/5ed5e36)) as a
GPG-signed Debian apt repository for arm64 and amd64.

## Why

tmux **3.7b** (the current release, and the newest in Debian sid) has a
`choose-tree` renderer bug: the session picker (`choose-tree -Zs`) renders a
**completely blank list whenever any session group has ≥2 members**. Upstream
`next-3.8` fixes it. Until 3.8 is released, this repo ships the fix.

## Install

```sh
curl -fsSL https://mithro.github.io/tmux/tmux.gpg \
  | sudo tee /etc/apt/keyrings/mithro-tmux.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/mithro-tmux.gpg] https://mithro.github.io/tmux/ ./" \
  | sudo tee /etc/apt/sources.list.d/mithro-tmux.list
sudo apt update
sudo apt install tmux
```

The package version is `3.8~git<commit-date>.<sha>-0+welland1`, which upgrades
over Debian's `3.7b-1` and is cleanly superseded by an official `3.8-1` when it
lands.

## How it's built

`.github/workflows/deb.yml` builds native arm64 + amd64 `.deb`s (in a
`debian:trixie` container) from this repo's `debian/` packaging, then publishes a
signed flat apt repo to GitHub Pages. Upstream source is unmodified; only
`debian/` and `packaging/` are added. Repackaged from Debian's tmux packaging
(switched to `3.0 (native)`; upstream tmux CI workflows removed).
