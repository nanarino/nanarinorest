import "@ui5/webcomponents-icons/dist/AllIcons.js"
import "@ui5/webcomponents/dist/Button.js"
import "@ui5/webcomponents/dist/Table.js"
import "@ui5/webcomponents/dist/TableColumn.js"
import "@ui5/webcomponents/dist/TableRow.js"
import "@ui5/webcomponents/dist/TableCell.js"
import "@ui5/webcomponents/dist/Select.js"
import "@ui5/webcomponents/dist/Option.js"
import "@ui5/webcomponents/dist/Toast.js"
import "@ui5/webcomponents/dist/Dialog.js"
import "@ui5/webcomponents/dist/Label.js"
import "@ui5/webcomponents/dist/Input.js"
import { range } from "./lib.js"

const add_btn = document.getElementById('add')
const del_btn = document.getElementById('del')

const table = document.getElementById('table')
const page = document.getElementById('page')
const pagenum = document.getElementById('pagenum')
const prev = document.getElementById('prev')
const next = document.getElementById('next')

const toast = document.getElementById('toast')
const dialog = document.getElementById('dialog')
const form_type = dialog.querySelector(`form #type`)
const form_name = dialog.querySelector(`form #name`)
const form_mark = dialog.querySelector(`form #mark`)
const submit_btn = dialog.querySelector(`#submit`)
const cancel_btn = dialog.querySelector(`#cancel`)

let selected_rows = []
table.addEventListener('selection-change', function (e) {
  selected_rows = e.detail.selectedRows
  if (selected_rows.length) {
    del_btn.removeAttribute('disabled')
  } else {
    del_btn.setAttribute('disabled', 'disabled')
  }
})

del_btn.addEventListener('click', async () => {
  const qs = selected_rows.reduce((qs, row) => (qs.append('id', row.id), qs), new URLSearchParams())
  const res = await fetch(`/demos?${qs}`, {
    cache: 'no-cache',
    method: "DELETE"
  })
  toast.innerText = (await res.json()).msg
  toast.show()
  pagenum.dispatchEvent(new Event("change"))
})

add_btn.addEventListener('click', () => {
  dialog.setAttribute(`header-text`, `Create Item`)
  dialog.show()
})

submit_btn.addEventListener('click', async () => {
  const title = dialog.getAttribute(`header-text`)
  if (title === `Create Item`) {
    const res = await fetch(`/demo`, {
      body: JSON.stringify({
        name: form_name.value,
        type: form_type.value,
        mark: form_mark.value,
      }),
      cache: 'no-cache',
      headers: { 'content-type': 'application/json' },
      method: "POST"
    })
    toast.innerText = (await res.json()).msg
  } else {
    const id = title.replace(/^Update Item /, '')
    const res = await fetch(`/demo/${id}`, {
      body: JSON.stringify({
        name: form_name.value,
        type: form_type.value,
        mark: form_mark.value,
      }),
      cache: 'no-cache',
      headers: { 'content-type': 'application/json' },
      method: "PUT"
    })
    toast.innerText = (await res.json()).msg
  }
  toast.show()
  dialog.close()
  form_name.value = ''
  form_type.value = ''
  form_mark.value = ''
  pagenum.dispatchEvent(new Event("change"))
})

cancel_btn.addEventListener('click', () => dialog.close())

