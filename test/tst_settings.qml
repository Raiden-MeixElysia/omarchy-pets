import QtQuick
import QtTest
import "../Settings.js" as Settings

TestCase {
  name: "Settings"

  readonly property string pluginId: "io.github.raiden-meixelysia.omarchy-pets"
  // Util.barSections in Omarchy 4.5.
  readonly property var sections: ["left", "centerBegin", "center", "centerEnd", "right", "tray"]

  // createObject turns arrays into Qt sequences.
  Component {
    id: facade
    QtObject { property var barConfig }
  }

  function barConfig(right) {
    return { position: "top", layout: { left: ["omarchy"], center: ["clock"], right: right } }
  }

  function current(config, injected) {
    return Settings.current(config, pluginId, injected, sections)
  }

  function test_stored_entry_wins_over_the_injected_copy() {
    var stale = { petId: "guga", pinned: false, pinnedX: 10 }
    var config = barConfig(["tray", { id: pluginId, petId: "remiel", pinned: true, pinnedX: 34 }])
    compare(current(config, stale), { petId: "remiel", pinned: true, pinnedX: 34 })
  }

  function test_entry_found_in_any_region() {
    var config = { layout: { left: [{ id: "other", smooth: true }, { id: pluginId, smooth: false }], center: [], right: [] } }
    compare(current(config, { smooth: true }), { smooth: false })
  }

  function test_entry_found_in_every_section_the_shell_writes() {
    for (var i = 0; i < sections.length; i++) {
      var layout = {}
      layout[sections[i]] = [{ id: pluginId, pinned: true }]
      compare(current({ layout: layout }, { pinned: false }), { pinned: true }, sections[i])
    }
  }

  function test_entry_found_in_a_facade_built_config() {
    var built = facade.createObject(null, { barConfig: barConfig(["tray", { id: pluginId, pinned: true }]) })
    verify(!Array.isArray(built.barConfig.layout.right))
    compare(current(built.barConfig, { pinned: false }), { pinned: true })
    built.destroy()
  }

  function test_string_entry_has_no_settings() {
    compare(current(barConfig([pluginId]), { pinned: false }), {})
  }

  function test_injected_copy_when_the_config_lacks_the_entry() {
    var injected = { pinned: false }
    compare(current(barConfig(["tray"]), injected), injected)
    compare(current({ position: "top" }, injected), injected)
    compare(current(null, injected), injected)
  }
}
