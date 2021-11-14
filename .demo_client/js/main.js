function range(s, e) {
    if (s > e) return []
    let arr = []
    for (let i = s; i < e; i++) {
        arr.push(i)
    }
    return arr
}
function check(id) {
    let el = document.querySelector(`.img_item[data-id='${id}']`)
    let els = Array.from(document.querySelectorAll(`.img_item`))
    let el_all = document.querySelector(`.img_all`)
    if (el.dataset['check'] === '1') {
        el.dataset['check'] = '0'
        el.src = '/img/未选.svg'
        el_all.dataset['check'] = '0'
        if (els.every(e => !(1 * e.dataset['check']))) {
            el_all.src = '/img/未选.svg'
        } else {
            el_all.src = '/img/增加.svg'
        }
    } else {
        el.dataset['check'] = '1'
        el.src = '/img/已选.svg'
        if (els.every(e => 1 * e.dataset['check'])) {
            el_all.src = '/img/已选.svg'
        } else {
            el_all.src = '/img/增加.svg'
            el_all.dataset['check'] = '1'
        }

    }
}
function checkAll() {
    let el_all = document.querySelector(`.img_all`)
    let els = Array.from(document.querySelectorAll(`.img_item`))
    if (el_all.dataset['check'] === '1') {
        el_all.dataset['check'] = '0'
        el_all.src = '/img/未选.svg'
        els.map(el => {
            el.dataset['check'] = '0'
            el.src = '/img/未选.svg'
        })
    } else {
        el_all.dataset['check'] = '1'
        el_all.src = '/img/已选.svg'
        els.map(el => {
            el.dataset['check'] = '1'
            el.src = '/img/已选.svg'
        })
    }
}
async function delone(id) {
    let res = await fetch(`http://127.0.0.1:8080/demos`, {
        body: JSON.stringify({
            "id_set": [id]
        }),
        cache: 'no-cache',
        headers: { 'content-type': 'application/json' },
        method: "DELETE"
    })
    let data = await res.json()
    console.log(data)
    alert(data.msg)
    let change = new Event("change")
    pagenum.dispatchEvent(change)
}
async function delmany() {
    let els = Array.from(document.querySelectorAll(`.img_item`))
    let ids = els.filter(el => el.dataset['check'] === '1').map(el => el.dataset['id'])
    if (ids.length < 1) {
        alert("只能选择后才能删除")
        return
    }
    let res = await fetch(`http://127.0.0.1:8080/demos`, {
        body: JSON.stringify({
            "id_set": ids
        }),
        cache: 'no-cache',
        headers: { 'content-type': 'application/json' },
        method: "DELETE"
    })
    let data = await res.json()
    console.log(data)
    alert(data.msg)
    let change = new Event("change")
    pagenum.dispatchEvent(change)
}
async function update(id) {
    if (!id) {
        let els = Array.from(document.querySelectorAll(`.img_item`))
        let ids = els.filter(el => el.dataset['check'] === '1').map(el => el.dataset['id'])
        if (ids.length !== 1) {
            alert("只能在选中一个的时候修改")
            return
        } else {
            id = ids[0]
        }

    }
    let res = await fetch(`http://127.0.0.1:8080/demo/${id}`)
    let data = await res.json()
    console.log(data);
    subm.value = "修改"
    markform_1.value = data.name
    markform_2.value = data.type
    markform_3.value = data.mark
    mark.style.display = "block"
    subm.onclick = async function () {
        let res = await fetch(`http://127.0.0.1:8080/demo`, {
            body: JSON.stringify({
                id,
                name: markform_1.value,
                type: markform_2.value,
                mark: markform_3.value,
            }),
            cache: 'no-cache',
            headers: { 'content-type': 'application/json' },
            method: "PUT"
        })
        let data = await res.json()
        console.log(data);
        let event = new Event('click')
        mark.dispatchEvent(event)
        alert(data.msg)
        this.onclick = null
        req()
    }
}
function create() {
    subm.value = "创建"
    mark.style.display = "block"
    subm.onclick = async function () {
        let res = await fetch(`http://127.0.0.1:8080/demo`, {
            body: JSON.stringify({
                name: markform_1.value,
                type: markform_2.value,
                mark: markform_3.value,
            }),
            cache: 'no-cache',
            headers: { 'content-type': 'application/json' },
            method: "POST"
        })
        let data = await res.json()
        console.log(data);
        let event = new Event('click')
        mark.dispatchEvent(event)
        alert(data.msg)
        this.onclick = null
        let change = new Event("change")
        pagenum.dispatchEvent(change)
    }
}

