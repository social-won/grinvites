import { FC } from 'react'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import ScheduleTab from './tabs/schedule-tab'
import HoursTab from './tabs/hours-tab'
import PreferencesTab from './tabs/preferences-tab'
import { useNavigate } from 'react-router-dom'
import { useUser } from '@/context/user-context'

const HomeScreen: FC = () => {

  const navigate = useNavigate();

  const { user } = useUser();

  console.log(user)

  return (
    <div className="min-h-screen bg-background">
      {/* Header with tabs and profile dropdown */}
      <div className="border-b">
        <div className="flex items-center justify-between lg:px-60 py-4 w-screen">
          <Tabs defaultValue="preferences" className="flex-1 items-center">
            <TabsList className="bg-transparent border-b">
              <TabsTrigger value="schedule">Schedule</TabsTrigger>
              <TabsTrigger value="hours">Hours</TabsTrigger>
              <TabsTrigger value="preferences">Preferences</TabsTrigger>
            </TabsList>

            <TabsContent value="schedule" className="w-full">
              <ScheduleTab />
            </TabsContent>

            <TabsContent value="hours" className="w-full">
              <HoursTab />
            </TabsContent>

            <TabsContent value="preferences" className="w-full">
              <PreferencesTab />
            </TabsContent>
          </Tabs>

          {/* Profile Dropdown */}
          <div className="absolute top-4 right-6">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground text-sm font-semibold">
                    {user?.display_name?.charAt(0)}
                  </div>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem>Profile</DropdownMenuItem>
                <DropdownMenuItem>Settings</DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => navigate("/signup")}>Logout</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomeScreen
