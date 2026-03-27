import { FC, ChangeEvent } from 'react'
import styles from './CheckSelection.module.css'

interface CheckSelectionProps {
  label: string
  checked: boolean
  onCheck: (e: ChangeEvent<HTMLInputElement>) => void
}

const CheckSelection: FC<CheckSelectionProps> = ({ label, checked, onCheck }) => {
  return (
    <label className={styles.checkboxContainer}>
      <div className={styles.checkboxWrapper}>
        <input
          type="checkbox"
          className={styles.hiddenCheckbox}
          checked={checked}
          onChange={onCheck}
        />
        <span className={styles.customBox}></span>
      </div>

      <div className={styles.labelWrapper}>
        {label}
      </div>
    </label>
  )
}

export default CheckSelection
