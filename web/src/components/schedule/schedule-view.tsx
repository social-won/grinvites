import { FC, ReactNode, useEffect, useMemo, useState } from 'react'
import { ApiEvent } from '@/lib/types'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import DayGroup from './day-group'
import EventCalendarView from './event-calendar-view'
import { groupEventsByDay } from './utils'

type ViewMode = 'simple' | 'detailed' | 'calendar'

type Props = {
  events: ApiEvent[]
  views?: ViewMode[]
  defaultView?: ViewMode
  emptyMessage?: string
}

const ALL_VIEWS: ViewMode[] = ['simple', 'detailed', 'calendar']
const VIEW_LABELS: Record<ViewMode, string> = {
  simple: 'Simple',
  detailed: 'Detailed',
  calendar: 'Calendar',
}

const ScheduleView: FC<Props> = ({
  events,
  views = ALL_VIEWS,
  defaultView,
  emptyMessage = 'No upcoming events',
}) => {
  const [view, setView] = useState<ViewMode>(defaultView ?? views[0])
  const days = useMemo(
    () => Array.from(groupEventsByDay(events).values()),
    [events]
  )


  useEffect(() => {
    console.log(events);

  }, [])

  const renderView = (mode: ViewMode): ReactNode => {
    if (mode === 'calendar') return <EventCalendarView events={events} />

    if (days.length === 0) {
      return (
        <p className="text-muted-foreground text-center py-6">{emptyMessage}</p>
      )
    }
    return (
      <div className="space-y-6">
        {days.map(({ date, events }) => (
          <DayGroup
            key={date.toISOString()}
            date={date}
            events={events}
            variant={mode}
          />
        ))}
      </div>
    )
  }

  if (views.length === 1) {
    return <div className="w-full">{renderView(views[0])}</div>
  }


  return (
    <Tabs
      value={view}
      onValueChange={(v) => setView(v as ViewMode)}
      className="w-full"
    >
      <div className="flex justify-end">
        <TabsList>
          {views.map((v) => (
            <TabsTrigger key={v} value={v}>
              {VIEW_LABELS[v]}
            </TabsTrigger>
          ))}
        </TabsList>
      </div>

      {views.map((v) => (
        <TabsContent key={v} value={v}>
          {renderView(v)}
        </TabsContent>
      ))}
    </Tabs>
  )
}

export default ScheduleView
