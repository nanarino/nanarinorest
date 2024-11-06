const add_btn = document.getElementById("add")
const del_btn = document.getElementById("del")

const table = document.getElementById("table")
const pagination = document.getElementById("pagination")
const pagenum = document.getElementById("pagenum")

let limit = 10,
    current,
    offset,
    total,
    length
const fetch_table_data = async function () {
    table.active = true // 请求并渲染table数据 返回是否需要去前一页
    current = location.hash.substring(1) * 1 || 1
    offset = (current - 1) * limit
    const res = await fetch(`/demos?${new URLSearchParams({ limit, offset })}`)
    const data = await res.json()
    total = data.total
    length = Math.ceil(total / limit)
    ;[...document.querySelectorAll("ui5-table-row")].forEach(row => table.removeChild(row))
    if (current > length) return (current = length)
    data.slice_data.forEach(v => {
        const new_row = document.createElement("ui5-table-row")
        new_row.id = v.id
        new_row.innerHTML = `
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
        table.appendChild(new_row)
    })
    table.active = false
}

// 更新分页器参数
const set_pagination_props = () => {
    pagination.total = length
    pagination.current = current
    pagination.onChange = i => (location.hash = "#" + i)
}

const toast = document.getElementById("toast")
const dialog = document.getElementById("dialog")
const form_type = dialog.querySelector(`form #type`)
const form_name = dialog.querySelector(`form #name`)
const form_mark = dialog.querySelector(`form #mark`)
const form_data = {
    get type() {
        return form_type.value
    },
    get name() {
        return form_name.value
    },
    get mark() {
        return form_mark.value
    },
}
const submit_btn = dialog.querySelector(`#submit`)
const cancel_btn = dialog.querySelector(`#cancel`)

let selected_rows = []
// 绑定表格选中行修改
table.addEventListener("selection-change", function (e) {
    selected_rows = e?.detail?.selectedRows ?? []
    if (selected_rows.length) {
        del_btn.removeAttribute("disabled")
    } else {
        del_btn.setAttribute("disabled", "disabled")
    }
})

del_btn.addEventListener("click", async () => {
    // 绑定表头上删除按钮点击
    const qs = selected_rows.reduce((qs, row) => (qs.append("id", row.id), qs), new URLSearchParams())
    const res = await fetch(`/demos?${qs}`, {
        cache: "no-cache",
        method: "DELETE",
    })
    toast.innerText = (await res.json()).msg
    toast.open = true
    pagenum.dispatchEvent(new Event("change"))
})

add_btn.addEventListener("click", () => {
    dialog.setAttribute(`header-text`, `Create Item`)
    dialog.open = true
})

// 绑定模态框提交按钮点击
submit_btn.addEventListener("click", async () => {
    const title = dialog.getAttribute(`header-text`)
    if (title === `Create Item`) {
        const res = await fetch(`/demo`, {
            body: JSON.stringify({ ...form_data }),
            cache: "no-cache",
            headers: { "content-type": "application/json" },
            method: "POST",
        })
        toast.innerText = (await res.json()).msg
    } else {
        const id = title.replace(/^Update Item /, "")
        const res = await fetch(`/demo/${id}`, {
            body: JSON.stringify({ ...form_data }),
            cache: "no-cache",
            headers: { "content-type": "application/json" },
            method: "PUT",
        })
        toast.innerText = (await res.json()).msg
    }
    toast.open = true
    dialog.open = false
    form_name.value = form_type.value = form_mark.value = ""
    pagenum.dispatchEvent(new Event("change"))
})

// 绑定模态框取消按钮点击
cancel_btn.addEventListener("click", () => (dialog.open = false))

Object.assign(window, {
    async onload() {
        this.afterhashchange = set_pagination_props
        this.onhashchange = async () => {
            if (!location.hash) return (location.hash = "#1")
            if (location.hash === "#NaN") return (location.hash = "#1")
            const is_goto_prev = await fetch_table_data()
            if (is_goto_prev) {
                this.afterhashchange = set_pagination_props
                return (location.hash = "#" + current)
            }
            table.fireEvent("selection-change") // 清除已选择的行
            await this.afterhashchange?.()
            this.afterhashchange = null
        }
        this.onhashchange()

        // 绑定下拉框改变
        pagenum.addEventListener(`change`, async e => {
            limit = Number.parseInt(e?.detail?.selectedOption?.value ?? limit)
            const wanna = Math.ceil((total * (current / length)) / limit)
            this.afterhashchange = set_pagination_props
            if (wanna === current) {
                this.onhashchange()
            } else {
                location.hash = "#" + wanna
            }
        })
    },
    async remove(id) {
        const res = await fetch(`/demos?id=${id}`, {
            cache: "no-cache",
            method: "DELETE",
        })
        toast.innerText = (await res.json()).msg
        toast.open = true
        pagenum.dispatchEvent(new Event("change"))
    },
    async update(item) {
        form_name.value = item.name
        form_type.value = item.type
        form_mark.value = item.mark
        dialog.setAttribute(`header-text`, `Update Item ${item.id}`)
        dialog.open = true
    },
})
