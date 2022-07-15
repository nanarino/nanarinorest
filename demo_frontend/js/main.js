function range(s, e) {
    if (s > e) return []
    const arr = []
    for (let i = s; i < e; i++) {
        arr.push(i)
    }
    return arr
}
function check(id) {
    const el = document.querySelector(`.img_item[data-id='${id}']`)
    const els = Array.from(document.querySelectorAll(`.img_item`))
    const el_all = document.querySelector(`.img_all`)
    if (el.dataset['check'] === '1') {
        el.dataset['check'] = '0'
        el.src = '/img/uncheck.svg'
        el_all.dataset['check'] = '0'
        if (els.every(e => !(1 * e.dataset['check']))) {
            el_all.src = '/img/uncheck.svg'
        } else {
            el_all.src = '/img/checkall.svg'
        }
    } else {
        el.dataset['check'] = '1'
        el.src = '/img/checked.svg'
        if (els.every(e => 1 * e.dataset['check'])) {
            el_all.src = '/img/checked.svg'
        } else {
            el_all.src = '/img/checkall.svg'
            el_all.dataset['check'] = '1'
        }

    }
}
function checkAll() {
    const el_all = document.querySelector(`.img_all`)
    const els = Array.from(document.querySelectorAll(`.img_item`))
    if (el_all.dataset['check'] === '1') {
        el_all.dataset['check'] = '0'
        el_all.src = '/img/uncheck.svg'
        els.map(el => {
            el.dataset['check'] = '0'
            el.src = '/img/uncheck.svg'
        })
    } else {
        el_all.dataset['check'] = '1'
        el_all.src = '/img/checked.svg'
        els.map(el => {
            el.dataset['check'] = '1'
            el.src = '/img/checked.svg'
        })
    }
}
async function delone(id) {
    const res = await fetch(`http://127.0.0.1:8080/demos?id=${id}`, {
        cache: 'no-cache',
        method: "DELETE"
    })
    alert((await res.json()).msg)
    pagenum.dispatchEvent(new Event("change"))
}
async function delmany() {
    const els = Array.from(document.querySelectorAll(`.img_item`))
    const ids = els.filter(el => el.dataset['check'] === '1').map(el => el.dataset['id'])
    if (ids.length < 1) {
        alert("Pick at least one")
        return
    }
    const qs = ids.reduce((qs,v)=>(qs.append('id',v),qs), new URLSearchParams())
    const res = await fetch(`http://127.0.0.1:8080/demos?${qs}`, {
        cache: 'no-cache',
        method: "DELETE"
    })
    alert((await res.json()).msg)
    pagenum.dispatchEvent(new Event("change"))
}
async function update(id) {
    if (!id) {
        const els = Array.from(document.querySelectorAll(`.img_item`))
        const ids = els.filter(el => el.dataset['check'] === '1').map(el => el.dataset['id'])
        if (ids.length !== 1) {
            alert("You can only pick one")
            return
        }
        id = ids[0]
    }
    const data = await (await fetch(`http://127.0.0.1:8080/demo/${id}`)).json()
    subm.value = "update"
    markform_1.value = data.name
    markform_2.value = data.type
    markform_3.value = data.mark
    mark.style.display = "block"
    subm.onclick = async function () {
        const res = await fetch(`http://127.0.0.1:8080/demo/${id}`, {
            body: JSON.stringify({
                name: markform_1.value,
                type: markform_2.value,
                mark: markform_3.value,
            }),
            cache: 'no-cache',
            headers: { 'content-type': 'application/json' },
            method: "PUT"
        })
        const data = await res.json()
        mark.dispatchEvent(new Event('click'))
        alert(data.msg)
        this.onclick = null
        req()
    }
}
function create() {
    subm.value = "create"
    mark.style.display = "block"
    subm.onclick = async function () {
        const res = await fetch(`http://127.0.0.1:8080/demo`, {
            body: JSON.stringify({
                name: markform_1.value,
                type: markform_2.value,
                mark: markform_3.value,
            }),
            cache: 'no-cache',
            headers: { 'content-type': 'application/json' },
            method: "POST"
        })
        const data = await res.json()
        mark.dispatchEvent(new Event('click'))
        alert(data.msg)
        this.onclick = null
        pagenum.dispatchEvent(new Event("change"))
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
            index = location.hash.substring(1) * 1 || 1
            offset = (index - 1) * limit
            let search = new URLSearchParams()
            search.append("limit", limit)
            search.append("offset", offset)
            const res = await fetch(`http://127.0.0.1:8080/demos?${search}`)
            const data = await res.json()
            total = data.total
            length = Math.ceil(total / limit)
            allnum.innerHTML = total
            if(total){
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
                        <span><img class='img_item' onclick="check(${v.id})" data-id='${v.id}' data-check='0' src='/img/uncheck.svg'></span>
                        <span>${v.id}</span>
                        <span>${v.name}</span>
                        <span>${v.type}</span>
                        <span>${v.mark}</span>
                        <span>${v.create_at}</span>
                        <span><a onclick="update(${v.id})"><img src='/img/edit.svg'></a>&nbsp;&nbsp;<a onclick="delone(${v.id})"><img src='/img/del.svg'></a></span>
                    </li>
                `, `<li>
                        <span><img class='img_all' onclick="checkAll()" data-check='0' src='/img/uncheck.svg'></span>
                        <span><b>id</b></span>
                        <span><b>name</b></span>
                        <span><b>type</b></span>
                        <span><b>mark</b></span>
                        <span><b>create time</b></span>
                        <span><b>operation</b></span>
                </li>`)
            }else{
                list.innerHTML = `<li>
                    <span><img class='img_all' onclick="checkAll()" data-check='0' src='/img/uncheck.svg'></span>
                    <span><b>id</b></span>
                    <span><b>name</b></span>
                    <span><b>type</b></span>
                    <span><b>mark</b></span>
                    <span><b>create time</b></span>
                    <span><b>operation</b></span>
                </li>` + `<li><span></span><span></span><span></span><span>no more</span><span></span><span></span><span></span></li>`
            }
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
            let ld = document.createElement("li"), rd = document.createElement("li")
            ld.id = 'ld'
            rd.id = 'rd'
            ld.innerHTML = '...'
            rd.innerHTML = '...'
            ld.style.display = 'none'
            rd.style.display = 'none'
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
            prev.onclick = () => pagebtn[Math.max(0, index - 2)].onclick()
            next.onclick = () => pagebtn[Math.min(length - 1, index)].onclick()
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
