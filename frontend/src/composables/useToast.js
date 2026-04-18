import { reactive } from 'vue'

const toasts = reactive([])
let nextId = 0

export function useToast() {
  const addToast = (message, type = 'info', duration = 4000) => {
    const id = nextId++
    toasts.push({ id, message, type })
    setTimeout(() => removeToast(id), duration)
  }

  const removeToast = (id) => {
    const idx = toasts.findIndex(t => t.id === id)
    if (idx !== -1) toasts.splice(idx, 1)
  }

  return {
    toasts,
    success: (msg) => addToast(msg, 'success'),
    error: (msg) => addToast(msg, 'error'),
    info: (msg) => addToast(msg, 'info'),
    warning: (msg) => addToast(msg, 'warning'),
    remove: removeToast
  }
}
