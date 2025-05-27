// /transform/brainsResponse.ts
export function transformBrainsResponse(data: any) {
  return data.contents.sort(
    (a: any, b: any) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
  )
}
