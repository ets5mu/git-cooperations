function AppContent() {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  // const [usernameClass, setusernametClass] = React.useState("input");
  const usernameClass = username.length <= 5 ? "input-error" : "input";
  const passwordClass = password.length <= 7 ? "input-error" : "input";

  function handleSubmit(event) {
    event.preventDefault();
    //防止页面重新刷新

    // if (username.length <= 5) {
    //   setusernametClass("input-error");
    //   return;
    // }

    if (usernameClass === "input-error" || passwordClass === "input-error") {
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
    <main
    // style={{ border: "1px solid black" }}
    >
      <h2
      // style={{
      //   textAlign: "center",
      // }}
      >
        Login Form
      </h2>
      <form onSubmit={handleSubmit} style={{ textAlign: "center" }}>
        <input
          className={usernameClass}
          type="text"
          value={username} //input变量和属性值来绑定
          onChange={(event) => setUsername(event.target.value)}
        />
        <br />
        <input
          className={passwordClass}
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <br />

        <button
          className="btn"
          type="submit"
          // style={{ margin: "1rem" }}
        >
          Login
        </button>
      </form>
    </main>
  );
}

const appEl = document.querySelector("#app");
const root = ReactDOM.createRoot(appEl);

root.render(<AppContent />);
