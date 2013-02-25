(function () {
    tinymce.create("tinymce.plugins.EmbedlyPlugin", {
        init: function (a, b) {
            this.editor = a;
            a.addCommand("mceEmbedlyLink", function () {
                var c = a.selection;
                if (c.isCollapsed() && !a.dom.getParent(c.getNode(), "A"))
                    return;
                a.windowManager.open({
                    file: b + "/embedly.htm",
                    width: 820 + parseInt(a.getLang("plonelink.delta_width", 0), 10),
                    height: 540 + parseInt(a.getLang("plonelink.delta_height", 0), 10),
                    inline: 1
                }, {
                    plugin_url: b
                });
            });
            a.addButton("embedlylink", {
                title: "Insert/Edit Embedly link",
                cmd: "mceEmbedlyLink",
                image: '/++resource++embedly.png'
            });
            a.onNodeChange.add(function(a, cm, n, co) {
                cm.setDisabled('embedlylink', co && n.nodeName != 'A');
                cm.setActive('embedlylink', n.nodeName == 'A' && !n.name);
            });
        },
        getInfo: function () {
            return {
                longname: "Embedly",
                author: "Roman Kozlovskyi",
                authorurl: "https://github.com/kroman0",
                infourl: "http://plone.org/products/collective.embedly/",
                version: tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });
    tinymce.PluginManager.add("embedly", tinymce.plugins.EmbedlyPlugin);
}());
