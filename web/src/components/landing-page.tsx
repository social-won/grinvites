import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { GiSquirrel } from "react-icons/gi"
import ScheduleView from "@/components/schedule/schedule-view"
import { ApiEvent } from "@/lib/types"
import { getEvents } from "@/lib/api"

export default function LandingPage() {
    const [events, setEvents] = useState<ApiEvent[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        let cancelled = false
        getEvents().then((res) => {
            if (cancelled) return
            if (res.data) setEvents(res.data)
            setLoading(false)
        })
        return () => {
            cancelled = true
        }
    }, [])

    return (
        <div className="min-h-screen flex flex-col">
            <nav className="flex justify-end gap-3 p-6">
                <Button variant="outline" asChild>
                    <Link to="/login">Log in</Link>
                </Button>
                <Button asChild>
                    <Link to="/signup">Sign up</Link>
                </Button>
            </nav>

            <main className="flex flex-1 flex-col items-center gap-10 px-4 pb-12">
                <div className="flex flex-col items-center gap-6 text-center">
                    <GiSquirrel className="text-8xl text-primary" />
                    <h1 className="text-5xl font-bold tracking-tight">Grinvites</h1>
                    <p className="text-muted-foreground text-lg max-w-md">
                        Find events at Grinnell that actually match your interests.
                    </p>
                    <Button size="lg" asChild>
                        <Link to="/signup">Get started</Link>
                    </Button>
                </div>

                <section className="w-full max-w-xl">
                    <h2 className="text-2xl font-semibold mb-4 text-center">
                        Upcoming events
                    </h2>
                    {loading ? (
                        <p className="text-muted-foreground text-center py-6">Loading…</p>
                    ) : (
                        <ScheduleView events={events} views={['simple']} />
                    )}
                </section>
            </main>
        </div>
    )
}
