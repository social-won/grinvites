import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { GiSquirrel } from "react-icons/gi"

export default function LandingPage() {
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

            <main className="flex flex-1 flex-col items-center justify-center gap-6 text-center px-4">
                <GiSquirrel className="text-8xl text-primary" />
                <h1 className="text-5xl font-bold tracking-tight">Grinvites</h1>
                <p className="text-muted-foreground text-lg max-w-md">
                    Find events at Grinnell that actually match your interests.
                </p>
                <Button size="lg" asChild>
                    <Link to="/signup">Get started</Link>
                </Button>
            </main>
        </div>
    )
}
