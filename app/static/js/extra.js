document.addEventListener("alpine:init", () => {
    Alpine.data('extraForm', () => ({
        materialprothemen: [],

        async loadData() {
            this.materialprothemen = await (await fetch('/material_count')).json()
        }
    }))
})