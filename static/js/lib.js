export function range(s, e) {
  if (s > e) return []
  const arr = []
  for (let i = s; i < e; i++) {
    arr.push(i)
  }
  return arr
}