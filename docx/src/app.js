//const root = ReactDOM.createRoot(document.getElementById("root"));
//const pokemons = ["皮卡丘", "杰尼龟", "小火龙"];

class App extends React.Component {
  constructor() {
    console.log("构造函数");
    super();
    this.state = {
      pokemons: [],
      filteredPokemons: [],
    };
  }

  componentDidMount() {
    console.log("组件已挂载");
    fetch("https://pokeapi.co/api/v2/pokemon")
      .then((res) => res.json())
      .then((json) => {
        this.setState(
          () => {
            //使用setState--挂载执行
            return { pokemons: json.results, filteredPokemons: json.results };
          },
          () => {
            // console.log(this.state);
          }
        );
        //直接赋值不会改变内存位置
      });
  }

  //ComponentDidMount组件挂载后再执行内容--获取api
  //react--对象属性不会 原生JS频繁修改DOM--创建新对象改变内存位置

  onChangeHandler = (event) => {
    const comparedPokemons = this.state.pokemons.filter((pokemon) => {
      return pokemon.name.includes(event.target.value);
    });

    this.setState(
      () => {
        return { filteredPokemons: comparedPokemons };
      },
      () => {
        console.log(this.state.searching);
      }
    );
  };

  render() {
    console.log("渲染");

    return (
      <div>
        <h1>宝可梦</h1>
        <input type="search" onChange={this.onChangeHandler} />
        {/*<ul>
          {/*<li>{pokemons[0]}</li>
                 <li>{pokemons[1]}</li>
                 <li>{pokemons[2]}</li>
                 元素过多不适用
                 */}
        {/*pokemons.map((pokemons) => (
                  <li>{pokemons}</li>
                ))*/}
        {/*this.state.filteredPokemons.map(
            (pokemon) => (
              <li key={pokemon.url}>{pokemon.name}</li>
            )
            //要改变的键值对-挂载执行-.name
          )}
        </ul>*/}
        <lists />
      </div>
    );
  }
}

//root.render(<App />);