window.onload = async () => {
  void async function pageInit() {
    let limit = 10, index, offset, total, length, isInited = false
    window.req = async function () {
      table.active = true
      index = location.hash.substring(1) * 1 || 1
      offset = (index - 1) * limit
      const res = await fetch(`/demos?${new URLSearchParams({ limit, offset })}`)
      const data = await res.json()
      total = data.total
      length = Math.ceil(total / limit)
      if (index < 1) {
        index = 1
        location.hash = '#1'
        return
      } else if (index > length) {
        index = length
        location.hash = '#' + length
        return
      }
      ;[...document.querySelectorAll("ui5-table-row")].forEach(row => table.removeChild(row))
      data.slice_data.forEach(v => {
        const new_row = document.createElement('ui5-table-row')
        new_row.id = v.id
        new_row.innerHTML = `
          <ui5-table-cell>${v.id}</ui5-table-cell>
          <ui5-table-cell>${v.name}</ui5-table-cell>
          <ui5-table-cell>${v.type}</ui5-table-cell>
          <ui5-table-cell>${v.mark}</ui5-table-cell>
          <ui5-table-cell>${v.create_at}</ui5-table-cell>
          <ui5-table-cell>
            <ui5-button design="Attention" icon="edit" onclick='update(${JSON.stringify(v)})'></ui5-button>
            <ui5-button design="Negative" icon="delete" onclick='delone(${v.id})'></ui5-button>
          </ui5-table-cell>
        `
        table.appendChild(new_row)
      })
      table.active = false
    }
    await req()
    window.onhashchange = async () => {
      if (location.hash === '') return location.hash = '#1'
      if (!isInited) return isInited = true
      await req()
    }
    window.onhashchange()
    const btninit = () => {
      const page_btn = []
      for (let i of range(0, length)) {
        let btn = document.createElement("ui5-button")
        btn.addEventListener('click', function () {
          if (i == 0) {
            prev.setAttribute('disabled', 'disabled')
          } else {
            prev.removeAttribute('disabled')
          }
          if (i == length - 1) {
            next.setAttribute('disabled', 'disabled')
          } else {
            next.removeAttribute('disabled')
          }
          page_btn[index - 1].design = 'Default'
          location.hash = `#` + (1 * i + 1)
          btn.design = "Emphasized"
          omit(1 * i + 1)
        })
        btn.className = 'page'
        btn.innerText = i + 1
        page.insertBefore(btn, next)
        page_btn.push(btn)
      }

      const ld = document.createElement("ui5-button"), rd = document.createElement("ui5-button")
      ld.id = 'ld'
      rd.id = 'rd'
      ld.innerText = '...'
      rd.innerText = '...'
      ld.design = 'Transparent'
      rd.design = 'Transparent'
      ld.style.display = 'none'
      rd.style.display = 'none'
      ld.setAttribute('disabled', 'disabled')
      rd.setAttribute('disabled', 'disabled')
      page.insertBefore(ld, page_btn[1])
      page.insertBefore(rd, page_btn[length - 1])

      function omit(i) {
        for (let i of page_btn) {
          i.style.display = `inline-block`
        }
        let arr
        arr = range(2, Math.min(i - 2, length - 5))
        if (arr.length) {
          for (let i of arr) {
            page_btn[i - 1].style.display = `none`
          }
          ld.style.display = 'inline-block'
        } else {
          ld.style.display = 'none'
        }
        arr = range(Math.max(7, i + 3), length)
        if (arr.length) {
          for (let i of arr) {
            page_btn[i - 1].style.display = `none`
          }
          rd.style.display = 'inline-block'
        } else {
          rd.style.display = 'none'
        }
      }

      page_btn[index - 1]?.dispatchEvent(new Event(`click`))
      prev.onclick = () => page_btn[Math.max(0, index - 2)]?.dispatchEvent(new Event(`click`))
      next.onclick = () => page_btn[Math.min(length - 1, index)]?.dispatchEvent(new Event(`click`))
    }
    btninit()

    pagenum.addEventListener(`change`, async function (e) {
      limit = Number.parseInt(e?.detail?.selectedOption?.value ?? limit)
        ;[...document.getElementsByClassName("page"), document.getElementById('ld'), document.getElementById('rd')].forEach(el => page.removeChild(el))
      location.hash = '#' + Math.ceil(total * (index / length) / limit)
      await req()
      btninit()
    })
  }()
}

Object.assign(window, {
  async delone(id) {
    const res = await fetch(`/demos?id=${id}`, {
      cache: 'no-cache',
      method: "DELETE"
    })
    toast.innerText = (await res.json()).msg
    toast.show()
    pagenum.dispatchEvent(new Event("change"))
  },
  async update(item) {
    form_name.value = item.name
    form_type.value = item.type
    form_mark.value = item.mark
    dialog.setAttribute(`header-text`, `Update Item ${item.id}`)
    dialog.show()
  }
})