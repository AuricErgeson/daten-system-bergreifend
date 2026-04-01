document.addEventListener("alpine:init", () => {
Alpine.data('mainForm',() =>({
    themen:[],
    kategorien: [],
    benutzer: [],
    tags:[],
    msg: '',
    ok: false,

    async init() {
        this.themen = await (await fetch('/themen')).json()
        this.kategorien = await (await fetch('/kategorie')).json()
        this.benutzer = await (await fetch('/users')).json()
        this.tags = await (await fetch('/tag')).json()
    },

        async upload(e) {
            this.msg = 'Datei wird verarbeitet ...'
            const form = new FormData(e.target)
            try {
                const res = await fetch('/material', {method: 'POST', body: form})
                if (!res.ok) throw new Error((await res.json()).detail)
                const data = await res.json()
                this.ok = true
                this.msg = '>>> Upload erfolgreich abgeschlossen!\n'
                    + '    Titel: ' + data.titel + '\n'
                    + '    Datei: ' + data.dateiname + '\n'
                    + '    Größe: ' + data.dateigroesse + ' Bytes\n'
                    + '    In DB: ' + (data.is_in_database ? 'Ja' : 'Nein (Dateisystem)')
            } catch (err) {
                this.ok = false
                this.msg = '>>> FEHLER: ' + err.message
            }
        }


}))
})