import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import axios from 'axios';
import Slider from '@material-ui/core/Slider';
import Typography from '@material-ui/core/Typography';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';

var ALL_GENRES = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Children', 'Comedy', 'Crime',
                 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical',
                 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show',
                 'Thriller', 'War', 'Western']


class Ip extends Component {
  constructor (props) {
    super(props);    
    this.state = {
      autocompleteInput: [],
      allRecommandations: [],
      movieReco: "",
      tags: [],
      minYear: 1950,
      genres: ALL_GENRES,
      minVotes: 0
    };
    this.curContent = "";
    this.recoType = "storyline";
  }
  


  getAllRecommandations(){
    axios.post(process.env.REACT_APP_API + "themes", {ip: this.curContent})
    .then(res => {
      this.setState({tags: res.data.results});
      console.log(res.data.results);
    });

    axios.post(process.env.REACT_APP_API + "ip/" + this.recoType, {ip: this.curContent})
    .then(res => {
      this.setState({allRecommandations: res.data.results});
      console.log(res.data.results);
    });
  }

  hasCommonGenre(genres){
    return genres.filter(genre => this.state.genres.includes(genre)).length > 0
  }

  filterRecommandation(){
    var recos = this.state.allRecommandations.filter(movie => this.hasCommonGenre(movie.genres) && movie.year >= this.state.minYear && movie.votes >= this.state.minVotes);
    return recos.slice(0, 25).map(movie => movie.title);                                            
  }

  handleTypeChange(event, newValue){
    this.recoType = newValue;
    this.getAllRecommandations();
  }

  handleGenreChange(event){
    if (event.target.checked){
      var newList = this.state.genres.map(x => x);
      newList.push(event.target.name);
    }
    else{
      console.log(event.target.name);
      var newList = this.state.genres.filter(genre => genre != event.target.name);
    }
    this.setState({genres: newList});
  };

  render(){

    const movies = [];

    this.filterRecommandation().forEach(movie => {
      movies.push(<li>{movie}</li>);
    });

    var tags = [];
    this.state.tags.forEach(tag => {
      tags.push(<span class="badge badge-pill badge-primary tags">{tag}</span>)
    });

    var genres = [];
    ALL_GENRES.forEach(genre => {
      genres.push(<FormControlLabel
      control={<Checkbox checked={this.state.genres.includes(genre)} onChange={this.handleGenreChange.bind(this)} name={genre} />}
      label={genre}
      color="primary"
      />)
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
            <div class="row tags-container">
                {tags}
            </div>
            <div class="row genre-container">
                {genres}
            </div>
            <div class="col-md-5">
                <Typography id="discrete-slider" gutterBottom>
                  Min Year:
                </Typography>
                <Slider
                defaultValue={1950}
                aria-labelledby="discrete-slider"
                valueLabelDisplay="auto"
                onChange={(event, newValue) => this.setState({minYear: newValue})}
                step={10}
                marks
                min={1950}
                max={2020}
                />
            </div>
            <div class="col-md-5">
                <Typography id="discrete-slider" gutterBottom>
                  Min Votes: (In thousands)
                </Typography>
                <Slider
                defaultValue={0}
                aria-labelledby="discrete-slider"
                valueLabelDisplay="auto"
                getAriaValueText={x => `${x}K`}
                onChange={(event, newValue) => this.setState({minVotes: newValue * 1000})}
                step={10}
                marks
                min={0}
                max={1000}
                />
            </div>
          </div>
          <div class="row align-items-center my-5">
            <div class="col-lg-7">
            <TextField fullWidth 
            id="outlined-multiline-static"
            label="Multiline"
            multiline
            rows={10}
            onChange={(val) => this.curContent = val.target.value}
            variant="outlined"
            />
            <Button variant="contained" color="primary" onClick={() => this.getAllRecommandations()}>
              Validate
            </Button>
            </div>
            <div class="col-lg-5">
              <h1 class="font-weight-light">Recommandation for the IP</h1>
              {movies}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Ip;
