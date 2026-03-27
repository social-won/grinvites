import { FC, ChangeEvent } from 'react'
import styles from './InputField.module.css'

interface InputFieldProps {
  type: string
  placeholder: string
  value: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
}

const InputField: FC<InputFieldProps> = ({ type, placeholder, value, onChange }) => {
  return (
    <input
      className={styles.inputField}
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  )
}

export default InputField
