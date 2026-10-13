// Cumulative layer export for Photoshop
// Finds the lowest layer whose name contains a digit.
// name_0.png = all layers below it, name_1.png = adds that layer, name_2.png = adds the next, etc.
// Top-level layers only (a group counts as one layer).
//
// I have this installed as a 
//
// To install it, run
//
//     % sudo cp ~/clean/bin/cumulative_layer_export.jsx "/Applications/Adobe Photoshop [VERSION]/Presets/Scripts/"
//
// It then appears under File > Scripts

#target photoshop

(function () {
    if (!app.documents.length) { alert("No document open."); return; }

    var doc = app.activeDocument;

    // Collect top-level layers bottom -> top
    var layers = [];
    for (var i = doc.layers.length - 1; i >= 0; i--) layers.push(doc.layers[i]);

    // Find lowest layer with a digit in its name
    var start = -1;
    for (var i = 0; i < layers.length; i++) {
        if (/\d/.test(layers[i].name)) { start = i; break; }
    }
    if (start === -1) { alert("No layer name contains a digit."); return; }
    // If start === 0, name_0.png has no layers visible (fully transparent)

    // Output to the PSD's folder; unsaved document is a fatal error
    var folder;
    try { folder = doc.path; } catch (e) { alert("Save the document first."); return; }

    // Remember original visibility
    var orig = [];
    for (var i = 0; i < layers.length; i++) orig.push(layers[i].visible);

    var base = doc.name.replace(/\.[^.]+$/, "");
    var opts = new PNGSaveOptions();
    opts.compression = 9;
    opts.interlaced = false;

    // Zero-pad numbers to the width of the highest index
    var total = layers.length - start + 1;
    var digits = String(total - 1).length;
    function pad(n) { var s = String(n); while (s.length < digits) s = "0" + s; return s; }

    var count = 0;
    try {
        // n = index of topmost visible layer
        for (var n = start - 1; n < layers.length; n++) {
            for (var j = 0; j < layers.length; j++) layers[j].visible = (j <= n);
            var f = new File(folder.fsName + "/" + base + "_" + pad(n - start + 1) + ".png");
            doc.saveAs(f, opts, true, Extension.LOWERCASE);
            count++;
        }
    } finally {
        for (var i = 0; i < layers.length; i++) layers[i].visible = orig[i];
    }

    alert("Exported " + count + " PNGs.");
})();
