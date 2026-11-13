.pragma library

// Stored entry wins; a reload injects stale settings.
function current(barConfig, id, injected, sections) {
  var layout = barConfig ? barConfig.layout : null
  if (!layout) return injected
  for (var r = 0; r < sections.length; r++) {
    // Facade arrays are Qt sequences; Array.isArray rejects them.
    var entries = layout[sections[r]] || []
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i]
      if (entry === id) return {}
      if (!entry || entry.id !== id) continue
      var settings = {}
      for (var key in entry) if (key !== "id") settings[key] = entry[key]
      return settings
    }
  }
  return injected
}
