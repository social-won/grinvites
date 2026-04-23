import { FC } from 'react'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import ScheduleTab from './tabs/schedule-tab'
import HoursTab from './tabs/hours-tab'
import PreferencesTab from './tabs/preferences-tab'
import { useUser } from '@/context/user-context'

const HomeScreen: FC = () => {
  const { user } = useUser();

  return (
    <div className="min-h-screen bg-background">

      {/* Tabs */}
      <Tabs defaultValue="preferences">
        {/* Top bar */}
        <div className="sticky top-0 z-10 bg-background border-b px-6 py-3 flex flex-col sm:flex-row sm:items-center gap-2">
          <div className="flex items-center justify-between sm:flex-1">
            <span className="text-sm text-muted-foreground">
              Logged in as: <span className="font-medium text-foreground">{user?.email}</span>
            </span>
          </div>

          <TabsList variant="default" className="bg-transparent border px-2 w-full sm:w-auto">
            <TabsTrigger value="schedule" className="flex-1 sm:w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Schedule</TabsTrigger>
            <TabsTrigger value="hours" className="flex-1 sm:w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Hours</TabsTrigger>
            <TabsTrigger value="preferences" className="flex-1 sm:w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Preferences</TabsTrigger>
          </TabsList>

          <div className="hidden sm:flex sm:flex-1 sm:justify-end"></div>
        </div>

        <div className="w-full max-w-xl mx-auto">
          <TabsContent value="schedule">
            <ScheduleTab />
          </TabsContent>
          <TabsContent value="hours">
            <HoursTab />
          </TabsContent>
          <TabsContent value="preferences">
            <PreferencesTab />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  )
}

export default HomeScreen
