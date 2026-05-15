import { FC, useEffect } from 'react'
import { ApiEvent } from '@/lib/types'
import { formatTimeRange } from './utils'
import { cn } from '@/lib/utils'

type Variant = 'simple' | 'detailed'

type Props = {
  event: ApiEvent
  variant?: Variant
}

const EventCard: FC<Props> = ({ event, variant = 'simple' }) => {

  useEffect(() => {
    console.log(event);
    
  
    // return () => {
    //   second
    // }
  }, [])
  
  return (
    <div
      className={cn(
        'flex items-stretch rounded-lg border bg-card overflow-hidden',
        variant === 'detailed' ? 'p-0' : 'p-0'
      )}
    >
      <div className="w-1.5 bg-primary/60 shrink-0" />
      <div className="relative flex flex-1 items-start justify-between gap-4 p-3">
        <div className="min-w-0 flex-1 pr-2">
          <div className="font-semibold truncate">
            {event.title.length > 30 ? `${event.title.slice(0, 30)}…` : event.title}
          </div>
          {event.org_name && (
            <div className="text-sm text-muted-foreground wrap-break-word">
              {event.org_name}
            </div>
          )}
          {variant === 'detailed' && event.summary && (
            <p className="text-sm text-muted-foreground mt-2 line-clamp-3">
              {event.summary}
            </p>
          )}
        </div>
        <div className="sticky top-3 self-start text-right text-sm shrink-0 max-w-[40%]">
          <div className="whitespace-nowrap">
            {formatTimeRange(event.start_time, event.end_time)}
          </div>
          {event.location && (
            <div className="text-muted-foreground wrap-break-word">
              {event.location}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default EventCard
