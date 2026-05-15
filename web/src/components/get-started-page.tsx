import { Link } from "react-router-dom"
import { CalendarCheck, MailPlus, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function GetStartedPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <nav className="flex justify-between gap-3 p-6">
        <Button variant="ghost" asChild>
          <Link to="/">Grinvites</Link>
        </Button>
        <Button variant="outline" asChild>
          <Link to="/login">Log in</Link>
        </Button>
      </nav>

      <main className="flex flex-1 items-center justify-center px-4 py-10">
        <section className="w-full max-w-3xl text-center">
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary">
            <Sparkles className="h-8 w-8" aria-hidden="true" />
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Find the campus events that fit you
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">
            Grinvites sends personalized event invitations to your calendar based on
            your interests and schedule, so the right campus plans find you.
          </p>

          <div className="mt-10 grid gap-4 text-left sm:grid-cols-2">
            <div className="rounded-lg border bg-card p-5">
              <CalendarCheck className="mb-4 h-6 w-6 text-primary" aria-hidden="true" />
              <h2 className="font-semibold">Stay in the campus loop</h2>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Hear about campus events before they happen.
              </p>
            </div>

            <div className="rounded-lg border bg-card p-5">
              <MailPlus className="mb-4 h-6 w-6 text-primary" aria-hidden="true" />
              <h2 className="font-semibold">Invites that match your life</h2>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Get personalized invitations that fit your hobbies, availability, and campus routine.
              </p>
            </div>
          </div>

          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Button size="lg" asChild>
              <Link to="/signup">Continue to email setup</Link>
            </Button>
            <Button size="lg" variant="ghost" asChild>
              <Link to="/">Back</Link>
            </Button>
          </div>
        </section>
      </main>
    </div>
  )
}
