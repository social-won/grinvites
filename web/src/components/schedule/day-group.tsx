import { FC } from 'react'
import { ApiEvent } from '@/lib/types'
import EventCard from './event-card'
import { formatDayHeader } from './utils'

const MAX_EVENTS_PER_DAY = 10

type Props = {
  date: Date
  events: ApiEvent[]
  variant: 'simple' | 'detailed'
}

const DayGroup: FC<Props> = ({ date, events, variant }) => {
  const visible = events.slice(0, MAX_EVENTS_PER_DAY)
  const hidden = events.length - visible.length

  return (
    <section className="space-y-2">
      <h3 className="text-lg font-semibold border-b pb-1">
        {formatDayHeader(date)}
      </h3>
      {events.length === 0 ? (
        <div className="rounded-lg bg-muted text-muted-foreground text-center py-3">
          No events
        </div>
      ) : (
        <div className="space-y-2">
          {visible.map((event) => (
            <EventCard key={event.id} event={event} variant={variant} />
          ))}
          {hidden > 0 && (
            <div className="text-sm text-muted-foreground text-center pt-1">
              {hidden} more event{hidden === 1 ? '' : 's'}
            </div>
          )}
        </div>
      )}
    </section>
  )
}

export default DayGroup
