import { FC } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import './App.css'
import { SignupForm } from './components/signup-form.tsx'

const App: FC = () => {
  return (
    <Routes>
      <Route path="/signup" element={<SignupForm />} />
      <Route path="/" element={<Navigate to="/signup" replace />} />
    </Routes>
  )
}

export default App