window.onload = async () => {
    mark.onclick = function (e) {
        if (e.target.id != 'mark') return
        markform_1.value = ''
        markform_2.value = ''
        markform_3.value = ''
        mark.style.display = 'none'
    }

    void async function pageInit() {
        let limit = 10
        let index, offset, total, length
        let isInited = false
        window.req = async function () {
            index = location.hash.substr(1) * 1 || 1
            offset = (index - 1) * limit
            let search = new URLSearchParams()
            search.append("limit", limit)
            search.append("offset", offset)
            let res = await fetch(`http://127.0.0.1:8080/demos?${search}`)
            let data = await res.json()
            total = data.total
            length = Math.ceil(total / limit)
            allnum.innerHTML = total
            if(index<1){
                index = 1
                location.hash = '#1'
                return
            }else if(index>length){
                index = length
                location.hash = '#' + length
                return
            }
            list.innerHTML = data.slice_data.reduce((html, v) => html + `
                <li>
                    <span><img class='img_item' onclick="check(${v.id})" data-id='${v.id}' data-check='0' src='/img/未选.svg'></span>
                    <span>${v.id}</span>
                    <span>${v.name}</span>
                    <span>${v.type}</span>
                    <span>${v.mark}</span>
                    <span>${v.create_at}</span>
                    <span><a onclick="update(${v.id})"><img src='/img/修改.svg'>修改</a> <a onclick="delone(${v.id})"><img src='/img/删除.svg'>删除</a></span>
                </li>
            `, `<li>
                    <span><img class='img_all' onclick="checkAll()" data-check='0' src='/img/未选.svg'></span>
                    <span><b>编号</b></span>
                    <span><b>名称</b></span>
                    <span><b>类型</b></span>
                    <span><b>备注</b></span>
                    <span><b>创建时间</b></span>
                    <span><b>操作</b></span>
            </li>`)
        }
        await req()
        window.onhashchange = async () => {
            if (location.hash === '') {
                location.hash = '#1'
                return
            }
            if (!isInited) {
                isInited = true
                return
            }
            await req()
        }
        window.onhashchange()
        const btninit = () => {
            window.pagebtn = []

            for (let i of range(0, length)) {
                let btn = document.createElement("li")
                btn.onclick = function () {
                    if (i == 0) {
                        prev.className = 'tra'
                    } else {
                        prev.className = ''
                    }
                    if (i == length - 1) {
                        next.className = 'tra'
                    } else {
                        next.className = ''
                    }
                    pagebtn[index - 1].id = ''
                    location.hash = `#` + (1 * i + 1)
                    btn.id = 'theone'
                    pageto.value = i + 1
                    omit(1 * i + 1)
                }
                btn.className = 'page'
                btn.innerHTML = i + 1
                page.insertBefore(btn, next)
                pagebtn.push(btn)
            }
            let ld = document.createElement("li")
            let rd = document.createElement("li")
            ld.style.display = 'none'
            rd.style.display = 'none'
            ld.id = 'ld'
            rd.id = 'rd'
            ld.innerHTML = '...'
            rd.innerHTML = '...'
            page.insertBefore(ld, pagebtn[1])
            page.insertBefore(rd, pagebtn[length - 1])
            function omit(i) {
                for (let i of pagebtn) {
                    i.style.display = `block`
                }
                let arr
                arr = range(2, Math.min(i - 2, length - 5))
                if (arr.length) {
                    for (let i of arr) {
                        pagebtn[i - 1].style.display = `none`
                    }
                    ld.style.display = 'block'
                } else {
                    ld.style.display = 'none'
                }
                arr = range(Math.max(7, i + 3), length)
                if (arr.length) {
                    for (let i of arr) {
                        pagebtn[i - 1].style.display = `none`
                    }
                    rd.style.display = 'block'
                } else {
                    rd.style.display = 'none'
                }
            }
            pagebtn[index - 1]?.click()
            prev.onclick = function () {
                pagebtn[Math.max(0, index - 2)].onclick()
            }
            next.onclick = function () {
                pagebtn[Math.min(length - 1, index)].onclick()
            }
        }
        btninit()
        pagenum.onchange = async function () {
            pagebf = index / length//%
            limit = Number.parseInt(this.value)
            if (Number.isNaN(limit)) limit = 10
            let delre = [...document.getElementsByClassName("page")]
            delre.push(document.getElementById('ld'))
            delre.push(document.getElementById('rd'))
            for (const el of delre) {
                page.removeChild(el)
            }
            location.hash = '#' + Math.ceil(total * pagebf / limit)
            await req()
            btninit()
        }
        pageto.onblur = async function () {
            let numto = this.value * 1
            if (numto && numto <= length) {
                window.pagebtn[numto - 1].click()
            } else {
                this.value = ''
            }
        }
    }()
}