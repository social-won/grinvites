import { FC } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

const HoursTab: FC = () => {
  return (
    <div className="p-6 w-full">
      <Card>
        <CardHeader>
          <CardTitle>Hours</CardTitle>
          <CardDescription>View department and club hours</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Hours content coming soon</p>
        </CardContent>
      </Card>
    </div>
  )
}

export default HoursTab
