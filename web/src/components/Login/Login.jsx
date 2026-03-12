import {useState} from "react";
import style from './Login.module.css';
import InputField from '../InputField/InputField';
import PrimaryButton from '../PrimaryButton/PrimaryButton';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('User sign on with: ${email} without reloading the page');
  };

  return (
    <div className={style.loginPage}>
      <div className={style.loginCard}>
        <h3 className={style.titleText}>Welcome Back!</h3>
        <form onSubmit={handleSubmit} className={style.loginForm}>
          <InputField
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <InputField
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
          <PrimaryButton text="Login" onClick={handleSubmit}/>
        </form>
      </div>
    </div>
  )
};

export default Login;