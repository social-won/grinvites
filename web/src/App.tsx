import { FC } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { SignupPage } from './components/signup-form.tsx'
import { LoginForm } from './components/login-form.tsx'
import OnboardingFlow from './components/onboarding-flow.tsx'
import HomeScreen from './components/home-screen.tsx'

const App: FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginForm />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/home" element={<HomeScreen />} />
      <Route path="/onboarding" element={<OnboardingFlow />} />
    </Routes>
  )
}

export default App
