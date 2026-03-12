import styles from './InputField.module.css';

const InputField = ({type, placeholder, value, onChange}) => {
    return (
        <input
            className={styles.inputField}
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
        />
    );
};

export default InputField;