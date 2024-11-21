let data_total = 0
const TABLE = document.querySelector("ui5-table")

// 绑定当前页改变
const PAGE_NUM_SELECT = document.querySelector("ui5-pagination")
PAGE_NUM_SELECT.onChange = i => (location.hash = "#" + i)

// 绑定下拉框改变
const PAGE_SIZE_SELECT = document.querySelector("ui5-select")
PAGE_SIZE_SELECT.addEventListener("change", async () => {
    const limit = PAGE_SIZE_SELECT.value
    const current = Math.ceil((data_total * (PAGE_NUM_SELECT.current / PAGE_NUM_SELECT.total)) / limit)
    PAGE_NUM_SELECT.onChange(current)
})
// 清空表格
TABLE._clean = () => {
    ;[...TABLE.querySelectorAll("ui5-table-row")].forEach(row => TABLE.removeChild(row))
    TABLE.fireEvent("selection-change") // 清除已选择的行
}
// 渲染表格
TABLE._update = async (
    offset = (PAGE_NUM_SELECT.current - 1) * PAGE_SIZE_SELECT.value,
    limit = PAGE_SIZE_SELECT.value
) => {
    TABLE.active = true
    const res = await fetch(`/demos?${new URLSearchParams({ limit, offset })}`)
    const data = await res.json()
    data_total = data.total
    PAGE_NUM_SELECT.total = Math.ceil(data.total / limit)
    TABLE._clean()
    if (PAGE_NUM_SELECT.current > PAGE_NUM_SELECT.total) return false
    data.slice_data.forEach(v => {
        const ROW = document.createElement("ui5-table-row")
        ROW.dataset.id = v.id
        ROW.innerHTML = `
            <ui5-table-cell>${v.id}</ui5-table-cell>
            <ui5-table-cell>${v.name}</ui5-table-cell>
            <ui5-table-cell>${v.type}</ui5-table-cell>
            <ui5-table-cell>${v.mark}</ui5-table-cell>
            <ui5-table-cell>${v.create_at}</ui5-table-cell>
            <ui5-table-cell>
                <ui5-button design="Attention" icon="edit" onclick='update(${JSON.stringify(v)})'></ui5-button>
                <ui5-button design="Negative" icon="delete" onclick='remove(${v.id})'></ui5-button>
            </ui5-table-cell>
        `
        TABLE.appendChild(ROW)
    })
    TABLE.active = false
}

// 彈框和提示
const TOAST = document.getElementById("toast")
const DIALOG = document.querySelector("ui5-dialog")
// 表單
const FORM = {
    _type: DIALOG.querySelector("#type"),
    _name: DIALOG.querySelector("#name"),
    _mark: DIALOG.querySelector("#mark"),
    set data(o) {
        this._type.value = o?.type ?? ""
        this._name.value = o?.name ?? ""
        this._mark.value = o?.mark ?? ""
    },
    get data() {
        return {
            type: this._type.value,
            name: this._name.value,
            mark: this._mark.value,
        }
    },
}

Object.assign(window, {
    onload() {
        if (!location.hash) return (location.hash = "#1")
        if (location.hash === "#NaN") return (location.hash = "#1")
        if (location.hash === "#Infinity") return (location.hash = "#1")
        PAGE_NUM_SELECT.current = Number.parseInt(location.hash.substring(1)) || 1
        TABLE._update()
    },
    onhashchange() {
        this.onload()
    },
    async remove(id) {
        const res = await fetch(`/demos?id=${id}`, {
            cache: "no-cache",
            method: "DELETE",
        })
        TOAST.innerText = (await res.json()).msg
        TOAST.open = true
        TABLE._update()
    },
    async update(item) {
        FORM.data = item
        DIALOG.setAttribute(`header-text`, `Update Item ${item.id}`)
        DIALOG.dataset.id = item.id
        DIALOG.open = true
    },
})

// 绑定表头上新增按钮点击
const APPEND_BTN = document.querySelector("header ui5-button[icon=add]")
APPEND_BTN.onclick = () => {
    DIALOG.setAttribute(`header-text`, `Create Item`)
    DIALOG.dataset.id = ""
    DIALOG.open = true
}


// 绑定表格选中行修改
const SELECTED_ROWS = []
TABLE.addEventListener("selection-change", function (e) {
    SELECTED_ROWS.splice(0, Infinity, ...(e?.detail?.selectedRows ?? []))
    if (SELECTED_ROWS.length) {
        REMOVE_BTN.removeAttribute("disabled")
    } else {
        REMOVE_BTN.setAttribute("disabled", "disabled")
    }
})

// 绑定表头上删除按钮点击
const REMOVE_BTN = document.querySelector("header ui5-button[icon=delete]")
REMOVE_BTN.onclick = async () => {
    const qs = SELECTED_ROWS.reduce((qs, row) => (qs.append("id", row.dataset.id), qs), new URLSearchParams())
    const res = await fetch(`/demos?${qs}`, {
        cache: "no-cache",
        method: "DELETE",
    })
    TOAST.innerText = (await res.json()).msg
    TOAST.open = true
    TABLE._update()
}

// 绑定模态框提交按钮点击
const SUBMIT_BTN = DIALOG.querySelector(`#submit`)
SUBMIT_BTN.onclick = async () => {
    const id = DIALOG.dataset.id
    if (!id) {
        const res = await fetch(`/demo`, {
            body: JSON.stringify(FORM.data),
            cache: "no-cache",
            headers: { "content-type": "application/json" },
            method: "POST",
        })
        TOAST.innerText = (await res.json()).msg
    } else {
        const res = await fetch(`/demo/${id}`, {
            body: JSON.stringify(FORM.data),
            cache: "no-cache",
            headers: { "content-type": "application/json" },
            method: "PUT",
        })
        TOAST.innerText = (await res.json()).msg
    }
    TOAST.open = true
    DIALOG.open = false
    FORM.data = {}
    TABLE._update()
}

// 绑定模态框取消按钮点击
const CANCEL_BTN = DIALOG.querySelector(`#cancel`)
CANCEL_BTN.onclick = () => (DIALOG.open = false)
