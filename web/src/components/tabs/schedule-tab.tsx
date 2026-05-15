import { FC, useEffect, useState } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import ScheduleView from '@/components/schedule/schedule-view'
import { ApiEvent } from '@/lib/types'
import { getUserEvents } from '@/lib/api'
import { useUser } from '@/context/user-context'

const ScheduleTab: FC = () => {
  const { user } = useUser()
  const [events, setEvents] = useState<ApiEvent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) return
    let cancelled = false
    setLoading(true)
    getUserEvents(user.id).then((res) => {
      if (cancelled) return
      if (res.data) setEvents(res.data)
      setLoading(false)
    })
    return () => {
      cancelled = true
    }
  }, [user])

  return (
    <div className="p-6 w-full">
      <Card>
        <CardHeader>
          <CardTitle>Schedule</CardTitle>
          <CardDescription>View your upcoming events</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-muted-foreground">Loading…</p>
          ) : (
            <ScheduleView events={events} />
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default ScheduleTab
