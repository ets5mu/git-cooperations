class Lists extends React.Component {
  render() {
    return (
      <ul>
        {/*<li>{pokemons[0]}</li>
                 <li>{pokemons[1]}</li>
                 <li>{pokemons[2]}</li>
                 元素过多不适用
                 */}
        {/*pokemons.map((pokemons) => (
                  <li>{pokemons}</li>
                ))*/}
        {this.state.filteredPokemons.map(
          (pokemon) => (
            <li key={pokemon.url}>{pokemon.name}</li>
          )
          //要改变的键值对-挂载执行-.name
        )}
      </ul>
    );
  }
}
