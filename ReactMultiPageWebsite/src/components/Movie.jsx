import React, {Component} from "react";
import { Autocomplete } from '@material-ui/lab';
import TextField from "@material-ui/core/TextField";
import axios from 'axios';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';


class Movie extends Component {
  constructor (props) {
    super(props);    
    this.state = {
      autocompleteInput: [],
      recommandations: [],
      movieReco: "",
      summary: "",
      tags: [],
    };
    this.currentMovie = "";
    this.recoType = "storyline";
  }
  
  componentDidMount(){
    axios.get(process.env.REACT_APP_API + "autocomplete")
      .then(res => {
        this.setState({ autocompleteInput: res.data.results });
      })
  }

  getTitleSuggestions(inputTitle){
    axios.get(process.env.REACT_APP_API + "autocomplete/" + inputTitle)
    .then(res => {
      this.setState({ autocompleteInput: res.data.results })
    })
  }

  getRecommandationsMovie(){
    axios.get(process.env.REACT_APP_API + "movie/" + this.recoType + "/" + this.currentMovie)
    .then(res => {
      this.setState({recommandations: res.data.results.map(x => x.title),
                     summary: res.data.summary,
                     tags: res.data.tags});
      console.log(res.data.results);
    });
  }

  getRecommandations(movie){
    this.currentMovie = movie;
    this.getRecommandationsMovie();
  }

  handleTypeChange(event, newValue){
    if(this.currentMovie == "")
      return
    
    this.recoType = newValue;
    this.getRecommandationsMovie();
  }

  render(){

    var movies = [];

    this.state.recommandations.slice(0, 25).forEach(movie => {
      movies.push(<li>{movie}</li>);
    });

    var tags = [];
    this.state.tags.forEach(tag => {
      tags.push(<span class="badge badge-pill badge-primary tags">{tag}</span>)
    });


    return (
      <div className="home">
        <div class="container">
        <div class="row align-items-center my-5">
            <div class="col-lg-7">
            <ToggleButtonGroup
              value={this.recoType}
              exclusive
              onChange={this.handleTypeChange.bind(this)}
              aria-label="text alignment">
              <ToggleButton value="tagline" aria-label="tagline">
                Tagline
              </ToggleButton>
              <ToggleButton value="storyline" aria-label="storyline">
                Storyline
              </ToggleButton>
              <ToggleButton value="synopsis" aria-label="synopsis">
                Synopsis
              </ToggleButton>
            </ToggleButtonGroup>
            </div>
          </div>
          <div class="row my-5">
            <div class="col-lg-7">
              <div class="row">
                <Autocomplete
                  style={{ width: 300 }}
                  options={this.state.autocompleteInput}
                  onChange={(str) => this.getRecommandations(str.target.textContent)}
                  onInputChange={(str) => this.getTitleSuggestions(str.target.value)}
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
