import styles from './CheckSelection.module.css'

const CheckSelection = ({label, checked, onCheck}) => {
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
    );
};

export default CheckSelection;