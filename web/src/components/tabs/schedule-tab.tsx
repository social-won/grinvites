import { FC } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

const ScheduleTab: FC = () => {
  return (
    <div className="p-6 w-full">
      <Card>
        <CardHeader>
          <CardTitle>Schedule</CardTitle>
          <CardDescription>View your upcoming events</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Schedule content coming soon</p>
        </CardContent>
      </Card>
    </div>
  )
}

export default ScheduleTab
