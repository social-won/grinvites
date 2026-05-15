import { ApiEvent } from '@/lib/types'

export const formatDayHeader = (date: Date): string =>
  date.toLocaleDateString(undefined, {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  })

export const formatTimeRange = (
  start: string,
  end: string | null
): string => {
  const startDate = new Date(start)
  const startStr = startDate.toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  })
  if (!end) return startStr
  const endStr = new Date(end).toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  })
  return `${startStr} – ${endStr}`
}

export const dayKey = (date: Date): string =>
  `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`

export const groupEventsByDay = (
  events: ApiEvent[]
): Map<string, { date: Date; events: ApiEvent[] }> => {
  const sorted = events
    .filter((e) => !isNaN(new Date(e.start_time).getTime()))
    .sort(
      (a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
    )
  const groups = new Map<string, { date: Date; events: ApiEvent[] }>()
  for (const event of sorted) {
    const date = new Date(event.start_time)
    const key = dayKey(date)
    const existing = groups.get(key)
    if (existing) {
      existing.events.push(event)
    } else {
      groups.set(key, { date, events: [event] })
    }
  }
  return groups
}
