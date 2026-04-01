import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useNavigate } from "react-router-dom"
import { useState } from "react"

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log(`User signing in with: ${email}`)
    navigate("/home")
  }

  const handleSignUp = () => {
    navigate("/signup")
  }

  return (
    <div className={cn("flex flex-col gap-6 p-4", className)} {...props}>
      <Card className="min-w-1/2">
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Welcome Back</CardTitle>
          <CardDescription>
            Enter your email and password to sign in
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  placeholder="john@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="password">Password</FieldLabel>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <FieldDescription>
                  <a href="#" className="text-primary hover:underline">Forgot your password?</a>
                </FieldDescription>
              </Field>
              <Field>
                <Button type="submit" className="w-full">Sign In</Button>
                <FieldDescription className="text-center">
                  Don't have an account? <a href="#" onClick={handleSignUp} className="text-primary hover:underline">Sign up</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
      <FieldDescription className="px-6 text-center">
        By signing in, you agree to our <a href="#" className="text-primary hover:underline">Terms of Service</a>{" "}
        and <a href="#" className="text-primary hover:underline">Privacy Policy</a>.
      </FieldDescription>
    </div>
  )
}
