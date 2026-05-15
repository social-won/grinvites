import { FC, useMemo, useState } from 'react'
import { ApiEvent } from '@/lib/types'
import { Calendar } from '@/components/ui/calendar'
import EventCard from './event-card'
import { dayKey, formatDayHeader, groupEventsByDay } from './utils'

type Props = {
  events: ApiEvent[]
}

const EventCalendarView: FC<Props> = ({ events }) => {
  const grouped = useMemo(() => groupEventsByDay(events), [events])
  const [selected, setSelected] = useState<Date | undefined>(() => {
    const first = grouped.values().next().value
    return first?.date ?? new Date()
  })

  const eventDays = useMemo(
    () => Array.from(grouped.values()).map((g) => g.date),
    [grouped]
  )

  const dayEvents = selected
    ? grouped.get(dayKey(selected))?.events ?? []
    : []

  return (
    <div className="flex flex-col md:flex-row gap-6">
      <Calendar
        mode="single"
        selected={selected}
        onSelect={setSelected}
        modifiers={{ hasEvents: eventDays }}
        modifiersClassNames={{
          hasEvents: 'font-bold underline underline-offset-4',
        }}
        className="rounded-md border"
      />
      <div className="flex-1 space-y-2">
        <h3 className="text-lg font-semibold border-b pb-1">
          {selected ? formatDayHeader(selected) : 'Select a day'}
        </h3>
        {dayEvents.length === 0 ? (
          <div className="rounded-lg bg-muted text-muted-foreground text-center py-3">
            No events
          </div>
        ) : (
          dayEvents.map((event) => (
            <EventCard key={event.id} event={event} variant="detailed" />
          ))
        )}
      </div>
    </div>
  )
}

export default EventCalendarView
