import { FC, MouseEvent } from 'react'
import styles from './PrimaryButton.module.css'

interface PrimaryButtonProps {
  text: string
  onClick: (e: MouseEvent<HTMLButtonElement>) => void
}

const PrimaryButton: FC<PrimaryButtonProps> = ({ text, onClick }) => {
  return (
    <button
      className={styles.primaryButton}
      onClick={onClick}
    >
      {text}
    </button>
  )
}

export default PrimaryButton
