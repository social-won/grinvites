import { FC, useEffect, useState } from 'react'
import { X } from 'lucide-react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
  FieldGroup,
  Field,
  FieldLabel,
} from '@/components/ui/field'
import { useUser } from '@/context/user-context'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../ui/dialog'
import { Badge } from '../ui/badge'
import supabase from '@/lib/supabase'
import { useNavigate } from 'react-router-dom'
import { Button } from '../ui/button'

interface PreferencesState {
  sendInvitesAt: string
}

const PreferencesTab: FC = () => {
  const navigate = useNavigate();

  const [schedulePreferences, setSchedulePreferences] = useState<PreferencesState>({
    sendInvitesAt: '5:00am',
  })

  const [watching, setWatching] = useState({
    classes: ['MAT-444', 'ANT-260', 'CSC-324'],
    departments: ['Art', 'Sociology', 'Computer Science'],
    athletics: ['Football', 'Track'],
    clubs: ['Brazilian Jujitsu', 'Campus Wide'],
  })

  useEffect(() => {
    console.log(schedulePreferences);
  }, [schedulePreferences])

  const { user } = useUser();

  console.log(user)

  const removeItem = (category: keyof typeof watching, item: string) => {
    setWatching((prev) => ({
      ...prev,
      [category]: prev[category].filter((i) => i !== item),
    }))
  }

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    navigate("/login");
  };

  return (
    <div className="p-6 space-y-6 w-full">
      {/* General Section */}
      <Card>
        <CardHeader>
          <CardTitle>General</CardTitle>
        </CardHeader>
        <CardContent>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="send-invites">Send me invites at</FieldLabel>
              <div className="flex gap-2">
                <Input
                  id="send-invites"
                  type="time"
                  defaultValue="05:00"
                  onChange={(e) =>
                    setSchedulePreferences({
                      ...schedulePreferences,
                      sendInvitesAt: e.target.value,
                    })
                  }
                  onBlur={() => console.log('blur!')}
                />
              </div>
            </Field>
          </FieldGroup>
        </CardContent>
      </Card>

      {/* Calendar Connection */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0">
          <div>
            <CardTitle>Calendar Connection</CardTitle>
            <CardDescription>{user?.calendar_type}</CardDescription>
          </div>
          <Dialog>
            <DialogTrigger>edit</DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Are you absolutely sure?</DialogTitle>
                <DialogDescription>
                  This action cannot be undone. This will permanently delete your account
                  and remove your data from our servers.
                </DialogDescription>
              </DialogHeader>
            </DialogContent>
          </Dialog>
          {/* <Button variant="ghost" size="sm">Edit</Button> */}
        </CardHeader>
      </Card>

      {/* Watching Section */}
      <Card>
        <CardHeader>
          <CardTitle>Watching</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Classes */}
          <div className="space-y-3">
            <h4 className="font-semibold">Classes</h4>
            <div className="flex flex-wrap gap-2">
              {watching.classes.map((cls) => (
                <Badge key={cls} aria-label={`Remove ${cls}`}>
                  <X onClick={() => removeItem('departments', cls)} className="h-3.5 w-3.5" />
                  {cls}
                </Badge>
              ))}
            </div>
          </div>

          {/* Departments */}
          <div className="space-y-3">
            <h4 className="font-semibold">Departments</h4>
            <div className="flex flex-wrap gap-2">
              {watching.departments.map((dept) => (
                <Badge key={dept} aria-label={`Remove ${dept}`}>
                  <X onClick={() => removeItem('departments', dept)} className="h-3.5 w-3.5" />
                  {dept}
                </Badge>
              ))}
            </div>
          </div>

          {/* Athletics */}
          <div className="space-y-3">
            <h4 className="font-semibold">Athletics</h4>
            <div className="flex flex-wrap gap-2">
              {watching.athletics.map((sport) => (
                <Badge key={sport} aria-label={`Remove ${sport}`}>
                  <X onClick={() => removeItem('athletics', sport)} className="h-3.5 w-3.5" />
                  {sport}
                </Badge>
              ))}
            </div>
          </div>

          {/* Clubs */}
          <div className="space-y-3">
            <h4 className="font-semibold">Clubs</h4>
            <div className="flex flex-wrap gap-2">
              {watching.clubs.map((club) => (
                <Badge key={club} aria-label={`Remove ${club}`}>
                  <X onClick={() => removeItem('clubs', club)} className="h-3.5 w-3.5" />
                  {club}
                </Badge>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      <Button variant="destructive" onClick={handleSignOut} className="w-full">
        Sign out
      </Button>
    </div>
  )
}

export default PreferencesTab
