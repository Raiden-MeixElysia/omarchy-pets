# AGENTS.md

Omarchy Pets is a third-party bar widget for the Omarchy 4.5 shell
(`omarchy-shell`, Quickshell, Qt 6 QML). It plays Codex Pets sprite sheets
from `~/.omarchy-pets/pets/`.

- Plugin id: `io.github.raiden-meixelysia.omarchy-pets`. The marketplace
  retired `raiden-meixelysia.omarchy-pets`; never reuse it.
- Repository: <https://github.com/Raiden-MeixElysia/omarchy-pets>.
- Version lives in `manifest.json`. Commit subjects start with it.

## Layout

| Path | Role |
|---|---|
| `manifest.json` | Plugin manifest and settings schema |
| `BarWidget.qml` | Bar icon; loads `Panel.qml`, feeds it the stored entry |
| `Settings.js` | Finds the widget's entry in `bar.layout` (all `Util.barSections`) |
| `Panel.qml` | Panel card, desktop window, settings writes |
| `PetLibrary.qml` | Runs `scan.py` and `bootstrap.py` |
| `PetSprite.qml`, `Sprite.js` | Atlas animation and pose tables |
| `scan.py` | Validates pets; prints one line per entry, sheets inline |
| `bootstrap.py` | First load: writes the CLI, installs `guga` |
| `cli/` | The omarchy-pets.com CLI, byte-identical to the site's build |

`cli/` is a copy. Change it in the site repository, then copy it here.

## Shell APIs

Read them in `$OMARCHY_PATH/shell` before use; do not guess.
`Ui/BarWidget.qml`, `Ui/Panel.qml`, `Ui/KeyboardPanel.qml`,
`Ui/PluginBarApi.qml`, `services/PluginShellApi.qml`, and
`default/agents/skills/omarchy/plugins.md`. Settings go through
`bar.shell.updateEntryInline`, which replaces the whole entry.

## Check

```sh
omarchy plugin validate .
mkdir -p /tmp/qs-import && ln -sfn "$OMARCHY_PATH/shell" /tmp/qs-import/qs
/usr/lib/qt6/bin/qmllint -I /tmp/qs-import *.qml
/usr/lib/qt6/bin/qmltestrunner -input test
python3 -m unittest discover -s test -p 'test_*.py'
```

A new version runs only after `omarchy restart shell`. Logs:
`journalctl --user | grep omarchy-pets`.

## Rules

- Errors surface. No fallback hides a failure; log with the `omarchy-pets:` prefix.
- Fix causes, not symptoms. Add logs when the cause is unknown.
- Comments: one line, ten words at most, only when needed.
- No dead code, no versioned APIs, no file over 1000 lines.
- Untrusted text renders with `textFormat: Text.PlainText`.
- Update this file when the stack, id, or direction changes.
