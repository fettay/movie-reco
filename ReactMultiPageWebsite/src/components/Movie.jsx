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
      summary: "",
      tags: []
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
                     summary: res.data.summary,
                     tags: res.data.tags});
      console.log(res.data.results);
    });
  }

  render(){

    var movies = [];

    this.state.recommandations.forEach(movie => {
      movies.push(<li>{movie}</li>);
    });

    var tags = [];
    this.state.tags.forEach(tag => {
      tags.push(<span class="badge badge-pill badge-primary tags">{tag}</span>)
    });


    return (
      <div className="home">
        <div class="container">
          <div class="row my-5">
            <div class="col-lg-7">
              <div class="row">
                <Autocomplete
                  style={{ width: 300 }}
                  options={this.state.autocompleteInput}
                  onChange={(str) => this.getRecommandations(str.target.textContent)}
                  renderInput={(params) => <TextField {...params} label="Movie" variant="outlined" />}/ >
              </div>
              <div class="row tags-container">
                {tags}
              </div>
              <div class="row summary-container">
                <p>
                  {this.state.summary}
                </p>
              </div>
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
