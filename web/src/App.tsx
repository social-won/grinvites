import { FC } from 'react'
import Login from './components/Login/Login.tsx'
import './App.css'
import { SignUp } from './components/index.ts'

const App: FC = () => {
  return (
    <div>
      <SignUp />
    </div>
  )
}

export default App
