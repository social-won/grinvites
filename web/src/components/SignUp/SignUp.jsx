import {useState} from "react"
import styles from './SignUp.module.css'
import InputField from '../InputField/InputField'
import PrimaryButton from '../PrimaryButton/PrimaryButton'
import CheckSelection  from "../CheckSelection/CheckSelection"

const SignUp = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [interestSports, setInterestSports] = useState(false)
    const [interestMath, setInterestMath] = useState(false)
    const [interestBear, setInterestBear] = useState(false)

    const newRegistration = (e) => {
        e.preventDefault();
        console.log('Attempting new user registration...');
        console.log('Name:', firstName, lastName);
        console.log('Email:', email);
        console.log('Password:', password);
        console.log('Sports Interest:', interestSports);
        console.log('MATH Interest:', interestBear);
        console.log('BEAR Interest:', interestBear);
    }


    return(
        <div className={styles.signUpPage}>
            <div className={styles.signUpCard}>
                <h3 className={styles.titleText}>Create Your Account!</h3>
                <div className={styles.signUpForm}>
                    <div className={styles.nameRow}>
                        <InputField
                        type='text'
                        placeholder="First Name"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                    />
                        <InputField
                            type='text'
                            placeholder="Last Name"
                            value={lastName}
                            onChange={(e) => setLastName(e.target.value)}
                    />
                    </div>
                    <InputField
                    type='email'
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    />
                    <InputField
                    type='password'
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    />
                    <hr className={styles.primaryHorizontalLine}/>
                    <CheckSelection
                    label='Sports: Basketball Games'
                    checked={interestSports}
                    onCheck={(e) => setInterestSports(e.target.checked)}/>
                    <CheckSelection
                    label='Math SEPC'
                    checked={interestMath}
                    onCheck={(e) => setInterestMath(e.target.checked)}/>
                    <CheckSelection
                    label='BEAR Gym Hours'
                    checked={interestBear}
                    onCheck={(e) => setInterestBear(e.target.checked)}/>
                    <hr className={styles.primaryHorizontalLine}/>
                    <PrimaryButton
                        text="Sign Up"
                        onClick={newRegistration}
                    />
                </div>
            </div>
        </div>
    );
};

export default SignUp;