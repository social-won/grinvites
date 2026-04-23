import { FC } from 'react'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import ScheduleTab from './tabs/schedule-tab'
import HoursTab from './tabs/hours-tab'
import PreferencesTab from './tabs/preferences-tab'
import { useNavigate } from 'react-router-dom'
import { useUser } from '@/context/user-context'
import supabase from '@/lib/supabase'

const HomeScreen: FC = () => {
  const navigate = useNavigate();
  const { user } = useUser();

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-background">

      {/* Tabs */}
      <Tabs defaultValue="schedule">
        {/* Top bar */}
        <div className="sticky top-0 z-10 bg-background border-b px-6 py-3 flex items-center gap-2">
          <div className="flex-1">
            <span className="text-sm text-muted-foreground flex flex-col lg:flex-row lg:gap-1">
              <span>Logged in as:</span>
              <span className="font-medium text-foreground">{user?.email}</span>
            </span>
          </div>

          {/* <TabsList variant="default" className="bg-transparent border px-2">
            <TabsTrigger value="schedule" className="w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Schedule</TabsTrigger>
            <TabsTrigger value="hours" className="w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Hours</TabsTrigger>
            <TabsTrigger value="preferences" className="w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Preferences</TabsTrigger>
          </TabsList> */}

          <div className="flex-1 flex justify-end">
            <Button variant="destructive" size="sm" onClick={handleSignOut} className="w-24">
              Sign out
            </Button>
          </div>
        </div>

        <div className="flex items-center justify-between lg:px-60 md:px-32 py-4 w-screen">
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
