from core.nse import NSE


class Render:
    def master(self):
        nse = NSE()
        html = open('core/ui/index.html').read()
        html = html.replace("__scripts__",  "<script>" +
                            open('core/ui/main.js', 'r').read()+"</script>")
        html = html.replace("__css__",  "<style>" +
                            open('core/ui/main.css', 'r').read()+"</style>")
        html = html.replace("_last_modified_", nse.status['last_modified'])
        html = html.replace("_table_", nse.read_html())
        return html
