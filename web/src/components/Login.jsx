import {useState} from "react";
const Login = () => {

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const accentColor = '#d13d3d';
  const fieldStyle = {
    flexGrow: 1,
    padding: '10px',
    fontSize: '16px',
    borderRadius: '4px',
    border: `1px solid ${accentColor}`
  }
  const h3Style = {
    textAlign: 'center',
    color: accentColor
  }
  const buttonStyle = {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '4px',
    border: `1px solid ${accentColor}`,
    backgroundColor: accentColor,
    color: '#ffffff',
  }
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      }}>
      <div style={{
      display: "flex",
      flexDirection: "column",
      width: "200%",
      padding: "20px",
      border: `1px solid ${accentColor}`,
      borderRadius: "8px",
      boxShadow: `0 4px 8px rgba(0, 0, 0, 0.1)`,
    }}>
      <h3 style={h3Style}>Welcome Back!</h3>
      <form
        style={{
              display: "flex",
              flexDirection: "column",
              gap: '10px'
            }}
      >
        <input
          style={fieldStyle}
        type="email" placeholder="Enter your email" value={email} onChange={(e) => setEmail(e.target.value)}/>
        <input style={fieldStyle} type="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)}/>
        <button style={buttonStyle} type="submit">Log In</button>
      </form>
    </div>
    </div>
  );
};

export default Login;