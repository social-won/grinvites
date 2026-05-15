import { FC, useState } from 'react'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'

const TAB_STORAGE_KEY = 'grinvites:active-tab'
import { Button } from '@/components/ui/button'
import ScheduleTab from './tabs/schedule-tab'
import HoursTab from './tabs/hours-tab'
import PreferencesTab from './tabs/preferences-tab'
import { useUser } from '@/context/user-context'
import { useNavigate } from 'react-router-dom'
import supabase from '@/lib/supabase'

const HomeScreen: FC = () => {
  const { user } = useUser();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<string>(
    () => localStorage.getItem(TAB_STORAGE_KEY) ?? 'schedule'
  );

  const handleTabChange = (value: string) => {
    setActiveTab(value);
    localStorage.setItem(TAB_STORAGE_KEY, value);
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-background">

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={handleTabChange}>
        {/* Top bar */}
        <div className="sticky top-0 z-10 bg-background border-b px-6 py-3 flex flex-col sm:flex-row sm:items-center gap-2">
          <div className="flex items-center justify-between sm:flex-1">
            <span className="text-sm text-muted-foreground">
              Logged in as: <span className="font-medium text-foreground">{user?.email}</span>
            </span>
            <Button variant="destructive" size="sm" onClick={handleSignOut} className="sm:hidden">Sign out</Button>
          </div>

          <TabsList variant="default" className="bg-transparent border px-2 w-full sm:w-auto">
            <TabsTrigger value="schedule" className="flex-1 sm:w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Schedule</TabsTrigger>
            <TabsTrigger value="hours" className="flex-1 sm:w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Hours</TabsTrigger>
            <TabsTrigger value="preferences" className="flex-1 sm:w-24 data-[state=active]:bg-gray-100 dark:data-[state=active]:bg-gray-800">Preferences</TabsTrigger>
          </TabsList>

          <div className="hidden sm:flex sm:flex-1 sm:justify-end">
            <Button variant="destructive" size="sm" onClick={handleSignOut}>Sign out</Button>
          </div>
        </div>

        <div className="w-full max-w-3xl mx-auto">
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
