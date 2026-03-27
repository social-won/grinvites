import { FC, FormEvent, ChangeEvent, useState } from 'react'
import styles from './SignUp.module.css'
import InputField from '../InputField/InputField'
import PrimaryButton from '../PrimaryButton/PrimaryButton'
import CheckSelection from '../CheckSelection/CheckSelection'

const SignUp: FC = () => {
  const [firstName, setFirstName] = useState<string>('')
  const [lastName, setLastName] = useState<string>('')
  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [interestSports, setInterestSports] = useState<boolean>(false)
  const [interestMath, setInterestMath] = useState<boolean>(false)
  const [interestBear, setInterestBear] = useState<boolean>(false)

  const newRegistration = (e: FormEvent<HTMLButtonElement>): void => {
    e.preventDefault()
    console.log('Attempting new user registration...')
    console.log('Name:', firstName, lastName)
    console.log('Email:', email)
    console.log('Password:', password)
    console.log('Sports Interest:', interestSports)
    console.log('MATH Interest:', interestMath)
    console.log('BEAR Interest:', interestBear)
  }

  return (
    <div className={styles.signUpPage}>
      <div className={styles.signUpCard}>
        <h3 className={styles.titleText}>Create Your Account!</h3>
        <div className={styles.signUpForm}>
          <div className={styles.nameRow}>
            <InputField
              type="text"
              placeholder="First Name"
              value={firstName}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFirstName(e.target.value)}
            />
            <InputField
              type="text"
              placeholder="Last Name"
              value={lastName}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setLastName(e.target.value)}
            />
          </div>
          <InputField
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          />
          <InputField
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          />
          <hr className={styles.primaryHorizontalLine} />
          <CheckSelection
            label="Sports: Basketball Games"
            checked={interestSports}
            onCheck={(e: ChangeEvent<HTMLInputElement>) => setInterestSports(e.target.checked)}
          />
          <CheckSelection
            label="Math SEPC"
            checked={interestMath}
            onCheck={(e: ChangeEvent<HTMLInputElement>) => setInterestMath(e.target.checked)}
          />
          <CheckSelection
            label="BEAR Gym Hours"
            checked={interestBear}
            onCheck={(e: ChangeEvent<HTMLInputElement>) => setInterestBear(e.target.checked)}
          />
          <hr className={styles.primaryHorizontalLine} />
          <PrimaryButton
            text="Sign Up"
            onClick={newRegistration}
          />
        </div>
      </div>
    </div>
  )
}

export default SignUp
