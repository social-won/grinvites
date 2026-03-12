import styles from './PrimaryButton.module.css';

const PrimaryButton = ({text, onClick}) => {
    return (
        <button
            className={styles.primaryButton}
            onClick={onClick}
            >
            {text}
        </button>
    );
};

export default PrimaryButton;