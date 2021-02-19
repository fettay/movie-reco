import React, {Component} from "react";
import { Autocomplete } from '@material-ui/lab';
import TextField from "@material-ui/core/TextField";
import axios from 'axios';


class Movie extends Component {
  constructor (props) {
    super(props);    
    this.state = {
      autocompleteInput: [],
      recommandations: [],
      movieReco: "",
      summary: ""
    };
  }
  
  componentDidMount(){
    axios.get(process.env.REACT_APP_API + "autocomplete" )
      .then(res => {
        this.setState({ autocompleteInput: res.data.results });
      })
  }

  getRecommandations(movie){
    axios.get(process.env.REACT_APP_API + "movie/" + movie)
    .then(res => {
      this.setState({recommandations: res.data.results,
                     summary: res.data.summary});
      console.log(res.data.results);
    });
  }

  render(){

    const movies = [];

    this.state.recommandations.forEach(movie => {
      movies.push(<li>{movie}</li>);
    });

    return (
      <div className="home">
        <div class="container">
          <div class="row align-items-center my-5">
            <div class="col-lg-7">
            <Autocomplete
              style={{ width: 300 }}
              options={this.state.autocompleteInput}
              onChange={(str) => this.getRecommandations(str.target.textContent)}
              renderInput={(params) => <TextField {...params} label="Movie" variant="outlined" />}/ >
            <p>
              {this.state.summary}
            </p>
            </div> 
            <div class="col-lg-5">
              <h1 class="font-weight-light">Recommandation for {this.state.movieReco}</h1>
              {movies}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Movie;
