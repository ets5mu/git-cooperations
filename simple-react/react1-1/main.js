function AppContent() {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  function handleSubmit(event) {
    event.preventDefault();
    //防止页面重新刷新

    if (username === "" || password === "") {
      alert('"usename" and "password" are required');
      return;
    }

    alert(`username: ${username}`);
    alert(`password: ${password}`);
    console.log("username:", username);
    console.log("password:", password);

    setUsername("");
    setPassword("");
  }
  return (
    <main style={{ border: "1px solid black" }}>
      <h2
        style={{
          textAlign: "center",
        }}
      >
        Login Form
      </h2>
      <form onSubmit={handleSubmit} style={{ textAlign: "center" }}>
        <input
          type="text"
          value={username} //input变量和属性值来绑定
          onChange={(event) => setUsername(event.target.value)}
        />
        <br />
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <br />

        <button type="submit" style={{ margin: "1rem" }}>
          Login
        </button>
      </form>
    </main>
  );
}

const appEl = document.querySelector("#app");
const root = ReactDOM.createRoot(appEl);

root.render(<AppContent />);
