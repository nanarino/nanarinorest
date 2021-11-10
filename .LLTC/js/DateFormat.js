/**
 *
 *本文件只针对日期格式做兼容IE7的处理
 *如"y/M/d" "y-M-d"  而不处理时刻
 *
 *注意 本文件的代码会污染Date的原型链
 *按需引入时需要注意调用关系
 */


/**
 * @desc 日期格式化 不改变原对象 
 *       原版格式中 yyyy-MM-dd[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]
 *       只会支持日期 yyyy-MM-dd ，时分秒时区将不做处理
 * @param date_string 格式字符串中的"yyyy"，'MM'，'dd'将会被替换；
 *                    注意，不区分大小写。即使MM写成了mm也不会被替换成分钟而是月份
 * @return -> 返回格式如 '2004-06-18'
 */
Date.prototype.format = function (date_string) {
    return (date_string
        .replace(/YYYY/ig, this.getFullYear())
        .replace(/MM/ig, ("0" + (this.getMonth() + 1)).slice(-2))
        .replace(/DD/ig, ("0" + this.getDate()).slice(-2))
    )

}


/**
 * @desc 日期按分隔符拼接 不改变原对象
 * @param connchar 分隔符 默认'-'
 * @return -> 返回格式如 '2004-06-18'
 */
Date.prototype.join = function (connchar) {
    return [this.getFullYear(), ("0" + (this.getMonth() + 1)).slice(-2), ("0" + this.getDate()).slice(-2)].join(connchar || "-")
}


/**
 * @desc 针对IE7兼容的日期对象生成 静态方法
 * @param dateStr 如'2004-06-05' （兼容不写0如'2004-6-5'，纯数字'20040605'，也兼容多种连接符）
 * @return -> 参数如上的返回值将是 [date] Sat Jun 5 00:00:00 UTC+0800 2004
 */
Date.from = function (dateStr) {
    if (!isNaN(+dateStr) && (dateStr.length === 8)) {
        dateStr = [dateStr.slice(0, 4), dateStr.slice(4, 6), dateStr.slice(6, 8)].join('/')
    }
    var _newDate = new Date(dateStr.replace(/\W/g, "/"))
    if (isNaN(_newDate)) throw new Error('时间格式错误');
    return _newDate
}


/**
 * @desc 判断日期是否符合格式
 * @param -> string 待检验的日期字符串dateStr
 * @return -> boolean
 */
Date.isDateStr = function (dateStr) {
    try {
        this.from(dateStr)
    } catch (e) {
        return false
    }
    return true
}


/**
 * @desc 日期区间计算及格式化 静态方法
 * @param start  [object Date]对象，起点
 * @param stop  [object Date]对象，终点
 * @param step  正整数，默认1，步长
 * @return -> Array<[object Date]>
 */
Date.dateRange = function (start, stop, step) {
    var _dateRange = [];
    for (var i = start.getTime(); i < stop.getTime(); i += 86400000 * (step || 1)) {
        _dateRange.push(new Date(i));
    }
    return _dateRange
}